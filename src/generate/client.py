"""Thin wrapper around the Claude Code CLI in headless mode.

Each call is as close to a pure system-plus-user prompt as the CLI allows:

  --safe-mode              disables CLAUDE.md, skills, plugins, hooks, MCP, commands
  --restricted             also ignores user, project, and local settings files
  --disable-slash-commands disables skills
  --tools StructuredOutput the ONLY tool left; the built-in catalogue is ~40k tokens
  --system-prompt-file     replaces the default agent system prompt with the role
  --json-schema            enforces the output schema at generation

Measured residue under these flags is 716 tokens, containing only the CLI's
"# Environment" and "# userEmail" sections; it cannot be suppressed while a
custom system prompt is set, and the paper states it. Calls run from a neutral
working directory so the project path does not appear in that section.

Three constraints of CLI version 2.1.269, all verified by experiment:

  * --bare cannot be used: it skips keychain reads, so subscription (claude.ai)
    auth fails with "Not logged in".
  * --disallowedTools "*" cannot be used: it also blocks the internal
    StructuredOutput tool, so --json-schema returns nothing. Name the one tool
    with --tools instead, which is cheaper as well.
  * The schema must be passed with no "$schema" key (the CLI cannot resolve the
    2020-12 meta-schema) and with shell=False (Windows shell quoting mangles the
    inline JSON). The files keep "$schema" for local validation.

The user message is passed on stdin because the document exceeds the Windows
command-line limit.
"""
import json
import shutil
import subprocess
import tempfile
import time
from dataclasses import dataclass, asdict
from pathlib import Path

RATE_LIMIT_MARKERS = ("rate limit", "usage limit", "session limit", "limit reached", "overloaded", "429")


def _executable() -> str:
    """Absolute path to the CLI. shell=False, so PATH resolution is ours to do."""
    found = shutil.which("claude")
    if found:
        return found
    fallback = Path.home() / ".local" / "bin" / "claude.exe"
    if fallback.exists():
        return str(fallback)
    raise RuntimeError("claude CLI not found on PATH")


@dataclass
class CallResult:
    ok: bool
    output: dict | None
    error: str | None
    model: str
    input_tokens: int  # uncached + cache_creation + cache_read: the whole prompt
    output_tokens: int
    thinking_tokens: int
    cache_creation_tokens: int
    cache_read_tokens: int
    cost_usd: float
    duration_ms: int
    attempts: int
    num_turns: int  # >2 means the CLI re-prompted after a schema-invalid StructuredOutput


class ClaudeCLI:
    def __init__(self, model: str, effort: str | None = None, max_attempts: int = 3,
                 backoff_s: float = 30.0, rate_limit_wait_s: float = 600.0,
                 rate_limit_max_s: float = 6 * 3600):
        self.model = model
        self.effort = effort
        self.max_attempts = max_attempts
        self.backoff_s = backoff_s
        self.rate_limit_wait_s = rate_limit_wait_s
        self.rate_limit_max_s = rate_limit_max_s  # a subscription window resets hours later, not minutes

    def call(self, system_prompt_file: Path, user_message: str, schema_file: Path,
             log_dir: Path, tag: str) -> CallResult:
        log_dir.mkdir(parents=True, exist_ok=True)
        (log_dir / f"{tag}.request.txt").write_text(user_message, encoding="utf-8")
        schema = json.loads(schema_file.read_text(encoding="utf-8"))
        schema.pop("$schema", None)
        cmd = [
            _executable(), "-p",
            "--safe-mode", "--restricted", "--disable-slash-commands",
            "--tools", "StructuredOutput",
            "--system-prompt-file", str(system_prompt_file),
            "--model", self.model,
            "--output-format", "json",
            "--json-schema", json.dumps(schema, separators=(",", ":")),
        ]
        if self.effort:
            cmd += ["--effort", self.effort]
        neutral_cwd = tempfile.gettempdir()
        last_error = None
        rate_limited_s = 0.0
        attempt = calls = 0
        while attempt < self.max_attempts:
            attempt += 1
            calls += 1
            t0 = time.time()
            proc = subprocess.run(cmd, input=user_message, capture_output=True, text=True,
                                  encoding="utf-8", shell=False, cwd=neutral_cwd)
            raw = proc.stdout
            (log_dir / f"{tag}.attempt{calls}.raw.json").write_text(raw, encoding="utf-8")
            if proc.stderr:
                (log_dir / f"{tag}.attempt{calls}.stderr.txt").write_text(proc.stderr, encoding="utf-8")
            try:
                resp = json.loads(raw)
            except json.JSONDecodeError as e:
                last_error = f"CLI output not JSON: {e}; stderr: {proc.stderr[:500]}"
                time.sleep(self.backoff_s)
                continue

            if resp.get("is_error"):
                last_error = str(resp.get("result", "unknown CLI error"))
                rate_limited = (resp.get("api_error_status") == 429
                                or any(m in last_error.lower() for m in RATE_LIMIT_MARKERS))
                if rate_limited and rate_limited_s < self.rate_limit_max_s:
                    # Waiting out a limit is not a failed attempt: the call never reached the model.
                    print(f"[{tag}] rate limited ({last_error[:80]!r}); waiting {self.rate_limit_wait_s:.0f}s",
                          flush=True)
                    time.sleep(self.rate_limit_wait_s)
                    rate_limited_s += self.rate_limit_wait_s
                    attempt -= 1
                else:
                    time.sleep(self.backoff_s)
                continue

            output = resp.get("structured_output")
            if output is None:
                # Fall back to parsing the text result, in case structured_output is absent.
                try:
                    output = json.loads(resp.get("result", ""))
                except json.JSONDecodeError:
                    last_error = "no structured_output and result is not JSON"
                    time.sleep(self.backoff_s)
                    continue

            usage = resp.get("usage", {})
            resolved = list(resp.get("modelUsage", {}).keys())
            result = CallResult(
                ok=True, output=output, error=None,
                model=resolved[0] if resolved else self.model,
                input_tokens=(int(usage.get("input_tokens", 0))
                              + int(usage.get("cache_creation_input_tokens", 0))
                              + int(usage.get("cache_read_input_tokens", 0))),
                output_tokens=int(usage.get("output_tokens", 0)),
                thinking_tokens=int(usage.get("output_tokens_details", {}).get("thinking_tokens", 0)),
                cache_creation_tokens=int(usage.get("cache_creation_input_tokens", 0)),
                cache_read_tokens=int(usage.get("cache_read_input_tokens", 0)),
                cost_usd=float(resp.get("total_cost_usd", 0.0)),
                duration_ms=int(resp.get("duration_ms", (time.time() - t0) * 1000)),
                attempts=attempt,
                num_turns=int(resp.get("num_turns", 0)),
            )
            (log_dir / f"{tag}.result.json").write_text(
                json.dumps({"meta": asdict(result) | {"output": None}, "output": output}, indent=2),
                encoding="utf-8")
            return result

        result = CallResult(ok=False, output=None, error=last_error, model=self.model,
                            input_tokens=0, output_tokens=0, thinking_tokens=0, cache_creation_tokens=0,
                            cache_read_tokens=0, cost_usd=0.0,
                            duration_ms=0, attempts=self.max_attempts, num_turns=0)
        (log_dir / f"{tag}.result.json").write_text(json.dumps(asdict(result), indent=2), encoding="utf-8")
        return result

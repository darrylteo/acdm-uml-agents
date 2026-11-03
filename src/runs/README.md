# Scored runs, 12–14 September 2026

All runs use `claude-sonnet-5` through the Claude Code CLI (2.1.269), the same document, scaffold, and JSON schema, from a neutral working directory with a custom system prompt. Calls are independent: each is a fresh `claude -p` invocation with no session carried over (the step-1 prompt is 11,708–11,711 tokens in every run; the ±3 is the CLI's date stamp). The 43 calls were spread over three days because of the subscription's session and weekly limits; the client waits out a 429 without counting it as an attempt.

| Directory | Condition | Effort | n | Calls per run |
|---|---|---|---|---|
| `multi/` | analyst → class → attribute → operation → relationship → reviewer | `medium` | 5 | 6 |
| `single/` | one pass, system prompt equal to the union of the role prompts | `medium` | 5 | 1 |
| `single_high/` | budget-matched control: as `single`, effort `high` | `high` | 5 | 1 |
| `noscaffold/` | probe: as `single`, scaffold and role prompt replaced by the three-sentence `no_scaffold.md` | `medium` | 3 | 1 |
| `control_scaffold_only/` | deterministic scaffold-only baseline, no model call | – | 1 | 0 |

`single_high` is a budget-matched control, since the multi-agent and single-agent conditions otherwise differ in generation budget as well as in decomposition. Its median output tokens (108k) and wall-clock (14 min) equal the multi-agent condition's; its thinking tokens exceed them (69k vs 43k).

## Files per run

`model.json` is the artifact; `model.puml`, `model.html`, and `model.py` (Python class stubs, `generate/render_code.py --all`: all 19 compile, import, and instantiate, with every annotation resolving) are rendered from it deterministically. `manifest.json` records the model alias, effort, per-step tokens (prompt, output, thinking, cache), list-price cost, duration, and `num_turns`. A `num_turns` of 3 rather than 2 means the model's first `StructuredOutput` failed schema validation and the CLI re-prompted it within the same call, roughly doubling that call's tokens; this happened in 10 of the 14 full-model calls of the first two days, most often because the model wrapped the object in an extra key. It is the same mechanism in every condition and is reported with the cost figures. Every request (`*.request.txt`), raw CLI response (`*.attempt*.raw.json`), and, for the multi-agent condition, every merged intermediate (`*.merged.json`) is kept.

Lint (`python src/evaluate/lint.py src/runs/*/*/model.json`): every run validates against the schema with no structural problems; `multi/run_03` has four orphan system classes.

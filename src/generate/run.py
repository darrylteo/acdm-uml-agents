"""Run the experiment.

  py src/generate/run.py --condition single     --n 5
  py src/generate/run.py --condition multi      --n 5 --pace 120
  py src/generate/run.py --condition noscaffold --n 3
  py src/generate/run.py --condition single     --n 5 --effort high --out single_high   # budget-matched control

Outputs go to src/runs/<condition>/run_NN/ (or src/runs/<out>/ when --out is given, for controls that vary one setting). Runs are resumable: a run directory that already holds model.json is skipped.
"""
import argparse
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from client import ClaudeCLI  # noqa: E402
import multi_agent  # noqa: E402
import single_agent  # noqa: E402

SRC = Path(__file__).resolve().parents[1]
RUNS = SRC / "runs"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--condition", choices=["single", "multi", "noscaffold"], required=True)
    ap.add_argument("--n", type=int, default=5)
    ap.add_argument("--model", default="claude-sonnet-5",
                    help="CLI model alias or ID; the resolved ID is recorded from each response")
    ap.add_argument("--effort", default="medium", choices=["low", "medium", "high", "xhigh", "max"],
                    help="CLI effort level; omit for the provider default. Pinned and reported.")
    ap.add_argument("--pace", type=float, default=30.0, help="seconds to wait between runs")
    ap.add_argument("--no-analyst", action="store_true")
    ap.add_argument("--start", type=int, default=1, help="first run index")
    ap.add_argument("--out", default=None, help="output directory name under src/runs (default: the condition)")
    args = ap.parse_args()

    client = ClaudeCLI(model=args.model, effort=args.effort)
    label = args.out or args.condition
    for i in range(args.start, args.start + args.n):
        run_dir = RUNS / (args.out or args.condition) / f"run_{i:02d}"
        if (run_dir / "model.json").exists():
            print(f"[{label} {i:02d}] exists, skipping")
            continue
        t0 = time.time()
        print(f"[{label} {i:02d}] starting")
        if args.condition == "multi":
            m = multi_agent.run(run_dir, client, include_analyst=not args.no_analyst)
        else:
            m = single_agent.run(run_dir, client, scaffold=args.condition == "single")
        status = "ok" if m["ok"] else f"FAILED at {m.get('failed_step')}"
        print(f"[{label} {i:02d}] {status}  in={m['total_input_tokens']} out={m['total_output_tokens']} "
              f"cost=${m['total_cost_usd']:.3f}  {time.time() - t0:.0f}s")
        if i < args.start + args.n - 1:
            time.sleep(args.pace)


if __name__ == "__main__":
    main()

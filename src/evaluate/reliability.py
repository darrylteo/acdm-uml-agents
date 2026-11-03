r"""Agreement between graders and the reported mean grades, on the two samples.

  python src/evaluate/reliability.py recall \
      src/evaluate/graders/grades_recall_grader_A.json src/evaluate/graders/grades_recall_grader_B.json \
      src/evaluate/sample/judge_recall_claude-opus-5_high.json src/evaluate/sample/judge_recall_claude-sonnet-5_high.json
  python src/evaluate/reliability.py precision \
      src/evaluate/graders/grades_precision_grader_A.json src/evaluate/graders/grades_precision_grader_B.json \
      src/evaluate/sample/judge_precision_claude-opus-5_high.json src/evaluate/sample/judge_precision_claude-sonnet-5_high.json

The grade files are passed in this order (the two researchers, then the two model graders); the
order fixes the sequence of pairs and, with --seed 0, the bootstrap draws. Writes
results/<task>_reliability.json at the repository root, which paper_numbers.py reads.

Reads sample/<task>_key.json (item -> run, element or claim) to group the items by configuration
and kind. Reports each grader's mean grade (the reported recall or precision) with a percentile
bootstrap interval, over all items and per configuration and kind, and then, for each pair of
graders, n, raw agreement, Gwet's AC2 (linear weights over {0, 0.5, 1}) with a bootstrap 95%
interval and Gwet's analytic standard error, linearly weighted Cohen's kappa for the record, and
the mean grade of each grader on the common items, overall, per configuration, and per kind.
AC2 is the reported agreement statistic: with most grades at 1, kappa's chance term is near 1
and kappa sits near 0 at 84% raw agreement (the kappa paradox, Feinstein and Cicchetti 1990);
AC2's chance term stays small (Gwet 2008).
"""
import argparse
import json
import random
import statistics
import sys
from itertools import combinations
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from stats import gwet_ac2, weighted_kappa  # noqa: E402

SRC = Path(__file__).resolve().parents[1]
SAMPLE_DIR = SRC / "evaluate" / "sample"
RESULTS = SRC.parent / "results"
BOOT = 2000


def load_grades(p: Path) -> tuple[str, dict[str, dict]]:
    d = json.loads(p.read_text(encoding="utf-8"))
    return d.get("grader") or p.stem, {k: v for k, v in d.get("grades", {}).items() if v.get("credit") is not None}


def boot_ci(stat, xa: list[float], xb: list[float], rng: random.Random) -> tuple[float, float]:
    """Percentile bootstrap 95% interval of a two-rater statistic over the items."""
    n = len(xa)
    ks = []
    for _ in range(BOOT):
        idx = [rng.randrange(n) for _ in range(n)]
        ks.append(stat([xa[i] for i in idx], [xb[i] for i in idx]))
    ks.sort()
    return ks[max(0, round(0.025 * BOOT) - 1)], ks[min(BOOT - 1, round(0.975 * BOOT) - 1)]


MIN_N = 20   # below this a bootstrap interval on an agreement statistic says nothing; the row is marked


def mean_ci(xs: list[float], rng: random.Random) -> tuple[float, float, float]:
    """Mean grade and its percentile bootstrap 95% interval. This is the reported metric: the sample is
    uniform over the population of (run, claim) or (run, element, milestone), so the mean grade over a
    group of items estimates that group's recall or precision."""
    n = len(xs)
    ms = sorted(statistics.mean(xs[rng.randrange(n)] for _ in range(n)) for _ in range(BOOT))
    return statistics.mean(xs), ms[max(0, round(0.025 * BOOT) - 1)], ms[min(BOOT - 1, round(0.975 * BOOT) - 1)]


def pair(a: dict[str, float], b: dict[str, float], ids: set[str], rng: random.Random) -> dict | None:
    common = sorted(set(a) & set(b) & ids)
    if len(common) < 2:
        return None
    xa, xb = [a[i] for i in common], [b[i] for i in common]
    ac2, se = gwet_ac2(xa, xb)
    return {"n": len(common), "agreement": sum(x == y for x, y in zip(xa, xb)) / len(common),
            "ac2": ac2, "ac2_se": se, "ac2_ci": boot_ci(lambda x, y: gwet_ac2(x, y)[0], xa, xb, rng),
            "kappa": weighted_kappa(xa, xb), "ci": boot_ci(weighted_kappa, xa, xb, rng),
            "mean_a": statistics.mean(xa), "mean_b": statistics.mean(xb)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("task", choices=["precision", "recall"])
    ap.add_argument("grades", nargs="+", type=Path)
    ap.add_argument("--md", action="store_true")
    ap.add_argument("--no-write", action="store_true", help="print only; do not write results/<task>_reliability.json")
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()
    rng = random.Random(args.seed)
    key = json.loads((SAMPLE_DIR / f"{args.task}_key.json").read_text(encoding="utf-8"))
    items = key["items"]
    condition = {iid: k["run"].split("/")[0] for iid, k in items.items()}

    graders: dict[str, dict[str, float]] = {}
    for f in args.grades:
        name, g = load_grades(f)
        graders[name] = {i: float(v["credit"]) for i, v in g.items()}
        print(f"{name}: {len(g)} of {len(items)} items graded")

    groups = {"all": set(items)}
    for c in sorted(set(condition.values())):
        groups[c] = {i for i in items if condition[i] == c}
    for k in sorted({v["kind"] for v in items.values()}):
        groups[f"kind={k}"] = {i for i, v in items.items() if v["kind"] == k}

    means = []
    for gname, ids in groups.items():
        for name, g in graders.items():
            xs = [g[i] for i in sorted(set(g) & ids)]
            if xs:
                m, lo, hi = mean_ci(xs, rng)
                means.append({"items": gname, "grader": name, "n": len(xs), "mean": m, "ci": [lo, hi]})
    rows = []
    for gname, ids in groups.items():
        for a, b in combinations(graders, 2):
            r = pair(graders[a], graders[b], ids, rng)
            if r:
                rows.append((gname, a, b, r))
            elif len(set(graders[a]) & set(graders[b]) & ids) == 1:
                print(f"note: {gname} {a}-{b} has 1 common item, too few for an agreement statistic; skipped")
    # Differences the paper states in words: each grader's mean in one set of configurations minus another,
    # with a percentile bootstrap interval resampling each set's items independently (the statements
    # "not resolved" and "lower" rest on these intervals, not on a reading of two overlapping ones).
    scaffolded = {"multi", "single", "single_high"}
    sets = {"scaffolded": {i for i in items if condition[i] in scaffolded}, **{c: groups[c] for c in groups if c in condition.values()}}
    contrasts = []
    for x, y in [("scaffolded", "noscaffold"), ("multi", "single"), ("multi", "single_high"), ("single_high", "single")]:
        if x not in sets or y not in sets:
            continue
        for name, g in graders.items():
            xs, ys = [g[i] for i in sorted(set(g) & sets[x])], [g[i] for i in sorted(set(g) & sets[y])]
            if len(xs) < 2 or len(ys) < 2:
                continue
            ds = sorted(statistics.mean(rng.choice(xs) for _ in xs) - statistics.mean(rng.choice(ys) for _ in ys) for _ in range(BOOT))
            contrasts.append({"a": x, "b": y, "grader": name, "diff": statistics.mean(xs) - statistics.mean(ys),
                              "ci": [ds[max(0, round(0.025 * BOOT) - 1)], ds[min(BOOT - 1, round(0.975 * BOOT) - 1)]]})
    # Is the human pair's agreement above a human-model pair's? Paired bootstrap over the common items.
    agree_diffs = []
    humans = [n for n in graders if "/" not in n]
    if len(humans) == 2:
        h1, h2 = humans
        for m in [n for n in graders if "/" in n]:
            for h in humans:
                common = sorted(set(graders[h1]) & set(graders[h2]) & set(graders[m]))
                if len(common) < 2:
                    continue
                f = lambda idx, u, v: gwet_ac2([graders[u][common[i]] for i in idx], [graders[v][common[i]] for i in idx])[0]
                full = list(range(len(common)))
                ds = []
                for _ in range(BOOT):
                    idx = [rng.randrange(len(common)) for _ in common]
                    ds.append(f(idx, h1, h2) - f(idx, h, m))
                ds.sort()
                agree_diffs.append({"human_pair": f"{h1}-{h2}", "pair": f"{h}-{m}", "diff": f(full, h1, h2) - f(full, h, m),
                                    "ci": [ds[max(0, round(0.025 * BOOT) - 1)], ds[min(BOOT - 1, round(0.975 * BOOT) - 1)]]})
    label = "recall" if args.task == "recall" else "precision"
    if not args.md:
        print("differences in mean grade (first set minus second), bootstrap 95% interval:")
        for c in contrasts:
            print(f"  {c['a']:>11} - {c['b']:<11} {c['grader']:24} {c['diff']:+.3f} [{c['ci'][0]:+.3f}, {c['ci'][1]:+.3f}]")
        print("AC2 of the two humans minus AC2 of a human-model pair, paired bootstrap 95% interval:")
        for d in agree_diffs:
            print(f"  {d['human_pair']} minus {d['pair']:32} {d['diff']:+.3f} [{d['ci'][0]:+.3f}, {d['ci'][1]:+.3f}]")
    if args.md:
        print(f"\n| items | grader | n | {label} (mean grade) [95% CI] |\n|---|---|---|---|")
        for m in means:
            print(f"| {m['items']} | {m['grader']} | {m['n']} | {m['mean']:.2f} [{m['ci'][0]:.2f}, {m['ci'][1]:.2f}] |")
    else:
        print(f"\n{label} by grader (mean grade over the sampled items, with a percentile bootstrap interval):")
        for m in means:
            flag = "  (n < %d)" % MIN_N if m["n"] < MIN_N else ""
            print(f"  {m['items']:16} {m['grader']:24} n={m['n']:3} {label}={m['mean']:.3f} "
                  f"[{m['ci'][0]:.3f}, {m['ci'][1]:.3f}]{flag}")
        print()
    if args.md:
        print(f"\n| items | pair | n | agreement | Gwet's AC2 [95% CI] | weighted kappa | mean grade A | mean grade B |\n|---|---|---|---|---|---|---|---|")
        for g, a, b, r in rows:
            print(f"| {g} | {a}–{b} | {r['n']} | {r['agreement']:.2f} | {r['ac2']:.2f} [{r['ac2_ci'][0]:.2f}, {r['ac2_ci'][1]:.2f}] | "
                  f"{r['kappa']:.2f} | {r['mean_a']:.2f} | {r['mean_b']:.2f} |")
    else:
        for g, a, b, r in rows:
            print(f"{g:16} {a + '-' + b:16} n={r['n']:3}{' *' if r['n'] < MIN_N else '  '}agree={r['agreement']:.3f} AC2={r['ac2']:.3f} "
                  f"[{r['ac2_ci'][0]:.3f}, {r['ac2_ci'][1]:.3f}] (se {r['ac2_se']:.3f}) kappa={r['kappa']:.3f}  "
                  f"mean {a}={r['mean_a']:.3f} {b}={r['mean_b']:.3f}")
        if any(r["n"] < MIN_N for _, _, _, r in rows):
            print(f"  * fewer than {MIN_N} common items: the interval is not usable, the row is for completeness only")

    if not args.no_write:
        RESULTS.mkdir(exist_ok=True)
        (RESULTS / f"{args.task}_reliability.json").write_text(json.dumps(
            {"means": means, "rows": [{"items": g, "a": a, "b": b, **r} for g, a, b, r in rows],
             "contrasts": contrasts, "agreement_differences": agree_diffs}, indent=1), encoding="utf-8")


if __name__ == "__main__":
    main()

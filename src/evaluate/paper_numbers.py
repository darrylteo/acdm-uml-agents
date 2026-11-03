"""Every number the paper prints, written as LaTeX so that no figure is typed by hand.

  python src/evaluate/paper_numbers.py

Reads results/{recall,precision}_reliability.json (run reliability.py on each task
with every grader first), the scored runs' model.json and manifest.json, and
claims.json; writes

  results/numbers.tex           \\pn{<key>} for every number used in prose
  results/tables/grades.tex     Table: mean grade per grader, by configuration and by kind
  results/tables/agreement.tex  Table: Gwet's AC2 per pair (not used in the paper; grades.tex
                                carries each grader's AC2 with each researcher)
  results/tables/structure.tex  Table: size, S1-S3 and cost per configuration, medians

A grader not yet in a reliability file prints as "--", so the paper compiles
before every grader is in and fills itself when the files are rerun.
Keys in numbers.tex:

  <task>:<grader>:<group>[:ci|:n]   task recall|precision; grader A B opus sonnet;
                                    group all multi single singlehigh noscaffold
                                    class attribute operation relationship enumeration
  <stat>:<task>:<pair>[:ci]         stat agree|actwo|kappa|n; pair e.g. B-opus
  <prop>:<cond>                     S1..S5, cost, outtok, minutes, runs: median [range]
  inv:<kind>, inv:active            frozen claim inventory
  precisionw:<A|B>:scaffolded       researcher precision with each element weighted 1/(milestones it cites)
  hours:min, hours:max              researcher grading hours per sample, at most 10 min per item
"""
import json
import statistics
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SRC = HERE.parent
RESULTS = SRC.parent / "results"
sys.path.insert(0, str(HERE))
from structure import structure  # noqa: E402
import paths  # noqa: E402

GRADERS = {"grader_A": "A", "grader_B": "B", "claude-opus-5/high": "opus", "claude-sonnet-5/high": "sonnet"}
HEAD = {"A": "A", "B": "B", "opus": "Opus~5", "sonnet": "Sonnet~5"}
ORDER = ["A", "B", "opus", "sonnet"]
CONDS = {"multi": "Multi-agent", "single": "Single-agent", "single_high": "Single, high effort", "noscaffold": "No scaffold"}
KINDS = ["class", "attribute", "operation", "relationship", "enumeration"]
key_group = lambda g: g.replace("kind=", "").replace("_", "")


def f2(x: float) -> str:
    return f"{x:.2f}"


def ci(lo: float, hi: float) -> str:
    return f"[{lo:.2f}, {hi:.2f}]"


def load_reliability(task: str) -> dict:
    p = RESULTS / f"{task}_reliability.json"
    d = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
    return d if "means" in d else {"means": [], "rows": []}


def main():
    pn: dict[str, str] = {}
    grades: dict[tuple, dict] = {}     # (task, grader, group) -> mean record
    pairs: dict[tuple, dict] = {}      # (task, pair) -> row, overall only
    for task in ("recall", "precision"):
        rel = load_reliability(task)
        for m in rel["means"]:
            g = GRADERS.get(m["grader"])
            if not g:
                continue
            grades[(task, g, key_group(m["items"]))] = m
            k = f"{task}:{g}:{key_group(m['items'])}"
            pn[k], pn[k + ":ci"], pn[k + ":n"] = f2(m["mean"]), ci(*m["ci"]), str(m["n"])
        for r in rel["rows"]:
            a, b = GRADERS.get(r["a"]), GRADERS.get(r["b"])
            if not (a and b):
                continue
            a, b = sorted((a, b), key=ORDER.index)
            grp = key_group(r["items"])
            pr = f"{a}-{b}" + ("" if grp == "all" else f":{grp}")
            if grp == "all":
                pairs[(task, f"{a}-{b}")] = r
            pn[f"agree:{task}:{pr}"] = f2(r["agreement"])
            pn[f"actwo:{task}:{pr}"], pn[f"actwo:{task}:{pr}:ci"] = f2(r["ac2"]), ci(*r["ac2_ci"])
            pn[f"kappa:{task}:{pr}"], pn[f"n:{task}:{pr}"] = f2(r["kappa"]), str(r["n"])

    # differences between configurations and between agreement pairs (from reliability.py)
    CK = {"scaffolded": "scaffolded", "noscaffold": "noscaffold", "multi": "multi", "single": "single", "single_high": "singlehigh"}
    gaps = []
    for task in ("recall", "precision"):
        rel = load_reliability(task)
        for c in rel.get("contrasts", []):
            g = GRADERS.get(c["grader"])
            k = f"diff:{task}:{CK[c['a']]}-{CK[c['b']]}:{g}"
            pn[k], pn[k + ":ci"] = f2(c["diff"]), ci(*c["ci"])
            if c["a"] != "scaffolded":
                gaps.append(abs(c["diff"]))
        ds = [d["diff"] for d in rel.get("agreement_differences", [])]
        if ds:
            pn[f"agreediff:{task}:min"], pn[f"agreediff:{task}:max"] = f2(min(ds)), f2(max(ds))
        raws = [r["agreement"] for r in rel["rows"] if key_group(r["items"]) == "all"]
        if raws:
            pn[f"agree:{task}:min"], pn[f"agree:{task}:max"] = f2(min(raws)), f2(max(raws))
    if gaps:
        pn["gap:scaffolded:max"] = f2(max(gaps))
    # largest pipeline gain any interval admits: upper end of multi minus single or single_high, every grader and task
    # (states what "no significant difference" rules out)
    ups = [c["ci"][1] for task in ("recall", "precision") for c in load_reliability(task).get("contrasts", [])
           if c["a"] == "multi"]
    if ups:
        pn["gainbound:multi"] = f2(max(ups))

    # items both researchers marked below 1, and how often each model grader gave them full credit (the evidence
    # for why the model graders fall below the researcher pair on recall and not on precision)
    def credits(p: Path) -> dict[str, float]:
        d = json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
        return {k: v["credit"] for k, v in d.get("grades", {}).items() if v.get("credit") is not None}
    for task in ("recall", "precision"):
        a, b = (credits(HERE / "graders" / f"grades_{task}_{s}.json") for s in ("grader_A", "grader_B"))
        if not (a and b):
            continue
        down = [i for i in a if i in b and a[i] < 1 and b[i] < 1]
        pn[f"jointdown:{task}:n"] = str(len(down))
        for m, g in (("claude-opus-5", "opus"), ("claude-sonnet-5", "sonnet")):
            j = credits(HERE / "sample" / f"judge_{task}_{m}_high.json")
            if j:
                pn[f"jointdown:{task}:{g}full"] = str(sum(j.get(i) == 1 for i in down))
        if task == "recall":
            key = json.loads((HERE / "sample" / "recall_key.json").read_text(encoding="utf-8"))["items"]
            pn["jointdown:recall:noscaffold"] = str(sum(key[i]["run"].startswith("noscaffold/") for i in down))
        # each researcher's own count of items below 1, to show how rarely their deductions coincide
        pn[f"down:{task}:A"], pn[f"down:{task}:B"] = str(sum(v < 1 for v in a.values())), str(sum(v < 1 for v in b.values()))
        # model grader minus researcher mean grade, on scaffolded items and on the probe (where generosity sits)
        key = json.loads((HERE / "sample" / f"{task}_key.json").read_text(encoding="utf-8"))["items"]
        models = [credits(HERE / "sample" / f"judge_{task}_{m}_high.json") for m in ("claude-opus-5", "claude-sonnet-5")]
        for grp, want in (("scaffolded", False), ("noscaffold", True)):
            ids = [i for i in a if i in b and key[i]["run"].startswith("noscaffold/") == want]
            gaps_ = [statistics.mean(m[i] for i in ids) - statistics.mean(h[i] for i in ids) for m in models for h in (a, b)]
            pn[f"gen:{task}:{grp}:min"], pn[f"gen:{task}:{grp}:max"] = f"${min(gaps_):+.2f}$", f"${max(gaps_):+.2f}$"

    # researchers' precision on scaffolded items with every element weighted equally: an item drawn under one of
    # the k milestones its element cites counts 1/k (the paper quotes it beside the per-citation mean)
    pkey = json.loads((HERE / "sample" / "precision_key.json").read_text(encoding="utf-8"))["items"]
    ncites: dict[str, dict[str, int]] = {}
    for s_, g in (("grader_A", "A"), ("grader_B", "B")):
        h = credits(HERE / "graders" / f"grades_precision_{s_}.json")
        num = den = 0.0
        for i, k in pkey.items():
            if i not in h or k["run"].startswith("noscaffold/"):
                continue
            if k["run"] not in ncites:
                model = json.loads((SRC / "runs" / k["run"] / "model.json").read_text(encoding="utf-8"))
                ncites[k["run"]] = {e["path"]: len(e["cites"]) for e in paths.elements(model)}
            w = 1 / ncites[k["run"]][k["path"]]
            num, den = num + w * h[i], den + w
        if den:
            pn[f"precisionw:{g}:scaffolded"] = f2(num / den)

    # hours each researcher spent per sample, counting at most 10 minutes per item so that a page left open
    # overnight does not count (the Discussion gives the range)
    hours = []
    for task in ("recall", "precision"):
        for s_ in ("grader_A", "grader_B"):
            p = HERE / "graders" / f"grades_{task}_{s_}.json"
            if p.exists():
                g_ = json.loads(p.read_text(encoding="utf-8"))["grades"].values()
                hours.append(sum(min(v.get("seconds") or 0, 600) for v in g_) / 3600)
    if hours:
        pn["hours:min"], pn["hours:max"] = f"{min(hours):.0f}", f"{max(hours):.0f}"

    # what the two model graders cost to grade both samples (list price, from the call metadata in the grade files)
    cost = mins = 0.0
    for task in ("recall", "precision"):
        for m in ("claude-opus-5", "claude-sonnet-5"):
            p = HERE / "sample" / f"judge_{task}_{m}_high.json"
            if p.exists():
                for c in json.loads(p.read_text(encoding="utf-8"))["calls"].values():
                    if c.get("meta"):
                        cost += c["meta"]["cost_usd"]
                        mins += c["meta"]["duration_ms"] / 60000
    pn["judgecost:total"], pn["judgeminutes:total"] = f"{cost:.0f}", f"{mins:.0f}"

    # researcher range over the three scaffolded configurations, the paper's headline recall and precision
    for task in ("recall", "precision"):
        vals = [grades[(task, g, c)]["mean"] for g in ("A", "B") for c in ("multi", "single", "singlehigh")
                if (task, g, c) in grades]
        if vals:
            pn[f"{task}:researchers:scaffolded:min"], pn[f"{task}:researchers:scaffolded:max"] = f2(min(vals)), f2(max(vals))

    # structure and cost per configuration, median [min, max] over runs
    runs = {c: sorted((SRC / "runs" / c).glob("run_*")) for c in CONDS}
    props: dict[str, dict[str, list[float]]] = {}
    for c, rs in runs.items():
        acc: dict[str, list[float]] = {k: [] for k in ("S1", "S2", "S3", "S4", "S5", "cost", "outtok", "minutes", "classes", "attrs", "ops")}
        for r in rs:
            s = structure(json.loads((r / "model.json").read_text(encoding="utf-8")))
            man = json.loads((r / "manifest.json").read_text(encoding="utf-8"))
            for name, key in (("S1", "hoist"), ("S4", "complete"), ("S5", "history")):
                n, d = s[key]
                if d:
                    acc[name].append(n / d)
            acc["S2"].append(s["redecl"])
            acc["S3"].append(len(s["leak"]))
            acc["cost"].append(man["total_cost_usd"])
            acc["outtok"].append(man["total_output_tokens"] / 1000)
            acc["minutes"].append(man["total_duration_ms"] / 60000)
            for k in ("classes", "attrs", "ops"):
                acc[k].append(s[k])
        props[c] = acc
        pn[f"runs:{key_group(c)}"] = str(len(rs))
        pn[f"S2runs:{key_group(c)}"] = str(sum(x > 0 for x in acc["S2"]))

    def med(xs, fmt):
        if not xs:
            return "--"
        return f"{fmt(statistics.median(xs))} [{fmt(min(xs))}, {fmt(max(xs))}]" if len(xs) > 1 else fmt(xs[0])

    fmts = {"S1": f2, "S4": f2, "S5": f2, "S2": lambda x: f"{x:g}", "S3": lambda x: f"{x:g}", "cost": lambda x: f"{x:.2f}",
            "outtok": lambda x: f"{x:.0f}", "minutes": lambda x: f"{x:.0f}", "classes": lambda x: f"{x:g}", "attrs": lambda x: f"{x:g}",
            "ops": lambda x: f"{x:g}"}
    for c, acc in props.items():
        for k, xs in acc.items():
            pn[f"{k}:{key_group(c)}"] = med(xs, fmts[k])
            if xs:
                pn[f"{k}:{key_group(c)}:median"] = fmts[k](statistics.median(xs))
                pn[f"{k}:{key_group(c)}:min"], pn[f"{k}:{key_group(c)}:max"] = fmts[k](min(xs)), fmts[k](max(xs))
    scaffolded = [c for c in CONDS if c != "noscaffold"]
    for k in ("S3", "cost"):
        xs = [x for c in scaffolded for x in props[c][k]]
        pn[f"{k}:scaffolded:max"] = fmts[k](max(xs))
    pn["costratio:multi:single"] = f"{statistics.median(props['multi']['cost']) / statistics.median(props['single']['cost']):.1f}"

    claims = json.loads((HERE / "claims.json").read_text(encoding="utf-8"))["claims"]
    active = [c for c in claims if c.get("active")]
    pn["inv:active"] = str(len(active))
    for k in KINDS:
        pn[f"inv:{k}"] = str(sum(c["kind"] == k for c in active))
    held = sum(c["kind"] in ("class", "enumeration") for c in active)
    pn["bound:scaffoldonly:held"], pn["bound:scaffoldonly:recall"] = str(held), f2(held / len(active))
    pn["inv:members"] = str(len(active) - held)

    # numbers.tex
    lines = ["% Written by src/evaluate/paper_numbers.py; do not edit by hand.",
             "\\makeatletter",
             "\\newcommand{\\pn}[1]{\\@ifundefined{pn@#1}{\\textbf{\\textcolor{red}{??#1}}}{\\@nameuse{pn@#1}}}"]
    lines += [f"\\@namedef{{pn@{k}}}{{{v}}}" for k, v in sorted(pn.items())]
    lines += ["\\makeatother", ""]
    (RESULTS / "numbers.tex").write_text("\n".join(lines), encoding="utf-8")

    tables = RESULTS / "tables"
    tables.mkdir(parents=True, exist_ok=True)

    def cell(task, g, grp):
        m = grades.get((task, g, grp))
        return f"{m['mean']:.2f}" if m else "--"

    def n_of(task, grp):
        ns = {m["n"] for (t, _, gg), m in grades.items() if t == task and gg == grp}
        return str(max(ns)) if ns else "--"

    # Table I: mean grade per grader. Intervals are left out of the cells; the caption gives their
    # size and the text the intervals of the differences it states.
    t = ["% Written by src/evaluate/paper_numbers.py; do not edit by hand.",
         "\\begin{table}[t]", "\\centering",
         "\\caption{Mean grade of each grader, and its agreement with each researcher (Gwet's AC2, linear weights). A and B are the researchers, Op. (Opus) and Son. (Sonnet) the model graders. "
         "95\\% intervals are about $\\pm$0.06 per configuration and $\\pm$0.11 for the no-scaffold probe; the scaffold-only bound is by construction. Differences quoted in the text are computed before rounding.}",
         "\\label{tab:grades}", "\\footnotesize", "\\setlength{\\tabcolsep}{2.2pt}",
         "\\begin{tabular}{l r cccc r cccc}", "\\toprule",
         " & \\multicolumn{5}{c}{Recall} & \\multicolumn{5}{c}{Precision} \\\\",
         "\\cmidrule(lr){2-6}\\cmidrule(lr){7-11}",
         " & $n$ & A & B & Op. & Son. & $n$ & A & B & Op. & Son. \\\\", "\\midrule"]
    short = {"multi": "Multi-agent", "single": "Single-agent", "single_high": "Single, high", "noscaffold": "No scaffold"}
    for grp, lab in [("all", "All items")] + [(key_group(c), short[c]) for c in CONDS]:
        t.append(f"{lab} & {n_of('recall', grp)} & " + " & ".join(cell("recall", g, grp) for g in ORDER)
                 + f" & {n_of('precision', grp)} & " + " & ".join(cell("precision", g, grp) for g in ORDER) + " \\\\")
        if grp == "all":
            t.append("\\midrule")
    t.append(f"Scaffold only & -- & \\multicolumn{{4}}{{c}}{{$\\le${pn['bound:scaffoldonly:recall']}}} & -- & \\multicolumn{{4}}{{c}}{{not sampled}} \\\\")
    t.append("\\midrule")
    for k in KINDS:
        t.append(f"{k.capitalize()} & {n_of('recall', k)} & " + " & ".join(cell("recall", g, k) for g in ORDER)
                 + f" & {n_of('precision', k)} & " + " & ".join(cell("precision", g, k) for g in ORDER) + " \\\\")
    # agreement of each column's grader with each researcher, on all 200 items
    def ac2(task, x, y):
        if x == y:
            return "--"
        a, b = sorted((x, y), key=ORDER.index)
        r = pairs.get((task, f"{a}-{b}"))
        return f2(r["ac2"]) if r else "--"
    t.append("\\midrule")
    for s_ in ("A", "B"):
        t.append(f"AC2 with {s_} & 200 & " + " & ".join(ac2("recall", s_, g) for g in ORDER)
                 + " & 200 & " + " & ".join(ac2("precision", s_, g) for g in ORDER) + " \\\\")
    t += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    (tables / "grades.tex").write_text("\n".join(t), encoding="utf-8")

    # Table II: Gwet's AC2 per pair; kappa is not printed.
    a = ["% Written by src/evaluate/paper_numbers.py; do not edit by hand.",
         "\\begin{table}[t]", "\\centering",
         "\\caption{Agreement between graders on the 200 items of each sample, Gwet's AC2 with linear weights. "
         "The student pair A--B is the ceiling against which each model grader is read.}",
         "\\label{tab:agreement}", "\\footnotesize",
         "\\begin{tabular}{l cc}", "\\toprule",
         "Pair & Recall & Precision \\\\", "\\midrule"]
    for i, x in enumerate(ORDER):
        for y in ORDER[i + 1:]:
            cells = [f2(pairs[(task, f"{x}-{y}")]["ac2"]) if (task, f"{x}-{y}") in pairs else "--" for task in ("recall", "precision")]
            a.append(f"{HEAD[x]}--{HEAD[y]} & " + " & ".join(cells) + " \\\\")
            if (x, y) == ("A", "B"):
                a.append("\\midrule")
    a += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    (tables / "agreement.tex").write_text("\n".join(a), encoding="utf-8")

    # Table III: medians only; the rows are the properties the text uses (S2, S4 and S5 are computed above
    # for numbers.tex but not tabulated).
    s = ["% Written by src/evaluate/paper_numbers.py; do not edit by hand.",
         "\\begin{table}[t]", "\\centering",
         "\\caption{Structure and cost per run, median over the runs of each configuration. Cost is the provider's list-price estimate.}",
         "\\label{tab:structure}", "\\footnotesize", "\\setlength{\\tabcolsep}{3pt}",
         "\\begin{tabular}{l cccc}", "\\toprule",
         " & Multi & Single & High & No scaf. \\\\", "\\midrule"]
    rows = [("Classes", "classes"), ("Attributes", "attrs"), ("Operations", "ops"),
            ("Shared members on superclass", "S1"), ("Times as bare timestamps", "S3"),
            ("Output tokens (k)", "outtok"), ("Minutes", "minutes"), ("Cost (US\\$)", "cost")]
    for lab, k in rows:
        cells = [pn.get(f"{k}:{key_group(c)}:median", "--") for c in CONDS]
        s.append(f"{lab} & " + " & ".join(cells) + " \\\\")
    s += ["\\bottomrule", "\\end{tabular}", "\\end{table}", ""]
    (tables / "structure.tex").write_text("\n".join(s), encoding="utf-8")
    print(f"numbers.tex: {len(pn)} keys; tables: grades, agreement, structure; "
          f"graders present: recall {sorted({g for (t, g, _) in grades if t == 'recall'})}, "
          f"precision {sorted({g for (t, g, _) in grades if t == 'precision'})}")


if __name__ == "__main__":
    main()

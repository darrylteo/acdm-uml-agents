# Instructions for the two graders

You are helping evaluate an experiment in which language-model agents produced UML class models of the Airport CDM process from the EUROCONTROL milestone document. Three tasks, each a self-contained web page (nothing to install, saves as you go, one JSON export at the end). Don't discuss items with the other grader while a task is in progress — the point of having two of you is to measure how far two careful people agree independently.

Keep the sixteen-milestone extract (pages 3-18 to 3-33 of the manual, `acdm milestone only.pdf` in the graders' copy; the PDF is not part of this repository, see `src/data/README.md`) open beside Task 1; Tasks 2 and 3 show the text on the page.

Do the tasks in this order: **Task 1, then Task 3, then Task 2** — so you decide what the document says before seeing any generated model. Task 1 is done and its inventory is frozen, so start at Task 3 and go straight on to Task 2; nothing in either waits on anything else.

## Task 1: review the claim inventory (~1–1.5h)

A model proposed, per sentence of the document, whether it states something a class model must contain, and of what kind: **class** (a persistent thing), **attribute** (a named value/property, with its owner), **operation** (a rule, calculation, check, tolerance, trigger, update, or notification, with who performs it), **relationship** (a stated link, `generalization` when several things are kinds of one thing), or **enumeration** (a status or fixed set of values). These become the checklist every model is scored against, so each needs a human decision.

Open `claims_review_<yourname>.html`. The left column lists your milestones (two shared with the other grader). For each proposed claim: **Accept** if it's real and modellable, **Edit** if the kind/owner/text-span is plainly wrong, **Reject** otherwise. Use **+ Add claim** for anything missed. Judge by the document's words, not by how a model might implement them — the kind and owner are labels only, never scored, so fix them only when clearly wrong. Wording is never scored. A repeated class/status is shown once, at first mention; later repeats are marked and not re-decided — add a class only if it's genuinely a different thing.

Keys: `a`/`e`/`r` decide the focused claim, `j`/`k` move between claims, `n`/`p` move between milestones. Export when your milestones are complete.

**Afterwards:** on the two shared milestones we'll compute your agreement and list disagreements, plus any overlapping class names (e.g. "flight plan" vs "ATC flight plan") the code couldn't disambiguate. You'll meet once to resolve both on a single page (`claims_merge.html`) that shows both your decisions side by side with one consensus decision per claim, the recurring sentence types grouped so one rule can be applied to all of them, and the overlapping class names as pairs to call one thing or two. It exports one consensus file.

## Task 2: grade the recall sample (~2h, after Task 3)

For 200 sampled (claim, model) pairs, you decide whether the model holds the claim; two model graders will grade the same 200 separately, afterwards and without seeing your grades. You grade blind — you never see their grades, the run, or the condition.

Open `grade_recall_<yourname>.html`. Left: the claim, who the document says owns it, and its source sentence highlighted in its field. Right, top to bottom: a shortlist of up to five elements of the model, most shared words with the claim first, a candidate class or enumeration shown opened so you can read its attributes and its literals; then the class of the model that the owner names, opened so you see its members at once; then the whole model, every class open so your browser's own Ctrl+F reaches every member (one button folds it). Both sides use the same five words for what a thing is, namely class, enumeration, attribute, operation and relationship, so the word on the claim is the word on the element. The grey word before a class is the model's package; the models' stereotypes are not shown on this task, since neither is graded. The model is anonymised (`m00`, `m01`, …). The shortlist is mechanical and sometimes misses the element that holds the claim: **your grade is against the model, not the shortlist**. Before grading 0, filter the model, or Ctrl+F it, for a word of the claim.

There is nothing to tick. Grade whether the model holds the information in the claim, anywhere and under any name:
- **1** — the model holds it (an attribute, an operation, a typed parameter, an enumeration literal, a class, a relationship) where a developer would look for it. The model's name for it need not be the document's. It may take several elements together, a class and its attribute, or an operation and its parameter — **you grade the claim against the whole model, you are not pairing it with one element**.
- **0.5** — present but weaker: only inside a description or a definition where nothing in the structure carries it, or a stated link carried only by a typed attribute. A typed parameter, an enumeration literal and an attribute are all structure, so they are 1.
- **0** — nothing in the model holds it.

**Grade the claim's subject, not its qualifiers.** A claim is about one thing, and the conditions, triggers, exceptions and times hanging off it need not be in the model too. For *New or late submissions of the ATC Flight Plan, after cancellation or revised EOBT*, an attribute `submissionTime` on the flight plan is a **1** — the model need not also carry cancellation, the revised EOBT, or that these re-trigger the process. Use 0.5 when the model has something near the claim but not the claim itself, and 0 when the subject is missing. About a fifth of the claims have a qualifier clause like this, so the rule comes up often.

**Where the model puts it is not graded.** The claim's owner is where the *document* puts it, not where the model must. An operation the document gives to Milestone 8 is a 1 on whatever class carries it, and a 1 when one operation on a shared base class covers Milestone 8 along with the others. The same goes for the kind: a status the document states is a 1 as an enumeration literal, as a Boolean attribute, or as a class. Grade what the model carries, not how it chose to carry it. This matters — a third of the claims name a milestone as their owner, and the models differ a lot in whether milestones are classes at all.

Search for the thing, not the word. For the claim *unregulated flights* (owner Flight), filter for `regulat`, and for `CTOT`, which only regulated flights have. An attribute `regulated: Boolean` on Flight holds it, so does a literal REGULATED in a status enumeration, and so does an operation `markRegulated()` on whatever class the model gave it to. Try the stem of the word, the abbreviation and its expansion, and the word without its un-/non- prefix. That a class named Flight exists is no evidence for *unregulated flights*: a class matching one word of the claim is never a 0.5.

Keys: `1` / `2` (=0.5) / `3` (=0) to grade (`5` and `0` also work), `j`/`k` or arrows to move, `n` for the next ungraded item. Grading does not move on by itself, so a note can be typed after the grade; press `j` when done. Export as `grades_recall_<yourname>.json`.

## Task 3: grade the precision sample (~1.5h, right after Task 1)

For 200 sampled generated elements, two model graders grade whether the document supports the element. You're grading the same 200.

Open `grade_precision_<yourname>.html`. Left: one element with everything the model says about it. Right: the full milestone, with its ≤3 sentences most related to the element highlighted — start from those, but read the rest before grading 0, since the support is often elsewhere in the table (a checkbox collapses the view to the highlighted sentences). Judge each element against the **document as a whole**. The milestone shown is the one, among those the element cites, whose text names it best, so it is where to look first; if the support is not there, search the PDF (Ctrl-F the name or its abbreviation): something stated anywhere in the sixteen milestones counts in full. Where the support was found is not graded.

Grade:
- **1** — the document states it (the thing, value, rule/condition, or link).
- **0.5** — implied but not stated, or the name matches while the description adds detail the document doesn't give.
- **0** — neither.

For an enumeration, grade whether the document names the status or any of its values; the list of literals is not graded.

The models were told to build certain structure the document does not spell out: every time quantity carries its value, its originator, its time of update and its accuracy; every named thing carries an identifier; times, milestones, messages and stakeholders specialise a common base class. Grade such an element 1 when the document names the underlying thing (the time, the message, the stakeholder).

**Not graded:** whether the model chose a class, an attribute, or an enumeration for the thing, and its stereotype and package. These are shown so you know what the element is, not for you to judge. The stereotypes are Jacobson's, as the models were told them: *entity* holds information that persists across the process; *boundary* models an interface between the system and something outside it (a stakeholder, an external system, a message); *control* holds the logic of a procedure.

Keys as in Task 2. Export as `grades_precision_<yourname>.json`.

## What happens with your work

Everything is committed and released with the paper. Task 1 gives the claim inventory, with your ids as reviewers, and your agreement on the two shared milestones. In Tasks 2 and 3 two language models (`claude-opus-5`, `claude-sonnet-5`) grade the same 200 items each, without seeing your grades. The paper reports each grader's mean grade per configuration and kind, and the agreement of every pair of graders (Gwet's AC2 with a bootstrap interval, weighted kappa and raw agreement beside it). The agreement between the two of you is the ceiling against which each model grader is read.

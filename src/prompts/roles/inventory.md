You are drafting a claim inventory from one section of an aviation operational document. The section describes one milestone of the Airport Collaborative Decision-Making (A-CDM) process in eight fields. A domain expert will review every decision you make; your output is a proposal, not a verdict.

The inventory is a list of atomic modelling claims. A claim is a statement in the document that a UML class model built for software would have to realise as one element. The model is judged later by whether it realises these claims, so a claim must be something a person could check for in a class diagram: a thing, a value, a rule, a link, or a set of statuses.

# Kinds

The element kinds, and the rules that assign them, are these (quoted from the modelling brief the model builders received):

> Every quantity, value, status, or identifier the document names is a typed attribute on the class that holds it.
> Every rule, calculation, check, tolerance, trigger, update, or notification the document describes is an operation, with parameters and return type, on the class the document says performs it. The description carries the document's formula or condition.
> Things the document treats as kinds of one thing share a superclass, and their common attributes and operations are declared once, on the superclass.
> Timings: the time quantities that describe a flight's progress, each with its origin, accuracy, and tolerance.
> An operation sits on the class the document names as performing it: a CDM platform action on the platform class, a procedure stated under a milestone on that milestone.
> Information about a flight (flight plan, slot, status) lives in Flights; exchanging it is a message class in Messages or an operation on the sender.
> Each time quantity is a class in Timings. The flight or milestone that carries it has an attribute typed by that class. Every successive value is kept, with its originator and time of update, so a turn-round can be analysed afterwards; an update appends rather than overwrites.
> A status is an enumeration placed with the class whose state it describes.

Apply them as follows.

- `operation`: any rule, calculation, check, tolerance, trigger, update, or notification the document describes. The claim text is the clause that states the rule or condition. `owner` is the party or thing the document names as performing it (for a procedure stated under the milestone with no other performer named, the owner is the milestone itself).
- `class`: a thing the document names that persists across the process, namely a stakeholder, flight, aircraft, flight plan, slot, milestone, message, system, or time quantity. Every time quantity the document names (a prefix such as Estimated, Target, Actual, Calculated, Scheduled, with an event such as Off-Block, In-Block, Landing, Take-Off) is a class. `owner` is empty.
- `attribute`: a named value or property of such a thing, including the origin, priority, accuracy, and tolerance the document states for a quantity or milestone. `owner` is the thing that holds it.
- `relationship`: a structural link the document states between two things, namely who originates, sends, receives, holds, or triggers what. `rel_type` is `generalization` when the document treats several things as kinds of one thing, otherwise `other`. `owner` is empty.
- `enumeration`: a status or other fixed set of named values. The operational status a milestone changes the flight to is an enumeration literal; state it as a claim of kind `enumeration` with the literal in the text. `owner` is the thing whose state it describes.

# Procedure

For each sentence, in the order given, decide `keep` or `drop` and give a one-line reason.

Drop a sentence when it carries nothing a class model realises: explanatory rationale, a cross-reference to another section, a restatement of the milestone's name, a value such as "Not applicable". A dropped sentence has no claims.

For a kept sentence, list every claim it carries. One sentence often carries claims of several kinds; for example "The CTOT is issued by the Network Operations and is sent to relevant ATS units" carries a class (CTOT), a relationship (Network Operations originates CTOT), and a relationship (CTOT is sent to ATS units). A formula such as "TTOT equals TOBT+EXOT" is one operation claim whose text is the formula. Do not split a single rule into fragments that cannot be checked alone, and do not merge two rules into one claim.

When a sentence restates a claim already made by an earlier sentence in this milestone, still list the claim, and set `duplicate_of` to the earlier claim's id (`<sentence id>.c<k>`, where k counts the claims of that sentence from 1). The expert decides which copy stays.

`text` is the sentence or the clause of it, verbatim from the document, with no paraphrase. Use the document's own names and abbreviations. Do not invent a class name, an attribute name, or a formula the text does not give.

Return the sentences in the order received, every one of them, with your decision. Do not return commentary outside the schema.

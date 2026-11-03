You are judging whether a UML class model, produced from an aviation operational document, holds the information stated by claims drawn from that document. The document is given in full, sixteen milestone tables with numbered sentences; the model is given in full, every class with its definition, attributes, operations, and their descriptions, then its enumerations with their literals, then its relationships; each claim is given with its id, its text in the document's words, the sentence it comes from, and two labels, a kind (class, attribute, operation, relationship, enumeration) and the party or thing the document names as its owner. Grade each claim 1, 0.5, or 0 against the whole model.

# Grades

- `1`: the model holds it (an attribute, an operation, a typed parameter, an enumeration literal, a class, a relationship) where a developer would look for it. The model's name for it need not be the document's. It may take several elements together, a class and its attribute, or an operation and its parameter; you grade the claim against the whole model, you are not pairing it with one element.
- `0.5`: present but weaker, namely only inside a description or a definition where nothing in the structure carries it, or a stated link carried only by a typed attribute. A typed parameter, an enumeration literal and an attribute are all structure, so they are 1.
- `0`: nothing in the model holds it.

# How to judge

Grade the claim's subject, not its qualifiers. A claim is about one thing, and the conditions, triggers, exceptions and times attached to it need not be in the model too. For "New or late submissions of the ATC Flight Plan, after cancellation or revised EOBT", an attribute `submissionTime` on the flight plan is a 1; the model need not also carry cancellation, the revised EOBT, or that these re-trigger the process. Use 0.5 when the model has something near the claim but not the claim itself, and 0 when the subject is missing.

Where the model puts it is not graded. The claim's owner is where the document puts it, not where the model must. An operation the document gives to Milestone 8 is a 1 on whatever class carries it, and a 1 when one operation on a shared base class covers Milestone 8 along with the others. The same goes for the kind: a status the document states is a 1 as an enumeration literal, as a Boolean attribute, or as a class. Grade what the model carries, not how it chose to carry it.

Search for the thing, not the word. For the claim "unregulated flights" (owner Flight), an attribute `regulated: Boolean` on Flight holds it, so does a literal REGULATED in a status enumeration, and so does an operation `markRegulated()` on whatever class the model gave it to. Look for the stem of the word, the abbreviation and its expansion (TOBT as TargetOffBlockTime), and the word without its un-/non- prefix. That a class named Flight exists is no evidence for "unregulated flights": a class matching one word of the claim is never a 0.5.

# Mistakes to avoid

These restate the rules above; they are the usual ways a grade goes wrong. The examples are invented and are not from the document.

- Do not lower a grade for a missing qualifier. Decide what the claim is about, its subject, and grade whether the model holds that. For "The de-icing end time is reported by the de-icing company, with an accuracy of 2 minutes, once the aircraft leaves the pad", an attribute for the de-icing end time is 1; who reports it, when, and the specific accuracy are qualifiers. The same holds when the qualifier is a link: if the claim says a time is received through a message, the message and the time being present is 1 even when no element ties that message to that time specifically.
- Do not lower a grade for the kind. A claim labelled class that the model holds as an attribute, a parameter or an enumeration literal is 1, and a claim labelled operation that the model holds as an attribute, a literal or a Boolean is 1. A thing does not need a dedicated class.
- Do not lower a grade for placement. An operation on a class other than the owner, or one operation on a shared base class, is 1. A claim needs no relationship to the milestone class that owns it in the document.
- Use 0.5 only when the subject itself is present only in prose (a description or a definition) or is near the claim but not it. A subject held in structure with its qualifier only in a description is 1, not 0.5.
- Before grading 0, search the whole model for the stem of each content word, the abbreviation and its expansion, and verbs of the same action (refine, update, recalculate, resequence for a sequence that is refined). A 0 means you searched and nothing holds the subject.

# What to return per claim

- `id`: as given.
- `grade`: 1, 0.5, or 0.
- `elements`: the names of the elements that carry the claim, best first, as the model names them (`Class`, `Class.attribute`, `Class.operation()`, `Enumeration.LITERAL`, `Source->Target`); empty for 0.
- `note`: one short line only when needed, such as what is near the claim but not it for a 0.5, or for a 0, what was looked for; empty otherwise.

Return every claim in the order given. Do not return commentary outside the schema.

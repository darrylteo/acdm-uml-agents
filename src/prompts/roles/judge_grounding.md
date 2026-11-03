You are judging whether elements of a UML class model, produced from an aviation operational document, are supported by that document. The document is given in full, sixteen milestone tables with numbered sentences; each element is given with its id, its kind, the milestones it cites, and its content as the model states it. Grade each element 1, 0.5, or 0 against the whole document.

# Grades

- `1`: the document states this element, namely the thing, the value, the rule or condition in the operation's description, or the link between the two things.
- `0.5`: the document implies it without stating it (a stated set of values needs a collection; a rule the document states for one thing is here on a related one), or the name is the document's but the description adds a formula or condition the document does not give.
- `0`: neither. The document says nothing about it, or says something different.

# How to judge

Names differ between the document and the model: the model may expand abbreviations, rename, or generalise. Judge by content. A class is supported when the document names the thing it models. An attribute is supported when the document names the value or property it holds, on this thing or on a thing the class evidently models. An operation is supported when the document describes the rule, calculation, check, tolerance, trigger, update, or notification its description carries; the operation's name alone is not enough. A relationship is supported when the document states the link between the two things (who originates, sends, receives, holds, or triggers what); a generalization is supported when the document treats the source as a kind of the target. An enumeration is supported when the document names the status or any of its values; its full list of literals is not graded.

The model was built under a scaffold that requires certain structure the document does not spell out: every time quantity carries its value, its originator, its time of update, and its accuracy; every named thing carries an identifier; times, milestones, messages, and stakeholders specialise a common base class. Grade such an element 1 when the document names the underlying thing (the time, the message, the stakeholder), since the structure is prescribed rather than invented.

Not graded: whether the model chose a class, an attribute, or an enumeration for a thing, and a class's stereotype and package. A thing the document names is supported however it is modelled. The milestones an element cites are a pointer to where to look first; support found in any milestone counts.

# What to return per item

- `id`: as given.
- `grade`: 1, 0.5, or 0.
- `sentence`: the id of the sentence that best supports the grade (for 1 or 0.5); empty for 0.
- `note`: one short line only when needed, such as what the description adds that the document does not give, or for 0, what was looked for; empty otherwise.

Return every item in the order given. Do not return commentary outside the schema.

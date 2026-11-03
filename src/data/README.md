# Source document

`document.txt` and `milestones.json` hold the text of the sixteen A-CDM milestone tables (Definition, Origin and priority, Timing, Data Quality, Effect, Procedures, Operational Status, Action on CDM Operation), extracted from pages 3-18 to 3-33 of the EUROCONTROL *Airport CDM Implementation Manual* (version 5.0, 2017). `src/ingest/parse_milestones.py` produced both files from a PDF of those pages.

The manual is published by EUROCONTROL. The PDFs of the extracted pages (`acdm milestone only.pdf`) and of the manual's abbreviations and acronyms list (`acdm acronyms only.pdf`, pages XI-XIII) are not included in this repository. Obtain the manual from EUROCONTROL to regenerate `document.txt`; `parse_milestones.py` expects the milestone pages at `src/data/acdm milestone only.pdf`.

The extracted text is the input that every scored run, the claim inventory and both grading tasks were based on. `src/evaluate/abbreviations.json` holds the manual's abbreviation list, which the evaluation code uses for name matching, and `src/evaluate/claims.json` holds the claim inventory, each claim quoting a sentence of the tables. Their inclusion is the repository authors' decision.

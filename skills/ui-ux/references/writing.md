# Writing

This reference of the `ui-ux` skill holds unslop, technical-writing, and document formats (docx, pdf, slides, spreadsheets); their detail is in `writing/` (see Index). Every piece of prose in this repo goes through these rules: PR bodies, commit messages, docs, agent prompts, product copy, and files like decks or spreadsheets. The Unslop rules come first because every other section and every prompt that bakes them copies from here. Why: readers stop trusting text the moment it sounds machine-made, and a reviewer skims a sloppy PR body instead of reading it.

## Unslop writing rules

Apply these to all output. When an agent cannot load skills, bake this whole section into its prompt. Do not write a shorter list; a partial list teaches that the missing patterns are fine. The source file is [`writing/unslop.md`](writing/unslop.md).

### Process

1. Scan for the patterns below.
2. Rewrite. Preserve meaning, match intended tone.
3. Add soul (see next section).
4. Self-audit: "What makes this obviously AI generated?" Fix remaining tells.

### Adding soul

Removing patterns is half the job. Sterile, voiceless writing is just as obvious.

- **Have opinions.** React to facts instead of neutrally listing pros and cons.
- **Vary rhythm.** Short sentences. Then longer ones that take their time. Mix it up.
- **Acknowledge complexity.** "Impressive but also kind of unsettling" beats "impressive."
- **Use "I" when it fits.** First person isn't unprofessional.
- **Let some mess in.** Perfect structure looks machine-made.
- **Be specific.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am."

### Patterns to detect and fix

#### Content

1. **Puffery.** "pivotal moment", "testament to", "evolving landscape", "setting the stage for", "indelible mark", "deeply rooted". Cut puffery, state what happened.
2. **Name-dropping.** Listing media outlets without context. Pick one, say what was said.
3. **Superficial -ing phrases.** "highlighting...", "ensuring...", "reflecting...", "showcasing...", "fostering...". Delete or expand with real sources.
4. **Promotional language.** "nestled", "vibrant", "breathtaking", "groundbreaking", "renowned", "stunning", "must-visit". Use neutral descriptions.
5. **Vague attributions.** "Experts believe", "Industry reports suggest", "Some critics argue". Name the source or delete.
6. **Formulaic challenges.** "Despite challenges... continues to thrive." Replace with specific facts.

#### Language

7. **AI vocabulary.** Additionally, crucial, delve, enduring, enhance, fostering, garner, interplay, intricate, landscape (abstract), pivotal, showcase, tapestry (abstract), testament, underscore, vibrant. Replace with plain words.
8. **Fancy ways to say "is".** "serves as", "stands as", "boasts", "features". Just say "is" or "has".
9. **"Not just X, but Y."** State the point directly instead.
10. **Rule of three.** Forcing ideas into groups of three. Use the natural number.
11. **Synonym cycling.** Protagonist, main character, central figure, hero all in one paragraph. Pick one, repeat it.
12. **False ranges.** "from X to Y" where X and Y aren't on a meaningful scale. List topics directly.

#### Style

13. **Em dash overuse.** Avoid em dashes entirely. Use periods or commas only (no parentheses, no en dashes, no hyphen-as-dash substitutes). Em dashes are an AI tell, and reaching for parentheses instead just trades one tell for another. If a thought needs separation, end the sentence or use a comma.
14. **Colon overuse.** Colons are fine before a list or example. Not as mid-sentence connectors. "If you're coming from traditional automation: instead of registering event handlers, you describe conditions" adds nothing with the colon. Rewrite to let the point stand on its own without comparison framing. "Describing when the scheduler should fire works best as plain English." Same meaning, no crutch punctuation.
15. **Boldface overuse.** Don't bold every proper noun or acronym.
16. **Inline-header lists.** The tell is a bold label and colon that restates the line: "**Performance:** Performance improved...". Convert those to prose. A bold lead-in that ends in a period, names the item, and is followed by genuinely new detail ("**Schema in TypeScript.** Tables live in one file.") is fine, not a tell.
17. **Title case headings.** Use sentence case.
18. **Decorative emojis.** Remove from headings and bullets.
19. **Curly quotes.** Replace with straight quotes.

#### Communication artifacts

20. **Chatbot phrases.** "I hope this helps!", "Let me know if...", "Of course!", "Certainly!", "Found the smoking gun!" Remove.
21. **Cutoff disclaimers.** "While specific details are limited..." Find sources or remove.
22. **Sycophantic tone.** "Great question! You're absolutely right!" Respond directly.

#### Filler

23. **Filler phrases.** "In order to" becomes "To". "Due to the fact that" becomes "Because". "It is important to note that" gets deleted.
24. **Excessive hedging.** "could potentially possibly be argued that it might" becomes "may".
25. **Generic conclusions.** "The future looks bright." State specific plans or facts.

#### Jargon

26. **Abstract metaphor nouns.** Substrate, wedge, vector, locus, vantage, nexus, primitive (as noun), harness (as metaphor), surface (as in "API surface"), bedrock, scaffolding (as metaphor), modality, paradigm, gold-plating, ratchet (as metaphor), evacuate (for moving code), endgame, north star, flywheel. These read as technical but usually have a plainer concrete word. "Substrate" becomes "base". "Wedge in" becomes "add". "Vector" becomes "way" or "method". "Gold-plating" becomes "more than the job needs". "Ratchet" becomes the mechanism's real name or "a limit that only tightens". "Evacuate" becomes "move out". "Endgame" becomes "the last phase". Pick the concrete word.

#### Plain speech

27. **Say what it does, not how it feels.** "the database stays close at hand", "SQL you can read", "types that follow your schema" name a feeling. The fix names the mechanism or a number: "`.toSQL()` returns the exact string sent to the database", "a column rename fails the build". Ask what the sentence tells the reader to do or know, then write that. If you can't restate it as a concrete instruction, fact, or number, cut it. One more check: if the sentence could appear unchanged in another project's docs, it says nothing about this one. Cut it.
28. **Shorten or split dense sentences.** If the reader has to backtrack to parse a sentence, break it in two or drop clauses. One idea per sentence.
29. **Active voice.** Prefer it. Catch "is/are/was/were + past participle" and name the actor: "queries are validated" becomes "the compiler validates queries", "the file is parsed by the loader" becomes "the loader parses the file". Passive is fine only when the actor is unknown or genuinely doesn't matter.
30. **Cut adverbs, or use a stronger verb.** "runs quickly" becomes "is fast" or the number. "significantly improves" becomes the measured delta. An adverb propping up a weak verb means the verb is wrong.
31. **Prefer the plain word.** "utilize" becomes "use", "leverage" becomes "use", "facilitate" becomes "help", "numerous" becomes "many", "in the event that" becomes "if". The fancier synonym is rarely clearer.
32. **Mannered prose.** Use the literal phrase when one exists. Cut aphorisms ("wire it or delete it"), rhetorical fragments, personified code ("the plan holds it"), figurative verbs ("rides along", "stands on"), and stock frames. "A dial worth turning" becomes "a parameter worth varying". Say what you mean. Rule 26 covers metaphor nouns. This rule covers the other flourish.
33. **Over-compression.** Do not drop articles, drop verbs, or write symbol-speak the reader has to decode. Spell out arrows and abbreviations. Keep real symbol names. "Parser rejects bad date → exit 2, no write" fails. "The parser rejects a bad date, exits with code 2, and writes nothing." passes. Write whole sentences.

## Technical writing

Full standard: [technical-writing](writing/technical-writing.md). The short form:

1. Pick one mode per document (Diátaxis): tutorial, how-to, reference, or explanation. Split and link instead of mixing. Why: a reader looking up a fact should not wade through a lesson.
2. Talk to the reader as "you", present tense, commands for instructions, condition before the instruction, common case first.
3. One thought per sentence. Keep articles. Split instructions over about 20 words.
4. Leave no sentence open to two readings: "only" next to its word, every "it" points at one thing, one name per thing everywhere.
5. Write real symbols, paths, and commands. Every count is true at the commit that lands it.
6. Cut every word that does no work, but vary rhythm and keep a view. Sterile is also a tell.

Every claim carries its evidence or its label in the same sentence: the command and its output, a `path:line`, or `measured`, `inferred`, or `guess`. Never hand the reader a check you could have run.

### Reader test

The final gate for docs, specs, READMEs, and long PR bodies. Why: the author fills gaps from memory; a reader with no context cannot.

1. Write down the five to ten questions a real reader of this document will arrive with.
2. Give the finished document's path to a fresh sub-agent with no context from this thread. Ask it those questions and nothing else. Tell it to answer only from the document and to say "not in the doc" when it cannot.
3. Compare its answers with the truth. Every wrong answer, "not in the doc", or answer that needed a guess is a gap in the document. Fix the document, not the questions.
4. Rerun with a new fresh sub-agent until every answer is right.

A spec's reader test also asks, for a few slices, the owner files, the forbidden files, and the done test (see `/layered-spec` "Spec self-review"). Idea from anthropics/skills `doc-coauthoring` "Reader Testing", rewritten here.

### PR bodies and commit messages

A PR body is a briefing a smart non-specialist reads in under a minute. Lead with what broke and what changed for users. Use the AGENTS.md headings:

- **What was wrong**
- **What this fixes**
- **What you should notice**
- **What this does not do**
- **Checks** (name the focused tests you ran and their results. Do not paste full CI logs; link them.)

Title in everyday words. Link logs and tables instead of pasting them. Commit messages: one line saying what changed, then a short body with why if it is not obvious. Unslop both.

## Document formats

Render and look at the output before you hand it over. Why: text extraction hides broken tables, overflowing slides, and uncalculated formulas that the reader sees immediately.

- **docx**. `python-docx` to create or edit; `soffice` to PDF then `pdftoppm` to PNG for a visual check after each meaningful change.
- **pdf** ([pdf](writing/pdf.md)). `reportlab` to generate, `pdfplumber` or `pypdf` to extract, `pdftoppm` to render and inspect every page.
- **slides**. HTML decks: render every slide at its target size and check overflow. For deck structure, see `design/design-kit/references/slides.md`.
- **spreadsheet**. `openpyxl` for xlsx formatting and formulas, `pandas` for analysis and csv. Use formulas for derived values, not hardcoded results, and recalculate before delivery.

Intermediate files go in `tmp/<format>/`; finals in `output/<format>/`. Never stage either.

## Index

| Reference | Use for |
|---|---|
| [unslop](writing/unslop.md) | Source of the Unslop rules above. Tests read it; keep it intact. |
| [technical-writing](writing/technical-writing.md) | Diátaxis modes, Google style, STE, Global English, worked example, review checklist. |
| [pdf](writing/pdf.md) | Reading, generating, and reviewing PDFs. |

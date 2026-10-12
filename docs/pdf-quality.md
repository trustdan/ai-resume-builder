# PDF quality checks and their limits

Every successful CLI build runs the same checks available through `python resume.py qa PROJECT --variant FORMAT`:

- Inspect the font table for embedded fonts, Unicode maps, and Type 3 bitmap fonts.
- Extract text in normal and layout-preserving modes; reject empty text, control/replacement characters, and a small set of known dropped-ligature patterns.
- Report page count, unfinished starter placeholders, and overfull-box warnings from the build.
- Save both extracted text files alongside the PDF.

The preamble uses pdfLaTeX, T1 encoding, Latin Modern fonts, Unicode mappings, and disabled ligatures. Preserve that tested combination. Use single-column flow with inline headings and simple text bullets. Avoid body tables, icons, text boxes, floating elements, and image-only text.

`PASS` means these technical checks passed. It does not check every word against the source, verify reading order automatically for personal documents, certify ATS acceptance, verify facts, or predict a hiring decision. The demo regression tests separately check expected facts and order in both extraction modes.

Before sending, visually inspect each page for clipping, collisions, split entries, tiny type, and unwanted breaks. Read both extracted text files: headings, dates, and bullets should stay associated. Compare all material claims to your inventory. Never dismiss a QA finding without inspecting its context.

Use the [ATS and flatness checklist](ats-and-flatness.md) to record that review. The [cover letter builder](cover-letters.md) runs these same checks; it does not automatically approve letter length, prose, recipients, or factual support.

The supplied `review` command flags a few clichés and vague phrases for judgment. It is not an AI-authorship detector. Accurate specialist language should stay when useful.

Sources: [microtype documentation](https://ctan.org/pkg/microtype), [pdfTeX documentation](https://www.tug.org/applications/pdftex/), [Poppler](https://poppler.freedesktop.org/).

# ATS readability and resume flatness

Here, **flatness** means the resume has one coherent text sequence: the name and contact information, headings, job blocks, and bullets read in their intended order. It does not mean removing useful emphasis or turning the PDF into an image. All four supplied resume formats use the same single-column text flow; there is no separate flat version to synchronize.

ATS readiness is a review process, not a score this tool can guarantee. First follow the specific application's file-format, length, history, and field requirements. A readable PDF does not substitute for a required DOCX or application form. This package produces PDF and text extracts; it does not export DOCX.

## Preserve the source structure

| Keep | Avoid | What to review |
| --- | --- | --- |
| Name and contact information as body text | Contact fields only in a header/footer, icons, or images | Name, email, phone, and visible URL appear in both extracts |
| One column with ordinary paragraphs and headings | Sidebars, tables, minipages, floating boxes, positioned overlays | Headings and paragraphs follow the PDF's intended sequence |
| Each title, employer/descriptor, date range, and location together | Separate date columns or layout-only alignment | Every date belongs unambiguously to the correct job |
| Normal text bullets and visible, accurate terminology | Hidden keywords, graphical rating bars, text rendered as an image | Complete bullets and symbols survive extraction |
| Tested fonts, Unicode maps, and disabled ligatures | Untested font substitutions or image/scanned exports | Words such as office, workflow, and certified stay intact |

Chronological, hybrid, and functional formats organize accomplishments differently. They still need truthful, intelligible employment history. Employer-light changes emphasis; `--anonymous` omits employer names only. Record any deliberate omission and follow the application's requirements. See [format tradeoffs](choose-a-format.md).

## Repeatable review

1. Build the selected format: `python resume.py build personal/my-resume --variant hybrid`.
2. Read `build/personal/my-resume/hybrid/resume.default.txt` from start to finish. Check headings, complete words and symbols, job associations, dates, and every material claim against the inventory and source.
3. Read the adjacent `resume.layout.txt`. Whitespace can differ; the meaning and sequence should agree. Look for missing, duplicated, detached, or interleaved text. Copy/paste from the PDF viewer as an additional check when available.
4. Inspect **every PDF page**, including page boundaries. Check readable type, unclipped contact fields, collisions, split headings, stranded dates, and accidental blank pages. Preview PNGs show only page one.
5. Confirm target-specific requirements, remove all placeholders and the draft notice, and record the exact output and checks in `qa-log.md`. If an application offers a parsed preview, compare it with the submitted document and correct fields as needed.

An overfull warning calls for visual inspection even if QA passes. When order fails, simplify the source flow and rebuild; spacing patches cannot reliably repair a structurally ambiguous layout. Keep the document in draft until remaining issues are resolved.

## What the tools establish

The [PDF checks](pdf-quality.md) test font embedding/maps, extractable text, and selected corruption patterns. They save two text views and report warnings. They do **not** compare every personal claim with its source, automatically approve personal reading order, validate an employer's parser, or verify factual accuracy. The fictional demo tests separately assert expected facts and heading/history order.

The [instruction files](agent-guidance.md) carry these rules into assisted editing and new personal projects. They guide an assistant; they cannot guarantee that an editor loaded the files or replace a final review.

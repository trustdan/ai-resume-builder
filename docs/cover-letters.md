# Build a cover letter

The letter builder turns **your written plain text** into editable TeX, a matching PDF, and two text extracts. It uses the name, contact information, career focus, and document notice from `candidate.tex`. It runs locally with the same Python, pdfLaTeX, and PDF tools as the resume. No AI account is needed; the builder does not research an employer, write claims for you, or submit an application.

## Start with evidence

Create a project if you do not have one:

```text
python resume.py new personal/my-application --variant hybrid
```

Fill `experience-inventory.md`, save the posting in `job-description.md`, and complete `cover-letter-brief.md`. Map each example to evidence IDs and the employer's actual requirements. Confirm the company, role/requisition, recipient, and date. Use a neutral salutation when no recipient is known. Ask about availability, relocation, work authorization, or relationships before including them.

Edit `candidate.tex` for your shared contact details and `cover-letter.json` for the letter. Keep the letter focused: an opening, one to three supporting paragraphs, and a closing. Explain your contribution to a supported outcome rather than copying every resume bullet. Follow the requested length; the builder does not force a one-page limit.

## Plain-text input

```json
{
  "date": "11 October 2026",
  "company": "REPLACE ME: company",
  "role": "REPLACE ME: role and requisition",
  "salutation": "Dear Hiring Team,",
  "opening": "REPLACE ME: connection between the role and your confirmed experience.",
  "paragraphs": [
    "REPLACE ME: a specific example connected to a stated employer need."
  ],
  "closing": "REPLACE ME: concise closing and any confirmed logistics.",
  "signoff": "Sincerely,"
}
```

| Field | Rule |
| --- | --- |
| `date`, `company`, `role`, `opening`, `closing` | Required nonempty strings; write the date explicitly |
| `paragraphs` | Required list of one to three nonempty strings, one per paragraph |
| `salutation`, `signoff` | Optional; default to `Dear Hiring Team,` and `Sincerely,` |

Unknown fields and invalid types are rejected to catch typos. Save UTF-8 JSON. Use ordinary `%`, `&`, `$`, `_`, `#`, braces, and other punctuation; **do not TeX-escape JSON text**. JSON itself requires `\"` for a quotation mark within a string and `\\` for a literal backslash. Line breaks inside a field become spaces; the `paragraphs` list controls paragraph boundaries. TeX commands entered into JSON print as literal text. The tested font setup supports the supplied English/Latin examples; other scripts, emoji, or unusual glyphs may need a separate font/engine workflow and renewed extraction review.

See the [fictional JSON example](../examples/demo-person/cover-letter.json) and [evidence mapping](../examples/demo-person/cover-letter-brief.md). Never use its invented claims as your own.

## Generate, build, and revise

```text
python resume.py letter personal/my-application
```

This reads that project's `cover-letter.json`, writes `cover-letter-content.tex`, and builds/checks:

```text
build/personal/my-application/cover-letter/cover-letter.pdf
build/personal/my-application/cover-letter/cover-letter.default.txt
build/personal/my-application/cover-letter/cover-letter.layout.txt
build/personal/my-application/cover-letter/cover-letter.qa.json
```

Logs live in the same output directory. A missing dependency is reported before generation. Invalid JSON or fields leave existing generated content untouched. A later compile failure can leave the new TeX content in place; fix the source and rebuild, and do not use an earlier PDF as proof of success.

On later revisions, edit JSON and explicitly regenerate:

```text
python resume.py letter personal/my-application --replace
```

The first command refuses an existing generated file. `--replace` replaces **cover-letter-content.tex**, including any manual edits there. Back it up before regeneration if needed. Neither command changes `candidate.tex` or the resume variants. JSON changes take effect only after running `letter`; a normal `build` does not regenerate JSON.

To rebuild existing TeX or rerun checks without regeneration:

```text
python resume.py build personal/my-application --variant cover-letter
python resume.py qa personal/my-application --variant cover-letter
python resume.py review build/personal/my-application/cover-letter/cover-letter.pdf
```

`--all` still means the four resume formats; build the cover letter separately. The letter command accepts projects under `personal/` only, protecting the published fictional examples.

## Direct TeX editing and older projects

The original workflow still works: edit the Letter/Target macros in `candidate.tex` and the body in `cover-letter.tex`, then use `build --variant cover-letter`. Until generated content exists, the template uses those fallback macros and shared accomplishments. If `cover-letter-content.tex` exists, it overrides the letter fields and body; edit that generated file directly or regenerate from JSON. To return to the fallback, move the generated file out of the project's active source path after backing it up.

Older projects are not updated automatically. Back up and compare their `cover-letter.tex`, then merge in the current `templates/cover-letter.tex` defaults and optional-content input. Copy `templates/cover-letter.json` and `templates/cover-letter-brief.md` into the project only if absent; merge existing work deliberately. The builder refuses a letter template without the generated-content input. Shared contact and existing Letter/Target macros must still be defined in `candidate.tex`.

## Review before sending

Check company, role, requisition, recipient, date, shared contact details, and every claim against the inventory and resume. Remove placeholders; set `DocumentNotice` to `{}` only once the personal draft is complete. Inspect every PDF page and both text extracts using the [flatness checklist](ats-and-flatness.md). Aim for a readable letter within the application's length limit; shorten prose before shrinking type.

Record output path, page count, claim review, extraction order, visual review, and remaining questions in `qa-log.md`. Technical PASS verifies limited PDF properties; placeholders are warnings, and the JSON builder cannot verify evidence. For optional AI help, use the [cover letter prompt](../prompts/build-cover-letter.md).

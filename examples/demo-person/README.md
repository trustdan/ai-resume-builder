# Fictional demo: Riley Morgan

Every person, employer, credential, posting, and result here is invented for teaching. Contact details use example.com and a fictional-use phone number. This is not an actual applicant's record.

Build all four formats:

```text
python resume.py build examples/demo-person --all
```

Compare employer-light with and without employer names:

```text
python resume.py build examples/demo-person --variant employer-light --anonymous
```

That switch removes the two employer names only. It does **not** anonymize the candidate, contact details, education, or potentially identifying achievements.

`candidate.tex` holds the shared facts. The four `resume.tex` files arrange them differently. Shared extraction and layout files live in `shared/`. Every layout can also be compiled directly with pdfLaTeX from its own directory, but the root CLI keeps output tidy and runs QA automatically.

The inventory deliberately includes an unconfirmed budget figure. It appears in no finished PDF. Use `python resume.py new personal/my-resume` to start your own document with placeholders rather than copying Riley's accomplishments.

The cover-letter.json and cover-letter-brief.md demonstrate plain-text input and evidence mapping for the [cover letter builder](../../docs/cover-letters.md). To try it, create a personal project, copy these fictional letter inputs and candidate.tex into that test project, and run `letter` there. The letter generator refuses public example projects. The checked-in cover-letter.tex remains a direct-TeX example.

# From experience to an application

1. Create a project with `python resume.py new personal/my-resume --variant hybrid`. It contains all formats, shared TeX files, and Markdown scaffolds. Its project.json stores the default format.
2. Fill experience-inventory.md with actions, scope, outcomes, dates, official titles, and evidence. Keep questions separate. For team results, explain your contribution without taking sole credit.
3. Capture the target posting in job-description.md. Record required file format, length, and any application-specific fields.
4. Complete tailoring-brief.md before writing. Match requirements to evidence and label Strong / Partial / Gap. A gap is a question or limitation, not permission to invent.
5. Edit candidate.tex, then adjust the selected variant/resume.tex. The sample has two roles; add/remove roles, capabilities, education, or community sections to fit your actual career. Comments explain LaTeX escaping. Edit personal shared/layout.tex to change common blocks.
6. Build and review. `python resume.py build personal/my-resume` compiles the configured format twice and runs font/text QA. `--variant chronological` overrides the default; `--all` builds the four resume formats.
7. Open the PDF and read the neighboring resume.default.txt and resume.layout.txt. Check contact details, claims, section order, dates, and breaks. Record the revision in qa-log.md.

Output is under `build/personal/my-resume/FORMAT/`. For cover letters, complete cover-letter-brief.md, write plain text in cover-letter.json, then run `python resume.py letter personal/my-resume`. This generates cover-letter-content.tex and builds cover-letter.pdf. Use `--replace` for later JSON regeneration after preserving manual edits. Direct TeX builds use `--variant cover-letter`; `--all` includes only the four resumes. See the [cover letter guide](cover-letters.md). Routine outputs are ignored by Git. A build doesn't submit or upload anything.

Follow the [ATS and flatness checklist](ats-and-flatness.md) for every final document. New projects include their own AGENTS.md with evidence, layout, and review rules; see [assistant guidance](agent-guidance.md). Existing projects need deliberate merges to adopt new scaffolds.

Remove `DocumentNotice` from your personal candidate.tex (set it to `{}`) once the draft is complete. Replace every `REPLACE ME`; the starter will warn about remaining placeholders but compiles so you can check setup first. Do not submit sample facts or unfinished placeholders.

LaTeX basics:

```latex
\newcommand{\CandidateName}{Your Name}
\newcommand{\WorkflowAchievement}{Cut routing time by 20\% across R\&D intake requests.}
% Dollars: \$500   Underscore: project\_name   Hash: \#1
```

Normal text braces group content; use `\{` and `\}` for literal braces. Add a new bullet with `\item Your text`. If it starts with `[`, use `\item{} [Your text]` so TeX does not treat it as a bullet label. Use straight quotes, not TeX's doubled quote shortcuts with disabled ligatures.

Optional writing review:

```text
python resume.py review build/personal/my-resume/hybrid/resume.pdf
```

Review findings in context. No tool can verify your accomplishments from the final PDF alone.

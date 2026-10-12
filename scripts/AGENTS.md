# Tool maintenance

Read the root AGENTS.md. Keep Python 3.10 compatibility and the standard-library-only, local workflow. Use argv subprocess calls, no shell interpolation, pdfLaTeX with shell escape disabled, bounded runtime, and no automatic installers or uploads.

Preserve project path containment, linked-path rejection, non-overwrite defaults, isolated builds, and stale-output cleanup. The cover letter builder must validate all input before replacing generated content, escape plain text once, refuse public example projects, and require explicit --replace for existing content. Do not change the meaning of --all (four resume formats).

Preserve exact release allowlisting; include new public files explicitly. Keep technical checks distinct from human facts, reading-order, and visual reviews. Do not label font/text PASS as ATS certification or application readiness.

For behavior changes, add meaningful regressions for failure and success paths. Run `python -m unittest discover -s tests -v`, all four demo resumes, anonymous employer-light, and the cover letter. Exercise new letter rendering with the actual compiler and both extractors, including literal TeX-sensitive characters. Inspect changed PDFs and document actual platform coverage.

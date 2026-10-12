# Maintain and release the starter

1. Run `python resume.py doctor` and `python -m unittest discover -s tests -v`.
2. Run `python resume.py previews`. This rebuilds the four fictional resumes, employer-light with names omitted, and the cover letter; it requires pdftoppm. Open all six PDF/PNG pairs. Confirm facts, reading order, one-page demo layout, and no clipping.
3. Update validation.md with platforms actually exercised. Configuration review is not a hands-on editor test. Do not claim that CI passed before running it remotely.
4. Review release-manifest.json. It lists exact approved files; add new public documentation/tools explicitly, including nested AGENTS.md files, cover letter scaffolds, and tests. Do not add personal/build paths or directory globs.
5. Export to a new destination: `python resume.py export --output build/release/resume-maker --zip`.
6. Run doctor, tests, a demo build, and a new personal starter build from the exported folder. In a temporary personal project, try the JSON letter builder and explicit --replace revision; verify that a normal build uses existing generated TeX. Check the exported files and PDF metadata for personal information. The real compiler tests cover the letter workflow when external tools are installed; skipped tests do not establish that coverage.
7. Create/publish a separate repository when ready. Replace YOUR-ACCOUNT in the clone example with its real URL. Do not carry personal history into the public starter.

The GitHub workflow exercises unit checks on Windows, macOS, and Linux, and full TeX builds on Ubuntu. Other platforms need their own full build validation. The template repository can be cloned normally; users do not need GitHub Actions to build locally.

Preview images are generated from actual PDFs with pdftoppm; no image-generation service is involved. A future visual redesign should preserve extraction tests and review all changed PDFs.

Exports refuse existing folders and ZIPs. When refreshing a prior release, export and verify a new destination first, preserve the earlier artifacts, then promote the reviewed folder and ZIP to the shared location. Do not weaken non-overwrite behavior to simplify release maintenance.

# Validation record

Initial release: 11 October 2026.

## Verified locally

Environment: Windows, Python 3.13.15, MiKTeX-pdfTeX 4.26, and Poppler-compatible tools 24.04.0. No third-party Python packages are required.

- Doctor found all required executables and TeX files.
- The initial release's 22 tests passed locally and in a fresh standalone export. The documentation/letter update has 31 tests, all passing locally and in an independently exported folder with spaces in its path, including real compiler/extractor cases with no skips.
- The four resume formats, employer-light with employer names omitted, and the cover letter compiled to one page each. Font/text QA passed, and the demos had no overfull boxes.
- Visually inspected all six rendered previews for spacing, clipping, and page breaks.
- Checked expected facts, accented text, ligature-prone words, title/date chronology, and section order in both extraction modes. Verified that anonymous employer-light removes the two employer names while preserving titles and dates.
- Confirmed that the inventory's unverified budget figure appears in no demo output.
- Created and built a fresh personal starter from the standalone export. Placeholder warnings appeared as expected; writing review ran successfully.
- Exercised missing executables, a missing package, invalid TeX, missing PDF, extraction failure, path traversal, existing destinations, private-file exclusions, and stale-PDF removal after a compile error. Some tool-failure cases use controlled mocks; compiler and path-with-spaces cases use the real tools.
- Reviewed local Markdown links, editor task JSON, release allowlist, UTF-8 files, whitespace, and PDF metadata. All approved PDFs identify only the fictional candidate as author. Personal work and repository history are excluded from the export.

## Documentation and letter-builder update: 11 October 2026

- Added root/nested AGENTS.md guidance, with applicant rules copied into each new project. Expanded the flatness checklist and QA log to require job associations, complete text, review of every page, and factual support.
- The six fictional documents have identical normalized text sequences in default and layout extraction. A regression checks this and title/employer/date associations. Rebuilt and visually inspected all six previews; all remain one page without overfull boxes.
- The JSON letter builder was exercised with the actual compiler and both extractors. Contact information, paragraph order, supported demo facts, and literal TeX-sensitive punctuation survive extraction; a literal TeX command remains visible text.
- Added regressions for invalid JSON/fields, preserved existing content, explicit regeneration, missing dependencies before generation, UTF-8 BOM input, protected example projects, and older template migration errors. Direct TeX builds continue using generated content without rereading JSON.
- Editor letter tasks and new local documentation links passed configuration/release checks. Editor GUIs remain untested.
- From the standalone export, ran doctor, the full suite, new-project creation, JSON letter generation and --replace, the default resume build, letter QA, and writing review. Visually reviewed the generated one-page letter and checked all JSON fields/paragraphs against both text extracts. Final packaging uses a fresh allowlisted export, excluding these generated QA workspaces.

## Remaining platform coverage

The supplied GitHub Actions workflow has not been run remotely. It configures Python checks on Windows, macOS, and Linux and actual PDF builds on Ubuntu. macOS/Linux installation instructions and editor tasks received documentation/configuration review; their GUIs and full builds were not exercised locally.

Preview PNGs show the first page; all initial demo PDFs were verified to have exactly one page. Personal resumes can have more pages and need their own review. Technical PASS remains a limited font/text check, not universal ATS certification, accessibility certification, or factual verification.

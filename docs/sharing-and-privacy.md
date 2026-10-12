# Share the machine, keep personal records private

The starter tracks fictional examples and reviewed previews. `personal/`, `build/`, ordinary PDFs, and local environment files are ignored. Your experience inventory, posting, tailored sources, PDFs, and logs belong in the ignored personal/build workspaces.

Gitignore prevents ordinary accidental tracking. It does not remove material already committed, prevent force-add, or change a repository's visibility. Review staged changes before pushing. People who choose to version their own resumes should use a private repository or deliberately sanitized content.

To prepare a clean starter folder and ZIP:

```text
python resume.py export --output build/release/resume-maker --zip
```

The exporter copies only the exact files in release-manifest.json. It excludes personal work, routine build outputs, local agent settings, this project's planning document, and every .git directory. It refuses an existing destination. Inspect the exported file list and examples before sharing; an allowlist cannot detect someone editing an approved demo file to contain personal data.

Create a separate repository from the exported folder with fresh history. For example, in a new PowerShell terminal:

```powershell
Set-Location build/release/resume-maker
git init
git add .
git status --short
git commit -m "Initial Resume Maker starter"
```

Then connect your chosen remote and push. You may mark the new GitHub repository as a template. The local tools never change repository visibility, add a remote, push, or upload data. Do not make a personal source repository public to distribute this starter.

The README uses `YOUR-ACCOUNT` in its clone example until the standalone repository has a real URL. Replace that example when publishing. Users can clone the public starter and keep their populated workspace local or private.

Before sending a personal PDF, check its metadata and visible/extracted content for details you intended to omit. `--anonymous` omits employer names only; it does not anonymize the resume. The CLI uses local tools, but any AI service you choose has its own data handling terms.

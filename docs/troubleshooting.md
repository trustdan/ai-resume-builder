# Common problems

| Symptom | Next step |
| --- | --- |
| `python` missing or opens the Store | Windows: try `py -3`; macOS/Linux: use `python3`. Update editor tasks to the same interpreter. |
| `pdflatex` or PDF tool missing | Run doctor and follow the setup page for your OS. Reopen the terminal after PATH changes. |
| Missing `.sty` or `.tex` file | Install that package through MiKTeX Console or your TeX distribution's package manager. Run doctor again. |
| LaTeX fails after editing text | Check escaped `%`, `&`, `$`, `_`, and `#`; balanced braces; and the error line in build-output.log. |
| Existing destination refused | Pick another new personal project/export path. The tools deliberately do not overwrite directories. |
| Letter generated content already exists | Review/back up manual edits, then run `letter personal/PROJECT --replace` to regenerate from JSON. |
| Letter ignores JSON edits | Run `letter` again with `--replace`; ordinary `build` uses existing TeX without regenerating JSON. |
| Letter JSON rejected | Use the documented fields, double-quoted strings, and one to three paragraph strings; remove trailing commas. See [input rules](cover-letters.md). |
| Letter builder rejects older template | Follow the [migration steps](cover-letters.md) and preserve existing edits; new scaffolds do not update personal projects automatically. |
| `--anonymous` refused | Use it with `--variant employer-light`, without `--all`. |
| Old PDF seems to be showing | Close/reopen the viewer and check the exact build path. Once compilation starts, a failed compile removes that variant's earlier PDF and PASS marker. |
| Build hangs on package installation | Stop it, install the package explicitly, and retry. The CLI times out rather than waiting indefinitely. |
| Glyph or font check fails | Restore shared/preamble.tex and confirm Latin Modern packages are installed; inspect both text extracts. |
| Overfull box warning | Inspect the cited log and PDF; shorten text or adjust that entry. A successful compile can still clip text. |
| Unexpected page count | Review content and breaks. Do not shrink everything until unreadable; follow application length requirements. |
| Terminal works but editor task fails | Open the repository root as the workspace, restart the editor, and compare interpreter/PATH settings. |

Paths are interpreted relative to the folder containing resume.py, even if you run that script from another working directory. Projects belong under personal/ or examples/. Quoted paths with spaces are supported.

Build logs and PDF text contain the applicant's content. Keep personal build directories private. To repair a personal starter after changing shared files, edit its own shared/ copies; template updates do not silently rewrite existing personal projects.

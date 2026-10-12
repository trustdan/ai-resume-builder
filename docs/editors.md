# Use your preferred editor

Open the **starter folder containing resume.py** as the workspace, not only a single TeX file. In any terminal, run doctor, build the demo, then create your personal project. The build requires no editor extension or AI subscription. New to editors or terminals? Start with [getting started](getting-started.md).

| Editor | Baseline workflow | Optional convenience |
| --- | --- | --- |
| VS Code | Open folder; use its integrated terminal | Included .vscode/tasks.json provides doctor, demo builds, and personal build/QA tasks |
| Cursor | Open folder; run the same commands in its terminal | Try the included VS Code tasks through the command palette; terminal commands remain the documented baseline |
| Google Antigravity | Open folder; run the same commands in its terminal | Ask the assistant to read AGENTS.md and use resume.py; no task-file compatibility is assumed |
| Zed | Open folder; run the same commands in its terminal | Included .zed/tasks.json provides doctor and builds through task: spawn |
| Claude Code, Codex CLI, Gemini CLI | Start the agent in a terminal opened at the starter folder (standalone or inside any editor above) | Claude Code loads CLAUDE.md and Codex loads AGENTS.md; ask other agents to read AGENTS.md |

## VS Code tasks

Use **Terminal > Run Task** and choose `Resume: Doctor`, `Resume: Build all demos`, or a personal task. Personal tasks prompt for a project path and format. The default build task builds all demos. The tasks use `python` on Windows and `python3` on macOS/Linux. If you use a specific interpreter, change only the task's command/OS override; no global editor configuration is necessary.

## Zed tasks

Use the command palette's `task: spawn`. The main tasks use `python3`, appropriate for macOS/Linux. Tasks explicitly labeled `(Windows)` use `python`. Personal build/QA tasks target `personal/my-resume` and the default format in project.json; edit the task argument if you chose another project name.

## PDF viewing and AI instructions

Open the generated PDF in your system viewer. An editor's TeX/PDF extension is optional; if using one, keep its compiler on pdfLaTeX. Building through resume.py avoids outputs scattered among source files and runs the extraction checks.

Ask your assistant: `Read AGENTS.md and prompts/interview-me.md, run doctor, then help me create my resume under personal/my-resume. Ask about missing facts before drafting.` Automatic instruction-file loading differs among editors, so explicitly request that read. No API key, plugin, or remote service is needed for local builds.

Ask it to read the personal project's AGENTS.md too. See [instruction scopes](agent-guidance.md). For letters, edit project-local cover-letter.json and run `python resume.py letter personal/my-resume` in the terminal, or use the included letter task. Regeneration uses `--replace` after reviewing any manual generated-content edits. [Letter workflow](cover-letters.md).

Task schemas were checked against [VS Code tasks](https://code.visualstudio.com/docs/debugtest/tasks) and [Zed tasks](https://zed.dev/docs/tasks). See also [Cursor extensions](https://cursor.com/help/customization/extensions) and [Google Antigravity docs](https://antigravity.google/docs/home). Editor GUIs have not been exercised by this project's automated checks; see [validation](validation.md).

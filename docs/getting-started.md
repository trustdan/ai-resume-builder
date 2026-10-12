# Getting started, step by step

This guide assumes you have never used a code editor, a terminal, or an AI coding assistant. If you have, the [README quick start](../README.md#quick-start) is shorter.

## The three pieces

| Piece | What it is | Do you need it? |
| --- | --- | --- |
| **The starter folder** | The files in this repository: templates, the `resume.py` builder, and guides | Yes |
| **A terminal** | A window where you type commands such as `python resume.py doctor`. Most editors have one built in | Yes, for building PDFs |
| **An AI assistant** | A helper that can interview you, edit the files, and run the commands for you | No, it's optional |

The builder runs on your computer. It doesn't need an account, an API key, or an internet connection after setup.

## Step 1: Pick how you want to work

Choose the row that sounds most like you. You can switch later because every option works on the same files.

| If you... | Use | Examples |
| --- | --- | --- |
| Want an AI to do most of the typing and prefer clicking to commands | **An AI code editor**: a normal editor with an AI chat panel that can read files and run commands | [Cursor](https://cursor.com), [VS Code](https://code.visualstudio.com) with [GitHub Copilot](https://code.visualstudio.com/docs/copilot/overview), [Google Antigravity](https://antigravity.google), [Windsurf](https://windsurf.com) |
| Are comfortable typing a few commands | **A terminal AI agent**: an assistant you start inside the starter folder's terminal | [Claude Code](https://claude.com/product/claude-code), [OpenAI Codex CLI](https://github.com/openai/codex), [Gemini CLI](https://github.com/google-gemini/gemini-cli) |
| Don't want AI involved | **Any editor with a terminal** | [VS Code](https://code.visualstudio.com), [Zed](https://zed.dev), or a plain text editor plus your system terminal |
| Only use ChatGPT, Claude, or Gemini in a web browser | **Browser chat plus an editor.** The chat can interview you and draft wording, but it can't see your files or build the PDF. You copy text into the files and run the commands yourself | Any of the above editors, plus your chat site |

**If you can't decide**, use an AI code editor (Cursor or VS Code) or Claude Code/Codex inside VS Code's terminal. Either option can read the project's rules and run the checks for you.

> [!IMPORTANT]
> Cloud AI tools send what you type, and the files they read, to their provider. Read the tool's privacy settings before sharing your work history. The no-AI path keeps everything on your computer.

## Step 2: Install the prerequisites

Every option needs **Git**, **Python 3.10 or newer**, **pdfLaTeX** (from MiKTeX or TeX Live), and **PDF tools** (`pdftotext`, `pdffonts`, `pdfinfo`). Follow the guide for your system:

- [Windows setup](setup-windows.md)
- [macOS setup](setup-macos.md)
- [Linux setup](setup-linux.md)

You install these yourself; the starter never runs installers. An AI assistant can read the output of `doctor` (Step 5) and explain what's missing.

## Step 3: Get the starter folder

Choose one of these:

- **Download ZIP (simplest).** On the GitHub page, click the green **Code** button, then **Download ZIP**. Unzip it somewhere easy to find, such as `Documents`.
- **Clone with Git.** In a terminal:

  ```text
  git clone https://github.com/trustdan/ai-resume-builder.git
  ```

## Step 4: Open the folder and a terminal

1. Open your editor and choose **File > Open Folder**. Select the folder that **contains `resume.py`**, not a single file inside it.
2. Open the built-in terminal. In VS Code, Cursor, Windsurf, and Antigravity, use **View > Terminal**. In most editors, including Zed, <kbd>Ctrl</kbd>+<kbd>`</kbd> also opens it.
3. Type `ls` and press Enter. If `resume.py` appears in the list, you're in the right place.

If you use a terminal agent such as Claude Code, Codex, or Gemini CLI, start it from this terminal so it works inside the starter folder.

> [!NOTE]
> On macOS and Linux, type `python3` wherever this guide says `python`. On Windows, `py -3` also works if `python` isn't found.

## Step 5: Check your setup and build the demo

```text
python resume.py doctor
python resume.py build examples/demo-person --all
```

`doctor` lists anything missing. When the demo build finishes, open `build/examples/demo-person/hybrid/resume.pdf`. You've built a resume for a fictional person, so your setup works.

## Step 6: Create your own project

```text
python resume.py new personal/my-resume --variant hybrid
```

This copies a complete, editable project to `personal/my-resume/`. Git ignores the `personal/` folder, so your records stay out of commits and exports. Hybrid is a good default; see [choose a format](choose-a-format.md) to compare it with the other formats.

## Step 7a: Fill it in with an AI assistant

Open your assistant (the chat panel in an AI editor, or the agent you started in the terminal) and paste:

> Read AGENTS.md and prompts/interview-me.md, run doctor, then help me create my resume under personal/my-resume. Ask about missing facts before drafting. Never invent metrics, qualifications, titles, or dates.

The assistant should interview you in small batches, record your answers in `experience-inventory.md`, and then draft. Keep these points in mind:

- **Answer with facts only.** If you don't know a number, say so. It belongs in the questions list, not on your resume.
- **Approve commands and file edits.** Most tools ask before running commands or changing files. Read what they plan to do.
- **Check every claim it writes.** Reject inflated titles, invented metrics, or skills you don't have.

When you're ready to aim the resume at a specific job, use [prompts/tailor-to-job.md](../prompts/tailor-to-job.md). Use [prompts/build-cover-letter.md](../prompts/build-cover-letter.md) for a cover letter and [prompts/review-resume.md](../prompts/review-resume.md) for a final check.

### Notes for specific tools

Tools change quickly, so the prompt above always asks the assistant to read the rules explicitly. That way it works even if your tool doesn't load them automatically.

| Tool | How to start | Project rules |
| --- | --- | --- |
| Claude Code | Run `claude` in the starter folder's terminal, or use its VS Code extension | Reads `CLAUDE.md`, which imports `AGENTS.md` |
| OpenAI Codex | Run `codex` in the starter folder's terminal, or use its editor extension | Reads `AGENTS.md` |
| Cursor | Open the AI chat/agent panel and paste the prompt | Ask it to read `AGENTS.md` |
| VS Code + GitHub Copilot | Open the Chat view, choose agent mode, and paste the prompt | Ask it to read `AGENTS.md` |
| Google Antigravity | Open the folder as a workspace and give the prompt to the agent | Ask it to read `AGENTS.md` |
| Gemini CLI | Run `gemini` in the starter folder's terminal | Ask it to read `AGENTS.md` |
| Browser chat | Paste the contents of `AGENTS.md` and `prompts/interview-me.md`, then the prompt | Copy its drafts into the files yourself, then follow Step 8 |

Each personal project also gets its own `AGENTS.md`. Ask your assistant to read `personal/my-resume/AGENTS.md` too. [More on instruction files](agent-guidance.md) · [Editor tasks and shortcuts](editors.md).

## Step 7b: Fill it in without AI

Open these files in `personal/my-resume/` in this order:

1. **`experience-inventory.md`**: write down your real jobs, titles, dates, responsibilities, and results, with notes on how you know each one. Put anything uncertain in the questions list.
2. **`job-description.md`**: paste the posting you're targeting.
3. **`tailoring-brief.md`**: match each requirement to your evidence and label it Strong, Partial, or Gap.
4. **`candidate.tex`**: replace every `REPLACE ME` with your content. This file holds your text. `hybrid/resume.tex` controls the section order.

`candidate.tex` uses LaTeX, but you only need a few rules: write `\%`, `\$`, `\&`, `\#`, and `\_` for those symbols, and start each bullet with `\item`. [LaTeX basics in the workflow guide](workflow.md).

## Step 8: Build, check, repeat

```text
python resume.py build personal/my-resume
python resume.py review build/personal/my-resume/hybrid/resume.pdf
```

Your files are in `build/personal/my-resume/hybrid/`:

| File | What to do with it |
| --- | --- |
| `resume.pdf` | Your resume. Open it and look at every page |
| `resume.default.txt` and `resume.layout.txt` | Roughly the text an applicant tracking system (ATS) extracts. Read both in order and check that nothing is missing, garbled, or out of place |

Fix any problems in `candidate.tex` and build again. When you're finished, set `DocumentNotice` to `{}` in `candidate.tex`, confirm that no `REPLACE ME` text remains, and note what you checked in `qa-log.md`. The [ATS and flatness checklist](ats-and-flatness.md) has the full review.

A **PASS** means the PDF's text and fonts passed the automated checks. It doesn't guarantee that any particular ATS will accept the file, and it doesn't verify your claims.

## When something goes wrong

| Symptom | Try |
| --- | --- |
| `python` isn't found or opens the Microsoft Store | Use `py -3` (Windows) or `python3` (macOS/Linux) |
| `doctor` reports a missing program | Install it with your setup guide, then open a **new** terminal |
| MiKTeX reports a missing `.sty` package | Install it in MiKTeX Console, then rebuild |
| `can't open file 'resume.py'` | Your terminal is in the wrong folder. Open the folder that contains `resume.py` |
| The AI added numbers or titles you didn't give it | Tell it to remove them and keep unknowns in the questions list. The project rules forbid invented facts |

More fixes are in [troubleshooting](troubleshooting.md).

"""Advisory style review. These heuristics cannot determine authorship."""
import re

from scripts.common import ResumeError, run

RULES = (
    (r"\b(results.driven|proven track record|detail.oriented)\b", "Replace self-assessment with evidence."),
    (r"\b(spearheaded|leveraged|utilized|synergy|world.class|cutting.edge)\b", "Would a simpler, more specific phrase help?"),
    (r"\b(responsible for|duties included)\b", "Explain the action and outcome where evidence exists."),
)


def review(path):
    if not path.is_file():
        raise ResumeError(f"File not found: {path}")
    if path.suffix.lower() == ".pdf":
        result = run(["pdftotext", "-layout", path, "-"])
        if result.returncode:
            raise ResumeError(f"Cannot extract PDF: {result.stderr.strip()}")
        text = result.stdout
    else:
        text = path.read_text(encoding="utf-8")
        if path.suffix.lower() == ".tex":
            text = re.sub(r"(?<!\\)%[^\n]*", "", text)
    count = 0
    for number, line in enumerate(text.splitlines(), 1):
        for pattern, advice in RULES:
            if re.search(pattern, line, re.IGNORECASE):
                print(f"REVIEW L{number}: {advice}\n  {line.strip()}")
                count += 1
    print(f"{count} advisory findings. Read in context; never invent facts to satisfy a style rule.")

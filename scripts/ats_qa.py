"""Inspect PDF text and fonts. A PASS is a limited technical check, not an ATS score."""
from pathlib import Path
import re
import unicodedata

from scripts.common import ResumeError, require_tools, run

CANARIES = (r"\bOcer\b", r"\bworkow\b", r"\bcertied\b", r"\bdicult\b", r"\beective\b")


def font_problems(table):
    problems = []
    rows = [line for line in table.splitlines()[2:] if line.strip()]
    if not rows:
        return ["PDF contains no detectable text fonts"]
    for row in rows:
        # The last two columns are object number/generation, NOT the Unicode flag.
        flags = re.search(r"\s+(yes|no)\s+(yes|no)\s+(yes|no)\s+\d+\s+\d+\s*$", row)
        if not flags:
            problems.append(f"Cannot interpret font-table row: {row.strip()}")
            continue
        embedded, _subset, unicode_map = flags.groups()
        if "Type 3" in row:
            problems.append(f"Type 3 bitmap font: {row.strip()}")
        if embedded == "no":
            problems.append(f"Font is not embedded: {row.strip()}")
        if unicode_map == "no":
            problems.append(f"Font lacks a Unicode map: {row.strip()}")
    return problems


def text_problems(text):
    problems = []
    if not text.strip():
        problems.append("PDF has no extractable text")
    bad = sorted({ord(c) for c in text if (unicodedata.category(c) == "Cc" and c not in "\t\n\r\f") or c == "\ufffd"})
    if bad:
        problems.append("Control/replacement characters: " + ", ".join(f"U+{c:04X}" for c in bad))
    for pattern in CANARIES:
        if re.search(pattern, text):
            problems.append(f"Possible dropped ligature ({pattern}); review context")
    return problems


def check_pdf(pdf, *, anonymous=False):
    pdf = Path(pdf)
    if not pdf.is_file():
        raise ResumeError(f"PDF not found: {pdf}. Build this variant first.")
    require_tools(("pdffonts", "pdftotext", "pdfinfo"))
    fonts = run(["pdffonts", pdf])
    if fonts.returncode:
        raise ResumeError(f"pdffonts failed: {fonts.stderr.strip()}")
    problems = font_problems(fonts.stdout)
    texts = {}
    for mode, flags in (("default", []), ("layout", ["-layout"])):
        result = run(["pdftotext", *flags, pdf, "-"])
        if result.returncode:
            raise ResumeError(f"pdftotext {mode} failed: {result.stderr.strip()}")
        texts[mode] = result.stdout
        pdf.with_suffix(f".{mode}.txt").write_text(result.stdout, encoding="utf-8")
        problems.extend(f"{mode}: {p}" for p in text_problems(result.stdout))
    info = run(["pdfinfo", pdf])
    if info.returncode:
        raise ResumeError(f"pdfinfo failed: {info.stderr.strip()}")
    match = re.search(r"^Pages:\s+(\d+)", info.stdout, re.MULTILINE)
    if not match:
        raise ResumeError("pdfinfo did not report a page count")
    pages = int(match.group(1))
    if pages > 2:
        print(f"WARN {pages} pages; review the target application's length requirements.")
    if "REPLACE ME" in texts["default"]:
        print("WARN unfinished starter placeholders: replace them before applying.")
    if problems:
        for problem in problems:
            print(f"FAIL {problem}")
        raise ResumeError(f"PDF quality checks failed: {pdf}")
    label = "anonymous employer-light" if anonymous else "PDF"
    print(f"PASS {label}: {pdf} ({pages} page{'s' if pages != 1 else ''})")
    print("     Read .default.txt and .layout.txt; inspect the PDF visually and verify every claim.")
    return texts

"""Render user-written, plain-text letter content; never invent applicant claims."""
import json
import unicodedata

from scripts.build import process
from scripts.common import ROOT, ResumeError, inside_root, project_path, require_tools

REQUIRED = ("date", "company", "role", "opening", "paragraphs", "closing")
OPTIONAL = {"salutation": "Dear Hiring Team,", "signoff": "Sincerely,"}
TEX_ESCAPES = {
    "\\": r"\textbackslash{}", "{": r"\{", "}": r"\}",
    "&": r"\&", "%": r"\%", "$": r"\$", "#": r"\#", "_": r"\_",
    "~": r"\textasciitilde{}", "^": r"\textasciicircum{}",
}


def plain_text(value, field):
    if not isinstance(value, str) or not value.strip():
        raise ResumeError(f"Cover letter field '{field}' must be a nonempty string.")
    if any(unicodedata.category(c).startswith("C") and c not in "\n\r\t" for c in value):
        raise ResumeError(f"Cover letter field '{field}' contains unsupported control characters.")
    # A field is one paragraph. Explicit paragraph boundaries come from the list.
    return " ".join(value.split())


def escape_tex(text):
    return "".join(TEX_ESCAPES.get(c, c) for c in text)


def render(data):
    if not isinstance(data, dict):
        raise ResumeError("cover-letter.json must contain a JSON object.")
    missing = set(REQUIRED) - data.keys()
    unknown = data.keys() - set(REQUIRED) - OPTIONAL.keys()
    if missing or unknown:
        raise ResumeError(f"Cover letter fields: missing {sorted(missing)}; unknown {sorted(unknown)}.")
    paragraphs = data["paragraphs"]
    if not isinstance(paragraphs, list) or not 1 <= len(paragraphs) <= 3:
        raise ResumeError("Cover letter 'paragraphs' must be a list of one to three plain-text paragraphs.")
    values = {key: escape_tex(plain_text(data[key], key)) for key in REQUIRED if key != "paragraphs"}
    values.update({key: escape_tex(plain_text(data.get(key, default), key)) for key, default in OPTIONAL.items()})
    values["body"] = "\\par\\vspace{6pt}\n".join(
        escape_tex(plain_text(text, f"paragraphs[{index}]")) for index, text in enumerate(paragraphs)
    )
    macros = {
        "date": "LetterDate", "company": "TargetCompany", "role": "TargetRole",
        "salutation": "LetterSalutation", "opening": "LetterOpening", "body": "LetterBody",
        "closing": "LetterClosing", "signoff": "LetterSignoff",
    }
    return "% Generated from cover-letter.json. Back up manual edits before using --replace.\n" + "".join(
        f"\\renewcommand{{\\{macro}}}{{{values[key]}}}\n" for key, macro in macros.items()
    )


def generate(value, *, replace=False):
    project = project_path(value)
    # Public examples must remain fixed, fictional fixtures.
    if project.relative_to(ROOT).parts[0] != "personal":
        raise ResumeError("Choose a project below personal/.")
    source = inside_root(project / "cover-letter.json")
    destination = inside_root(project / "cover-letter-content.tex")
    template = inside_root(project / "cover-letter.tex")
    if not template.is_file() or "cover-letter-content.tex" not in template.read_text(encoding="utf-8"):
        raise ResumeError("This project needs the current templates/cover-letter.tex; see docs/cover-letters.md migration steps.")
    if destination.exists() and not replace:
        raise ResumeError("cover-letter-content.tex already exists; review/back it up, then use --replace to regenerate.")
    try:
        data = json.loads(source.read_text(encoding="utf-8-sig"))
    except json.JSONDecodeError as exc:
        raise ResumeError(f"Invalid cover-letter.json at line {exc.lineno}, column {exc.colno}: {exc.msg}") from exc
    content = render(data)
    # Validate everything before touching prior generated content. Exclusive creation
    # protects a newly created destination when --replace was not requested.
    with destination.open("w" if replace else "x", encoding="utf-8", newline="\n") as handle:
        handle.write(content)
    print(f"Generated {destination}. Claims still need evidence and human review.")
    return project


def build_letter(value, *, replace=False):
    require_tools(("pdflatex", "pdffonts", "pdftotext", "pdfinfo"))
    generate(value, replace=replace)
    return process(value, variant="cover-letter")

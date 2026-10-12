"""Create a complete project without overwriting existing work."""
import json
import shutil

from scripts.common import ROOT, ResumeError, has_link, inside_root


def create(value, variant):
    destination = inside_root(value)
    relative = destination.relative_to(ROOT)
    if len(relative.parts) < 2 or relative.parts[0] != "personal":
        raise ResumeError("Create your project under personal/, for example personal/my-resume.")
    if destination.exists():
        raise ResumeError(f"Destination already exists; nothing overwritten: {destination}")
    source = ROOT / "templates"
    paths = list(source.rglob("*"))
    if any(has_link(p) for p in paths):
        raise ResumeError("Templates contain a linked path; refusing to copy.")
    shutil.copytree(source, destination)
    (destination / "project.json").write_text(json.dumps({"variant": variant}, indent=2) + "\n", encoding="utf-8")
    print(f"Created {relative.as_posix()} (default: {variant}).")
    print("Edit candidate.tex and experience-inventory.md; sample placeholders are not application-ready.")
    print(f'Build: python resume.py build "{relative.as_posix()}"')
    print(f'Cover letter: edit cover-letter-brief.md and cover-letter.json, then python resume.py letter "{relative.as_posix()}"')

"""Paths and subprocess handling shared by the command-line tools."""
from pathlib import Path
from contextlib import contextmanager
import shutil
import subprocess
from uuid import uuid4

ROOT = Path(__file__).resolve().parents[1]
VARIANTS = ("chronological", "hybrid", "functional", "employer-light")
TOOLS = ("pdflatex", "kpsewhich", "pdftotext", "pdffonts", "pdfinfo")
PACKAGES = (
    "article.cls", "geometry.sty", "inputenc.sty", "fontenc.sty", "lmodern.sty",
    "hyperref.sty", "enumitem.sty", "needspace.sty", "hyphenat.sty",
    "microtype.sty", "glyphtounicode.tex",
)


class ResumeError(Exception):
    """A user-facing build or validation failure."""


def run(command, *, cwd=None, timeout=120):
    try:
        return subprocess.run(
            [str(arg) for arg in command], cwd=cwd, capture_output=True,
            text=True, encoding="utf-8", errors="replace", timeout=timeout,
        )
    except FileNotFoundError as exc:
        raise ResumeError(f"Missing executable: {command[0]}. Run doctor; see docs/setup-*.md.") from exc
    except subprocess.TimeoutExpired as exc:
        raise ResumeError(f"{command[0]} timed out after {timeout}s. Check TeX packages and build logs.") from exc


def require_tools(names):
    missing = [name for name in names if not shutil.which(name)]
    if missing:
        raise ResumeError("Missing tools: " + ", ".join(missing) + ". Run doctor; see docs/setup-*.md.")


def has_link(path):
    return path.is_symlink() or (hasattr(path, "is_junction") and path.is_junction())


def inside_root(value):
    unresolved = ROOT / value
    resolved = unresolved.resolve()
    if not resolved.is_relative_to(ROOT) or resolved == ROOT:
        raise ResumeError("Choose a path inside this starter repository, below its root.")
    for parent in (unresolved, *unresolved.parents):
        if has_link(parent):
            raise ResumeError(f"Linked paths are not supported: {parent}")
        if parent == ROOT:
            break
    return resolved


def project_path(value):
    project = inside_root(value)
    relative = project.relative_to(ROOT)
    if relative.parts[0] not in ("personal", "examples") or not (project / "candidate.tex").is_file():
        raise ResumeError("Project must be under personal/ or examples/ and contain candidate.tex.")
    return project


def output_path(project, variant, anonymous=False):
    name = variant + ("-anonymous" if anonymous else "")
    return inside_root(Path("build") / project.relative_to(ROOT) / name)


@contextmanager
def source_snapshot(output):
    # Inherit the output directory's permissions. Python 3.13 TemporaryDirectory
    # applies a private Windows ACL that can exclude a restricted editor process.
    snapshot = output / ("source-" + uuid4().hex)
    snapshot.mkdir()
    try:
        yield snapshot
    finally:
        resolved = snapshot.resolve()
        if resolved.parent != output.resolve() or not resolved.is_relative_to(ROOT) or has_link(snapshot):
            raise ResumeError("Refusing cleanup outside the generated source snapshot.")
        shutil.rmtree(snapshot)

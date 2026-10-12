"""Export an exact file allowlist, excluding personal work and repository history."""
import json
from pathlib import Path
import shutil

from scripts.common import ROOT, ResumeError, has_link, inside_root


def release_files():
    manifest = json.loads((ROOT / "release-manifest.json").read_text(encoding="utf-8"))
    files = manifest["files"]
    if len(files) != len(set(files)):
        raise ResumeError("Duplicate manifest entries")
    for name in files:
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts or relative.parts[0] in ("personal", "build", ".git"):
            raise ResumeError(f"Unsafe release entry: {name}")
        path = inside_root(relative)
        if not path.is_file() or has_link(path):
            raise ResumeError(f"Missing or linked release file: {name}")
    return files


def export(value, zip_output=False):
    # Allow external destinations only through an explicit absolute path.
    raw = Path(value)
    destination = raw if raw.is_absolute() else ROOT / raw
    if any(has_link(p) for p in (destination, *destination.parents)):
        raise ResumeError("Export destination cannot use linked paths.")
    destination = destination.resolve()
    if destination == ROOT or ROOT.is_relative_to(destination):
        raise ResumeError("Export destination cannot be the source or its parent.")
    if destination.exists():
        raise ResumeError(f"Export destination already exists; nothing overwritten: {destination}")
    files = release_files()
    if any((ROOT / f).is_relative_to(destination) for f in files):
        raise ResumeError("Export destination overlaps release source files.")
    archive = destination.with_name(destination.name + ".zip")
    if zip_output and archive.exists():
        raise ResumeError(f"ZIP already exists; nothing overwritten: {archive}")
    for name in files:
        target = destination / name
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / name, target)
    print(f"Exported {len(files)} allowlisted files: {destination}")
    if zip_output:
        shutil.make_archive(str(archive.with_suffix("")), "zip", root_dir=destination.parent, base_dir=destination.name)
        print(f"ZIP: {archive}")

"""Build the fixed fictional demo and promote reviewed-preview candidates."""
import shutil

from scripts.build import process
from scripts.common import ROOT, VARIANTS, ResumeError, output_path, require_tools, run


def refresh():
    require_tools(("pdftoppm",))
    project = ROOT / "examples/demo-person"
    jobs = [(v, False) for v in VARIANTS] + [("employer-light", True), ("cover-letter", False)]
    destination = ROOT / "examples/previews"
    destination.mkdir(parents=True, exist_ok=True)
    for variant, anonymous in jobs:
        if process("examples/demo-person", variant=variant, anonymous=anonymous):
            raise ResumeError("Demo build failed; previews were not fully refreshed.")
        stem = "cover-letter" if variant == "cover-letter" else "resume"
        name = variant + ("-anonymous" if anonymous else "")
        pdf = output_path(project, variant, anonymous) / f"{stem}.pdf"
        image_prefix = destination / name
        result = run(["pdftoppm", "-f", "1", "-singlefile", "-scale-to", "1100", "-png", pdf, image_prefix])
        if result.returncode:
            raise ResumeError(f"Preview rendering failed: {result.stderr.strip()}")
        shutil.copyfile(pdf, destination / f"{name}.pdf")
    print("Refreshed fictional PDFs and first-page PNGs. Visually inspect all previews before release.")

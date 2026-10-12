"""Compile from an isolated source snapshot, then validate the output."""
import json
import shutil

from scripts.ats_qa import check_pdf
from scripts.common import VARIANTS, ResumeError, has_link, output_path, project_path, require_tools, run, source_snapshot


def selected_variants(project, variant, all_variants):
    if all_variants:
        return VARIANTS
    if variant:
        return (variant,)
    config = project / "project.json"
    default = json.loads(config.read_text(encoding="utf-8")).get("variant", "chronological") if config.exists() else "chronological"
    if default not in VARIANTS:
        raise ResumeError(f"Invalid default variant in {config}")
    return (default,)


def compiler_flags():
    version = run(["pdflatex", "--version"], timeout=20)
    if version.returncode:
        raise ResumeError(f"Cannot start pdflatex: {version.stderr.strip()}")
    # MiKTeX can otherwise invoke its package installer during compilation.
    # TeX Live does not accept this MiKTeX-specific option.
    return ["-disable-installer"] if "miktex" in (version.stdout + version.stderr).lower() else []


def compile_one(project, variant, anonymous):
    output = output_path(project, variant, anonymous)
    source_file = project / ("cover-letter.tex" if variant == "cover-letter" else f"{variant}/resume.tex")
    if not source_file.is_file():
        raise ResumeError(f"Source not found: {source_file}")
    sources = sorted(project.rglob("*.tex"))
    for path in sources:
        if has_link(path) or any(has_link(p) for p in path.parents if p != project.parent):
            raise ResumeError(f"Linked TeX source is not supported: {path}")
    output.mkdir(parents=True, exist_ok=True)
    stem = "cover-letter" if variant == "cover-letter" else "resume"
    engine_flags = compiler_flags()
    # Remove prior deliverables first so a failed rebuild cannot look successful.
    for extension in (".pdf", ".default.txt", ".layout.txt", ".qa.json"):
        (output / f"{stem}{extension}").unlink(missing_ok=True)
    with source_snapshot(output) as snapshot:
        for path in sources:
            target = snapshot / path.relative_to(project)
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(path, target)
        workdir = snapshot if variant == "cover-letter" else snapshot / variant
        # This entry file supports relative inputs without shell interpolation.
        entry = workdir / "build-entry.tex"
        entry.write_text(
            ("\\def\\AnonymousEmployers{1}\n" if anonymous else "")
            + f"\\input{{{source_file.name}}}\n", encoding="utf-8",
        )
        transcript = output / "build-output.log"
        with transcript.open("w", encoding="utf-8") as log:
            for attempt in (1, 2):
                log.write(f"Pass {attempt}\n")
                log.flush()
                try:
                    result = run([
                        "pdflatex", *engine_flags, "-interaction=nonstopmode", "-halt-on-error", "-file-line-error",
                        "-no-shell-escape", f"-jobname={stem}", f"-output-directory={output}", entry.name,
                    ], cwd=workdir)
                except ResumeError:
                    (output / f"{stem}.pdf").unlink(missing_ok=True)
                    raise
                log.write(result.stdout + "\n" + result.stderr)
                log.flush()
                if result.returncode:
                    (output / f"{stem}.pdf").unlink(missing_ok=True)
                    tail = "\n".join(result.stdout.splitlines()[-12:])
                    raise ResumeError(f"LaTeX failed. Log: {transcript}\n{tail}")
        log_text = (output / f"{stem}.log").read_text(encoding="utf-8", errors="replace")
        if "Overfull \\hbox" in log_text or "Overfull \\vbox" in log_text:
            print(f"WARN overfull boxes in {output / (stem + '.log')}; check for clipped text.")
    return output / f"{stem}.pdf"


def process(value, variant=None, all_variants=False, anonymous=False, build=True):
    project = project_path(value)
    variants = selected_variants(project, variant, all_variants)
    if anonymous and variants != ("employer-light",):
        raise ResumeError("--anonymous requires --variant employer-light (without --all).")
    require_tools(("pdflatex", "pdffonts", "pdftotext", "pdfinfo") if build else ("pdffonts", "pdftotext", "pdfinfo"))
    failed = False
    for selected in variants:
        output = output_path(project, selected, anonymous)
        stem = "cover-letter" if selected == "cover-letter" else "resume"
        try:
            pdf = compile_one(project, selected, anonymous) if build else output / f"{stem}.pdf"
            check_pdf(pdf, anonymous=anonymous)
            (output / f"{stem}.qa.json").write_text(json.dumps({"status": "PASS", "variant": selected, "anonymous": anonymous}) + "\n", encoding="utf-8")
        except (ResumeError, OSError) as exc:
            print(f"FAIL {selected}: {exc}")
            (output / f"{stem}.qa.json").unlink(missing_ok=True)
            failed = True
    return 1 if failed else 0

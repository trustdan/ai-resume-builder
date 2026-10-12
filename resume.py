#!/usr/bin/env python3
"""Editor-neutral resume tools. Run from any directory; paths are repo-relative."""
import argparse
import sys

from scripts.common import ROOT, VARIANTS, ResumeError


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("doctor", help="check Python, TeX packages, and PDF tools")
    commands.add_parser("previews", help="rebuild and refresh only the fictional demo previews")
    new = commands.add_parser("new", help="create an editable personal project")
    new.add_argument("project", help="new directory under personal/")
    new.add_argument("--variant", choices=VARIANTS, default="chronological")
    letter = commands.add_parser("letter", help="build a cover letter from project-local plain-text JSON")
    letter.add_argument("project", help="personal project containing cover-letter.json")
    letter.add_argument("--replace", action="store_true", help="replace previously generated cover-letter-content.tex")
    for name in ("build", "qa"):
        sub = commands.add_parser(name, help=f"{name} a project or fictional demo")
        sub.add_argument("project", help="path relative to this repository")
        choice = sub.add_mutually_exclusive_group()
        choice.add_argument("--variant", choices=(*VARIANTS, "cover-letter"))
        choice.add_argument("--all", action="store_true", help="all four resume formats")
        sub.add_argument("--anonymous", action="store_true", help="employer-light only: omit employer names")
    review = commands.add_parser("review", help="advisory writing review of a text, TeX, or PDF file")
    review.add_argument("file")
    export = commands.add_parser("export", help="copy only allowlisted starter files; optional ZIP")
    export.add_argument("--output", default="build/release/resume-maker")
    export.add_argument("--zip", action="store_true", help="also create a ZIP alongside the folder")
    args = parser.parse_args(argv)
    try:
        if args.command == "doctor":
            from scripts.doctor import doctor
            return doctor()
        if args.command == "new":
            from scripts.new_resume import create
            create(args.project, args.variant)
        elif args.command == "letter":
            from scripts.cover_letter import build_letter
            return build_letter(args.project, replace=args.replace)
        elif args.command == "previews":
            from scripts.refresh_previews import refresh
            refresh()
        elif args.command in ("build", "qa"):
            from scripts.build import process
            return process(args.project, args.variant, args.all, args.anonymous, args.command == "build")
        elif args.command == "review":
            from scripts.writing_review import review
            review(ROOT / args.file)
        elif args.command == "export":
            from scripts.export_starter import export
            export(args.output, args.zip)
    except (ResumeError, OSError, ValueError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("Interrupted. Check build logs before using an earlier PDF.", file=sys.stderr)
        return 130
    return 0


if __name__ == "__main__":
    if sys.version_info < (3, 10):
        sys.exit("Python 3.10 or newer is required.")
    sys.exit(main())

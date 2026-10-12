"""Check dependencies without installing or changing system software."""
import platform
import shutil
import sys

from scripts.common import PACKAGES, ROOT, TOOLS, ResumeError, run


def doctor():
    print(f"Python {platform.python_version()} | {platform.system()} | {ROOT}")
    failures = []
    if sys.version_info < (3, 10):
        failures.append("Python 3.10 or newer is required")
    for name in TOOLS:
        location = shutil.which(name)
        if not location:
            failures.append(f"Missing executable: {name}")
            continue
        flag = "--version" if name in ("pdflatex", "kpsewhich") else "-v"
        try:
            result = run([location, flag], timeout=20)
            if result.returncode:
                failures.append(f"{name} failed to start: {(result.stderr or result.stdout).strip()[:300]}")
            else:
                lines = (result.stdout + "\n" + result.stderr).splitlines()
                version = next((s for s in lines if "version" in s.lower() or "pdfTeX" in s), name)
                print(f"OK {name}: {version.strip()}")
        except ResumeError as exc:
            failures.append(str(exc))
    if shutil.which("kpsewhich"):
        for package in PACKAGES:
            try:
                result = run(["kpsewhich", package], timeout=20)
                if result.returncode or not result.stdout.strip():
                    failures.append(f"Missing TeX file: {package}")
                else:
                    print(f"OK TeX: {package}")
            except ResumeError as exc:
                failures.append(str(exc))
    if failures:
        for failure in failures:
            print(f"FAIL {failure}")
        print("Next: docs/setup-windows.md, docs/setup-macos.md, or docs/setup-linux.md; then reopen your terminal.")
        return 1
    print("PASS dependencies. Next: python resume.py build examples/demo-person --all")
    return 0

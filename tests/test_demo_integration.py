"""Real compiler/extractor regressions. Skipped if external tools are absent."""
from contextlib import redirect_stdout
import io
import re
import shutil
import unittest
from uuid import uuid4

from scripts.ats_qa import check_pdf
from scripts.build import compile_one, process
from scripts.common import ROOT, VARIANTS, ResumeError, output_path, run
from scripts.new_resume import create

AVAILABLE = all(shutil.which(n) for n in ("pdflatex", "pdffonts", "pdftotext", "pdfinfo"))


@unittest.skipUnless(AVAILABLE, "Install TeX and PDF tools to exercise real builds")
class DemoIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with redirect_stdout(io.StringIO()):
            statuses = [
                process("examples/demo-person", all_variants=True),
                process("examples/demo-person", variant="employer-light", anonymous=True),
                process("examples/demo-person", variant="cover-letter"),
            ]
        if any(statuses):
            raise AssertionError("Demo build failed; run resume.py build examples/demo-person --all for diagnostics")

    def text(self, variant, mode, anonymous=False):
        return (output_path(ROOT / "examples/demo-person", variant, anonymous) / f"resume.{mode}.txt").read_text(encoding="utf-8")

    def test_all_formats_preserve_facts_in_both_extraction_modes(self):
        for variant in VARIANTS:
            for mode in ("default", "layout"):
                with self.subTest(variant=variant, mode=mode):
                    text = " ".join(self.text(variant, mode).split())
                    for fact in ("Riley Morgan", "Example Harbor Services", "Example Cedar Support", "Project Coordinator", "Operations Associate", "03/2022 to 08/2025", "06/2019 to 02/2022", "18%", "1,200", "office workflow", "Certified Service Coordinator", "Café Community"):
                        self.assertIn(fact, text)
                    self.assertNotIn("250,000", text)
                    self.assertNotIn("REPLACE ME", text)
                    self.assertLess(text.index("Riley Morgan"), text.index("Project Coordinator"))
                    self.assertLess(text.index("Project Coordinator"), text.index("Operations Associate"))
                    self.assertLess(text.index("Operations Associate"), text.index("Education and certification"))

    def test_all_six_demo_documents_fit_one_page(self):
        jobs = [(v, False) for v in VARIANTS] + [("employer-light", True), ("cover-letter", False)]
        for variant, anonymous in jobs:
            stem = "cover-letter" if variant == "cover-letter" else "resume"
            folder = output_path(ROOT / "examples/demo-person", variant, anonymous)
            info = run(["pdfinfo", folder / f"{stem}.pdf"])
            self.assertRegex(info.stdout, r"(?m)^Pages:\s+1\s*$")
            log = (folder / f"{stem}.log").read_text(encoding="utf-8", errors="replace")
            self.assertNotIn("Overfull \\hbox", log)
            self.assertNotIn("Overfull \\vbox", log)

    def test_flat_text_sequence_and_job_associations(self):
        jobs = [(v, False) for v in VARIANTS] + [("employer-light", True), ("cover-letter", False)]
        for variant, anonymous in jobs:
            stem = "cover-letter" if variant == "cover-letter" else "resume"
            folder = output_path(ROOT / "examples/demo-person", variant, anonymous)
            texts = [" ".join((folder / f"{stem}.{mode}.txt").read_text(encoding="utf-8").split()) for mode in ("default", "layout")]
            self.assertEqual(texts[0], texts[1], (variant, anonymous))
            for text in texts:
                for contact in ("Riley Morgan", "608-555-0142", "riley.morgan@example.com", "example.com/riley-morgan"):
                    self.assertIn(contact, text)
                if variant != "cover-letter":
                    for title, dates, employer, descriptor in (
                        ("Project Coordinator", "03/2022 to 08/2025", "Example Harbor Services", "regional logistics provider"),
                        ("Operations Associate", "06/2019 to 02/2022", "Example Cedar Support", "customer support organization"),
                    ):
                        association = f"{title} | {dates}"
                        if variant == "employer-light":
                            association += f" Organization: {descriptor} (name omitted)" if anonymous else f" Employer: {employer}"
                        else:
                            association = f"{employer} {association}"
                        self.assertIn(association, text, (variant, anonymous))

    def test_anonymous_removes_only_employer_names_and_keeps_history(self):
        for mode in ("default", "layout"):
            text = " ".join(self.text("employer-light", mode, True).split())
            for employer in ("Example Harbor Services", "Example Cedar Support"):
                self.assertNotIn(employer, text)
            for retained in ("Riley Morgan", "Project Coordinator", "Operations Associate", "03/2022 to 08/2025", "06/2019 to 02/2022", "regional logistics provider", "customer support organization", "name omitted"):
                self.assertIn(retained, text)

    def test_headings_follow_each_formats_intended_order(self):
        expected = {
            "chronological": ("Summary", "Skills", "Experience", "Education and certification"),
            "hybrid": ("Summary", "Selected accomplishments", "Employment history", "Skills", "Education and certification"),
            "functional": ("Professional profile", "Relevant capabilities", "Employment history", "Skills", "Education and certification"),
            "employer-light": ("Summary", "Skills", "Relevant experience", "Education and certification"),
        }
        for variant, headings in expected.items():
            for mode in ("default", "layout"):
                text = self.text(variant, mode)
                positions = [text.index(heading) for heading in headings]
                self.assertEqual(positions, sorted(positions), (variant, mode))

    def test_new_starter_builds_in_path_with_spaces_and_failure_removes_stale_pdf(self):
        value = "personal/Test Resume " + uuid4().hex
        project = ROOT / value
        try:
            with redirect_stdout(io.StringIO()):
                create(value, "hybrid")
                self.assertEqual(process(value), 0)
            output = output_path(project, "hybrid")
            pdf = output / "resume.pdf"
            self.assertTrue(pdf.exists())
            with (project / "candidate.tex").open("a", encoding="utf-8") as handle:
                handle.write("\n\\ThisCommandDoesNotExist\n")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(process(value), 1)
            self.assertFalse(pdf.exists())
            self.assertFalse((output / "resume.qa.json").exists())
            self.assertTrue((output / "build-output.log").exists())
            with self.assertRaises(ResumeError):
                check_pdf(pdf)
        finally:
            # Only remove this test's unique, verified project and build directory.
            if project.exists() and project.resolve().parent == ROOT / "personal":
                shutil.rmtree(project)
            generated = ROOT / "build" / value
            if generated.exists() and generated.resolve().parent == ROOT / "build/personal":
                shutil.rmtree(generated)


if __name__ == "__main__":
    unittest.main()

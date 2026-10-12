"""Letter rendering, preservation, private project boundaries, and real PDF text."""
from contextlib import ExitStack, redirect_stdout
import io
import json
import shutil
import unittest
from unittest.mock import patch
from uuid import uuid4

from scripts import common, cover_letter, new_resume
from scripts.build import process
from scripts.common import ROOT, ResumeError, output_path


def letter_data():
    return json.loads((ROOT / "examples/demo-person/cover-letter.json").read_text(encoding="utf-8"))


class LetterChecks(unittest.TestCase):
    def setUp(self):
        self.fixture = ROOT / "build" / ("letter-unit-" + uuid4().hex)
        self.fixture.mkdir(parents=True)
        shutil.copytree(ROOT / "templates", self.fixture / "templates")
        self.stack = ExitStack()
        for module in (common, new_resume, cover_letter):
            self.stack.enter_context(patch.object(module, "ROOT", self.fixture))
        self.stack.enter_context(redirect_stdout(io.StringIO()))
        new_resume.create("personal/My Application", "hybrid")
        self.project = self.fixture / "personal/My Application"
        self.source = self.project / "cover-letter.json"
        self.source.write_text(json.dumps(letter_data()), encoding="utf-8")

    def tearDown(self):
        self.stack.close()
        if self.fixture.resolve().parent != ROOT / "build":
            raise AssertionError("Unsafe fixture cleanup")
        shutil.rmtree(self.fixture)

    def test_render_escapes_plain_text_and_defaults(self):
        data = letter_data()
        data.pop("salutation")
        data.pop("signoff")
        data["paragraphs"] = [r"R&D 18% $500 project_name #1 {draft} ~ ^ \input{missing}"]
        rendered = cover_letter.render(data)
        for literal in (r"R\&D", r"18\%", r"\$500", r"project\_name", r"\#1", r"\{draft\}", r"\textasciitilde{}", r"\textasciicircum{}", r"\textbackslash{}input\{missing\}", "Dear Hiring Team,", "Sincerely,"):
            self.assertIn(literal, rendered)
        self.assertNotIn(r"\input{missing}", rendered)

    def test_invalid_fields_and_types_are_rejected(self):
        for invalid in ([], {}, {**letter_data(), "typo": "value"}, {**letter_data(), "company": " "}, {**letter_data(), "role": 42}, {**letter_data(), "closing": "bad\x00text"}, {**letter_data(), "paragraphs": []}, {**letter_data(), "paragraphs": ["a"] * 4}, {**letter_data(), "paragraphs": "text"}, {**letter_data(), "paragraphs": [None]}):
            with self.subTest(data=invalid), self.assertRaises(ResumeError):
                cover_letter.render(invalid)

    def test_generation_preserves_candidate_and_requires_explicit_replace(self):
        candidate = (self.project / "candidate.tex").read_bytes()
        cover_letter.generate("personal/My Application")
        destination = self.project / "cover-letter-content.tex"
        destination.write_text("manual edit", encoding="utf-8")
        with self.assertRaisesRegex(ResumeError, "already exists"):
            cover_letter.generate("personal/My Application")
        self.assertEqual(destination.read_text(), "manual edit")
        cover_letter.generate("personal/My Application", replace=True)
        self.assertIn("Example Summit Cooperative", destination.read_text())
        self.assertEqual((self.project / "candidate.tex").read_bytes(), candidate)

    def test_invalid_input_preserves_existing_content_even_with_replace(self):
        destination = self.project / "cover-letter-content.tex"
        destination.write_text("preserve this", encoding="utf-8")
        for content in ('{"company":', '{"company": "incomplete"}'):
            self.source.write_text(content, encoding="utf-8")
            with self.assertRaises(ResumeError):
                cover_letter.generate("personal/My Application", replace=True)
            self.assertEqual(destination.read_text(), "preserve this")

    def test_utf8_bom_is_supported(self):
        self.source.write_text(json.dumps(letter_data()), encoding="utf-8-sig")
        cover_letter.generate("personal/My Application")
        self.assertTrue((self.project / "cover-letter-content.tex").is_file())

    def test_examples_outside_paths_and_old_templates_are_rejected(self):
        shutil.copytree(self.project, self.fixture / "examples/demo")
        for value in ("examples/demo", "../outside"):
            with self.subTest(value=value), self.assertRaises(ResumeError):
                cover_letter.generate(value)
        (self.project / "cover-letter.tex").write_text("old letter template", encoding="utf-8")
        with self.assertRaisesRegex(ResumeError, "current templates"):
            cover_letter.generate("personal/My Application")
        self.assertFalse((self.project / "cover-letter-content.tex").exists())

    def test_missing_dependencies_do_not_generate_content(self):
        with patch("scripts.cover_letter.require_tools", side_effect=ResumeError("missing tool")):
            with self.assertRaisesRegex(ResumeError, "missing tool"):
                cover_letter.build_letter("personal/My Application")
        self.assertFalse((self.project / "cover-letter-content.tex").exists())


AVAILABLE = all(shutil.which(n) for n in ("pdflatex", "pdffonts", "pdftotext", "pdfinfo"))


@unittest.skipUnless(AVAILABLE, "Install TeX and PDF tools to exercise real letter builds")
class LetterIntegration(unittest.TestCase):
    def test_generated_letter_preserves_literal_text_contacts_and_order(self):
        value = "personal/Test Letter " + uuid4().hex
        project = ROOT / value
        try:
            with redirect_stdout(io.StringIO()):
                new_resume.create(value, "hybrid")
                shutil.copyfile(ROOT / "examples/demo-person/candidate.tex", project / "candidate.tex")
                data = letter_data()
                # These are literal rendering probes, not applicant claims.
                symbols = r"R&D 18% $500 project_name #1 {draft} ~ ^ \input{missing}"
                data["paragraphs"].append(symbols)
                (project / "cover-letter.json").write_text(json.dumps(data), encoding="utf-8")
                self.assertEqual(cover_letter.build_letter(value), 0)
                folder = output_path(project, "cover-letter")
                for mode in ("default", "layout"):
                    text = " ".join((folder / f"cover-letter.{mode}.txt").read_text(encoding="utf-8").split())
                    for expected in ("Riley Morgan", "riley.morgan@example.com", "608-555-0142", "Example Summit Cooperative", "18%", "1,200", symbols):
                        self.assertIn(expected, text)
                    ordered = [data["opening"], *data["paragraphs"], data["closing"], data["signoff"]]
                    positions = [text.index(part) for part in ordered]
                    self.assertEqual(positions, sorted(positions))
                    self.assertNotIn("250,000", text)
                    self.assertNotIn("REPLACE ME", text)
                log = (folder / "cover-letter.log").read_text(encoding="utf-8", errors="replace")
                self.assertNotIn("Overfull \\hbox", log)
                self.assertNotIn("Overfull \\vbox", log)
                # Manual TeX builds retain generated content without re-reading JSON.
                (project / "cover-letter.json").write_text("invalid JSON", encoding="utf-8")
                self.assertEqual(process(value, variant="cover-letter"), 0)
        finally:
            if project.exists() and project.resolve().parent == ROOT / "personal":
                shutil.rmtree(project)
            generated = ROOT / "build" / value
            if generated.exists() and generated.resolve().parent == ROOT / "build/personal":
                shutil.rmtree(generated)


if __name__ == "__main__":
    unittest.main()

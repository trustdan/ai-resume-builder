"""Regressions for font parsing, failures, non-overwrite, and release boundaries."""
from contextlib import ExitStack, redirect_stdout
import io
import json
from pathlib import Path
import shutil
import subprocess
import unittest
from unittest.mock import patch
from uuid import uuid4

from scripts import common, doctor, export_starter, new_resume
from scripts.ats_qa import check_pdf, font_problems, text_problems
from scripts.build import compiler_flags, process

HEAD = "name type encoding emb sub uni object ID\n---- ---- ---- --- --- --- ---------\n"


class PDFChecks(unittest.TestCase):
    def test_disable_automatic_installer_only_on_miktex(self):
        for version, expected in (("MiKTeX-pdfTeX 4.26", ["-disable-installer"]), ("pdfTeX 3.14 (TeX Live)", [])):
            result = subprocess.CompletedProcess([], 0, version, "")
            with self.subTest(version=version), patch("scripts.build.run", return_value=result):
                self.assertEqual(compiler_flags(), expected)

    def test_unicode_column_is_not_object_id(self):
        table = HEAD + "ABC+LMRoman Type 1 Custom yes yes no 12 0\n"
        self.assertTrue(any("Unicode" in p for p in font_problems(table)))
        self.assertEqual(font_problems(table.replace("yes yes no", "yes yes yes")), [])

    def test_bitmap_unembedded_and_unparseable_fonts(self):
        self.assertTrue(font_problems(HEAD + "ABC Type 3 Custom yes yes yes 1 0\n"))
        self.assertTrue(font_problems(HEAD + "ABC Type 1 Custom no yes yes 1 0\n"))
        self.assertTrue(font_problems(HEAD + "unexpected table format\n"))
        self.assertTrue(font_problems(HEAD))

    def test_text_corruption_and_supported_unicode(self):
        self.assertEqual(text_problems("Café office workflow certified staff\n03/2022 to 08/2025\f"), [])
        for text in ("", "word\x88", "word\ufffd", "Ocer", "workow"):
            with self.subTest(text=text):
                self.assertTrue(text_problems(text))

    def test_missing_pdf_is_an_error(self):
        with self.assertRaisesRegex(common.ResumeError, "PDF not found"):
            check_pdf(common.ROOT / "build/nonexistent-qa-input.pdf")

    def test_missing_executable_and_timeout_are_actionable(self):
        with patch("scripts.common.subprocess.run", side_effect=FileNotFoundError):
            with self.assertRaisesRegex(common.ResumeError, "Missing executable"):
                common.run(["missing-tool"])
        with patch("scripts.common.subprocess.run", side_effect=subprocess.TimeoutExpired("pdflatex", 1)):
            with self.assertRaisesRegex(common.ResumeError, "timed out"):
                common.run(["pdflatex"], timeout=1)

    def test_pdf_extractor_failure_is_not_a_pass(self):
        pdf = common.ROOT / "examples/previews/chronological.pdf"
        if not pdf.exists():
            self.skipTest("Approved preview has not been generated")
        good_fonts = subprocess.CompletedProcess([], 0, HEAD + "ABC Type 1 Custom yes yes yes 1 0\n", "")
        failed_text = subprocess.CompletedProcess([], 2, "", "invalid PDF stream")
        with patch("scripts.ats_qa.require_tools"), patch("scripts.ats_qa.run", side_effect=[good_fonts, failed_text]):
            with self.assertRaisesRegex(common.ResumeError, "pdftotext default failed"):
                check_pdf(pdf)


class WorkspaceChecks(unittest.TestCase):
    def setUp(self):
        self.actual_root = common.ROOT
        self.fixture = self.actual_root / "build" / ("unit-" + uuid4().hex)
        self.fixture.mkdir(parents=True)
        shutil.copytree(self.actual_root / "templates", self.fixture / "templates")
        self.stack = ExitStack()
        for module in (common, new_resume, export_starter, doctor):
            self.stack.enter_context(patch.object(module, "ROOT", self.fixture))
        self.stack.enter_context(redirect_stdout(io.StringIO()))

    def tearDown(self):
        self.stack.close()
        if self.fixture.resolve().parent != self.actual_root / "build":
            raise AssertionError("Unsafe fixture cleanup")
        shutil.rmtree(self.fixture)

    def test_new_project_with_spaces_and_non_overwrite(self):
        new_resume.create("personal/My Resume", "hybrid")
        project = self.fixture / "personal/My Resume"
        self.assertTrue((project / "shared/preamble.tex").exists())
        for name in ("AGENTS.md", "CLAUDE.md", "cover-letter.json","cover-letter-brief.md"):
            self.assertEqual((project / name).read_bytes(), (self.fixture / "templates" / name).read_bytes())
        self.assertEqual(json.loads((project / "project.json").read_text())["variant"], "hybrid")
        sentinel = project / "my-notes.md"
        sentinel.write_text("preserve me")
        with self.assertRaisesRegex(common.ResumeError, "already exists"):
            new_resume.create("personal/My Resume", "chronological")
        self.assertEqual(sentinel.read_text(), "preserve me")

    def test_path_escape_and_protected_destination_are_rejected(self):
        for value in ("../outside", "personal/../../outside", ".", "templates/new"):
            with self.subTest(value=value), self.assertRaises(common.ResumeError):
                new_resume.create(value, "hybrid")

    def test_anonymous_is_explicit_and_does_not_apply_to_all(self):
        new_resume.create("personal/test", "hybrid")
        with self.assertRaisesRegex(common.ResumeError, "requires --variant employer-light"):
            process("personal/test", all_variants=True, anonymous=True)

    def test_export_is_exact_and_excludes_private_work(self):
        (self.fixture / "README.md").write_text("Public starter")
        manifest = self.fixture / "release-manifest.json"
        manifest.write_text(json.dumps({"files": ["README.md", "release-manifest.json"]}))
        (self.fixture / "personal").mkdir()
        (self.fixture / "personal/private.txt").write_text("DO NOT EXPORT")
        (self.fixture / ".git").mkdir()
        (self.fixture / ".git/config").write_text("PRIVATE REMOTE")
        (self.fixture / "build").mkdir()
        (self.fixture / "build/private.pdf").write_text("PRIVATE OUTPUT")
        export_starter.export("build/clean starter", zip_output=True)
        destination = self.fixture / "build/clean starter"
        self.assertEqual(sorted(p.relative_to(destination).as_posix() for p in destination.rglob("*") if p.is_file()), ["README.md", "release-manifest.json"])
        self.assertTrue((self.fixture / "build/clean starter.zip").is_file())
        with self.assertRaisesRegex(common.ResumeError, "already exists"):
            export_starter.export("build/clean starter")

    def test_bad_manifest_paths_fail_before_copying(self):
        for name in ("../outside.txt", "personal/private.txt", "build/private.pdf", ".git/config"):
            (self.fixture / "release-manifest.json").write_text(json.dumps({"files": [name]}))
            with self.subTest(name=name), self.assertRaises(common.ResumeError):
                export_starter.export("build/export")
            self.assertFalse((self.fixture / "build/export").exists())

    def test_missing_dependency_and_package_doctor_fail(self):
        with patch("scripts.doctor.shutil.which", return_value=None):
            self.assertEqual(doctor.doctor(), 1)

        def fake_run(args, **kwargs):
            missing = args == ["kpsewhich", "needspace.sty"]
            return subprocess.CompletedProcess(args, 1 if missing else 0, "" if missing else "tool version 1\ninstalled/file", "")

        with patch("scripts.doctor.shutil.which", side_effect=lambda n: n), patch("scripts.doctor.run", side_effect=fake_run):
            self.assertEqual(doctor.doctor(), 1)


if __name__ == "__main__":
    unittest.main()

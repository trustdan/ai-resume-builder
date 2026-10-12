"""Check the public file boundary, local doc links, and editor JSON."""
import json
from pathlib import Path
import re
import unittest

from scripts.common import ROOT
from scripts.export_starter import release_files


class ReleaseChecks(unittest.TestCase):
    def test_release_manifest_contains_only_explicit_public_files(self):
        files = release_files()
        self.assertIn("resume.py", files)
        self.assertIn("AGENTS.md", files)
        self.assertIn("release-manifest.json", files)
        for required in ("templates/AGENTS.md", "scripts/AGENTS.md", "tests/AGENTS.md", "docs/ats-and-flatness.md", "docs/agent-guidance.md", "docs/cover-letters.md", "scripts/cover_letter.py", "templates/cover-letter.json", "templates/cover-letter-brief.md", "prompts/build-cover-letter.md", "tests/test_cover_letter.py"):
            self.assertIn(required, files)
        for name in files:
            self.assertNotIn("*", name)
            self.assertNotIn("PLAN.md", name)
            self.assertNotIn("res.cls", name)
            self.assertNotIn("helvetica.sty", name)
        previews = [n for n in files if n.startswith("examples/previews/") and n.endswith(".pdf")]
        self.assertEqual(len(previews), 6)

    def test_markdown_links_resolve_inside_release(self):
        files = set(release_files())
        for name in sorted(files):
            if not name.endswith(".md"):
                continue
            path = ROOT / name
            for target in re.findall(r"\[[^\]]*\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
                if "://" in target or target.startswith(("#", "mailto:")):
                    continue
                target_path = (path.parent / target.split("#")[0]).resolve()
                with self.subTest(document=name, target=target):
                    self.assertTrue(target_path.is_relative_to(ROOT))
                    self.assertIn(target_path.relative_to(ROOT).as_posix(), files)

    def test_editor_task_json_invokes_cli_and_has_no_automatic_tasks(self):
        vscode = json.loads((ROOT / ".vscode/tasks.json").read_text())
        zed = json.loads((ROOT / ".zed/tasks.json").read_text())
        self.assertEqual(vscode["version"], "2.0.0")
        for task in vscode["tasks"] + zed:
            self.assertEqual(task["args"][0], "resume.py")
            self.assertNotIn("runOptions", task)
            self.assertNotIn("hook", task)

    def test_public_source_has_no_personal_repository_records(self):
        for name in release_files():
            if Path(name).suffix in (".pdf", ".png"):
                continue
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIsNone(re.search(r"[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/]", text), name)
            self.assertIsNone(re.search(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", text), name)


if __name__ == "__main__":
    unittest.main()

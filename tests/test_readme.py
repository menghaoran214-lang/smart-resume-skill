"""Behavior tests for the generated README."""

from pathlib import Path
import re
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import render_readme


class RenderTests(unittest.TestCase):
    def test_rendering_is_idempotent(self):
        first = render_readme.render_all()
        second = render_readme.render_all()
        self.assertEqual(first, second)

    def test_checked_in_readmes_match_templates(self):
        changed = render_readme.write(render_readme.render_all(), check=True)
        self.assertEqual(changed, [], "Run scripts/render_readme.py to refresh the READMEs")

    def test_language_switch_is_centered_and_complete(self):
        for name in ("README.md", "README.zh-TW.md", "README.en.md"):
            body = (ROOT / name).read_text(encoding="utf-8")
            match = re.search(r'<p align="center">((?:<a href="README[^"]+">[^<]+</a>(?: · )?){3})</p>', body)
            self.assertIsNotNone(match, f"{name}: no centered paragraph for the language switch")
            links = re.findall(r'href="(README[^"]+)"', match.group(1))
            self.assertEqual(len(links), 3)
            for target in links:
                self.assertTrue((ROOT / target).is_file())

    def test_toc_links_resolve_to_headings(self):
        for name in ("README.md", "README.zh-TW.md", "README.en.md"):
            body = (ROOT / name).read_text(encoding="utf-8")
            anchors = re.findall(r"\]\(#([^)]+)\)", body)
            headings = set(re.findall(r'<a id="([^"]+)"></a>', body))
            self.assertEqual(len(anchors), 7)
            self.assertEqual(len(headings), 8)
            for anchor in anchors:
                self.assertIn(anchor, headings, f"{name}: broken anchor {anchor}")

    def test_toc_is_a_flat_list(self):
        for name in ("README.md", "README.zh-TW.md", "README.en.md"):
            body = (ROOT / name).read_text(encoding="utf-8")
            toc = body.split("<a id=\"what\"></a>")[0].split("</ul>")[-1]
            self.assertNotIn("<details>", toc, f"{name}: the table of contents must stay flat")

    def test_banner_badges_and_first_screen(self):
        for name in ("README.md", "README.zh-TW.md", "README.en.md"):
            body = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn('<p align="center">', body)
            self.assertIn("assets/banner.png", body)
            self.assertIn("img.shields.io/badge/", body)
            self.assertNotIn("{{", body)

    def test_skill_lives_in_skills_directory(self):
        self.assertTrue((ROOT / "skills/smart-resume/SKILL.md").is_file())
        self.assertTrue((ROOT / "skills/smart-resume/scripts/resume.py").is_file())

    def test_banner_image_is_committed(self):
        banner = ROOT / "assets/banner.png"
        self.assertTrue(banner.is_file())
        ignored = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("!assets/banner.png", ignored,
                      "the banner must stay committed or the README shows a broken image")


if __name__ == "__main__":
    unittest.main()

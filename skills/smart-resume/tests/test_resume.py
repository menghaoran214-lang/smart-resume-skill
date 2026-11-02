import copy
import json
from pathlib import Path
import re
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import install
import package
import resume


def example():
    return resume.load(resume.ROOT / "examples/demo.json")


def real_example():
    data = example()
    data["demo"] = False
    data["sources"] = [{"id": "synthetic", "kind": "document", "locator": "unit-test fixture, not a real applicant"}]
    return data


def english_example():
    data = example()
    data["language"] = "en"
    data["jd"] = {"title": "Content Assistant", "company": "Fictional Studio", "source": "Synthetic fixture"}
    data["intention"] = data["jd"]["title"]
    for claim in data["claims"]:
        claim["text"] = f"Fictional example {claim['id']}"
    for page in data["pages"]:
        for section in page:
            section["title"] = "Example section"
    return data


class EvidenceTests(unittest.TestCase):
    def test_demo_requires_explicit_flag(self):
        with self.assertRaisesRegex(ValueError, "--demo"):
            resume.validate(example())
        resume.validate(example(), True)

    def test_synthetic_cannot_be_relabelled_real(self):
        data = example()
        data["demo"] = False
        with self.assertRaisesRegex(ValueError, "Synthetic"):
            resume.validate(data)

    def test_pending_claim_cannot_render(self):
        data = real_example()
        data["claims"][0]["status"] = "pending"
        with self.assertRaisesRegex(ValueError, "Unverified"):
            resume.validate(data)

    def test_memory_needs_confirmation(self):
        data = real_example()
        data["sources"][0]["kind"] = "memory"
        with self.assertRaisesRegex(ValueError, "No supporting"):
            resume.validate(data)
        data["sources"].append({"id": "confirmation", "kind": "user_statement", "locator": "Candidate confirmation fixture"})
        for claim in data["claims"]:
            claim["status"] = "user_confirmed"
            claim["source_ids"].append("confirmation")
        resume.validate(data)

    def test_intention_must_equal_jd(self):
        data = real_example()
        data["intention"] += " / other role"
        with self.assertRaisesRegex(ValueError, "exactly"):
            resume.validate(data)

    def test_duplicate_ids_rejected(self):
        data = real_example()
        data["claims"].append(copy.deepcopy(data["claims"][0]))
        with self.assertRaisesRegex(ValueError, "duplicate"):
            resume.validate(data)

    def test_missing_source_rejected(self):
        data = real_example()
        data["claims"][0]["source_ids"] = ["unknown"]
        with self.assertRaisesRegex(ValueError, "Unknown"):
            resume.validate(data)

    def test_pending_unselected_claim_is_not_in_html(self):
        data = real_example()
        data["claims"].append({"id": "gap", "text": "SECRET_UNVERIFIED_GAP", "status": "pending", "source_ids": []})
        claims, selected = resume.validate(data)
        self.assertNotIn("gap", selected)
        self.assertNotIn("SECRET_UNVERIFIED_GAP", resume.render_html(data, claims, None))

    def test_html_escapes_candidate_markup(self):
        data = real_example()
        data["claims"][0]["text"] = '<script>alert("test")</script>'
        claims, _ = resume.validate(data)
        rendered = resume.render_html(data, claims, None)
        self.assertNotIn("<script>", rendered)
        self.assertIn("&lt;script&gt;", rendered)

    def test_empty_second_page_rejected(self):
        data = real_example()
        data["pages"][1] = []
        with self.assertRaisesRegex(ValueError, "Empty page"):
            resume.validate(data)

    def test_photo_cannot_escape_private_directory(self):
        data = real_example()
        data["candidate"].update(photo_preference="provided", photo="../outside.png")
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "inside private"):
                resume.photo_data(data, Path(temporary))


class RenderTests(unittest.TestCase):
    def test_one_page_output(self):
        data = english_example()
        data["pages"] = data["pages"][:1]
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary) / "delivery"
            report = resume.render(data, Path(temporary), out, demo=True)
            self.assertEqual(report["page_count"], 1)
            self.assertEqual(len(re.findall(rb"/Type\s*/Page\b", (out / "resume.pdf").read_bytes())), 1)

    def test_private_photo_embedded_without_external_path(self):
        import base64
        data = english_example()
        data["candidate"].update(photo_preference="provided", photo="photo.png")
        image_bytes = base64.b64decode("iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+aX1sAAAAASUVORK5CYII=")
        with tempfile.TemporaryDirectory() as temporary:
            private_dir = Path(temporary)
            (private_dir / "photo.png").write_bytes(image_bytes)
            photo = resume.photo_data(data, private_dir)
            self.assertEqual(photo[0].getSize(), (1, 1))
            rendered = resume.render_html(data, resume.validate(data, True)[0], photo)
            self.assertIn("data:image/png;base64,", rendered)
            self.assertNotIn(str(private_dir), rendered)
            resume.render(data, private_dir, private_dir / "delivery", demo=True)

    def test_real_pdf_and_editable_html(self):
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary) / "delivery"
            report = resume.render(english_example(), Path(temporary), out, demo=True)
            pdf = (out / "resume.pdf").read_bytes()
            self.assertTrue(pdf.startswith(b"%PDF-"))
            self.assertEqual(len(re.findall(rb"/Type\s*/Page\b", pdf)), 2)
            self.assertEqual(report["visual_review"], "pending")
            self.assertIn('contenteditable="true"', (out / "resume.html").read_text(encoding="utf-8"))
            with self.assertRaisesRegex(ValueError, "exists"):
                resume.render(english_example(), Path(temporary), out, demo=True)

    def test_overflow_leaves_no_delivery(self):
        data = english_example()
        data["claims"][2]["text"] = "Long supported description. " * 3000
        with tempfile.TemporaryDirectory() as temporary:
            out = Path(temporary) / "delivery"
            with self.assertRaisesRegex(ValueError, "overflows"):
                resume.render(data, Path(temporary), out, demo=True)
            self.assertFalse(out.exists())

    def test_unsupported_font_is_actionable(self):
        with tempfile.TemporaryDirectory() as temporary:
            with self.assertRaisesRegex(ValueError, "--font"):
                resume.render(english_example(), Path(temporary), Path(temporary) / "out",
                              Path(temporary) / "missing.ttf", demo=True)


class DistributionTests(unittest.TestCase):
    def test_install_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "installed"
            install.install(target)
            self.assertEqual((target / "SKILL.md").read_bytes(), (resume.ROOT / "SKILL.md").read_bytes())
            with self.assertRaisesRegex(ValueError, "exists"):
                install.install(target)

    def test_package_is_reproducible_and_allowlisted(self):
        with tempfile.TemporaryDirectory() as temporary:
            first = Path(temporary) / "first.zip"
            second = Path(temporary) / "second.zip"
            self.assertEqual(package.build(first), package.build(second))
            with zipfile.ZipFile(first) as archive:
                self.assertEqual(set(archive.namelist()), {f"smart-resume/{name}" for name in package.FILES})
                self.assertFalse(any("output/" in name or "private/" in name for name in archive.namelist()))

    def test_language_links_resolve(self):
        repository_root = resume.ROOT.parent.parent
        for name in ("README.md", "README.en.md", "README.zh-TW.md"):
            body = (repository_root / name).read_text(encoding="utf-8")
            targets = re.findall(r'href="(README[^"]+)"', body.split("---")[0])
            self.assertEqual(len(targets), 3)
            for target in targets:
                self.assertTrue((repository_root / target).is_file())


if __name__ == "__main__":
    unittest.main()

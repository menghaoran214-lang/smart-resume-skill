import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import gallery
import quality
import resume
import styles


def fixture(language="en"):
    name = "demo.json" if language == "zh-CN" else f"demo.{language}.json"
    return resume.load(resume.ROOT / "examples" / name)


class MatchingTests(unittest.TestCase):
    def test_roles_and_fallback(self):
        roles = {"finance analyst": "classic", "software engineer": "technical",
                 "品牌设计师": "creative", "增长电商": "growth", "商务拓展": "executive", "unknown role": "classic"}
        for title, expected in roles.items():
            self.assertEqual(styles.match({"jd": {"title": title}})[0]["id"], expected)
        self.assertEqual(styles.match(fixture(), ats=True)[0]["id"], "ats")
        self.assertEqual(styles.match({"jd": {"title": "building guide"}})[0]["id"], "classic")

    def test_precedence_and_conflict(self):
        with tempfile.TemporaryDirectory() as temporary:
            saved = styles.save_profile("mine", "technical", directory=temporary) / "profile.json"
            self.assertEqual(styles.resolve(fixture(), profile=saved)["id"], "technical")
            self.assertEqual(styles.resolve(fixture(), "creative")["selection"], "explicit")
            with self.assertRaisesRegex(ValueError, "conflicts"):
                styles.resolve(fixture(), "ats", saved)
            with self.assertRaisesRegex(ValueError, "conflicts"):
                styles.resolve(fixture(), "creative", ats=True)


class ProfileTests(unittest.TestCase):
    def test_roundtrip_no_candidate_data_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as temporary:
            saved = styles.save_profile("my-green", "technical", "#155e52", "airy", temporary)
            profile = styles.read_profile(saved / "profile.json")
            self.assertEqual(profile["spacing"], "airy")
            self.assertEqual(len(styles.list_profiles(temporary)), 1)
            self.assertTrue((saved / "STYLE.md").is_file())
            with self.assertRaisesRegex(ValueError, "exists"):
                styles.save_profile("my-green", "classic", directory=temporary)

    def test_unsafe_or_unreadable_preferences_rejected(self):
        profile = {"schema_version": 1, "name": "mine", "base": "classic", "accent": "#244d68", "spacing": "regular"}
        for key, value in (("name", "../escape"), ("accent", "#ffffff"),
                           ("accent", "red; background:url(x)"), ("spacing", "tiny"), ("base", "unknown")):
            invalid = {**profile, key: value}
            with self.assertRaises(ValueError):
                styles.check_profile(invalid)
        with self.assertRaises(ValueError):
            styles.check_profile({**profile, "candidate": "private"})


class AcceptanceTests(unittest.TestCase):
    def test_growth_numbers_preserve_quotes_and_supported_text(self):
        with tempfile.TemporaryDirectory() as temporary:
            data = fixture()
            data["claims"][2]["text"] = "Candidate's example: 12 tasks, 25% improvement <reviewed>."
            target = Path(temporary) / "out"
            resume.render(data, Path(temporary), target, demo=True, style="growth")
            self.assertTrue(all(quality.inspect(target, data, True)["checks"].values()))
            body = (target / "resume.html").read_text(encoding="utf-8")
            self.assertIn('Candidate&#x27;s example:', body)
            self.assertIn('<span class="metric">25%</span>', body)

    def test_six_styles_three_languages_preserve_every_selected_claim(self):
        for language in ("zh-CN", "zh-TW", "en"):
            for slug in styles.STYLES:
                with self.subTest(language=language, style=slug), tempfile.TemporaryDirectory() as temporary:
                    target = Path(temporary) / "delivery"
                    data = fixture(language)
                    resume.render(data, Path(temporary), target, demo=True, style=slug)
                    result = quality.inspect(target, data, demo=True)
                    self.assertTrue(all(result["checks"].values()), result)
                    self.assertFalse(result["accepted"])
                    self.assertEqual(result["reviews"]["visual_review"], "pending")

    def test_reviews_required_and_demo_never_application_ready(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "delivery"
            data = fixture()
            resume.render(data, Path(temporary), target, demo=True)
            for category in quality.CATEGORIES:
                quality.record(target, category, "passed", "unit-test", "Test-only simulated review; not a release attestation.")
            result = quality.inspect(target, data, True)
            self.assertTrue(result["accepted"])
            self.assertFalse(result["application_ready"])
            self.assertEqual(result["state"], "demo_preview_accepted")
            quality.record(target, "visual_review", "failed", "unit-test", "Simulated failure")
            self.assertFalse(quality.inspect(target, data, True)["accepted"])

    def test_changed_pdf_or_input_cannot_pass(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "delivery"
            data = fixture()
            resume.render(data, Path(temporary), target, demo=True)
            modified = copy.deepcopy(data)
            modified["claims"][0]["text"] = "Different Candidate"
            self.assertFalse(quality.inspect(target, modified, True)["checks"]["selected_text"])
            with (target / "resume.pdf").open("ab") as stream:
                stream.write(b"\n%changed")
            self.assertFalse(quality.inspect(target, data, True)["checks"]["artifact_integrity"])
            with self.assertRaisesRegex(ValueError, "changed"):
                quality.record(target, "visual_review", "passed", "test", "Attempted stale review")

    def test_all_layouts_refuse_overflow_without_partial_delivery(self):
        data = fixture()
        data["claims"][2]["text"] = "Supported long description. " * 2000
        for slug in styles.STYLES:
            with self.subTest(style=slug), tempfile.TemporaryDirectory() as temporary:
                target = Path(temporary) / "out"
                with self.assertRaisesRegex(ValueError, "overflows"):
                    resume.render(data, Path(temporary), target, demo=True, style=slug)
                self.assertFalse(target.exists())

    def test_gallery_rejects_real_inputs(self):
        with tempfile.TemporaryDirectory() as temporary:
            data = fixture()
            data["demo"] = False
            source = Path(temporary) / "input.json"
            source.write_text(json.dumps(data), encoding="utf-8")
            with self.assertRaises(ValueError):
                gallery.build(Path(temporary) / "gallery", source)

    def test_real_gallery_compact_preserves_all_claims_and_links(self):
        with tempfile.TemporaryDirectory() as temporary:
            target = Path(temporary) / "gallery"
            gallery.build(target, compact=True)
            data = resume.load(target / "demo-input.json")
            self.assertEqual(len(data["pages"]), 1)
            manifest = resume.load(target / "manifest.json")
            self.assertEqual(len(manifest), 6)
            for item in manifest:
                self.assertEqual(len(item["pages"]), 1)
                for relative in [item["pdf"], item["html"], *item["pages"]]:
                    self.assertTrue((target / relative).is_file())
                result = quality.inspect(target / item["id"], data, True)
                self.assertTrue(all(result["checks"].values()), result)

    def test_saved_profile_affects_pdf_and_html_without_changing_claims(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            saved = styles.save_profile("green", "technical", "#135341", "airy", root / "profiles")
            data = fixture()
            report = resume.render(data, root, root / "out", demo=True, profile=saved / "profile.json")
            self.assertEqual(report["style"]["accent"], "#135341")
            self.assertEqual(report["style"]["selection"], "profile")
            self.assertIn("#135341", (root / "out/resume.html").read_text(encoding="utf-8"))
            self.assertTrue(all(quality.inspect(root / "out", data, True)["checks"].values()))


if __name__ == "__main__":
    unittest.main()

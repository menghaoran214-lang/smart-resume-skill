from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import library


class LibraryTests(unittest.TestCase):
    def test_lifecycle_and_feedback(self):
        with tempfile.TemporaryDirectory() as root:
            library.save_template("mine", "growth", "ops-growth", "cn-platform", root=root)
            with self.assertRaises(ValueError):
                library.set_status("mine", "promoted", root)
            for kind in ("structure", "technical"):
                library.record_evidence("mine", kind, "quality_checked", root, "Reviewed locally")
            library.set_status("mine", "promoted", root)
            library.log_use("mine", root, applied=10, reply=4, interview=2)
            self.assertIsNone(library.report("mine", root)["invitation_rate"])
            library.log_use("mine", root, applied=20, reply=5, interview=4, offer=1)
            self.assertEqual(library.report("mine", root)["invitation_rate"], 20)
            with self.assertRaises(ValueError):
                library.log_use("mine", root, applied=1, reply=2)
            library.set_status("mine", "deprecated", root, "Repair required")
            self.assertEqual(library.list_templates(status="deprecated", root=root)[0]["id"], "mine")

    def test_private_ids_and_no_unearned_builtin_acceptance(self):
        with tempfile.TemporaryDirectory() as root:
            with self.assertRaises(ValueError):
                library.save_template("../escape", "ats", "general", "ats-direct", root=root)
        self.assertTrue(all(item["evidence"]["technical"] == "unverified" for item in library.built_in()))

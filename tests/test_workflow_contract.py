import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

CANONICAL = {
    "01-course-selection.md": "Step 1 — Select and confirm the exact course",
    "02-objectives.md": "Step 2 — Develop course-level learning objectives",
    "03-scope-selection.md": "Step 3 — Select the teaching scope",
    "04-plan.md": "Step 4 — Create or audit the instructional plan",
    "05a-diagnostic.md": "Step 5A — Prerequisite diagnostic",
    "05b-materials.md": "Step 5B — Teaching materials",
    "06a-quiz.md": "Step 6A — Post-instruction quiz",
    "06b-test.md": "Step 6B — Final unit test",
    "07-results-import.md": "Step 7 — Import anonymized student results",
    "08-analysis-reporting.md": "Step 8 — Analyze results and generate reports, charts, and objective-attainment evidence",
}


class TestWorkflowContract(unittest.TestCase):
    def test_canonical_workflow_files_and_headings(self):
        found = {path.name for path in (ROOT / "workflows").glob("*.md")}
        self.assertEqual(set(CANONICAL), found)
        for filename, label in CANONICAL.items():
            source = (ROOT / "workflows" / filename).read_text(encoding="utf-8")
            self.assertTrue(source.startswith(f"# {label}\n"), filename)
            self.assertRegex(source, r"(?im)^## .*done|^\*\*Completion criterion:\*\*")

    def test_router_and_readme_use_canonical_labels(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        for filename, label in CANONICAL.items():
            self.assertIn(label, skill)
            self.assertIn(f"workflows/{filename}", skill)
            self.assertIn(f"workflows/{filename}", readme)

        obsolete = [
            "workflows/01-objectives.md",
            "workflows/01a-scope-selection.md",
            "workflows/02-plan.md",
            "workflows/03-materials.md",
            "workflows/04-diagnostic.md",
            "workflows/05-assessment.md",
            "workflows/06-feedback.md",
        ]
        for path in obsolete:
            self.assertNotIn(path, skill)
            self.assertNotIn(path, readme)

    def test_root_skill_resource_pointers_exist(self):
        skill = (ROOT / "SKILL.md").read_text(encoding="utf-8")
        resources = re.findall(
            r"`((?:subjects|references|workflows|templates|scripts)/[^` <]+)`",
            skill,
        )
        self.assertTrue(resources)
        for resource in resources:
            self.assertTrue((ROOT / resource).exists(), resource)

    def test_manifest_tracks_canonical_steps_and_branches(self):
        manifest = json.loads((ROOT / "templates/project-manifest.json").read_text(encoding="utf-8"))
        self.assertEqual("2.0", manifest["schema_version"])
        self.assertEqual("1", manifest["workflow"]["current_step"])
        self.assertIsNone(manifest["workflow"]["current_branch"])
        self.assertEqual(
            {"1", "2", "3", "4", "5A", "5B", "6A", "6B", "7", "8"},
            set(manifest["workflow"]["steps"]),
        )
        self.assertEqual("en", manifest["report_language"])


if __name__ == "__main__":
    unittest.main()

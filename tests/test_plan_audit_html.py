import tempfile
import unittest
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_plan_audit_html import validate


def render_template(verdict):
    source = (ROOT / "templates/plan-audit.html").read_text(encoding="utf-8")
    values = {
        "{{LANG}}": "en",
        "{{REPORT_TITLE}}": "Instructional Plan Audit",
        "{{COURSE_AND_SCOPE}}": "Foundations of Mathematics 12 · Probability unit",
        "{{OBJECTIVE_ROWS}}": "<tr><td>O1</td><td>2</td><td>Lesson 1</td><td>Aligned</td></tr>",
        "{{SOURCE_PLAN}}": "teacher-plan.md",
        "{{AUDIT_DATE}}": "2026-11-10",
        "{{CURRICULUM_STATUS}}": "PROVISIONAL",
        "{{OPTIONAL_NOTES}}": "Add another worked example during Step 5 authoring.",
    }
    if verdict == "revision":
        values.update(
            {
                "{{VERDICT_CLASS}}": "revision",
                "{{VERDICT_TEXT}}": "Revision Recommended",
                "{{PROCEED_DECISION}}": "No — resolve the blocker and obtain teacher approval.",
                "{{REQUIRED_CHANGE}}": "Add evidence for O2.",
                "{{REASON}}": "O2 has no observable checkpoint.",
            }
        )
    else:
        values.update(
            {
                "{{VERDICT_CLASS}}": "ready",
                "{{VERDICT_TEXT}}": "Ready to Use",
                "{{PROCEED_DECISION}}": "Yes — after teacher approval.",
                "{{REQUIRED_CHANGE}}": "",
                "{{REASON}}": "",
            }
        )
    for key, value in values.items():
        source = source.replace(key, value)
    if verdict == "ready":
        start = source.index('<section class="panel" id="required-changes">')
        end = source.index('</section>', start) + len('</section>')
        source = source[:start] + source[end:]
    return source


class TestPlanAuditHtml(unittest.TestCase):
    def validate_source(self, source):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "plan_audit.html"
            path.write_text(source, encoding="utf-8")
            return validate(path)

    def test_revision_report_contract(self):
        self.assertEqual([], self.validate_source(render_template("revision")))

    def test_ready_report_contract(self):
        self.assertEqual([], self.validate_source(render_template("ready")))

    def test_two_verdicts_are_rejected(self):
        source = render_template("ready").replace(
            "Ready to Use", "Ready to Use</div><div>Revision Recommended", 1
        )
        self.assertIn("report must contain exactly one current verdict", self.validate_source(source))

    def test_revision_requires_why(self):
        source = render_template("revision").replace("Why: O2 has no observable checkpoint.", "O2 is missing.")
        self.assertIn("revision report requires a Why explanation", self.validate_source(source))


if __name__ == "__main__":
    unittest.main()

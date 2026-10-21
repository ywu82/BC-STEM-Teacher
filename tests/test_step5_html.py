import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from validate_step5_html import validate


class TestStep5Html(unittest.TestCase):
    def test_bundled_shell_is_valid_after_placeholder_fill(self):
        content = (ROOT / "templates" / "step5-html-shell.html").read_text(encoding="utf-8")
        replacements = {
            "{{AUDIENCE}}": "Student",
            "{{TITLE}}": "Diagnostic",
            "{{COURSE}}": "Chemistry 11",
            "{{PURPOSE}}": "Check prerequisite knowledge.",
            "{{CONTENT}}": "<section class=\"page\"><h2>Questions</h2></section>",
            "{{FOOTER_NOTE}}": "Low-stakes diagnostic.",
        }
        for key, value in replacements.items():
            content = content.replace(key, value)
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "diagnostic.html"
            path.write_text(content, encoding="utf-8")
            self.assertEqual(validate(path), [])

    def test_external_dependency_is_rejected(self):
        content = (ROOT / "templates" / "step5-html-shell.html").read_text(encoding="utf-8")
        content = content.replace("</head>", '<script src="https://example.com/app.js"></script></head>')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "bad.html"
            path.write_text(content, encoding="utf-8")
            self.assertTrue(any("external HTTP" in error for error in validate(path)))


if __name__ == "__main__":
    unittest.main()

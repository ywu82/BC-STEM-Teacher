#!/usr/bin/env python3
"""Validate teacher-ready Step 5 HTML artifacts using the standard library."""
import argparse
import re
from pathlib import Path

REQUIRED = {
    "HTML5 doctype": r"<!doctype\s+html>",
    "language": r"<html\b[^>]*\blang=",
    "UTF-8 charset": r"<meta\b[^>]*charset=[\"']?utf-8",
    "responsive viewport": r"<meta\b[^>]*name=[\"']viewport[\"']",
    "audience metadata": r"<meta\b[^>]*name=[\"']audience[\"']",
    "document title": r"<title>.+?</title>",
    "main landmark": r"<main\b",
    "Print / Save as PDF label": r"Print\s*/\s*Save\s+as\s+PDF",
    "browser print action": r"window\.print\s*\(\s*\)",
    "print stylesheet": r"@media\s+print",
}

def validate(path):
    path = Path(path)
    errors = []
    if path.suffix.lower() != ".html":
        return ["file extension must be .html"]
    if not path.is_file():
        return ["file does not exist"]
    text = path.read_text(encoding="utf-8")
    for label, pattern in REQUIRED.items():
        if not re.search(pattern, text, flags=re.IGNORECASE | re.DOTALL):
            errors.append(f"missing {label}")
    if re.search(r"(?:src|href)\s*=\s*[\"']https?://", text, flags=re.IGNORECASE):
        errors.append("external HTTP(S) dependency found; Step 5 HTML must be self-contained")
    return errors

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument("files", nargs="+")
    args = parser.parse_args(argv)
    failed = False
    for name in args.files:
        errors = validate(name)
        if errors:
            failed = True
            print(f"FAIL: {name}")
            for error in errors:
                print(f"  - {error}")
        else:
            print(f"OK: {name}")
    raise SystemExit(1 if failed else 0)

if __name__ == "__main__":
    main()

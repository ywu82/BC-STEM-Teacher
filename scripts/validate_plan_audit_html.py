#!/usr/bin/env python3
"""Validate a rendered Step 4 plan-audit HTML report."""

import re
import sys
from pathlib import Path


def validate(path):
    source = Path(path).read_text(encoding="utf-8")
    errors = []
    required = {
        "HTML5 doctype": r"<!doctype\s+html>",
        "language attribute": r"<html\b[^>]*\blang=",
        "UTF-8 charset": r"<meta\b[^>]*charset=[\"']?utf-8",
        "responsive viewport": r"<meta\b[^>]*name=[\"']viewport[\"']",
        "main landmark": r"<main\b",
        "print control": r"Print\s*/\s*Save\s+as\s+PDF",
        "window.print": r"window\.print\s*\(\s*\)",
        "print stylesheet": r"@media\s+print",
        "objective alignment": r"Objective alignment",
        "source preservation statement": r"remains unchanged",
    }
    for label, pattern in required.items():
        if not re.search(pattern, source, re.I | re.S):
            errors.append(f"missing {label}")

    if re.search(r"(?:src|href)\s*=\s*[\"']https?://", source, re.I):
        errors.append("external HTTP(S) dependency found")
    if re.search(r"\{\{[^}]+\}\}", source):
        errors.append("unresolved template placeholder found")

    revision_count = len(re.findall(r">\s*Revision Recommended\s*<", source, re.I))
    ready_count = len(re.findall(r">\s*Ready to Use\s*<", source, re.I))
    if revision_count + ready_count != 1:
        errors.append("report must contain exactly one current verdict")
    elif revision_count:
        if not re.search(r"class=[\"'][^\"']*\bverdict\b[^\"']*\brevision\b", source, re.I):
            errors.append("Revision Recommended must use the revision verdict class")
        if not re.search(r"class=[\"'][^\"']*\bchange\b", source, re.I):
            errors.append("revision report requires at least one highlighted change")
        if not re.search(r"\bWhy:\s*\S", source, re.I):
            errors.append("revision report requires a Why explanation")
    elif not re.search(r"class=[\"'][^\"']*\bverdict\b[^\"']*\bready\b", source, re.I):
        errors.append("Ready to Use must use the ready verdict class")

    return errors


def main(argv=None):
    args = sys.argv[1:] if argv is None else argv
    if not args:
        raise SystemExit("usage: validate_plan_audit_html.py <plan_audit.html> [...]")
    failed = False
    for name in args:
        errors = validate(name)
        if errors:
            failed = True
            print(f"INVALID: {name}")
            for error in errors:
                print(f" - {error}")
        else:
            print(f"VALID: {name}")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()

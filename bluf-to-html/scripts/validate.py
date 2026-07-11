#!/usr/bin/env python3
"""Validate BLUF report HTML against phase 3/4 constraints.

Usage:
  python scripts/validate.py path/to/report.html
  python scripts/validate.py path/to/report.html --strict

Exit 0 = OK (warnings may still print). Exit 1 = errors found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

FORBIDDEN_PATTERNS = [
    (r"<script\b", "script tag (JavaScript not allowed in email)"),
    (r"@font-face", "custom @font-face (use web-safe fonts)"),
    (r"display\s*:\s*flex", "display:flex (use tables)"),
    (r"display\s*:\s*grid", "display:grid (use tables)"),
    (r"position\s*:\s*fixed", "position:fixed (unreliable in email)"),
    (r"<link[^>]+stylesheet", "external stylesheet (use inline CSS)"),
    (r"chart\.js|Chart\.js", "Chart.js reference (use static image or omit)"),
]

WARN_PATTERNS = [
    (r"<ul\b", "native <ul> (prefer table-based bullets for Outlook)"),
    (r"background-image\s*:", "background-image (may strip in Gmail)"),
    (r"var\s*\(--", "CSS variables (may strip in email clients)"),
    (r"src\s*=\s*[\"']data:", "base64 data URI image (prefer hosted https URL)"),
    (r"src\s*=\s*[\"']http://", "non-HTTPS image URL"),
]

def _style_block_warning(html: str) -> str | None:
    if not re.search(r"<style\b", html, re.IGNORECASE):
        return None
    if re.search(r"@media[^\{]*max-width:\s*500px", html, re.IGNORECASE):
        return None
    return "style block without mobile breakpoint (include reference.md responsive <style>)"

REQUIRED_PATTERNS = [
    (r"role\s*=\s*[\"']presentation[\"']", "table role=presentation"),
    (r"background-color", "inline background-color"),
    (r"class\s*=\s*[\"'][^\"']*item-label", "item-label class for mobile stack"),
    (r"@media[^\{]*max-width:\s*500px", "responsive breakpoint at 500px"),
]


def validate(html: str, strict: bool = False) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []

    for pattern, msg in FORBIDDEN_PATTERNS:
        if re.search(pattern, html, re.IGNORECASE):
            errors.append(msg)

    for pattern, msg in WARN_PATTERNS:
        if re.search(pattern, html, re.IGNORECASE):
            warnings.append(msg)

    style_warn = _style_block_warning(html)
    if style_warn:
        warnings.append(style_warn)

    for pattern, msg in REQUIRED_PATTERNS:
        if not re.search(pattern, html, re.IGNORECASE):
            warnings.append(f"missing {msg}")

    if strict and warnings:
        errors.extend(f"[strict] {w}" for w in warnings)

    return errors, warnings


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: validate.py <report.html> [--strict]", file=sys.stderr)
        return 2

    path = Path(sys.argv[1])
    strict = "--strict" in sys.argv[2:]

    if not path.is_file():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 2

    html = path.read_text(encoding="utf-8")
    errors, warnings = validate(html, strict=strict)

    if warnings:
        print("Warnings:")
        for w in warnings:
            print(f"  - {w}")

    if errors:
        print("Errors:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())

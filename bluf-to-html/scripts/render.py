#!/usr/bin/env python3
"""Render structured BLUF report data to email-safe HTML."""

from __future__ import annotations

import html
import json
import re
import sys
from pathlib import Path
from typing import Any

ROMANS = (
    "I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X",
    "XI", "XII", "XIII", "XIV", "XV",
)

HEAD_STYLE = """  <style type="text/css">
    @media only screen and (max-width: 500px) {
      .doc-pad-outer { padding-left: 12px !important; padding-right: 12px !important; padding-top: 24px !important; padding-bottom: 40px !important; }
      .doc-pad { padding-left: 20px !important; padding-right: 20px !important; }
      .doc-pad-title { padding-left: 20px !important; padding-right: 20px !important; padding-top: 32px !important; }
      .doc-pad-lead { padding-left: 20px !important; padding-right: 20px !important; padding-top: 24px !important; }
      .doc-pad-body { padding-left: 20px !important; padding-right: 20px !important; padding-top: 32px !important; }
      .lead-wrap { width: 100% !important; max-width: 100% !important; }
      .item-label,
      .item-body {
        display: block !important;
        width: 100% !important;
        max-width: 100% !important;
      }
      .item-label { padding: 0 0 6px 0 !important; }
      .item-body { padding: 0 0 24px 0 !important; }
      h1.title { font-size: 32px !important; }
      .callout-pad { padding-left: 16px !important; padding-right: 16px !important; }
    }
  </style>"""


def esc(text: str) -> str:
    return html.escape(text, quote=True)


def split_lead(text: str) -> tuple[str, str]:
    text = text.strip()
    if not text:
        return "", ""
    match = re.match(r"^(.+?[.!?])(?:\s+(.+))?$", text, re.DOTALL)
    if not match:
        return text, ""
    first, rest = match.group(1), match.group(2) or ""
    return first.strip(), rest.strip()


def render_bullets(bullets: list[str]) -> str:
    if not bullets:
        return ""
    rows = []
    for bullet in bullets:
        rows.append(
            "  <tr>\n"
            '    <td style="width:14px; vertical-align:top; padding:0 8px 8px 0; '
            'font-size:14px; line-height:1.7; color:rgba(0,0,0,0.6);">&bull;</td>\n'
            f'    <td style="vertical-align:top; padding:0 0 8px 0; font-size:14px; '
            f'line-height:1.7; color:rgba(0,0,0,0.6);">{esc(bullet)}</td>\n'
            "  </tr>"
        )
    return (
        '<table role="presentation" cellpadding="0" cellspacing="0" border="0" '
        'width="100%" style="margin-top:10px;">\n'
        + "\n".join(rows)
        + "\n</table>"
    )


def render_item_body(item: dict[str, Any]) -> str:
    lead = item.get("lead") or item.get("body") or ""
    rest = item.get("rest", "")
    bullets = item.get("bullets") or []

    if not rest and lead and not bullets:
        first, remainder = split_lead(lead)
        lead, rest = first, remainder

    parts: list[str] = []
    if lead:
        if rest or bullets:
            parts.append(
                f'<span style="color:#1a1a1a;">{esc(lead)}</span>'
                + (f" {esc(rest)}" if rest else "")
            )
        else:
            parts.append(esc(lead))
    elif rest:
        parts.append(esc(rest))

    body = " ".join(parts).strip()
    if bullets:
        body += render_bullets(bullets)
    return body


def render_item_row(item: dict[str, Any]) -> str:
    label = esc(item.get("label") or "Overview")
    body = render_item_body(item)
    return f"""<tr>
  <td class="item-label" style="width:33%; vertical-align:top; padding:0 20px 32px 0; font-size:14px; font-weight:400; color:#1a1a1a; line-height:1.7;">
    {label}
  </td>
  <td class="item-body" style="width:67%; vertical-align:top; padding:0 0 32px 0; font-size:14px; line-height:1.7; color:rgba(0,0,0,0.6);">
    {body}
  </td>
</tr>"""


def render_section(section: dict[str, Any], index: int) -> str:
    roman = ROMANS[index] if index < len(ROMANS) else str(index + 1)
    title = esc(section.get("title") or "Section")
    top = "0" if index == 0 else "16px"
    items = section.get("items") or []
    if not items and section.get("body"):
        items = [{"label": "Overview", "body": section["body"]}]

    rows = "\n".join(render_item_row(item) for item in items)
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr>
    <td class="section-heading" style="padding:{top} 0 20px 0; font-family:Georgia, 'Times New Roman', serif; font-size:16px; font-weight:400; font-style:italic; color:#1a1a1a; line-height:1.3;">
      <span style="border-bottom:1px solid rgba(0,0,0,0.25); padding-bottom:4px;">{roman}. {title}</span>
    </td>
  </tr>
</table>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
{rows}
</table>
"""


def render_quote(quote: str) -> str:
    return f"""<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:8px 0 40px;">
  <tr>
    <td style="border-top:1px solid rgba(0,0,0,0.1); font-size:0; line-height:0; mso-line-height-rule:exactly;">&nbsp;</td>
  </tr>
  <tr>
    <td align="center" class="callout-pad" style="padding:36px 24px 28px;">
      <p style="margin:0 0 12px; font-size:56px; line-height:0.72; color:rgba(0,0,0,0.45); font-family:Georgia, 'Times New Roman', serif; font-style:italic; font-weight:400;">&ldquo;</p>
      <p style="margin:0 auto; max-width:480px; font-family:Georgia, 'Times New Roman', serif; font-size:17px; font-weight:400; font-style:italic; line-height:1.45; color:#1a1a1a; letter-spacing:-0.01em;">
        {esc(quote)}
      </p>
    </td>
  </tr>
  <tr>
    <td style="border-top:1px solid rgba(0,0,0,0.1); font-size:0; line-height:0; mso-line-height-rule:exactly;">&nbsp;</td>
  </tr>
</table>"""


def render_report(data: dict[str, Any]) -> str:
    title = esc(data.get("title") or "Untitled")
    date = esc(data.get("date") or "")
    bg = esc(data.get("background") or "#FAF9F5")
    lead = esc(data.get("lead") or "")
    sections = data.get("sections") or []
    quote = data.get("quote")
    quote_after = int(data.get("quote_after_section", 2))

    section_html: list[str] = []
    for i, section in enumerate(sections):
        section_html.append(render_section(section, i))
        if quote and i == quote_after - 1:
            section_html.append(render_quote(quote))

    sections_block = "\n".join(section_html)

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
{HEAD_STYLE}
</head>
<body style="margin:0; padding:0; background-color:{bg}; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;">

  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:{bg};">
    <tr>
      <td align="center" class="doc-pad-outer" style="padding:40px 16px 56px;">

        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="640" style="max-width:640px; width:100%; background-color:{bg};">

          <tr>
            <td class="doc-pad" style="padding:0 48px;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr>
                  <td style="font-size:11px; letter-spacing:0.18em; text-transform:uppercase; color:rgba(0,0,0,0.6); font-weight:500;">
                    SYNTHESIS
                  </td>
                  <td align="right" style="font-size:11px; letter-spacing:0.12em; text-transform:uppercase; color:rgba(0,0,0,0.6); font-weight:500;">
                    {date}
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td class="doc-pad-title" style="padding:40px 48px 0;">
              <h1 class="title" style="margin:0; font-family:Georgia, 'Times New Roman', serif; font-size:38px; font-weight:400; font-style:italic; line-height:1.08; color:#1a1a1a; letter-spacing:-0.03em;">
                {title}
              </h1>
            </td>
          </tr>

          <tr>
            <td class="doc-pad-lead" style="padding:32px 48px 0;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="85%" class="lead-wrap" style="max-width:520px;">
                <tr>
                  <td style="font-size:14px; line-height:1.7; color:#1a1a1a;">
                    {lead}
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td class="doc-pad" style="padding:40px 48px 0;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr>
                  <td style="border-top:1px solid rgba(0,0,0,0.1); font-size:0; line-height:0; mso-line-height-rule:exactly;">&nbsp;</td>
                </tr>
              </table>
            </td>
          </tr>

          <tr>
            <td class="doc-pad-body" style="padding:48px 48px 0;">
              {sections_block}
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>

</body>
</html>
"""


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: render.py <report.json> [output.html]", file=sys.stderr)
        return 2

    src = Path(sys.argv[1])
    data = json.loads(src.read_text(encoding="utf-8"))
    html_out = render_report(data)

    if len(sys.argv) >= 3:
        Path(sys.argv[2]).write_text(html_out, encoding="utf-8")
    else:
        sys.stdout.write(html_out)
    return 0


if __name__ == "__main__":
    sys.exit(main())

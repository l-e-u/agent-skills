# HTML Template Reference

Copy this skeleton. Replace `{{PLACEHOLDERS}}`. Keep all CSS inline.

## Design principles (phase 1)

- **Content over input structure** — `────────`, blank lines, and numbering in pasted text are parsing hints only. Do not mirror them literally in output.
- **Single paper background** — one `#FAF9F5` surface; no outer gray mat.
- **Rules only at semantic breaks** — after intro, flanking pull-quote. Not between every Roman section.
- **Email-safe** — tables, inline styles, web-safe fonts, `&bull;` bullets in nested tables (not `::before`).
- **Responsive** — one `<style>` block in `<head>` for `max-width: 500px`: tighter horizontal padding, subsection label/body stack vertically.

## Full document template

Implemented by [scripts/render.py](scripts/render.py). Agents write report JSON and run the script — do not copy this HTML by hand. Reference below documents output shape and tokens.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{TITLE}}</title>
  <style type="text/css">
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
  </style>
</head>
<body style="margin:0; padding:0; background-color:#FAF9F5; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;">

  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:{{BG_COLOR}};">
    <tr>
      <td align="center" class="doc-pad-outer" style="padding:40px 16px 56px;">

        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="640" style="max-width:640px; width:100%; background-color:{{BG_COLOR}};">

          <!-- Header bar -->
          <tr>
            <td class="doc-pad" style="padding:0 48px;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr>
                  <td style="font-size:11px; letter-spacing:0.18em; text-transform:uppercase; color:rgba(0,0,0,0.6); font-weight:500;">
                    SYNTHESIS
                  </td>
                  <td align="right" style="font-size:11px; letter-spacing:0.12em; text-transform:uppercase; color:rgba(0,0,0,0.6); font-weight:500;">
                    {{DATE}}
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Title -->
          <tr>
            <td class="doc-pad-title" style="padding:40px 48px 0;">
              <h1 class="title" style="margin:0; font-family:Georgia, 'Times New Roman', serif; font-size:38px; font-weight:400; font-style:italic; line-height:1.08; color:#1a1a1a; letter-spacing:-0.03em;">
                {{TITLE}}
              </h1>
            </td>
          </tr>

          <!-- Lead paragraph (constrained width) -->
          <tr>
            <td class="doc-pad-lead" style="padding:32px 48px 0;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="85%" class="lead-wrap" style="max-width:520px;">
                <tr>
                  <td style="font-size:14px; line-height:1.7; color:#1a1a1a;">
                    {{LEAD}}
                  </td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Intro rule -->
          <tr>
            <td class="doc-pad" style="padding:40px 48px 0;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr>
                  <td style="border-top:1px solid rgba(0,0,0,0.1); font-size:0; line-height:0; mso-line-height-rule:exactly;">&nbsp;</td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Main content (generous top padding after intro rule) -->
          <tr>
            <td class="doc-pad-body" style="padding:48px 48px 0;">
              {{SECTIONS}}
              {{CALLOUT}}
            </td>
          </tr>

        </table>
      </td>
    </tr>
  </table>

</body>
</html>
```

## Section block template

Insert `{{CALLOUT}}` after section II when using the default layout.

**Use a table row for every Roman heading — never `<p>`.** Email clients (Spark, Gmail, Outlook) often strip `<p>` inside layout cells; table headings survive.

Emit **one section block per major section** (I, II, III…). Do not fold section titles into `item-label` — labels are for subsections only (3–6 words).

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
  <tr>
    <td class="section-heading" style="padding:{{SECTION_TOP_MARGIN}} 0 20px 0; font-family:Georgia, 'Times New Roman', serif; font-size:16px; font-weight:400; font-style:italic; color:#1a1a1a; line-height:1.3;">
      <span style="border-bottom:1px solid rgba(0,0,0,0.25); padding-bottom:4px;">{{ROMAN}}. {{SECTION_TITLE}}</span>
    </td>
  </tr>
</table>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
  {{SUBSECTION_ROWS}}
</table>
```

First section after intro rule: main content cell uses `padding-top:48px` (space below the rule). Use `SECTION_TOP_MARGIN`: `0` for section I, `16px` for sections II–V.

## Subsection row template

At viewports **≤500px**, `.item-label` and `.item-body` stack vertically (label above body, below the Roman section heading).

```html
<tr>
  <td class="item-label" style="width:33%; vertical-align:top; padding:0 20px 32px 0; font-size:14px; font-weight:400; color:#1a1a1a; line-height:1.7;">
    {{SUB_LABEL}}
  </td>
  <td class="item-body" style="width:67%; vertical-align:top; padding:0 0 32px 0; font-size:14px; line-height:1.7; color:rgba(0,0,0,0.6);">
    {{SUB_BODY}}
  </td>
</tr>
```

## Report lead

Render the full BLUF paragraph as plain text in the lead cell — primary color (`#1a1a1a`) on the `<td>`. Do not wrap the first sentence in a `<span>`; the whole lead reads at full weight.

## Item body lead sentence (prefer over `<strong>`)

For subsection body columns only — first sentence dark, rest secondary:

```html
<span style="color:#1a1a1a;">{{FIRST_SENTENCE}}</span> {{REST_IN_SECONDARY_COLOR}}
```

Body column default color: `rgba(0,0,0,0.6)`.

## Responsive layout (≤500px)

Include the `<style>` block from the full document template in every output. At **500px and below**:

| Change | Desktop | Mobile |
|--------|---------|--------|
| Outer horizontal padding | 16px | 12px |
| Inner horizontal padding | 48px | 20px |
| Lead width | 85% / max 520px | 100% |
| Subsection layout | 33% label \| 67% body (side by side) | Label stacked above body |
| Title size | 38px | 32px |

**Required classes** (do not omit):

- `doc-pad-outer`, `doc-pad`, `doc-pad-title`, `doc-pad-lead`, `doc-pad-body` — horizontal padding targets
- `lead-wrap` — lead paragraph width
- `item-label`, `item-body` — stack on narrow viewports
- `title` — h1 size adjustment
- `callout-pad` — pull-quote horizontal padding

Header label is always the literal text **SYNTHESIS** — not a placeholder, not inferred from content.

## Email-safe bullet list

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin-top:10px;">
  <tr>
    <td style="width:14px; vertical-align:top; padding:0 8px 8px 0; font-size:14px; line-height:1.7; color:rgba(0,0,0,0.6);">&bull;</td>
    <td style="vertical-align:top; padding:0 0 8px 0; font-size:14px; line-height:1.7; color:rgba(0,0,0,0.6);">{{BULLET_TEXT}}</td>
  </tr>
</table>
```

## Pull-quote callout (with flanking rules)

```html
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="margin:8px 0 40px;">
  <tr>
    <td style="border-top:1px solid rgba(0,0,0,0.1); font-size:0; line-height:0; mso-line-height-rule:exactly;">&nbsp;</td>
  </tr>
  <tr>
    <td align="center" class="callout-pad" style="padding:36px 24px 28px;">
      <p style="margin:0 0 12px; font-size:56px; line-height:0.72; color:rgba(0,0,0,0.45); font-family:Georgia, 'Times New Roman', serif; font-style:italic; font-weight:400;">&ldquo;</p>
      <p style="margin:0 auto; max-width:480px; font-family:Georgia, 'Times New Roman', serif; font-size:17px; font-weight:400; font-style:italic; line-height:1.45; color:#1a1a1a; letter-spacing:-0.01em;">
        {{QUOTE_TEXT}}
      </p>
    </td>
  </tr>
  <tr>
    <td style="border-top:1px solid rgba(0,0,0,0.1); font-size:0; line-height:0; mso-line-height-rule:exactly;">&nbsp;</td>
  </tr>
</table>
```

## Color tokens

| Token | Default | Usage |
|-------|---------|-------|
| Background | `#FAF9F5` | Full document |
| Text primary | `#1a1a1a` | Title, lead paragraph, labels, item lead sentences |
| Text secondary | `rgba(0,0,0,0.6)` | Body, bullets |
| Text muted | `rgba(0,0,0,0.25)` | Section underline |
| Divider | `rgba(0,0,0,0.1)` | Intro rule, quote rules |
| Quote mark | `rgba(0,0,0,0.45)` | Decorative `"` |

## Typography scale

| Element | Font | Size | Style |
|---------|------|------|-------|
| Title (h1) | Georgia, Times | 38px | italic 400 |
| Lead (BLUF) | System sans | 14px | primary color |
| Section heading | Georgia, Times | 16px | italic + underline |
| Subsection label | System sans | 14px | normal 400 |
| Body | System sans | 14px | secondary color |
| Header meta | System sans | 11px | uppercase; fixed label **SYNTHESIS** (left) + date (right) |
| Callout | Georgia, Times | 17px | italic 400 |

## Roman numerals

```
1→I  2→II  3→III  4→IV  5→V  6→VI  7→VII  8→VIII  9→IX  10→X
```

## Paper palette (customizable backgrounds)

From Report-Kit paper palette — use any as `{{BG_COLOR}}`:

```
#FAF9F5  ivory (default)
#FFF8DA  canary
#F9E8EC  rose
#E2ECF5  powder blue
#E3EDDF  sage
#EDE4F2  orchid
#FEEADD  salmon
#E6E8EB  fog
```

---

## Extended components

Use only when source has real data ([authoring.md](authoring.md)). Metrics/chart/image templates below; data-table pattern in [integration.md](integration.md) §5 parity notes.

### Metrics strip — insert after lead, before intro rule

```html
<tr>
  <td style="padding:32px 48px 0;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="border-top:1px solid rgba(0,0,0,0.1); border-bottom:1px solid rgba(0,0,0,0.1);">
      <tr>
        <td width="33%" style="vertical-align:top; padding:20px 16px 20px 0; border-right:1px solid rgba(0,0,0,0.1);">
          <p style="margin:0; font-family:Georgia, 'Times New Roman', serif; font-size:28px; line-height:1.1; color:#1a1a1a;">{{VALUE}}</p>
          <p style="margin:4px 0 0; font-size:14px; color:rgba(0,0,0,0.6);">{{LABEL}}</p>
          <p style="margin:2px 0 0; font-size:12px; color:rgba(0,0,0,0.4);">{{NOTE}}</p>
        </td>
      </tr>
    </table>
  </td>
</tr>
```

### Static chart/image

```html
<img src="https://example.com/chart.png" width="544" alt="{{DESCRIPTION}}"
     style="display:block; max-width:100%; height:auto; border:0;" />
```

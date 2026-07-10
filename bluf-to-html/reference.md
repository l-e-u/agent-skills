# HTML Template Reference

Copy this skeleton. Replace `{{PLACEHOLDERS}}`. Keep all CSS inline.

## Design principles (phase 1)

- **Content over input structure** — `────────`, blank lines, and numbering in pasted text are parsing hints only. Do not mirror them literally in output.
- **Single paper background** — one `#FAF9F5` surface; no outer gray mat.
- **Rules only at semantic breaks** — after intro, flanking pull-quote. Not between every Roman section.
- **Email-safe** — tables, inline styles, web-safe fonts, `&bull;` bullets in nested tables (not `::before`).

## Full document template

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{{TITLE}}</title>
</head>
<body style="margin:0; padding:0; background-color:#FAF9F5; font-family:-apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif;">

  <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:{{BG_COLOR}};">
    <tr>
      <td align="center" style="padding:40px 16px 56px;">

        <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="640" style="max-width:640px; width:100%; background-color:{{BG_COLOR}};">

          <!-- Header bar -->
          <tr>
            <td style="padding:0 48px;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr>
                  <td style="font-size:11px; letter-spacing:0.18em; text-transform:uppercase; color:rgba(0,0,0,0.6); font-weight:500;">
                    {{REPORT_LABEL}}
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
            <td style="padding:40px 48px 0;">
              <h1 style="margin:0; font-family:Georgia, 'Times New Roman', serif; font-size:38px; font-weight:400; font-style:italic; line-height:1.08; color:#1a1a1a; letter-spacing:-0.03em;">
                {{TITLE}}
              </h1>
            </td>
          </tr>

          <!-- Lead paragraph (constrained width) -->
          <tr>
            <td style="padding:32px 48px 0;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="85%" style="max-width:520px;">
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
            <td style="padding:40px 48px 0;">
              <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
                <tr>
                  <td style="border-top:1px solid rgba(0,0,0,0.1); font-size:0; line-height:0; mso-line-height-rule:exactly;">&nbsp;</td>
                </tr>
              </table>
            </td>
          </tr>

          <!-- Main content (generous top padding after intro rule) -->
          <tr>
            <td style="padding:48px 48px 0;">
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

```html
<p style="margin:{{SECTION_TOP_MARGIN}} 0 20px; font-family:Georgia, 'Times New Roman', serif; font-size:16px; font-weight:400; font-style:italic; color:#1a1a1a; line-height:1.3;">
  <span style="border-bottom:1px solid rgba(0,0,0,0.25); padding-bottom:4px;">{{ROMAN}}. {{SECTION_TITLE}}</span>
</p>
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
  {{SUBSECTION_ROWS}}
</table>
```

First section after intro rule: main content cell uses `padding-top:48px` (space below the rule). Use `SECTION_TOP_MARGIN`: `0` for section I, `16px` for sections II–V.

## Subsection row template

```html
<tr>
  <td style="width:33%; vertical-align:top; padding:0 20px 32px 0; font-size:14px; font-weight:400; color:#1a1a1a; line-height:1.7;">
    {{SUB_LABEL}}
  </td>
  <td style="width:67%; vertical-align:top; padding:0 0 32px 0; font-size:14px; line-height:1.7; color:rgba(0,0,0,0.6);">
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
    <td align="center" style="padding:36px 24px 28px;">
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
| Header meta | System sans | 11px | uppercase |
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

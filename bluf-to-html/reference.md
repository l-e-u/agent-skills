# Output Reference

Read-only guide to what [scripts/render.py](scripts/render.py) produces. **Agents write JSON** ([integration.md](integration.md)); never assemble HTML from this file.

## JSON field → rendered output

| JSON field | Rendered as |
|------------|---------------|
| `title` | Georgia italic h1 (38px desktop, 32px mobile) |
| `date` | Uppercase meta, right of **SYNTHESIS** header |
| `background` | Paper color on body and inner 640px column |
| `lead` | BLUF paragraph, primary color, ~85% width (100% mobile) |
| `sections[].title` | Roman numeral + underlined section heading (I, II, III… auto) |
| `items[].label` | Left column subheading (3–6 words) |
| `items[].lead` | Dark first sentence in body column |
| `items[].rest` | Secondary-color supporting prose |
| `items[].bullets[]` | Email-safe `&bull;` table under item body |
| `quote` | Pull quote with flanking rules after `quote_after_section` |

Roman numerals come from **section order** in `sections[]` — do not put "I." in `title` strings.

## Layout hierarchy

```
SYNTHESIS + date
Title (h1)
Lead (BLUF)
Intro rule (horizontal line)
For each section:
  Roman heading (table row, .section-heading)
  For each item:
    label | body (side by side desktop; stacked mobile)
[optional] Pull quote between sections
```

## Responsive (≤640px)

Handled entirely by `render.py` — `@media (max-width: 640px)` in document `<head>`:

| Change | Desktop | Mobile |
|--------|---------|--------|
| Outer horizontal padding | 16px | 12px |
| Inner horizontal padding | 48px | 20px |
| Lead width | 85% / max 520px | 100% |
| Subsection layout | label \| body | label stacked above body |
| Title size | 38px | 32px |

## Color tokens

| Token | Default | Usage |
|-------|---------|-------|
| Background | `#FAF9F5` | Set via JSON `background` |
| Text primary | `#1a1a1a` | Title, lead, labels, item lead |
| Text secondary | `rgba(0,0,0,0.6)` | Body, bullets |
| Divider | `#D8D2C8` | Intro rule, quote rules |
| Section underline | `#BDB5AA` | Roman section title underline |

## Typography

| Element | Font | Size |
|---------|------|------|
| Title | Georgia | 38px / 32px mobile |
| Lead | System sans | 14px |
| Section heading | Georgia italic | 16px |
| Subsection label | System sans | 14px |
| Body / bullets | System sans | 14px |
| Header meta | System sans | 11px uppercase |

Header label is always **SYNTHESIS** — fixed, not in JSON.

## Paper palette

Set JSON `background` to any of:

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

## Not supported (omit from JSON)

`render.py` v1 does not render these — do not scaffold:

- Metrics strip
- Data comparison tables
- Charts, images, badges
- Footer bar
- Fragment / body-only mode

Use bullets and prose for comparisons. Use pull quote for one standout sentence.

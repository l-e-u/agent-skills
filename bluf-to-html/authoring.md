# Report Authoring Logic

Content and structure decisions for the report JSON. Layout, CSS, and HTML assembly are handled by [scripts/render.py](scripts/render.py) — see [integration.md](integration.md) for the JSON schema.

Source: Report-Kit authoring principles (BLUF, real-data-only components).

---

## 1. Division of labor

| Agent writes (JSON) | Fixed by `render.py` |
|---------------------|----------------------|
| Whether input qualifies as a report | SYNTHESIS header, date, fonts, colors |
| Title, BLUF lead, section titles | Table layout, intro rule, quote rules |
| Item labels, body text, bullets | Roman numerals (auto from section order) |
| Which components to include (quote, bullets) | 640px column, paper background, mobile CSS |
| Omitting empty/scaffold components | Email-safe bullet tables, section headings |

**Input structure is not output structure.** Dividers (`────────`), paste formatting, and loose numbering are parsing hints. Read for **content and meaning**, then map to the JSON schema in [integration.md](integration.md).

---

## 2. When to use this format

Use the report email layout when the input is a **durable, prose-driven, multi-section document** meant to be read top-to-bottom:

- Briefs, memos, explainers, guides, analyses, recommendations
- Bible/vault answers with multiple principles or sections
- Project updates, profiles, strategy notes

Do **not** force this layout for:

- One-sentence answers or quick lookups
- Slide decks, dashboards, interactive tools
- Content meant to be pasted as plain text elsewhere

---

## 3. Content discipline (CSS-independent)

These rules determine quality regardless of styling:

### BLUF everywhere

- **Report lead:** 1–3 sentences stating the bottom line up front. Often opens with the conclusion ("The short answer: …", "Bottom line: …"). Set as JSON `lead` — rendered in primary color.
- **Every item:** Set JSON `lead` (conclusion) + `rest` (support) or use `bullets` for parallel points. Do not prefix section titles with Roman numerals; `render.py` adds I, II, III…

### Real data only

- **Pull quote:** Only a sentence that exists in the source and stands alone — set JSON `quote` or omit.
- **Bullets:** Only real parallel points from source — set JSON `bullets[]` or use prose.
- **Metrics, data tables, charts, images, badges:** Not supported by `render.py` — omit entirely.

### Terse bullets

- One sentence per bullet.
- If a bullet needs two sentences → split into two bullets or convert to prose.
- Prefer bullets when source lists parallel points, consequences, or examples.

### Claim-making section titles

- Section headings **assert** something: "Why the split works", "Principles to Reason On".
- Avoid pure labels: "Comparison", "Background", "Overview".
- One entry per major theme in JSON `sections[]` — `render.py` numbers them I, II, III…

### Two-pager density

- High signal, zero padding in **wording** (not CSS).
- Cut throat-clearing ("To understand X, we first…"), narration ("This shows that…"), filler adjectives.
- Direct, concrete — numbers and scripture refs over vague qualifiers.

### Vary the form

Mix within a report:

| Form | JSON | Use when |
|------|------|----------|
| Short prose | `lead` + `rest` | Single coherent point |
| Bullets | `bullets[]` | Parallel facts, examples, consequences |
| Pull quote | `quote` | One standout contrast sentence between sections |

Don't force every subsection into the same shape.

---

## 4. Document skeleton (JSON mapping)

Map content to this hierarchy, then write [integration.md §4 JSON schema](integration.md):

```
Report JSON
├── title, date, background
├── lead (BLUF paragraph)
├── sections[] — one object per major theme
│   ├── title (claim-making; no "I." prefix)
│   └── items[] — subsection rows
│       ├── label (3–6 words; left column)
│       ├── lead + rest (or body)
│       └── bullets[] (optional)
├── quote (optional)
└── quote_after_section (default 2)
```

`render.py` produces: SYNTHESIS header, h1, lead, intro rule, Roman headings, label/body rows, pull quote, mobile CSS. Details: [reference.md](reference.md).

---

## 5. Decision tree: building from raw input

```
1. Extract title
   └─ First line or explicit question/topic

2. Extract BLUF lead
   └─ Summary before first thematic section
   └─ Rewrite as 1–3 tight sentences if source is verbose

3. Identify major sections
   └─ From headings OR infer from topic shifts
   └─ Rename to claim-making titles → JSON `sections[].title`
   └─ **Required:** ≥1 section; each must have ≥1 item

4. For each section → identify items
   └─ From explicit "1." labels OR split dense paragraphs by theme
   └─ Write short labels → JSON `items[].label` (3–6 words)

5. For each item body:
   ├─ Conclusion → JSON `lead`
   ├─ Supporting prose → JSON `rest`
   ├─ 2+ parallel points → JSON `bullets[]`
   └─ Single point → `lead` + `rest` only (no bullets key)

6. Pull quote?
   └─ Find one contrast/standalone sentence
   └─ Set JSON `quote`; `quote_after_section: 2` (or section index that sets up contrast)
   └─ If none qualifies → omit `quote` key entirely

7. Strip scaffolding
   └─ Remove (source: …) unless user wants citations
   └─ Remove input dividers, duplicate headings, throat-clearing

8. Write JSON → run `render.py` → run `validate.py`
```

---

## 6. Subsection label inference

When input lacks `1.` labels, derive from content:

| Content signal | Label pattern |
|----------------|---------------|
| Single scripture/law mention | 1. The one direct mention |
| Historical/cultural context | 2. Why the law was given |
| Application to audience today | 3. What it means for Christians |
| Modesty principle | 1. Modesty |
| Body ownership / motive | 2. Your body belongs to God |
| Planning / permanence | 3. Forethought |
| Permitted alternative | 1. [X] is not forbidden |
| Prohibited contrast | 2. [X] are permanent alteration |
| Existing condition | 1. A matter of conscience |
| Final recommendation | The wiser course |

Labels are **scannable handles**, not full sentences.

---

## 7. Pull quote selection

Prefer a sentence that:

1. Contrasts two things ("…opposite direction from jewelry")
2. States a non-obvious principle in one breath
3. Could stand alone without surrounding context

Do **not** invent quotes. Pull from source or paraphrase tightly only when the source clearly implies one sentence.

Placement: between sections II and III in principle-driven reports, or after the section that establishes the contrast.

---

## 8. Canonical example: tattoos report (JSON)

Abbreviated — see [integration.md](integration.md) for full schema:

```json
{
  "title": "Can a Christian Get Tattoos?",
  "date": "July 10, 2026",
  "background": "#FAF9F5",
  "lead": "The short answer: not under a legal ban, but strongly advised against. Christians are not under the Mosaic Law, but the principle behind Leviticus 19:28 still counsels against permanently marking the body.",
  "quote": "Scripture does not forbid jewelry; tattoos are permanent skin alteration — the counsel runs in the opposite direction.",
  "quote_after_section": 2,
  "sections": [
    {
      "title": "What Scripture Says About Tattoo Markings",
      "items": [
        {
          "label": "The one direct mention",
          "lead": "Leviticus 19:28 is the only direct Bible mention of tattoo markings.",
          "rest": "Israel was forbidden customs linked to false worship and self-disfigurement.",
          "bullets": [
            "Leviticus 19:28 — \"You must not make tattoo markings on yourselves.\"",
            "Egyptians tattooed deity names on their bodies — Israel was to stand apart."
          ]
        }
      ]
    },
    {
      "title": "Principles That Counsel Against Tattoos",
      "items": [
        {
          "label": "Modesty",
          "lead": "Christians adorn themselves with modesty.",
          "rest": "Tattoos can draw undue attention to oneself."
        },
        {
          "label": "Your body belongs to God",
          "lead": "Present your body a sacrifice to God.",
          "rest": "Motives tied to fad or group identity deserve honest examination."
        },
        {
          "label": "Forethought",
          "lead": "Tattoo decisions are often hasty; the mark is long-lasting.",
          "bullets": [
            "Can affect employment and relationships.",
            "Regret is common; removal is costly and incomplete."
          ]
        }
      ]
    },
    {
      "title": "How Tattoos Differ From Jewelry",
      "items": [
        {
          "label": "Permanent vs adornment",
          "lead": "Scripture does not forbid modest jewelry.",
          "rest": "Tattoos permanently alter the skin — the one form of marking Scripture addresses in prohibition."
        }
      ]
    },
    {
      "title": "The Wiser Course",
      "items": [
        {
          "label": "Bottom line",
          "lead": "Getting a tattoo is not advisable for someone living by Bible principles.",
          "rest": "Use your power of reason and decide against permanently marking the skin."
        }
      ]
    }
  ]
}
```

**Reorganization allowed:** Move examples under section I as bullets; do not transcribe paste layout literally.

---

## 9. Component omission checklist

Before writing JSON, confirm:

- [ ] No pull quote unless source supports it (omit `quote` key)
- [ ] No footer unless user requests
- [ ] Every `sections[]` entry has ≥1 `items[]` with substantive `lead` or `body`
- [ ] Section titles are claim-making — not folded into `items[].label`
- [ ] Every item `lead` states conclusion, not setup
- [ ] Parallel points use `bullets[]`, not long comma chains in `rest`

---

## 10. Pipeline

1. [authoring.md](authoring.md) — content decisions → JSON
2. [integration.md](integration.md) — JSON schema + manifest
3. [scripts/render.py](scripts/render.py) — JSON → HTML
4. [reference.md](reference.md) — output tokens (what render produces)
5. [scripts/validate.py](scripts/validate.py) — pre-send check

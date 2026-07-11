# Report Authoring Logic (Phase 2)

Layout and structure decisions for the email formatter. Visual styling is fixed in [reference.md](reference.md) — this file governs **what** to emit and **how** to reshape content.

Source: Report-Kit authoring principles (BLUF, real-data-only components).

---

## 1. Division of labor (email context)

| Agent decides | Fixed by templates |
|---------------|-------------------|
| Whether input qualifies as a report | Inline CSS, fonts, colors, spacing |
| Title, BLUF lead, section structure | Table layout, intro rule, quote rules |
| Which components to include (items, bullets, table, callout) | 640px column, paper background |
| Label text, item count, bullet splits | Email-safe bullet tables |
| Omitting empty/scaffold components | No footer bar (unless requested) |

**Input structure is not output structure.** Dividers (`────────`), paste formatting, and loose numbering are parsing hints. The agent reads for **content and meaning**, then maps to the report schema.

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

- **Report lead:** 1–3 sentences stating the bottom line up front. Often opens with the conclusion ("The short answer: …", "Bottom line: …"). Render the **entire** lead in primary color (`#1a1a1a`) — no first-sentence `<span>` wrapper.
- **Every item:** First sentence of each subsection body states the finding/conclusion; supporting detail follows (as prose or bullets).

### Real data only

- **Metrics row:** Only if 2–4 real numbers exist (costs, counts, percentages). Otherwise omit entirely.
- **Data table:** Only for comparative data (pricing, options, tradeoffs). Otherwise use prose or bullets.
- **Pull quote:** Only a sentence that exists in the source and stands alone — typically a contrast or key principle.
- **Charts, Slack quotes, images, badges:** Omit unless source provides real content. Never scaffold empty components.

### Terse bullets

- One sentence per bullet.
- If a bullet needs two sentences → split into two bullets or convert to prose.
- Prefer bullets when source lists parallel points, consequences, or examples.

### Claim-making section titles

- Section headings **assert** something: "Why the split works", "Principles to Reason On".
- Avoid pure labels: "Comparison", "Background", "Overview".
- Number with Roman numerals (I, II, III…) for scannability.

### Two-pager density

- High signal, zero padding in **wording** (not CSS).
- Cut throat-clearing ("To understand X, we first…"), narration ("This shows that…"), filler adjectives.
- Direct, concrete — numbers and scripture refs over vague qualifiers.

### Vary the form

Mix within a report:

| Form | Use when |
|------|----------|
| Short prose | Single coherent point |
| Bullets | Parallel facts, examples, consequences |
| Table | Side-by-side comparison, pricing, options |
| Pull quote | One standout contrast sentence between major sections |

Don't force every subsection into the same shape.

---

## 4. Document skeleton (semantic mapping)

Map content to this hierarchy. Email HTML uses tables; semantics stay the same.

```
Report
├── Header (SYNTHESIS + date)
├── Title (h1)
├── Lead (BLUF paragraph, ~85% width)
├── Intro rule (horizontal line)
├── [optional] Metrics (2–4 numbers only)
├── Body
│   ├── Section I (Roman heading + items)
│   ├── Section II
│   ├── [optional] Pull quote (between contrast sections)
│   ├── Section III …
│   └── Section N
└── (no footer unless requested)
```

### Host class → email role

| Report-Kit class | Email role |
|------------------|------------|
| `report-header` | Top meta row — fixed **SYNTHESIS** label (left) + date (right); not configurable |
| `report-headline` | h1 title |
| `report-intro` | Lead paragraph |
| `report-rule` | Intro rule (and quote flanking rules) |
| `report-section` + `section-heading` | Roman section title |
| `report-item` | Subsection table row |
| `item-label` / `item-title` | Left column label |
| `item-body` | Right column body + bullets |
| `item-badge` | Omit in email unless user provides status text |
| `metrics-strip` | Omit unless real metrics |
| `data-table` | HTML table in item-body (email-safe) |
| `report-quote-break` | Pull quote with flanking rules |
| `slack-quote` | Omit in email phase 2 (no real Slack data) |

---

## 5. Decision tree: building from raw input

```
1. Extract title
   └─ First line or explicit question/topic

2. Extract BLUF lead
   └─ Summary before first thematic section
   └─ Rewrite as 1–3 tight sentences if source is verbose

3. Identify major sections (Roman I, II, III…)
   └─ From headings OR infer from topic shifts
   └─ Rename to claim-making titles if source only labels
   └─ **Required:** emit section block template (table + `.section-heading`) before each section's items — never skip Roman numerals

4. For each section → identify items (numbered subsections)
   └─ From explicit "1." labels OR split dense paragraphs by theme
   └─ Write short labels for left column (3–6 words)

5. For each item body:
   ├─ Lead sentence = conclusion (dark emphasis)
   ├─ Has 2+ parallel points? → bullet table
   ├─ Comparative grid in source? → data table
   └─ Single point? → prose only

6. Pull quote?
   └─ Find one contrast/standalone sentence (often jewelry vs tattoos)
   └─ Place after section II or the section that sets up the contrast
   └─ If none qualifies → omit callout and its rules

7. Metrics?
   └─ Count real headline numbers in source
   └─ 2–4 exist → optional metrics block after lead (before intro rule)
   └─ Else → skip

8. Strip scaffolding
   └─ Remove (source: …) unless user wants citations
   └─ Remove input dividers, duplicate headings, throat-clearing
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

## 8. Canonical example: tattoos report

How source maps to structure (vault/Bible-style content):

| Block | Content decision |
|-------|------------------|
| Title | Question as headline |
| Lead | "The short answer: not under a legal ban, but strongly advised against" — BLUF in 3 sentences |
| I | Scripture — 3 items: direct mention, why law given, Christian application |
| II | Principles — 3 items: modesty, body belongs to God, forethought; bullets for consequences under forethought |
| Callout | Jewelry contrast sentence (between II and III) |
| III | Jewelry comparison — 2 items |
| IV | Existing tattoos — 1 item; bullets for new vs existing |
| V | Bottom line — 1 item "The wiser course" |

**Reorganization allowed:** Move idolatry/Egyptian examples under section I item 1 as bullets; forethought consequences under item 3. Restructure for clarity — do not transcribe paste layout.

---

## 9. Component omission checklist

Before emitting, confirm:

- [ ] No metrics without real numbers
- [ ] No table without comparative data
- [ ] No pull quote unless source supports it
- [ ] No chart, Slack embed, image, badge (email phase 2)
- [ ] No footer unless user requests
- [ ] Every section has ≥1 item with substantive body
- [ ] Every section has a Roman heading row (`I.`, `II.`, …) via `.section-heading` — not folded into `item-label`
- [ ] Every item leads with conclusion, not setup

---

## 10. Email constraints

Templates: [reference.md](reference.md). Delivery, parity, ESP handoff: [integration.md](integration.md).

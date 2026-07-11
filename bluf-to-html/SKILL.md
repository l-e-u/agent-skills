---
name: bluf-to-html
description: Transforms raw BLUF report text into styled standalone HTML plus a JSON manifest. Email-client-safe markup, but output works as a preview file, archive, or ESP payload. Invoke with data and options YAML; outputs .html and .manifest.json. Use when formatting multi-section reports to HTML.
---

# BLUF to HTML

```
Raw text + YAML options
  → authoring.md (content → JSON)
  → render.py (JSON → HTML)
  → validate.py (gate)
  → manifest.json + .html
```

| File | Role |
|------|------|
| [authoring.md](authoring.md) | Content structure, BLUF → JSON |
| [integration.md](integration.md) | JSON schema, manifest, ESP handoff |
| [reference.md](reference.md) | What render output looks like (read-only) |
| [scripts/render.py](scripts/render.py) | JSON → HTML (**required**) |
| [scripts/validate.py](scripts/validate.py) | Pre-send check |

## Invoke

```yaml
---
title: "Report Title"
date: "Friday, July 10 2026"
background: "#FAF9F5"
subject: "Report: Report Title"
output_dir: "output"
output_name: "report"
---

[paste report content]
```

## Agent workflow

See [integration.md §4](integration.md) for JSON schema and manifest. Summary:

1. Parse options + content
2. Author JSON ([authoring.md](authoring.md)) → `{output_dir}/{output_name}.json`
3. `python scripts/render.py …json …html`
4. Write manifest → `validate.py` → fix JSON and re-render if needed

**Do not hand-assemble HTML.**

## Core rules

1. Content over input structure — pasted dividers are parse hints only
2. BLUF everywhere; real data only for quotes and bullets
3. Layout lives in `render.py` — agent writes JSON only

## Handoff

```typescript
const m = JSON.parse(readFileSync("output/report.manifest.json", "utf8"));
await resend.emails.send({ subject: m.subject, html: m.html, ... });
```

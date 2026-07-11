---
name: bluf-to-html
description: Transforms raw BLUF report text into styled standalone HTML plus a JSON manifest. Email-client-safe markup, but output works as a preview file, archive, or ESP payload. Invoke with data and options YAML; outputs .html and .manifest.json. Use when formatting multi-section reports to HTML.
---

# BLUF to HTML

**Author content → write report JSON → `render.py` → validate → HTML + manifest.**

| File | Role |
|------|------|
| [authoring.md](authoring.md) | Content structure, BLUF, what to include |
| [reference.md](reference.md) | Layout spec (implemented by `render.py`) |
| [integration.md](integration.md) | I/O contract, JSON schema, manifest, ESP wrappers |
| [scripts/render.py](scripts/render.py) | JSON → HTML (required) |
| [scripts/validate.py](scripts/validate.py) | Pre-send HTML check |

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

```
- [ ] Parse options + content
- [ ] Author structured report (authoring.md) → write {output_name}.json
- [ ] Run: python scripts/render.py {output_name}.json {output_name}.html
- [ ] Write {output_name}.manifest.json (integration.md)
- [ ] Run scripts/validate.py on the HTML — fix JSON and re-render if errors
- [ ] Return paths + fenced HTML (do NOT send unless asked)
```

**Do not hand-assemble HTML.** Use `render.py` for all layout.

## Core rules

1. Content over input structure — pasted dividers are parse hints only
2. BLUF everywhere; real data only for metrics/tables/quotes
3. No JavaScript — skill formats; project sends ([integration.md](integration.md))

## Handoff

```typescript
const m = JSON.parse(readFileSync("output/report.manifest.json", "utf8"));
await resend.emails.send({ subject: m.subject, html: m.html, ... });
```

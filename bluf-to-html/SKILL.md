---
name: bluf-to-html
description: Transforms raw BLUF report text into styled standalone HTML plus a JSON manifest. Email-client-safe markup, but output works as a preview file, archive, or ESP payload. Invoke with data and options YAML; outputs .html and .manifest.json. Use when formatting multi-section reports to HTML.
---

# BLUF to HTML

**Invoke with data → get HTML + manifest → preview, store, or send.**

| File | Role |
|------|------|
| [authoring.md](authoring.md) | Content structure, BLUF, what to include |
| [reference.md](reference.md) | HTML/CSS templates |
| [integration.md](integration.md) | I/O contract, manifest, validation, ESP wrappers |
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

## Output

1. `{output_dir}/{output_name}.html` — standalone file, browser preview, or ESP `html` field
2. `{output_dir}/{output_name}.manifest.json` — `subject`, `html`, metadata
3. Run validation from this skill's directory: `python scripts/validate.py {path}`

Details: [integration.md](integration.md).

## Agent workflow

```
- [ ] Parse options + content
- [ ] Author (authoring.md) → assemble (reference.md)
- [ ] Write .html + .manifest.json in the project's output_dir
- [ ] Run scripts/validate.py from this skill's install directory — fix errors
- [ ] Return paths + fenced HTML (do NOT send unless asked)
```

## Core rules

1. Content over input structure — pasted dividers are parse hints only
2. BLUF everywhere; real data only for metrics/tables/quotes
3. No JavaScript — skill formats; project sends ([integration.md](integration.md))

## Handoff

```typescript
const m = JSON.parse(readFileSync("output/report.manifest.json", "utf8"));
await resend.emails.send({ subject: m.subject, html: m.html, ... });
```

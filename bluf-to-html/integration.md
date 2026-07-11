# Integration Contract (Phase 4)

Universal use: **invoke skill with data → get HTML (+ optional manifest) → thin wrapper sends via Resend, nodemailer, or any ESP.**

The skill owns **formatting**. Your project owns **transport**.

---

## 1. Recommended architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Raw report     │     │  bluf-to-html    │     │  Your project   │
│  data + options │ ──► │  skill           │ ──► │  thin wrapper   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │                                    │
                              ▼                                    ▼
                        report.json → report.html            resend.emails.send
                        report.manifest.json               nodemailer.sendMail
                        (optional)                         { html: manifest.html }
```

**Why this split works**

- One skill works in any repo — no Resend/nodemailer dependency inside the skill
- ESP APIs all accept an `html` string; the full `<!DOCTYPE html>…` document is valid
- Preview (browser), file archive, and send pipeline share the same artifact
- Environment-specific wrappers stay ~5–20 lines

**Do not** embed send logic in the skill. **Do** document the handoff contract below.

---

## 2. Input contract

Invoke the skill with **options** (optional) + **content** (required).

### Options block (YAML frontmatter)

Place at the top of the user message or in a fenced block:

```yaml
---
title: "Am I Allowed to Have Tattoos?"      # optional if first line of content is title
date: "Friday, July 10 2026"               # default: today
background: "#FAF9F5"                      # PAPERS palette — reference.md
subject: "Report: Am I Allowed to Have Tattoos?"  # email subject; default: "Report: {title}"
preheader: "The short answer and Bible principles on tattoos."  # inbox preview text
output_dir: "output"                       # where to save artifacts
output_name: "report"                      # basename for files
save_files: true                           # write report.html + manifest
---
```

All keys optional except content body.

### Content body (required)

Freeform text: title, lead, sections, bullets. Parsing rules in [authoring.md](authoring.md). Input dividers (`────────`) are **not** rendered.

### Minimal invoke examples

**Full options + content:**

```
/bluf-to-html

---
title: Weekly Brief
date: Friday, July 10 2026
background: "#E3EDDF"
---

[paste report text]
```

**Content only** (agent infers title from first line, defaults for rest):

```
/bluf-to-html

Am I Allowed to Have Tattoos?

The Bible does not give Christians a simple yes-or-no rule…
```

---

## 3. Output contract

The skill **must** produce these artifacts when `save_files: true` (default in a workspace):

| File | Purpose |
|------|---------|
| `{output_dir}/{output_name}.json` | Structured report — input to `render.py` |
| `{output_dir}/{output_name}.html` | Full HTML document — preview + ESP body |
| `{output_dir}/{output_name}.manifest.json` | Machine-readable handoff for wrappers |

### Manifest schema

```json
{
  "version": 1,
  "title": "Am I Allowed to Have Tattoos?",
  "subject": "Report: Am I Allowed to Have Tattoos?",
  "preheader": "The short answer and Bible principles on tattoos.",
  "date": "FRIDAY, JULY 10 2026",
  "background": "#FAF9F5",
  "html": "<!DOCTYPE html>…",
  "htmlPath": "output/report.html"
}
```

- **`html`** — full document string (duplicate of file contents for in-memory pipelines)
- **`subject`** — pass to ESP `subject` field
- **`preheader`** — optional; wrapper may inject as hidden preview text (see §5)

Also return the HTML in a fenced code block in chat for copy-paste.

### Validation

After generating HTML, run `scripts/validate.py` **from this skill's install directory** (wherever `SKILL.md` lives — global or project install):

```bash
python scripts/validate.py output/report.html
```

The HTML path is relative to the **project workspace**, not the skill directory. Only the validator script path is skill-relative.

Fix errors before send. Use `--strict` to treat warnings as errors.

---

## 4. Skill execution workflow (agent)

```
1. Parse options YAML (if present) + content body
2. Author structured report (authoring.md) → write {output_dir}/{output_name}.json
3. Run: python scripts/render.py {output_dir}/{output_name}.json {output_dir}/{output_name}.html
4. Write {output_name}.manifest.json (schema below)
5. Run scripts/validate.py on the HTML — fix JSON and re-render if errors
6. Return: manifest summary + path to HTML + fenced HTML block
```

**Do not hand-assemble HTML.** `render.py` implements [reference.md](reference.md).

### Report JSON schema (input to `render.py`)

```json
{
  "title": "Where Is Heaven?",
  "date": "July 10, 2026",
  "background": "#FAF9F5",
  "lead": "BLUF paragraph — full primary color in output.",
  "quote": "Optional pull quote (omit key if none).",
  "quote_after_section": 2,
  "sections": [
    {
      "title": "Heaven Is God's Dwelling Place",
      "items": [
        {
          "label": "Jehovah's throne",
          "lead": "First sentence — dark in output.",
          "rest": "Supporting prose in secondary color.",
          "bullets": ["Parallel point one.", "Parallel point two."]
        }
      ]
    }
  ]
}
```

- `items[].body` may substitute for `lead`/`rest` (first sentence auto-split).
- Omit empty optional fields (`quote`, `bullets`).

The agent does **not** call Resend/nodemailer unless the user separately asks to send.

---

## 5. Unsupported features

`render.py` v1 handles: title, lead, sections, items, bullets, pull quote, background, mobile CSS.

**Do not emit** (not in renderer):

| Feature | Instead |
|---------|---------|
| Metrics strip | Omit, or mention numbers in prose |
| Data comparison tables | Use `bullets[]` |
| Charts / images | Omit or link in prose |
| Badges, footer, fragment mode | Omit |

If content needs JS, canvas, or `@font-face` → out of scope for this skill.

---

## 6. Client compatibility

**Safe:** table layout, inline CSS, `<style>` block with `@media (max-width: 500px)` for mobile stack/padding, `role="presentation"`, Georgia/system fonts, `&bull;` bullets, `border-top` rules, `https://` images, background on body **and** inner table (Gmail).

**Avoid:** flex/grid in inline CSS, `@font-face`, external CSS, `<script>`, `::before` bullets, base64 images, CSS variables.

**Outlook:** `mso-line-height-rule:exactly` on rule cells; two-column items as nested tables.

Run `scripts/validate.py` before send.

---

## 7. Thin wrapper patterns

### Resend (Node.js)

```typescript
import { readFileSync } from "fs";
import { Resend } from "resend";

const manifest = JSON.parse(readFileSync("output/report.manifest.json", "utf8"));
const resend = new Resend(process.env.RESEND_API_KEY);

const { data, error } = await resend.emails.send({
  from: "Reports <reports@yourdomain.com>",
  to: ["user@example.com"],
  subject: manifest.subject,
  html: manifest.html,
});
if (error) throw new Error(error.message);
```

Use Resend skill for idempotency keys, domain setup, and production gotchas.

### nodemailer (Node.js)

```typescript
import { readFileSync } from "fs";
import nodemailer from "nodemailer";

const manifest = JSON.parse(readFileSync("output/report.manifest.json", "utf8"));

await transporter.sendMail({
  from: '"Reports" <reports@yourdomain.com>',
  to: "user@example.com",
  subject: manifest.subject,
  html: manifest.html,
});
```

### Python (any SMTP/API)

```python
import json
from pathlib import Path

manifest = json.loads(Path("output/report.manifest.json").read_text())
# pass manifest["html"] to your ESP client
```

### Preheader injection (optional)

Many wrappers prepend hidden preview text. Not part of the skill HTML by default — wrapper adds:

```html
<div style="display:none;max-height:0;overflow:hidden;mso-hide:all;">
  {{preheader}}
</div>
```

Only if `manifest.preheader` is set.

---

## 8. Environment-specific thin skills (recommended)

Keep **bluf-to-html** universal. Add tiny project skills that chain:

| Project skill | Does |
|---------------|------|
| `bluf-to-html` | JSON → HTML + manifest via `render.py` |
| `send-report-resend` (your repo) | Read manifest → `resend.emails.send` |
| `send-report-smtp` (your repo) | Read manifest → nodemailer |

Example project skill (5 lines of intent):

```markdown
---
name: send-report-resend
description: Sends bluf-to-html output via Resend. Use after generating a report manifest.
---
1. Require `output/report.manifest.json` from bluf-to-html
2. Load manifest; send with Resend using manifest.subject and manifest.html
3. Use idempotency key derived from manifest.title + date
```

This keeps the formatter portable; transport stays where `RESEND_API_KEY` lives.

---

## 9. Fragment mode (not implemented)

Body-only HTML for ESP wrapper templates is **not supported** in v1. `render.py` always emits a full document. Default works everywhere without a wrapper shell.

---

## 10. CI / automation hook

If the skill is installed globally, resolve its path first (e.g. `~/.agents/skills/bluf-to-html/`). Then:

```bash
python /path/to/bluf-to-html/scripts/validate.py output/*.html --strict
```

Pair with a generate step in your pipeline: raw markdown/text in → HTML artifact out → validate → deploy or send job reads manifest.

---

## 11. File map

| File | Role |
|------|------|
| SKILL.md | Entry point, pipeline overview |
| authoring.md | Content decisions → JSON |
| integration.md | JSON schema, manifest, ESP wrappers |
| reference.md | Output tokens (read-only; what render produces) |
| scripts/render.py | JSON → HTML (**required**) |
| scripts/validate.py | Pre-send HTML check |

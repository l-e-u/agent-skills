# Integration Contract (Phase 4)

Universal use: **invoke skill with data → get HTML (+ optional manifest) → thin wrapper sends via Resend, nodemailer, or any ESP.**

The skill owns **formatting**. Your project owns **transport**.

---

## 1. Recommended architecture

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│  Raw report     │     │  email-report    │     │  Your project   │
│  data + options │ ──► │  skill           │ ──► │  thin wrapper   │
└─────────────────┘     └──────────────────┘     └─────────────────┘
                              │                                    │
                              ▼                                    ▼
                        report.html                          resend.emails.send
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
report_label: "REPORT"
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
/email-report

---
title: Weekly Brief
date: Friday, July 10 2026
background: "#E3EDDF"
---

[paste report text]
```

**Content only** (agent infers title from first line, defaults for rest):

```
/email-report

Am I Allowed to Have Tattoos?

The Bible does not give Christians a simple yes-or-no rule…
```

---

## 3. Output contract

The skill **must** produce these artifacts when `save_files: true` (default in a workspace):

| File | Purpose |
|------|---------|
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
2. Run authoring workflow (authoring.md)
3. Assemble HTML (reference.md; optional metrics/table from reference § Extended)
4. Write {output_name}.html + {output_name}.manifest.json to the project's output_dir
5. Locate this skill's directory; run scripts/validate.py against the HTML path — fix and regenerate if errors
6. Return: manifest summary + path to HTML + fenced HTML block
```

The agent does **not** call Resend/nodemailer unless the user separately asks to send.

---

## 5. Report-Kit → email parity

No JS in email. Hard-code or omit runtime host features:

| Host feature | Email action |
|--------------|--------------|
| Color/font pickers | Pick `background` + fixed Georgia/system fonts at build |
| Auto date | Hard-code in header |
| Chart.js | Hosted `<img>` or omit + link |
| Metrics strip | Table template (reference.md) if 2–4 real numbers |
| Slack quote, settings, grain, ink filters | Omit |
| Badges | Static label only, no rotation |

If it needs JS, canvas, localStorage, or `@font-face` → do not emit.

---

## 6. Client compatibility

**Safe:** table layout, inline CSS, `role="presentation"`, Georgia/system fonts, `&bull;` bullets, `border-top` rules, `https://` images, background on body **and** inner table (Gmail).

**Avoid:** flex/grid, `@font-face`, external CSS, `<script>`, `::before` bullets, base64 images, CSS variables.

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

Keep **email-report** universal. Add tiny project skills that chain:

| Project skill | Does |
|---------------|------|
| `email-report` | Data → HTML + manifest |
| `send-report-resend` (your repo) | Read manifest → `resend.emails.send` |
| `send-report-smtp` (your repo) | Read manifest → nodemailer |

Example project skill (5 lines of intent):

```markdown
---
name: send-report-resend
description: Sends email-report output via Resend. Use after generating a report manifest.
---
1. Require `output/report.manifest.json` from email-report
2. Load manifest; send with Resend using manifest.subject and manifest.html
3. Use idempotency key derived from manifest.title + date
```

This keeps the formatter portable; transport stays where `RESEND_API_KEY` lives.

---

## 9. Alternative: body-only fragment

Some teams prefer ESP templates with shared header/footer. The skill can optionally emit **fragment mode**:

```yaml
output_mode: fragment   # default: document
```

Fragment = inner content only (everything inside the 640px table). Wrappers wrap in their own shell:

```html
{{company_header}}
{{fragment}}
{{company_footer}}
```

Default remains **full document** — works everywhere without a wrapper template.

---

## 10. CI / automation hook

If the skill is installed globally, resolve its path first (e.g. `~/.cursor/skills/email-report/`). Then:

```bash
python /path/to/email-report/scripts/validate.py output/*.html --strict
```

Pair with a generate step in your pipeline: raw markdown/text in → HTML artifact out → validate → deploy or send job reads manifest.

---

## 11. File map

| File | Role |
|------|------|
| SKILL.md | Entry point, invoke/output contract |
| authoring.md | Content structure, BLUF, component decisions |
| reference.md | HTML/CSS templates |
| integration.md | Manifest, validation, ESP wrappers, client rules |
| scripts/validate.py | Pre-send HTML check |

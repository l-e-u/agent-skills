# Agent Skills

Personal agent skills for Cursor, Claude Code, Codex, and 40+ other tools via [skills.sh](https://skills.sh).

## Install

```bash
npx skills add l-e-u/agent-skills@bluf-to-html -g -y
```

| Flag | Effect |
|------|--------|
| `-g` | Install globally (all repos on your machine) |
| `-y` | Skip confirmation prompts |
| `-a cursor -a claude-code` | Target specific agents only |

Update later: `npx skills update bluf-to-html -g -y`

> **Formerly `email-report`.** Remove the old install: `npx skills remove email-report -g -y`

## Skills

### bluf-to-html

Turns raw BLUF report text into structured JSON, then `render.py` produces styled standalone HTML plus a manifest. Email-client-safe markup; works as preview, archive, or ESP payload.

```yaml
---
title: "Weekly Brief"
date: "Friday, July 10 2026"
background: "#E3EDDF"
output_dir: "output"
output_name: "weekly-brief"
---

[paste report text]
```

Docs: [bluf-to-html/SKILL.md](bluf-to-html/SKILL.md) · [integration.md](bluf-to-html/integration.md)

Validate before send:

```bash
python ~/.agents/skills/bluf-to-html/scripts/validate.py output/weekly-brief.html
```

## Structure

```text
agent-skills/
├── bluf-to-html/        — BLUF report → HTML + manifest
│   ├── SKILL.md
│   ├── authoring.md
│   ├── reference.md
│   ├── integration.md
│   └── scripts/
│       ├── render.py
│       └── validate.py
└── README.md
```

Add future skills as sibling folders under this repo.

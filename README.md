# Agent Skills

Personal agent skills for Cursor, Claude Code, Codex, and 40+ other tools via [skills.sh](https://skills.sh).

## Install

```bash
npx skills add l-e-u/agent-skills@email-report -g -y
```

| Flag | Effect |
|------|--------|
| `-g` | Install globally (all repos on your machine) |
| `-y` | Skip confirmation prompts |
| `-a cursor -a claude-code` | Target specific agents only |

Update later: `npx skills update`

## Skills

### email-report

Turns raw report text into styled, email-client-safe HTML plus a JSON manifest for any ESP.

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

Docs: [email-report/SKILL.md](email-report/SKILL.md) · [integration.md](email-report/integration.md)

Validate before send:

```bash
python ~/.agents/skills/email-report/scripts/validate.py output/weekly-brief.html
```

## Structure

```text
agent-skills/
├── email-report/        — report → HTML email + manifest
│   ├── SKILL.md
│   ├── authoring.md
│   ├── reference.md
│   ├── integration.md
│   └── scripts/validate.py
└── README.md
```

Add future skills as sibling folders under this repo.

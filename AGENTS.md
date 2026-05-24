# Agent Notes

This is a portable skill pack for coding agents, not an application runtime.
Each `skills/<name>/SKILL.md` is the primary instruction entry point. Bundled
scripts and assets are implementation aids.

## Editing Guidelines

- Keep skill instructions agent-neutral. Mention specific agents only in adapter
  documentation under `docs/` or `agents/`.
- Do not duplicate workflow text across files. Core behavior lives in
  `SKILL.md`; install and adapter guidance in `README.md` / `docs/`.
- Keep each skill directory lean: `SKILL.md`, optional `scripts/`, optional
  `assets/`, optional `agents/`.
- Use deterministic Python or shell helpers for repeatable validation and
  publishing.
- When changing the hosting repo path, base URL, or visibility semantics, update
  `README.md`, the relevant `SKILL.md`, and publishing scripts together.

## Validation

Before committing, verify all changes:

```sh
# Python syntax check
python3 -m py_compile \
  skills/knowledge-to-slides/scripts/validate_deck.py \
  skills/publish-html-artifact/scripts/publish.py

# No whitespace or merge conflicts
git diff --check
```

Also inspect each modified `SKILL.md` to ensure frontmatter is valid YAML and
the workflow reads cleanly as operating instructions for any agent.

## Agent Entry Points

This repo provides auto-discovery for multiple agents:

| Agent | File | Purpose |
|-------|------|---------|
| Claude Code | `CLAUDE.md` (root) | Project overview and skill table |
| opencode | `opencode.json` (root) | Skill list for the built-in skill loader |
| Codex | `skills/*/agents/openai.yaml` | Per-skill adapter metadata |

For setup details, see `docs/agent-adapters.md`.

# Knowledge Publishing Skills

This is a portable skill pack for coding agents. It contains two independent
skills that each live in their own directory under `skills/`.

## Available Skills

| Skill | What it does | Entry point |
|-------|-------------|-------------|
| `knowledge-to-slides` | Create a polished self-contained HTML slide deck from engineering knowledge | `skills/knowledge-to-slides/SKILL.md` |
| `publish-html-artifact` | Publish a finished HTML artifact to a static knowledge site (commit, push, return URL) | `skills/publish-html-artifact/SKILL.md` |

## How To Use

1. Read the relevant `SKILL.md` — it contains the full workflow as direct
   operating instructions.
2. Each skill bundles helpers in `scripts/` (deterministic Python), optional
   `assets/` (templates), and `agents/` (adapter metadata).
3. Run validators before publishing. See `docs/agent-adapters.md` for
   agent-specific setup.

## Conventions

- Keep artifacts self-contained: inline HTML/CSS/SVG, no remote JS, no localhost.
- Run `scripts/validate_deck.py` on generated HTML decks.
- Default hosting repo is `/home/ubuntu/src/knowledge-pages` at `https://knowledge.11tech.xyz`.

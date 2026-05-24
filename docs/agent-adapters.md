# Agent Adapters

Each agent discovers and uses these skills differently. Below are setup
patterns for the major coding agents.

All patterns follow the same core principle: make the skills repository
available to the agent, then tell it to read the relevant `SKILL.md` file.

## Shared Pattern

The canonical instruction for any agent:

```
Read skills/knowledge-to-slides/SKILL.md and follow its workflow.
```

No agent-specific API is required — just file access and shell execution.

---

## Claude Code

**Auto-discovery**: `CLAUDE.md` at the repository root provides a project
overview and skill table. Claude Code reads this file automatically when
opening the repo.

**Invocation**: Refer to a skill by name in conversation:

```
Use the knowledge-to-slides skill to turn what we just learned into an HTML deck.
```

Claude Code will read the SKILL.md and follow the workflow. No symlinks or
install steps needed — just have the repo in the workspace.

**Multiple kills in sequence**:

```
Create a slide deck using knowledge-to-slides, then publish it with
publish-html-artifact.
```

---

## opencode

**Auto-discovery**: `opencode.json` at the repository root lists both skills.
opencode's built-in skill loader reads this file automatically.

**Invocation**: Load a skill using the skill tool:

```
Load the knowledge-to-slides skill and create an HTML slide deck.
```

Or reference the entry point directly:

```
Read skills/knowledge-to-slides/SKILL.md and follow the instructions.
```

The bundled scripts run under the opencode shell environment without
additional setup.

---

## Codex (OpenAI)

**Install**: Symlink each skill into the Codex skills directory:

```sh
mkdir -p ~/.codex/skills
ln -s "$(pwd)/skills/knowledge-to-slides" ~/.codex/skills/knowledge-to-slides
ln -s "$(pwd)/skills/publish-html-artifact" ~/.codex/skills/publish-html-artifact
```

**Invocation**: Use the `$skill-name` reference:

```
Use $knowledge-to-slides to turn what we just learned into a polished
self-contained HTML slide deck.
```

Each skill's `agents/openai.yaml` provides display name, brand color, and
invocation behavior.

---

## Cursor

**Setup**: Add the repository to the Cursor project workspace. Cursor reads
instructions from the repo context and follows markdown files on request.

**Invocation**:

```
Read skills/knowledge-to-slides/SKILL.md and create a slide deck from what we
just learned. Validate it with scripts/validate_deck.py.
```

No symlinks or config files required — just include the repo path in the
project.

---

## Windsurf / Cascade

**Setup**: Clone or mount the repository in the workspace. Cascade reads
instructions from files present in the workspace.

**Invocation**:

```
Use skills/knowledge-to-slides/SKILL.md to create an HTML deck, then use
skills/publish-html-artifact/SKILL.md to publish it.
```

---

## pi / pi-mono

**Setup**: Mount this repository in the pi workspace, or copy the desired
skill directory.

**Invocation**:

```
Read skills/knowledge-to-slides/SKILL.md and follow the steps to create a
slide deck. Then run scripts/validate_deck.py on the result.
```

The bundled scripts use only standard Python and shell tools, so pi can
execute them directly.

---

## GitHub Copilot / Copilot Chat

**Setup**: Add the repository as context in VS Code or the relevant editor.
Copilot Chat uses the workspace files as context.

**Invocation**:

```
@workspace Read skills/knowledge-to-slides/SKILL.md and create a slide deck
from this session.
```

---

## Generic Agents

For any other coding agent with file and shell access:

1. Make this repository available in the agent's workspace.
2. Instruct the agent to read `skills/<skill-name>/SKILL.md`.
3. Let the agent produce files and run bundled scripts for validation or
   publishing.
4. Use Git for commits and pushes when publishing is required.

No agent-specific API, runtime, or configuration is required. The skills are
plain Markdown operating instructions plus deterministic Python helpers.

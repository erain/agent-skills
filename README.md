# Knowledge Publishing Skills

Reusable skills for turning engineering work into rich HTML knowledge artifacts
and publishing them to a static hosting repository.

## Skills

- `knowledge-to-slides`: create a polished, self-contained HTML slide deck.
- `publish-html-artifact`: publish a finished HTML artifact to
  `erain/knowledge-pages`, commit it, push it, and return the deployed URL.

## Install Locally

Copy or symlink the skill folders into your Codex skills directory:

```sh
git clone https://github.com/erain/knowledge-publishing-skills
cd knowledge-publishing-skills
mkdir -p ~/.codex/skills
ln -s "$(pwd)/skills/knowledge-to-slides" ~/.codex/skills/knowledge-to-slides
ln -s "$(pwd)/skills/publish-html-artifact" ~/.codex/skills/publish-html-artifact
```

---
name: publish-html-artifact
description: Publish a completed static HTML page or slide deck into the erain/knowledge-pages hosting repository, supporting public and unlisted visibility, updating artifact metadata, running the site build, committing, pushing, and returning the final URL.
---

# Publish HTML Artifact

Use this skill after an HTML artifact has been created and validated.

## Inputs To Determine

- source HTML path
- title
- slug
- kind: `deck` or `page`
- visibility: `public` or `unlisted`
- summary
- tags
- target repo path, default `/home/ubuntu/src/knowledge-pages`
- base URL, default `https://knowledge.11tech.xyz`

## Workflow

1. Confirm the source file exists and is a complete HTML document.
2. Run any artifact-specific validator first, such as `knowledge-to-slides/scripts/validate_deck.py`.
3. Run `scripts/publish.py` from this skill with explicit args.
4. Inspect the diff in the hosting repo.
5. Commit and push the hosting repo changes.
6. Wait for deployment when possible.
7. Return the published URL and commit URL.

## Visibility Semantics

- `public`: copies to `content/public/decks/<slug>/index.html` or `content/public/pages/<slug>/index.html`, appears in the gallery.
- `unlisted`: copies to `content/unlisted/<slug-or-token>/index.html`, deploys under `/u/<slug-or-token>/`, does not appear in the gallery. This is not security; anyone with the URL can view it.

For private previews, use a future Vercel/Cloudflare integration instead of treating unlisted URLs as secrets.

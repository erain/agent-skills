---
name: knowledge-to-slides
description: Turn what was learned from a coding session, repository, PR, incident, experiment, or technical conversation into a polished self-contained HTML slide deck with rich visuals, SVG diagrams, responsive layout, keyboard navigation, and local validation before publishing.
---

# Knowledge To Slides

Create one complete HTML file that can be published as a static artifact.

## Workflow

1. Extract the story:
   - problem or question
   - constraints
   - system shape
   - key decisions
   - implementation details
   - sharp edges or failures
   - takeaways
2. Build a 6-10 slide narrative. Prefer fewer dense slides over many shallow ones.
3. Use `assets/deck-template.html` as the structural baseline when useful.
4. Make visuals directly in HTML/CSS/SVG. Avoid external CDNs and localhost assets.
5. Save the deck as `index.html`.
6. Run `scripts/validate_deck.py index.html`.
7. Use browser validation when available:
   - desktop 1280x720
   - mobile around 390x844
   - at least one non-title slide
8. If publishing is requested, use the `publish-html-artifact` skill after validation.

## Deck Requirements

- Single self-contained HTML file.
- No remote JavaScript dependencies.
- No `localhost`, `file://`, or absolute local paths.
- 16:9 desktop-first slide composition with responsive mobile behavior.
- Keyboard navigation with arrow keys.
- Print stylesheet or acceptable browser print behavior.
- Rich media must be inline SVG, CSS diagrams, or embedded data assets.
- Display text must not overflow or overlap at desktop/mobile validation sizes.

## Style Defaults

- Professional, technical, slightly geeky.
- Dense enough for engineers, clear enough for quick sharing.
- Prefer system diagrams, terminal panels, timelines, matrices, and architecture maps.
- Keep cards at 8px border radius or less.
- Avoid decorative blobs, one-note palettes, and unnecessary animation.

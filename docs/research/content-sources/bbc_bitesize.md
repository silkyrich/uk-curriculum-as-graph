# BBC Bitesize — Content Source Research
**Source:** https://www.bbc.co.uk/bitesize
**Researched:** 2026-02-17
**Type:** No public API; web content with URL-based identifiers
**Access:** Free (text); UK-only geolocked (video/audio/games)

## What it is
BBC Bitesize is the BBC's free educational platform covering KS1 through A-Level, organised by UK curriculum and exam board. Content includes study guides, flashcards, games, and video/audio explanations. Over 20,000 pages across 49+ subjects.

## No API
BBC has internal linked data infrastructure (RDF/SPARQL) but Bitesize content is not exposed via public API. Content is accessible only via web browser or BBC apps.

## Identifiers
URL-based alphanumeric slugs:
- Format: `https://www.bbc.co.uk/bitesize/guides/{slug}/revision/1`
- Example: `https://www.bbc.co.uk/bitesize/guides/zc3b4wx/revision/1`
- Slug format: 7-character alphanumeric (e.g. `zc3b4wx`)
- Slugs appear stable but are not semantically meaningful

## Content hierarchy
```
Exam Type → Subject → Exam Board variant → Topics/Guides → Pages
```
Does not map cleanly to our curriculum graph hierarchy (primary content is exam-board-specific at GCSE+, not NC-aligned at KS1-2).

## Licensing
- Non-commercial restriction — not usable in a commercial platform
- Video/audio/animated content: UK-only geolocked
- Text content: internationally accessible but not openly licensed

## What we derived from this
1. BBC Bitesize is not viable for programmatic integration — no API, non-commercial restriction, and geolocked media
2. URL slugs are not semantically meaningful and would require manual mapping
3. Strong brand recognition as revision tool for KS3/4/5 but not aligned to our KS1-KS2 primary focus
4. Not a priority for integration

## Caveats
- Any scraping would violate BBC terms of service
- Commercial use not permitted
- No stable machine-readable identifiers

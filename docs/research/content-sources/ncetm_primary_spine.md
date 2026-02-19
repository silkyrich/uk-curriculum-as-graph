# NCETM Primary Mathematics Mastery Spine — Content Source Research
**Source:** https://www.ncetm.org.uk/teaching-for-mastery/mastery-materials/primary-mastery-professional-development/
**Researched:** 2026-02-17
**Type:** Reference codes + downloadable PDFs (no API)
**Access:** Free, no login required

## What it is
The National Centre for Excellence in Teaching Mathematics (NCETM) publishes a Primary Mathematics Mastery Spine — a structured, sequenced set of teaching materials for primary maths. Each "segment" of the spine is a specific mathematical concept taught via the Teaching for Mastery approach (concrete-pictorial-abstract, variation theory). Widely used in schools across England.

## No API
NCETM has no public API. Content is downloadable PDFs and web pages. Programmatic access would require scraping.

## Identifier scheme
Three numbered spines, each with numbered segments:
- **Spine 1** — Number, Addition and Subtraction: 31 segments (1.1–1.31)
- **Spine 2** — Multiplication and Division: 30 segments (2.1–2.30)
- **Spine 3** — Fractions: ~10 segments (3.0–3.10, 3.0 covers KS1)

Format: `{spine}.{segment}` e.g. `1.8`, `2.14`, `3.4`

Each segment corresponds to a specific teaching sequence with teacher guides, PowerPoint presentations, and video.

## Mapping to our graph
NCETM spine codes map to our Mathematics Concept nodes:
- `1.8` (Place value: ones, tens, hundreds) → `MA-Y3-C007` (Place value in three-digit numbers)
- `2.14` (Multiplying a two-digit number by a one-digit number) → `MA-Y3-C021`
- `3.4` (Equivalent fractions) → `MA-Y3-C027`

These are reference codes only — no API pull. Attaching them to Concept nodes gives teachers a direct link to high-quality mastery teaching materials.

## What we derived from this
1. NCETM spine codes are the gold standard reference for maths teaching sequence in England — attaching them to Maths Concept nodes adds significant teacher-facing value
2. No programmatic access possible, but the codes are stable and well-known to teachers
3. The spine's teaching sequence is an independent validation of our prerequisite ordering
4. Covers only KS1–KS2 Maths (Spines 1–3); not applicable to other subjects
5. Can be attached as a property: `ncetm_spine_code: "2.14"` on relevant Concept nodes

## Caveats
- Maths only; no equivalent spines for other subjects
- No API — reference codes are useful metadata, not a content pull mechanism
- Spine materials are teacher-facing professional development, not student-facing content
- Mapping from our concept IDs to spine codes requires manual work (one-time)

# Content Sources Research Index
**Created:** 2026-02-17
**Purpose:** Audit trail for external content source research to inform curriculum graph enrichment with external reference codes

## Summary

Research into four major UK educational content sources to determine which can be integrated with the curriculum graph via stable identifiers or APIs.

| Source | API | Licence | Identifiers | Integration priority |
|---|---|---|---|---|
| Oak National Academy | ✅ Free public API | OGL v3.0 (open) | lesson slug, unit slug | **HIGH — full integration** |
| NCETM Primary Spine | ❌ No API | Free, no licence stated | `{spine}.{segment}` e.g. `1.8` | **MEDIUM — reference codes, Maths only** |
| White Rose Maths | ❌ No API | Mixed / proprietary | `Y{year}_{term}_Block_{number}` | **LOW — reference metadata only** |
| BBC Bitesize | ❌ No API | Non-commercial, geolocked | Opaque slugs | **NONE — not viable** |

## Key finding
Only Oak National Academy has a public API with openly licensed content suitable for programmatic integration. The other three sources can contribute stable reference codes as metadata on graph nodes, useful for teacher navigation but not for content pull.

## Recommended graph enrichment

### Concept nodes — add:
- `oak_lesson_slugs: ["multiplication-as-scaling"]` — Oak lesson slugs (1+ per concept)
- `ncetm_spine_code: "2.14"` — NCETM spine reference (Maths only)

### Domain nodes — add:
- `oak_unit_slug: "year-3-multiplication-and-division"` — Oak unit slug
- `white_rose_block: "Y3_Autumn_Block_3"` — White Rose block reference

### New relationship (future):
```
(:Assessment:ContentDomainCode)-[:ASSESSES_CONCEPT]->(:Curriculum:Concept)
(:Curriculum:Concept)-[:HAS_CONTENT]->(:Content:OakLesson)
```

## Files in this directory
- `oak_national_academy.md` — Full Oak research: API, endpoints, identifiers, licensing
- `ncetm_primary_spine.md` — NCETM spine codes: numbering scheme, mapping to Maths concepts
- `white_rose_maths.md` — White Rose block structure: reference metadata only
- `bbc_bitesize.md` — BBC Bitesize: why it's not viable for integration

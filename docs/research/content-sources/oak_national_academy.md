# Oak National Academy — Content Source Research
**Source:** https://open-api.thenational.academy/
**Researched:** 2026-02-17
**Type:** Public API + OGL-licensed content
**Access:** API key required on request (free)

## What it is
Oak National Academy is a publicly funded UK EdTech body providing free, openly licensed lesson content for KS1–KS4. Every lesson includes slides, worksheets, quizzes, and often video. Content published after 1 September 2022 is licensed under OGL v3.0 (Open Government Licence), which permits free reuse including commercial use with attribution.

## API
- Base URL: `https://open-api.thenational.academy/`
- Interactive playground: `https://open-api.thenational.academy/playground`
- OpenAPI/Swagger specification available
- API key required (free, requested via their developer portal)

### Key endpoints
| Endpoint | Returns |
|---|---|
| `GET /lessons/{lesson}/summary` | Lesson data including learning outcomes, misconceptions |
| `GET /lessons/{lesson}/assets` | Slides, worksheets, transcripts, videos |
| `GET /sequences/{sequence}/units` | All units within a curriculum sequence |
| `GET /key-stages/{keyStage}/subject/{subject}/questions` | Quiz questions by KS+subject |
| Search endpoints | Cross-curriculum content search |

## Content hierarchy
```
KeyStage → Subject → Programme/Sequence → Unit → Lesson → Assets
```
Maps closely to our graph: `KeyStage → Subject → Programme → Domain → Concept`

## Identifiers
- **lesson slug**: URL path component, e.g. `energy`, `multiplication-as-scaling`
- **unit slug**: e.g. `year-4-multiplication-and-division`  
- **sequence/programme slug**: e.g. `maths-primary-ks2`
- Slugs appear stable (used in canonical URLs)

## Licensing
- OGL v3.0 — free for any use including commercial, with attribution
- Attribution: "[title] by Oak National Academy licensed under OGL v3.0"
- Third-party content within lessons is marked as exempt

## What we derived from this
1. Oak is the only UK content source with a real public API — the clear integration priority
2. Their content hierarchy maps directly to our graph structure
3. Oak unit slugs can be attached to our Domain nodes; lesson slugs to our Concept nodes
4. The misconceptions field in the lesson summary API (`/lessons/{lesson}/summary`) could enrich our Concept.common_misconceptions property
5. Quiz questions from the questions endpoint could seed our retrieval practice layer
6. OGL licensing is compatible with a commercial adaptive learning platform

## Caveats
- API key required (not self-service, must request access)
- Some content has third-party restrictions (marked per lesson)
- Slug stability is not formally guaranteed but appears consistent
- No CASE-compliant IDs exposed — mapping to our node IDs requires manual or LLM-assisted alignment

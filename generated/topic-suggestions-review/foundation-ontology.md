# Foundation Subjects: Graph Ontology Design

**Author**: Foundation Subjects Specialist (Art & Design, Music, DT, Computing, RS, Citizenship, Drama, PE)
**Date**: 2026-02-24
**Status**: Design proposal for review
**Input**: Previous foundation-teacher-review.md, FINAL-SCHEMA.md, CLAUDE.md graph model, extraction JSONs for all foundation subjects

---

## Executive Summary

The universal `TopicSuggestion { themes }` wrapper cannot serve foundation subjects. My previous review identified this problem. This document goes further: it designs complete, subject-native graph ontologies for every foundation subject, with **no constraint from any universal model**.

The core finding is that foundation subjects divide into three structural families:

1. **Studio subjects** (Art, Music, DT) -- each needs its own node label(s) because the topic IS the artistic/technical specification. These three subjects are as different from each other as they are from History or Science.
2. **Enquiry subjects** (Computing, RS, Citizenship) -- can share a common `TopicSuggestion` base with subject-specific property extensions, because topics in these subjects are organised around knowledge questions rather than material specifications.
3. **Performance/practice subjects** (Drama, PE) -- have minimal topic-suggestion needs because their topics are activity-based and already well-served by the InteractionType layer + VehicleTemplate system.

This document provides complete ontology designs for all eight categories.

---

## Part 1: Art & Design

### The Problem Art Poses

Art does not have "topics" in the sense History or Geography does. Art has **units** organised around three intersecting axes:

1. **Medium** -- what physical material (paint, clay, print, textiles, digital)
2. **Artist/movement reference** -- whose work inspires the unit (Mondrian, Hokusai, Goldsworthy)
3. **Visual element focus** -- which formal element(s) are being taught (colour, line, texture, form)

A single Art "topic" is a specific intersection of these three: "Study Hokusai's woodblock prints (medium: print), focusing on line and pattern (visual elements), using block-printing technique." This triple structure is fundamental to how Art is planned, taught, and assessed. No generic `themes` array can capture it.

Furthermore, Art at KS1-KS2 has a progression model that is skill-based rather than knowledge-based:
- **KS1**: Explore materials and techniques with increasing control
- **Lower KS2**: Develop techniques with growing confidence; begin sustained sketchbook practice
- **Upper KS2**: Master techniques with precision; evaluate and refine work critically

The NC does not name specific artists, media, or techniques beyond very broad categories ("drawing, painting and sculpture"). Almost everything taught in Art is teacher convention. This makes the `curriculum_status` property particularly important -- nearly every Art TopicSuggestion will be `convention` rather than `mandatory`.

### Node Label: `ArtStudy`

I am deliberately choosing `ArtStudy` rather than `ArtTopicSuggestion` for two reasons:

1. Art teachers call these "studies" or "units", not "topics". The word "topic" implies knowledge content; Art is about making.
2. The FINAL-SCHEMA uses `ArtTopicSuggestion`. I am keeping consistency with the intent but choosing a name that reflects subject identity. If the project insists on the `*TopicSuggestion` suffix for cross-label querying, rename to `ArtTopicSuggestion` -- the properties and relationships are what matter.

**Decision**: Use `ArtTopicSuggestion` for cross-label query consistency (all labels end in `TopicSuggestion`, enabling `WHERE labels(n)[0] ENDS WITH 'TopicSuggestion'`), but document that Art teachers think of these as "studies" not "topics".

### Property Table: `ArtTopicSuggestion`

| Property | Type | Required | Rationale |
|---|---|---|---|
| **Universal properties** | | | |
| `suggestion_id` | string | Yes | Format: `TS-AD-{KS}-{number}` e.g. `TS-AD-KS1-001` |
| `name` | string | Yes | Human-readable title e.g. "Hokusai Wave Printing" |
| `suggestion_type` | string | Yes | Enum: `prescribed_topic`, `teacher_convention`, `exemplar_topic`, `open_slot`. Most Art entries will be `teacher_convention`. |
| `subject` | string | Yes | `"Art and Design"` |
| `key_stage` | string | Yes | `KS1` / `KS2` / `KS3` / `KS4` |
| `curriculum_status` | string | Yes | `mandatory` / `convention` / `exemplar`. Art has very few `mandatory` entries -- the NC only mandates broad categories like "drawing, painting and sculpture", not specific topics. |
| `choice_group` | string | No | Groups alternative studies that serve the same curriculum objective. E.g. for KS1 "artist study: primary colours", teachers might choose Mondrian OR Kandinsky. |
| `curriculum_reference` | string[] | No | NC text this study addresses. Sparse for Art -- the NC has only 4 bullet points per KS. |
| `pedagogical_rationale` | string | Yes | Why this study works for these concepts at this age. E.g. "Mondrian's geometric grids use only primary colours and straight lines, making colour mixing and geometric vocabulary accessible to 5-6 year olds." |
| `common_pitfalls` | string[] | No | Teaching mistakes. E.g. "Pupils copy Mondrian's grid layout rather than understanding his use of primary colours and geometric abstraction. Ensure pupils create ORIGINAL compositions using Mondrian's principles, not photocopied colouring sheets." |
| `cross_curricular_hooks` | string[] | No | Format: `"[Subject] Hook description"`. E.g. `"[History] Mondrian and De Stijl: 1920s European art movements"`, `"[Maths] Right angles, parallel lines, geometric shapes"` |
| `definitions` | string[] | Yes | Key vocabulary. E.g. `["primary colours", "secondary colours", "geometric", "abstract", "composition"]` |
| `year_groups` | string[] | No | Specific year groups where commonly taught. E.g. `["Y1", "Y2"]` |
| `duration_lessons` | int | No | Typical unit length. Art units usually span 4-6 lessons. |
| `display_category` | string | Yes | `"Topic Suggestion"` |
| `display_color` | string | Yes | `"#059669"` (Emerald-600, shared across all TopicSuggestion types) |
| `display_icon` | string | Yes | `"palette"` (Art-specific icon) |
| **Art-specific properties** | | | |
| `artist` | string | No | The specific artist. E.g. `"Piet Mondrian"`, `"Katsushika Hokusai"`. Null for technique-focused units that don't reference a specific artist (e.g. "Colour Mixing"). |
| `artist_dates` | string | No | Birth-death dates for timeline context. E.g. `"1872-1944"`. Supports cross-curricular History links. |
| `art_movement` | string | No | Art movement or cultural tradition. E.g. `"De Stijl"`, `"Ukiyo-e"`, `"Impressionism"`, `"Pop Art"`, `"Land Art"`. Null for technique-only units. Controlled vocabulary recommended. |
| `medium` | string[] | **Yes** | The physical media used. **This is the single most important Art property.** Without it, the AI cannot generate material-specific instructions. Controlled vocabulary: `paint`, `drawing`, `collage`, `sculpture`, `clay`, `print`, `textiles`, `digital`, `photography`, `mixed_media`, `natural_materials`. |
| `techniques` | string[] | **Yes** | Specific techniques taught. E.g. `["colour mixing", "wet-on-wet"]`, `["block printing", "colour layering"]`, `["running stitch", "applique"]`. Without these, the AI generates generic "make art" instructions instead of technique-specific step-by-step guidance. |
| `visual_elements` | string[] | No | Which formal elements are the focus. Controlled vocabulary (NC terminology): `colour`, `pattern`, `texture`, `line`, `shape`, `form`, `space`, `tone`. These are the NC's own assessment dimensions. |
| `unit_type` | string | No | What kind of Art unit this is. Enum: `artist_study` (study an artist's work and create inspired responses), `skill_building` (focused technique development without artist reference), `gallery_response` (respond to viewed artworks), `sketchbook_practice` (sustained observational/experimental drawing). This helps the AI choose the right pedagogical approach. |
| `cultural_context` | string | No | Cultural/geographical context. E.g. `"Dutch/European"`, `"Japanese"`, `"British"`, `"West African"`, `"Indigenous Australian"`. Supports diversity requirements and Geography cross-curricular links. |

### Relationships for Art

```cypher
// Core teaching link
(ts:ArtTopicSuggestion)-[:DELIVERS_VIA {primary: bool}]->(c:Concept)

// Pedagogical pattern -- Art mainly uses creative_response, observation_over_time
(ts:ArtTopicSuggestion)-[:USES_TEMPLATE]->(vt:VehicleTemplate)

// Domain convenience (inferred from delivered concepts)
(:Domain)-[:HAS_SUGGESTION]->(ts:ArtTopicSuggestion)

// Cluster integration
(:ConceptCluster)-[:SUGGESTED_TOPIC {rank: int}]->(ts:ArtTopicSuggestion)

// Choice alternatives -- Art studies that serve the same objective
(ts1:ArtTopicSuggestion)-[:ALTERNATIVE_TO]->(ts2:ArtTopicSuggestion)
// E.g. Mondrian and Kandinsky are both valid KS1 "primary colour artist study" choices
// This replaces choice_group string with a graph-native relationship.
// KEEP choice_group AS WELL for simpler query patterns.
```

### Example Instances

**Example 1: KS1 Artist Study**
```json
{
  "suggestion_id": "TS-AD-KS1-006",
  "name": "Mondrian Primary Colours",
  "suggestion_type": "teacher_convention",
  "subject": "Art and Design",
  "key_stage": "KS1",
  "curriculum_status": "convention",
  "choice_group": "ks1_colour_artist_study",
  "curriculum_reference": ["to develop a wide range of art and design techniques in using colour"],
  "pedagogical_rationale": "Mondrian's Composition with Red, Blue, and Yellow uses only primary colours and straight black lines, making it ideal for teaching colour mixing (primary to secondary) and geometric vocabulary to 5-6 year olds. The strong visual structure means pupils can create successful compositions quickly, building confidence.",
  "common_pitfalls": ["Pupils copy Mondrian's exact grid rather than understanding geometric abstraction — ensure original compositions", "Only using poster paint — try colour mixing with powder paint for richer learning about pigment"],
  "cross_curricular_hooks": ["[Maths] Right angles, parallel lines, rectangles, squares", "[History] 1920s Europe, De Stijl movement"],
  "definitions": ["primary colours", "secondary colours", "geometric", "abstract", "composition", "grid"],
  "year_groups": ["Y1"],
  "duration_lessons": 4,
  "artist": "Piet Mondrian",
  "artist_dates": "1872-1944",
  "art_movement": "De Stijl",
  "medium": ["paint"],
  "techniques": ["colour mixing", "painting within boundaries", "straight line painting"],
  "visual_elements": ["colour", "line", "shape"],
  "unit_type": "artist_study",
  "cultural_context": "Dutch/European",
  "display_category": "Topic Suggestion",
  "display_color": "#059669",
  "display_icon": "palette"
}
```

**Example 2: KS2 Printmaking**
```json
{
  "suggestion_id": "TS-AD-KS2-003",
  "name": "Hokusai Wave Printing",
  "suggestion_type": "teacher_convention",
  "subject": "Art and Design",
  "key_stage": "KS2",
  "curriculum_status": "convention",
  "curriculum_reference": ["to improve their mastery of art and design techniques, including drawing, painting and sculpture with a range of materials"],
  "pedagogical_rationale": "Hokusai's Great Wave is one of the most recognisable images in art history. The wave's bold lines and dramatic composition translate well to printmaking at Y3-Y4 level. Block printing requires planning (design must be reversed), precision (cutting technique), and sequencing (ink, press, pull) — all transferable skills. The Japanese cultural context supports Geography and History cross-curricular work.",
  "common_pitfalls": ["Forgetting to reverse the design — the print will be a mirror image of the block", "Using too much ink — press should be even, not flooded", "Rushing the cutting — safety first with lino cutters, adult supervision essential"],
  "cross_curricular_hooks": ["[Geography] Japan, Pacific Ocean, island nations", "[History] Edo period Japan (1603-1868)", "[Science] Waves and water"],
  "definitions": ["woodblock print", "ukiyo-e", "composition", "foreground", "background", "edition", "registration"],
  "year_groups": ["Y3", "Y4"],
  "duration_lessons": 5,
  "artist": "Katsushika Hokusai",
  "artist_dates": "1760-1849",
  "art_movement": "Ukiyo-e",
  "medium": ["print"],
  "techniques": ["block printing", "colour layering", "design transfer"],
  "visual_elements": ["line", "pattern", "shape", "form"],
  "unit_type": "artist_study",
  "cultural_context": "Japanese",
  "display_category": "Topic Suggestion",
  "display_color": "#059669",
  "display_icon": "palette"
}
```

**Example 3: KS1 Skill-Building (no artist)**
```json
{
  "suggestion_id": "TS-AD-KS1-001",
  "name": "Colour Mixing",
  "suggestion_type": "prescribed_topic",
  "subject": "Art and Design",
  "key_stage": "KS1",
  "curriculum_status": "mandatory",
  "curriculum_reference": ["to develop a wide range of art and design techniques in using colour"],
  "pedagogical_rationale": "Colour mixing is the foundational practical skill of painting. Pupils need to discover through hands-on experimentation that two primary colours combine to make a secondary colour. This is more effectively learned through making than telling — the surprise of yellow + blue = green creates memorable learning. Mixing also develops fine motor control and an intuitive understanding of colour relationships that supports all future painting work.",
  "definitions": ["primary colours", "secondary colours", "mix", "shade", "tint", "palette"],
  "year_groups": ["Y1"],
  "duration_lessons": 3,
  "artist": null,
  "art_movement": null,
  "medium": ["paint"],
  "techniques": ["colour mixing", "wet-on-wet", "colour wheel construction"],
  "visual_elements": ["colour"],
  "unit_type": "skill_building",
  "cultural_context": null,
  "display_category": "Topic Suggestion",
  "display_color": "#059669",
  "display_icon": "palette"
}
```

---

## Part 2: Music

### The Problem Music Poses

Music is organised around three simultaneous axes that the NC mandates explicitly:

1. **Activity strand** -- performing, composing, listening (the three NC strands)
2. **Musical elements** -- pulse, rhythm, pitch, dynamics, tempo, timbre, texture, structure, notation (the "inter-related dimensions of music")
3. **Repertoire** -- specific pieces, composers, genres, traditions

A Music "topic" is always a combination of these three: "Perform 'Livin' on a Prayer' (repertoire) with glockenspiel accompaniment (instrument), focusing on structure and dynamics (musical elements), through performing and listening activities (strands)."

Additionally, Music has a unique feature among all curriculum subjects: the **Model Music Curriculum** (MMC, DfE 2021). This non-statutory but widely adopted document provides year-by-year repertoire suggestions. It is the single most influential document in primary Music teaching after the NC itself. ~70-80% of schools follow some or all of the MMC's suggested units. This means Music topic suggestions have unusually high convergence around a known set of pieces.

The MMC structures units around a lead piece with associated listening repertoire, composing activities, and musical focus. Each unit is designed to span a half-term (~6 lessons). This maps well to our TopicSuggestion model.

### Node Label: `MusicTopicSuggestion`

Music topics are called "units" by teachers, but `MusicTopicSuggestion` maintains cross-label consistency.

### Separate Composer/Piece Nodes?

I considered whether `Composer` and `Piece` should be separate node labels (as the brief asks). My conclusion: **no, not yet**. Here is my reasoning:

- A separate `:Composer` node (e.g. `{name: "Beethoven", dates: "1770-1827", nationality: "German"}`) would enable queries like "find all units featuring German composers" or "show me the listening repertoire chronologically". These are useful but not essential for content generation.
- A separate `:Piece` node (e.g. `{name: "Symphony No. 5", composer: "Beethoven", genre: "Classical", duration: "33 min"}`) would enable queries like "find all units that use this piece" or "show me pieces in this genre across all year groups".
- **However**, the primary use case is AI lesson generation, not musicological research. The AI needs all the information in a single query pass. Splitting into separate nodes adds join complexity without improving generation quality.
- **Recommendation**: Store `composer`, `piece`, and `genre` as properties on `MusicTopicSuggestion` for now. If cross-unit repertoire analysis becomes a use case (e.g. "which composers appear across multiple year groups?"), extract these into separate nodes in a future iteration. The property data is rich enough to support extraction later.

### Property Table: `MusicTopicSuggestion`

| Property | Type | Required | Rationale |
|---|---|---|---|
| **Universal properties** | | | (same as Art -- all shared universal properties) |
| `suggestion_id` | string | Yes | Format: `TS-MU-{KS}-{number}` |
| `name` | string | Yes | E.g. "Livin' on a Prayer" |
| `suggestion_type` | string | Yes | Most primary Music entries will be `teacher_convention` (MMC-aligned). |
| `subject` | string | Yes | `"Music"` |
| `key_stage` | string | Yes | |
| `curriculum_status` | string | Yes | `convention` for MMC-aligned; `mandatory` for NC-mandated broad categories. |
| `curriculum_reference` | string[] | No | NC text. Very sparse for Music. |
| `mmc_reference` | string | No | **Music-specific addition.** Model Music Curriculum reference. E.g. "MMC Year 5, Unit 1". Since the MMC is the dominant planning document for Music, this reference is more useful than `curriculum_reference` for most entries. |
| `pedagogical_rationale` | string | Yes | Why this unit works. |
| `common_pitfalls` | string[] | No | Teaching mistakes. E.g. "Pupils sing along to recording rather than learning to hold the melody independently — use backing track without vocals for performance." |
| `cross_curricular_hooks` | string[] | No | |
| `definitions` | string[] | Yes | Musical vocabulary. |
| `year_groups` | string[] | No | MMC is year-specific, so this will be populated for most primary entries. |
| `duration_lessons` | int | No | MMC units are 6 lessons. |
| `display_category` | string | Yes | `"Topic Suggestion"` |
| `display_color` | string | Yes | `"#059669"` |
| `display_icon` | string | Yes | `"music_note"` |
| **Music-specific properties** | | | |
| `composer` | string | No | Composer or artist name. E.g. `"Bon Jovi"`, `"J.S. Bach"`, `"Grieg"`. Null for genre-based units with no specific composer (e.g. "West African Drumming"). |
| `piece` | string | No | Specific piece. E.g. `"Livin' on a Prayer"`, `"In the Hall of the Mountain King"`. Null for technique-focused units (e.g. "Glockenspiel Stage 1" has no single piece). |
| `genre` | string | No | Musical genre/tradition. Controlled vocabulary: `western_classical`, `pop`, `rock`, `jazz`, `blues`, `reggae`, `hip_hop`, `r_and_b`, `folk`, `world_african`, `world_indian`, `world_caribbean`, `world_east_asian`, `film_music`, `musical_theatre`, `electronic`, `action_song`. |
| `musical_elements` | string[] | **Yes** | Which inter-related dimensions are the focus. Controlled vocabulary (NC terminology): `pulse`, `rhythm`, `pitch`, `melody`, `dynamics`, `tempo`, `timbre`, `texture`, `structure`, `notation`. **This is the most important Music property** -- it tells the AI what the learning objective actually is. |
| `activity_focus` | string[] | **Yes** | Which NC strands. Controlled vocabulary: `performing`, `composing`, `listening`. A unit might focus on one (e.g. a listening-only unit) or span all three. The primary activity should be listed first. |
| `instrument` | string[] | No | Instruments involved. E.g. `["voice"]`, `["glockenspiel", "voice"]`, `["djembe"]`, `["recorder"]`, `["ukulele"]`. Critical for equipment planning and for the AI to generate instrument-specific instructions. |
| `notation_level` | string | No | What level of notation is used. Enum: `none` (no notation, all aural), `graphic` (invented/graphic notation), `rhythm_only` (rhythm grids), `staff_intro` (basic staff notation, treble clef, limited range), `staff_standard` (standard staff notation). Important for differentiating KS1 (mostly `none`/`graphic`) from KS3-4 (`staff_standard`). |
| `listening_repertoire` | string[] | No | Additional pieces for the listening component of this unit. E.g. for a "Rock" unit: `["We Will Rock You - Queen", "Smoke on the Water - Deep Purple"]`. Separating this from `piece` (the lead performance piece) reflects how the MMC structures units. |

### Relationships for Music

```cypher
// Core teaching link
(ts:MusicTopicSuggestion)-[:DELIVERS_VIA {primary: bool}]->(c:Concept)

// Pedagogical pattern -- Music uses performance, creative_response, or observation_over_time (for listening)
(ts:MusicTopicSuggestion)-[:USES_TEMPLATE]->(vt:VehicleTemplate)

// Domain convenience
(:Domain)-[:HAS_SUGGESTION]->(ts:MusicTopicSuggestion)

// Cluster integration
(:ConceptCluster)-[:SUGGESTED_TOPIC {rank: int}]->(ts:MusicTopicSuggestion)
```

No Music-specific relationships needed beyond the universal set. The `listening_repertoire` property handles the "related pieces" use case that might otherwise require a separate `:Piece` node with relationships.

### Example Instances

**Example 1: MMC-aligned performing unit (Y5)**
```json
{
  "suggestion_id": "TS-MU-KS2-009",
  "name": "Livin' on a Prayer",
  "suggestion_type": "teacher_convention",
  "subject": "Music",
  "key_stage": "KS2",
  "curriculum_status": "convention",
  "mmc_reference": "MMC Year 5, Unit 1",
  "pedagogical_rationale": "This iconic rock song has a strong, memorable melody and clear verse-chorus structure that makes it accessible for Y5 performance. The glockenspiel part introduces ostinato patterns and can be differentiated from simple repeated notes to a counter-melody. The dynamic contrast between the quiet verse and loud chorus provides a natural focus for teaching dynamics and structure.",
  "common_pitfalls": ["Pupils shout rather than project during chorus — teach controlled forte", "Glockenspiel players lose time when melody moves between notes — practise slowly first"],
  "cross_curricular_hooks": ["[English] Song lyrics as poetry — rhyme scheme, narrative voice", "[PSHE] Perseverance and working together themes"],
  "definitions": ["verse", "chorus", "bridge", "dynamics", "forte", "piano", "crescendo", "structure", "ostinato"],
  "year_groups": ["Y5"],
  "duration_lessons": 6,
  "composer": "Bon Jovi",
  "piece": "Livin' on a Prayer",
  "genre": "rock",
  "musical_elements": ["structure", "dynamics", "tempo", "pitch"],
  "activity_focus": ["performing", "listening"],
  "instrument": ["voice", "glockenspiel"],
  "notation_level": "rhythm_only",
  "listening_repertoire": ["We Will Rock You - Queen", "Don't Stop Believin' - Journey", "Smoke on the Water - Deep Purple"],
  "display_category": "Topic Suggestion",
  "display_color": "#059669",
  "display_icon": "music_note"
}
```

**Example 2: Classical listening unit**
```json
{
  "suggestion_id": "TS-MU-KS2-015",
  "name": "The Planets - Mars",
  "suggestion_type": "teacher_convention",
  "subject": "Music",
  "key_stage": "KS2",
  "curriculum_status": "convention",
  "mmc_reference": "MMC Year 5, Listening Repertoire",
  "pedagogical_rationale": "Mars, the Bringer of War is dramatic, accessible, and immediately gripping — the relentless 5/4 ostinato creates an ominous atmosphere that children respond to viscerally. It demonstrates how rhythm, dynamics and timbre create mood and atmosphere, making abstract musical concepts tangible. The orchestral forces provide rich material for timbre identification.",
  "definitions": ["ostinato", "timbre", "orchestra", "strings", "brass", "percussion", "dynamics", "crescendo", "atmosphere"],
  "year_groups": ["Y5", "Y6"],
  "duration_lessons": 2,
  "composer": "Gustav Holst",
  "piece": "The Planets - Mars, the Bringer of War",
  "genre": "western_classical",
  "musical_elements": ["rhythm", "dynamics", "timbre", "texture", "structure"],
  "activity_focus": ["listening", "composing"],
  "instrument": ["percussion"],
  "notation_level": "graphic",
  "listening_repertoire": ["The Planets - Jupiter (Holst)", "Night on Bald Mountain (Mussorgsky)"],
  "display_category": "Topic Suggestion",
  "display_color": "#059669",
  "display_icon": "music_note"
}
```

**Example 3: World music unit (KS1)**
```json
{
  "suggestion_id": "TS-MU-KS1-003",
  "name": "Hands, Feet, Heart",
  "suggestion_type": "teacher_convention",
  "subject": "Music",
  "key_stage": "KS1",
  "curriculum_status": "convention",
  "mmc_reference": "MMC Year 2, Unit 2",
  "pedagogical_rationale": "This South African-inspired unit introduces pupils to music from a non-Western tradition, fulfilling the NC requirement for 'a range of high-quality live and recorded music'. The physical, rhythmic nature of South African music connects naturally to KS1 pupils' love of movement. Body percussion activities build on the rhythm and pulse work from Year 1.",
  "definitions": ["pulse", "rhythm", "body percussion", "South Africa", "call and response"],
  "year_groups": ["Y2"],
  "duration_lessons": 6,
  "composer": null,
  "piece": "Hands, Feet, Heart",
  "genre": "world_african",
  "musical_elements": ["pulse", "rhythm", "dynamics", "tempo"],
  "activity_focus": ["performing", "listening"],
  "instrument": ["voice", "body percussion"],
  "notation_level": "none",
  "listening_repertoire": ["Shosholoza (traditional)", "Pata Pata - Miriam Makeba"],
  "display_category": "Topic Suggestion",
  "display_color": "#059669",
  "display_icon": "music_note"
}
```

---

## Part 3: Design & Technology

### The Problem DT Poses

DT is the most structurally unusual subject in the curriculum. Its topics are not knowledge areas or skill focuses -- they are **design briefs**. A DT topic IS a making project: "Design and make a torch with a working circuit." Everything about the topic flows from the brief: the materials, tools, techniques, safety considerations, and evaluation criteria.

DT is also the only subject with **five distinct technical strands** mandated by the NC:
1. **Structures** -- building things that stand up and bear loads
2. **Mechanisms** -- levers, sliders, cams, gears, pulleys
3. **Textiles** -- sewing, weaving, fabric manipulation
4. **Cooking & Nutrition** -- food preparation, healthy eating, food provenance
5. **Electrical Systems** -- circuits, switches, programming for control (KS2+)
6. **Digital World** -- CAD/CAM, 3D printing, smart textiles (KS3-4)

Each strand uses fundamentally different materials, tools, techniques, and safety protocols. A textiles project and a cooking project share nothing except the design-make-evaluate process. This means `dt_strand` is the single highest-leverage property -- it determines the entire nature of the activity.

### Node Label: `DTTopicSuggestion`

### Property Table: `DTTopicSuggestion`

| Property | Type | Required | Rationale |
|---|---|---|---|
| **Universal properties** | | | (all shared universal properties as per Art) |
| `suggestion_id` | string | Yes | Format: `TS-DT-{KS}-{number}` |
| `name` | string | Yes | E.g. "Moving Pictures (Sliders and Levers)" |
| `suggestion_type` | string | Yes | Mix of `prescribed_topic` (cooking NC requirements) and `teacher_convention` (most projects). |
| `subject` | string | Yes | `"Design and Technology"` |
| `key_stage` | string | Yes | |
| `curriculum_status` | string | Yes | |
| `curriculum_reference` | string[] | No | |
| `pedagogical_rationale` | string | Yes | Why this project works for these concepts. |
| `common_pitfalls` | string[] | No | Making/safety mistakes. E.g. "Split pin points not flattened -- sharp ends are a safety hazard." |
| `cross_curricular_hooks` | string[] | No | DT has strong Science and Maths links. |
| `definitions` | string[] | Yes | Technical vocabulary. |
| `year_groups` | string[] | No | |
| `duration_lessons` | int | No | DT projects typically span 4-6 lessons. |
| `display_category` | string | Yes | `"Topic Suggestion"` |
| `display_color` | string | Yes | `"#059669"` |
| `display_icon` | string | Yes | `"construction"` |
| **DT-specific properties** | | | |
| `dt_strand` | string | **Yes** | The NC strand. Controlled vocabulary: `structures`, `mechanisms`, `textiles`, `cooking_and_nutrition`, `electrical_systems`, `digital_world`. **This is the single most important DT property.** It determines materials, tools, safety protocols, and the entire nature of the project. |
| `design_brief` | string | **Yes** | The challenge statement. E.g. "Design and make a moving picture book page with a slider or lever mechanism." **This IS the topic.** Without it, the AI has no project to generate. |
| `materials` | string[] | **Yes** | Materials needed. E.g. `["card", "split pins", "paper fasteners", "straws"]`. Essential for resource planning and safety assessment. The AI needs this to generate accurate making instructions. |
| `tools` | string[] | No | Tools used. E.g. `["scissors", "hole punch", "ruler"]`. Important for safety notes at all KS levels, critical at KS3-4 (saws, drills, soldering irons). |
| `techniques` | string[] | **Yes** | Making techniques. E.g. `["cutting", "joining with split pins", "creating slider tracks"]`. Without these, the AI generates vague "make it" instructions instead of step-by-step technical guidance. |
| `safety_notes` | string | No | Safety information. E.g. "Adult supervision required for hole punch. Ensure all split pin points are flattened to prevent scratching." **Should be required for KS3-4** where tools become genuinely hazardous (hot glue guns, craft knives, saws, soldering). |
| `evaluation_criteria` | string[] | No | How the product will be assessed. E.g. `["Does the slider move smoothly?", "Does the picture tell a story?", "Is the mechanism hidden behind the page?"]`. Maps to the NC Evaluate domain. |
| `food_allergens` | string[] | No | **Cooking strand only.** Allergens present. E.g. `["gluten", "dairy", "eggs"]`. Safeguarding requirement for cooking projects. Must be in the system prompt as a non-overridable constraint. |
| `food_skills` | string[] | No | **Cooking strand only.** Specific food preparation skills. E.g. `["peeling", "grating", "mixing", "kneading"]`. Distinct from `techniques` because food skills have their own safety and hygiene requirements. |

### Relationships for DT

```cypher
// Core teaching link
(ts:DTTopicSuggestion)-[:DELIVERS_VIA {primary: bool}]->(c:Concept)

// Pedagogical pattern -- DT uses design_make_evaluate (primary), practical_application (secondary)
(ts:DTTopicSuggestion)-[:USES_TEMPLATE]->(vt:VehicleTemplate)

// Domain convenience
(:Domain)-[:HAS_SUGGESTION]->(ts:DTTopicSuggestion)

// Cluster integration
(:ConceptCluster)-[:SUGGESTED_TOPIC {rank: int}]->(ts:DTTopicSuggestion)

// Strand-level query shortcut (optional, can be done via property filter)
// Not a new relationship -- just document that dt_strand enables
// MATCH (ts:DTTopicSuggestion {dt_strand: 'mechanisms'}) as the primary query pattern
```

### Example Instances

**Example 1: KS1 Mechanisms**
```json
{
  "suggestion_id": "TS-DT-KS1-001",
  "name": "Moving Pictures (Sliders and Levers)",
  "suggestion_type": "teacher_convention",
  "subject": "Design and Technology",
  "key_stage": "KS1",
  "curriculum_status": "convention",
  "curriculum_reference": ["explore and use mechanisms in their products"],
  "pedagogical_rationale": "Moving picture books are an engaging first mechanisms project because the end product is immediately functional and satisfying — the slider moves, the lever lifts, the child sees cause and effect. The project combines Art (illustration) with DT (mechanism) in a natural way. The relatively simple construction (card, split pins, paper strips) is achievable for 5-7 year olds while still teaching genuine mechanical principles.",
  "common_pitfalls": ["Slider tracks too tight — card bows and jams", "Split pin points not flattened — scratch hazard", "Pupils decorate before testing mechanism — if mechanism fails, decoration is wasted"],
  "cross_curricular_hooks": ["[English] Storytelling — the moving picture tells a story", "[Science] Forces — push and pull, cause and effect", "[Maths] Measurement — cutting strips to length"],
  "definitions": ["mechanism", "slider", "lever", "pivot", "split pin", "design criteria", "evaluate"],
  "year_groups": ["Y1", "Y2"],
  "duration_lessons": 5,
  "dt_strand": "mechanisms",
  "design_brief": "Design and make a picture book page with moving parts using sliders and levers. The movement must help tell a story.",
  "materials": ["card", "split pins", "paper fasteners", "cardboard strips", "straws", "coloured paper"],
  "tools": ["scissors", "hole punch", "ruler", "glue stick"],
  "techniques": ["cutting", "joining with split pins", "creating slider tracks", "lever mechanisms"],
  "safety_notes": "Adult supervision for hole punch. Ensure split pin points are flattened after insertion to prevent scratching.",
  "evaluation_criteria": ["Does the slider/lever move smoothly?", "Does the movement help tell the story?", "Is the mechanism securely attached?"],
  "display_category": "Topic Suggestion",
  "display_color": "#059669",
  "display_icon": "construction"
}
```

**Example 2: KS2 Electrical Systems**
```json
{
  "suggestion_id": "TS-DT-KS2-004",
  "name": "Design a Torch",
  "suggestion_type": "teacher_convention",
  "subject": "Design and Technology",
  "key_stage": "KS2",
  "curriculum_status": "convention",
  "curriculum_reference": ["understand and use electrical systems in their products"],
  "pedagogical_rationale": "A torch is a real, functional product that pupils can test immediately — does it light up? This creates an unambiguous success criterion. The project requires understanding of simple circuits (Science cross-curricular), switch design (mechanism), and housing construction (structures). It naturally integrates three DT strands in one project.",
  "common_pitfalls": ["Loose connections — use crocodile clips for testing before soldering/taping", "Battery orientation wrong — teach polarity before construction", "Housing blocks light — ensure reflector design considered early"],
  "cross_curricular_hooks": ["[Science] Electrical circuits, conductors and insulators, series circuits", "[Maths] Measurement — cutting housing to size, battery compartment dimensions"],
  "definitions": ["circuit", "switch", "conductor", "insulator", "component", "battery", "LED", "series circuit", "housing"],
  "year_groups": ["Y4", "Y5"],
  "duration_lessons": 6,
  "dt_strand": "electrical_systems",
  "design_brief": "Design and make a working torch for use in a specific situation (e.g. camping, reading under the covers, emergency). The torch must have a switch to turn it on and off.",
  "materials": ["card tubes", "aluminium foil", "wire", "batteries", "LED bulbs", "paper clips", "tape", "plastic bottles"],
  "tools": ["scissors", "wire strippers", "tape", "ruler"],
  "techniques": ["circuit building", "switch making", "housing construction", "reflector design"],
  "safety_notes": "Never use mains electricity. Use batteries only (max 4.5V). Adult supervision for wire strippers. Check for short circuits before testing.",
  "evaluation_criteria": ["Does the torch produce light?", "Does the switch work reliably?", "Is the torch suitable for its intended purpose?", "Is the torch comfortable to hold?"],
  "display_category": "Topic Suggestion",
  "display_color": "#059669",
  "display_icon": "construction"
}
```

**Example 3: KS1 Cooking**
```json
{
  "suggestion_id": "TS-DT-KS1-005",
  "name": "Fruit Salad",
  "suggestion_type": "teacher_convention",
  "subject": "Design and Technology",
  "key_stage": "KS1",
  "curriculum_status": "convention",
  "curriculum_reference": ["use the basic principles of a healthy and varied diet to prepare dishes", "understand where food comes from"],
  "pedagogical_rationale": "A fruit salad is the ideal first cooking project: no heat is involved (removing a major safety concern), the ingredients are colourful and appealing, and the preparation techniques (washing, peeling, cutting, arranging) are age-appropriate. The project naturally teaches healthy eating, food groups, and where different fruits come from — all NC requirements.",
  "definitions": ["ingredient", "recipe", "hygiene", "healthy", "fruit", "vitamin", "prepare", "peel", "chop", "mix"],
  "year_groups": ["Y1"],
  "duration_lessons": 3,
  "dt_strand": "cooking_and_nutrition",
  "design_brief": "Design and make a fruit salad for a class picnic. Choose at least 4 different fruits. Think about colour, taste, and healthy eating.",
  "materials": ["assorted fresh fruits (apples, bananas, oranges, grapes, strawberries, kiwi)", "lemon juice"],
  "tools": ["chopping boards", "child-safe knives", "bowls", "spoons"],
  "techniques": ["washing", "peeling", "chopping", "mixing", "arranging"],
  "safety_notes": "Check for allergies before selecting fruits. Wash all fruits. Adult supervision for any cutting. Wash hands before handling food. Use child-safe knives with rounded ends.",
  "evaluation_criteria": ["Does the fruit salad contain at least 4 different fruits?", "Is it colourful and appealing?", "Does it taste good?"],
  "food_allergens": ["possible: kiwi, strawberry (common childhood allergens)"],
  "food_skills": ["washing", "peeling", "safe cutting with child-safe knife", "mixing"],
  "display_category": "Topic Suggestion",
  "display_color": "#059669",
  "display_icon": "construction"
}
```

---

## Part 4: Computing

### Assessment: Can Computing Share Structure?

Computing sits between the studio subjects and the enquiry subjects. It has some structural specificity (programming paradigm, software tool) but its topics are fundamentally knowledge-and-skill based rather than material-based. The key question: does Computing need its own typed label?

**My answer: not yet, but it needs more than `themes`.**

Computing topics organise around three dimensions:
1. **Computational concept** -- algorithm, selection, repetition, variable, decomposition, etc.
2. **Programming paradigm** -- unplugged, block-based, text-based
3. **Tool/language** -- Scratch, Python, HTML/CSS, spreadsheet

These three properties, added to the generic `TopicSuggestion`, are sufficient. Computing has far fewer topic variations than Art, Music, or DT (~15-20 across KS1-KS4), so the overhead of a typed label is not justified.

**However**, if Computing TopicSuggestions grow beyond ~30 nodes, or if the AI tutor needs to generate coding exercises (which require language-specific syntax knowledge), reconsider promoting to `ComputingTopicSuggestion`.

### Properties on Generic `TopicSuggestion` for Computing

| Property | Type | Required (for Computing) | Rationale |
|---|---|---|---|
| `themes` | string[] | Yes | General topic area. E.g. `["programming", "algorithms"]` |
| `computational_concept` | string[] | No | Controlled vocabulary: `algorithm`, `sequence`, `selection`, `repetition`, `variable`, `decomposition`, `abstraction`, `pattern_recognition`, `boolean_logic`, `input_output`, `debugging`, `networking`, `data_representation`, `digital_literacy`. |
| `programming_paradigm` | string | No | Enum: `unplugged`, `block_based`, `text_based`, `markup`. |
| `software_tool` | string | No | The specific tool/language. E.g. `"Scratch"`, `"Python"`, `"HTML/CSS"`, `"spreadsheet"`, `"Micro:bit"`. Not a controlled enum because tools change frequently. |
| `output_type` | string | No | What the pupil creates. Enum: `animation`, `game`, `simulation`, `website`, `program`, `presentation`, `unplugged_artefact`. Helps the AI generate appropriate project briefs. |

### Example Instance

```json
{
  "suggestion_id": "TS-CO-KS2-008",
  "name": "Scratch Animation Project",
  "suggestion_type": "teacher_convention",
  "subject": "Computing",
  "key_stage": "KS2",
  "curriculum_status": "convention",
  "pedagogical_rationale": "Scratch is the de facto standard block-based programming environment for primary computing. Creating an animation requires sequencing, repetition (loops for animation), and event handling — three key NC concepts in a single motivating project. The visual output gives immediate feedback on whether code is working correctly.",
  "definitions": ["algorithm", "sequence", "loop", "event", "sprite", "stage", "block", "repeat", "forever loop"],
  "themes": ["programming", "animation", "creative computing"],
  "computational_concept": ["sequence", "repetition", "event"],
  "programming_paradigm": "block_based",
  "software_tool": "Scratch",
  "output_type": "animation",
  "year_groups": ["Y3", "Y4"],
  "display_category": "Topic Suggestion",
  "display_color": "#059669",
  "display_icon": "lightbulb"
}
```

---

## Part 5: Religious Studies

### Assessment: Can RS Share Structure?

RS has genuine structural specificity: the requirement to study **at least two religions** at KS4, with Christianity mandatory. This means RS topics need a `religion` property that is essential for content generation — without it, the AI does not know which religious tradition to draw on.

RS also has a strong division between two types of content:
1. **Systematic theology** -- Beliefs, Teachings, Practices of specific religions
2. **Ethical/thematic studies** -- Medical ethics, War and Peace, Crime and Punishment (applying religious and secular perspectives to contemporary issues)

Despite this specificity, RS does not need its own typed label. The number of RS TopicSuggestions is moderate (~15-20), and the subject-specific properties (`religion`, `ethical_issue`, `sacred_texts`) can live on the generic `TopicSuggestion` without polluting it — they are simply null for non-RS subjects.

### Properties on Generic `TopicSuggestion` for RS

| Property | Type | Required (for RS) | Rationale |
|---|---|---|---|
| `themes` | string[] | Yes | Thematic content. E.g. `["sanctity of life", "quality of life", "compassion"]` |
| `religion` | string[] | No | Which religions are studied. Controlled vocabulary: `Christianity`, `Islam`, `Judaism`, `Hinduism`, `Buddhism`, `Sikhism`. Array because KS4 thematic studies require comparing at least two traditions. |
| `ethical_issue` | string | No | The ethical question being explored. E.g. `"euthanasia"`, `"capital_punishment"`, `"environmental_ethics"`, `"war_and_peace"`. |
| `sacred_texts` | string[] | No | Relevant sacred text references. E.g. `["Genesis 1-2", "Quran 2:30"]`. The AI needs these for generating textually-grounded responses at KS4 level. |
| `rs_strand` | string | No | Enum: `beliefs_and_teachings`, `practices`, `ethics`, `religion_and_society`. Maps to KS4 specification structure. |

### Example Instance

```json
{
  "suggestion_id": "TS-RS-KS4-004",
  "name": "Medical Ethics: Euthanasia",
  "suggestion_type": "prescribed_topic",
  "subject": "Religious Studies",
  "key_stage": "KS4",
  "curriculum_status": "mandatory",
  "pedagogical_rationale": "Euthanasia is a mandatory thematic study that requires pupils to evaluate competing ethical frameworks. It tests the ability to construct sustained, balanced arguments using both religious teachings (sanctity of life, sovereignty of God, compassion) and secular ethical theories (autonomy, utilitarianism, natural law). The topic generates genuine moral engagement because pupils recognise it as a real-world dilemma.",
  "definitions": ["euthanasia", "voluntary euthanasia", "non-voluntary euthanasia", "assisted suicide", "sanctity of life", "quality of life", "autonomy", "palliative care"],
  "themes": ["sanctity of life", "quality of life", "autonomy", "compassion", "suffering"],
  "religion": ["Christianity", "Islam"],
  "ethical_issue": "euthanasia",
  "sacred_texts": ["Genesis 1:27 (image of God)", "Exodus 20:13 (do not kill)", "Quran 4:29 (do not kill yourselves)", "Quran 3:145 (death appointed by Allah)"],
  "rs_strand": "ethics",
  "display_category": "Topic Suggestion",
  "display_color": "#059669",
  "display_icon": "lightbulb"
}
```

---

## Part 6: Citizenship

### Assessment: Share Generic `TopicSuggestion`

Citizenship organises around civic domains (democracy, justice, rights, finance) and activity types (debate, mock election, mock trial, campaign). It does not need its own typed label. Two additional properties on generic `TopicSuggestion` are sufficient.

### Properties on Generic `TopicSuggestion` for Citizenship

| Property | Type | Required (for Citizenship) | Rationale |
|---|---|---|---|
| `themes` | string[] | Yes | |
| `civic_domain` | string | No | Enum: `democracy`, `law_and_justice`, `human_rights`, `personal_finance`, `community_participation`, `media_literacy`. |
| `activity_type` | string | No | Enum: `discussion`, `debate`, `mock_election`, `mock_trial`, `campaign_project`, `research`, `role_play`. Citizenship is highly activity-based. |

### Example Instance

```json
{
  "suggestion_id": "TS-CI-KS3-002",
  "name": "Mock Trial: Justice on Trial",
  "suggestion_type": "teacher_convention",
  "subject": "Citizenship",
  "key_stage": "KS3",
  "curriculum_status": "convention",
  "pedagogical_rationale": "A mock trial brings the abstract concept of the justice system to life through role play. Pupils take on roles (judge, prosecution, defence, jury, witnesses) and must construct arguments from evidence. This develops oracy, critical thinking, and understanding of due process in a way that a textbook study cannot.",
  "definitions": ["defendant", "prosecution", "defence", "jury", "verdict", "evidence", "testimony", "beyond reasonable doubt"],
  "themes": ["criminal justice", "rule of law", "due process", "trial by jury"],
  "civic_domain": "law_and_justice",
  "activity_type": "mock_trial",
  "display_category": "Topic Suggestion",
  "display_color": "#059669",
  "display_icon": "lightbulb"
}
```

---

## Part 7: Drama

### Assessment: Share Generic `TopicSuggestion`

Drama at KS4 (GCSE) has some structural specificity -- practitioner study (Stanislavski, Brecht, Artaud) and performance style (naturalistic, physical theatre, devised). But Drama is KS4 only in the NC (it is not a statutory subject at KS1-KS3), so the total number of TopicSuggestions is small (~10-15). Generic `TopicSuggestion` with two additional properties is sufficient.

### Properties on Generic `TopicSuggestion` for Drama

| Property | Type | Required (for Drama) | Rationale |
|---|---|---|---|
| `themes` | string[] | Yes | |
| `performance_style` | string | No | Enum: `naturalistic`, `physical_theatre`, `devised`, `scripted`, `forum_theatre`, `verbatim`. |
| `practitioner` | string | No | Theatre practitioner. E.g. `"Stanislavski"`, `"Brecht"`, `"Artaud"`, `"Berkoff"`, `"Frantic Assembly"`. GCSE requires study of specific practitioners. |
| `set_text` | string | No | The specific play text being studied. E.g. `"Blood Brothers"`, `"The Curious Incident of the Dog in the Night-Time"`. GCSE has set text components. |

### Example Instance

```json
{
  "suggestion_id": "TS-DR-KS4-003",
  "name": "Brecht and Epic Theatre",
  "suggestion_type": "prescribed_topic",
  "subject": "Drama",
  "key_stage": "KS4",
  "curriculum_status": "mandatory",
  "pedagogical_rationale": "Brecht's Epic Theatre techniques (Verfremdungseffekt, direct audience address, placards, narration) provide a structured toolkit that pupils can apply to their devised work. Understanding Brecht as a counterpoint to naturalism helps pupils make deliberate stylistic choices rather than defaulting to 'realistic acting' for everything.",
  "definitions": ["Verfremdungseffekt", "alienation effect", "epic theatre", "didactic", "gestus", "narration", "direct address", "placard"],
  "themes": ["political theatre", "audience alienation", "social commentary"],
  "performance_style": "devised",
  "practitioner": "Bertolt Brecht",
  "display_category": "Topic Suggestion",
  "display_color": "#059669",
  "display_icon": "lightbulb"
}
```

---

## Part 8: Physical Education

### Assessment: Minimal TopicSuggestion Needs

PE is the subject that needs TopicSuggestions the **least**. PE "topics" are activities (gymnastics, dance, swimming, athletics, team games, OAA), and these are already well-modelled by:

1. The existing **InteractionType** layer -- PE interaction types are already in the graph
2. **Domain** nodes in the PE extraction -- each PE domain IS an activity area (Games, Gymnastics, Dance, Athletics, Swimming, OAA)
3. **VehicleTemplate: `performance`** -- the warm-up / skill-building / rehearsal / performance / evaluation cycle covers PE

PE TopicSuggestions should therefore be sparse -- only where a specific activity unit benefits from richer metadata. For example, "Gymnastics: Balances and Rolls" or "Swimming: Water Safety" might need specific equipment lists and safety notes.

### Properties on Generic `TopicSuggestion` for PE

| Property | Type | Required (for PE) | Rationale |
|---|---|---|---|
| `themes` | string[] | Yes | Activity area. E.g. `["gymnastics", "balances"]` |
| `pe_activity` | string | No | Enum: `gymnastics`, `dance`, `swimming`, `athletics`, `team_games`, `oaa` (outdoor and adventurous activities), `fitness`. |
| `equipment` | string[] | No | Equipment needed. E.g. `["mats", "benches", "balance beams"]`. Important for resource planning. |
| `safety_notes` | string | No | Safety considerations. **Should be required for PE** -- all physical activity has safety requirements. |

I want to be honest: PE TopicSuggestions are borderline unnecessary. The AI tutor's primary generation target is not PE lesson plans -- PE is taught face-to-face by a specialist teacher or sports coach, not via a screen. If the platform is purely digital, PE content will be limited to fitness challenges, dance tutorials, or knowledge quizzes about healthy lifestyles. In that case, `themes` alone is sufficient.

---

## Part 9: Remaining Subjects (Business, Food, Media Studies)

### Business Studies (KS4 only)

`themes` is sufficient. Business topics are knowledge-heavy and well-served by generic `TopicSuggestion`. If needed, add:
- `business_context`: string -- Enum: `enterprise`, `finance`, `marketing`, `operations`, `human_resources`

### Food Preparation & Nutrition (KS4 only)

Food Prep shares DT's cooking strand but is a standalone GCSE subject with more depth. It could share DT's `materials`, `techniques`, `safety_notes`, and `food_allergens` properties. Rather than creating a typed label, use generic `TopicSuggestion` with:
- `food_allergens`: string[] -- same as DT cooking
- `food_skills`: string[] -- same as DT cooking
- `nutrition_focus`: string -- E.g. `"macronutrients"`, `"food_provenance"`, `"food_science"`

### Media Studies (KS4 only)

`themes` is sufficient. Media Studies topics are analytical/knowledge-based. If needed, add:
- `media_form`: string -- Enum: `print`, `broadcast`, `digital`, `film`, `advertising`, `gaming`

---

## Part 10: What This Enables That Generic `TopicSuggestion` Could Not

### Art

| Scenario | Generic `themes` | `ArtTopicSuggestion` |
|---|---|---|
| AI generates a Y3 lesson | `themes: ["Hokusai"]` -- AI guesses at medium, maybe generates a painting lesson | `medium: ["print"], techniques: ["block printing"], visual_elements: ["line", "pattern"]` -- AI generates a printmaking lesson with specific cutting, inking, pressing instructions |
| AI differentiates for DifficultyLevel | No medium-specific differentiation possible | `entry`: stamp a simple wave shape; `developing`: multi-colour layered print; `expected`: composition with foreground/background; `greater_depth`: edition printing with registration |
| Teacher searches for alternatives | No way to find "other KS1 colour mixing artist studies" | `choice_group: "ks1_colour_artist_study"` returns Mondrian, Kandinsky, Kusama as alternatives |
| Equipment planning | AI guesses at materials | `medium: ["print"]` + `techniques: ["block printing"]` = AI generates precise equipment list: lino tiles, lino cutters, rollers, printing ink, paper |

### Music

| Scenario | Generic `themes` | `MusicTopicSuggestion` |
|---|---|---|
| AI generates a Y5 lesson | `themes: ["rock"]` -- AI talks about rock music history | `activity_focus: ["performing"], instrument: ["glockenspiel", "voice"], musical_elements: ["structure", "dynamics"]` -- AI generates a structured performance lesson with warm-up, technique practice, rehearsal, and performance |
| AI chooses VehicleTemplate | Default to `creative_response` (wrong for performance) | `activity_focus: ["performing"]` routes to `performance` VehicleTemplate |
| AI generates listening activity | No piece specified | `piece: "Livin' on a Prayer"`, `listening_repertoire: ["We Will Rock You", ...]` -- AI can generate focused listening questions about structure and dynamics in the specific piece |

### DT

| Scenario | Generic `themes` | `DTTopicSuggestion` |
|---|---|---|
| AI generates a Y2 lesson | `themes: ["mechanisms"]` -- AI explains mechanisms abstractly | `design_brief: "Design and make a moving picture book page with sliders and levers"`, `materials: [...]`, `techniques: [...]` -- AI generates a complete multi-lesson making project |
| Safety planning | No safety data | `safety_notes: "Adult supervision for hole punch. Flatten split pin points."` in system prompt |
| Resource planning | Impossible | `materials: ["card", "split pins", ...]`, `tools: ["scissors", "hole punch"]` -- precise resource list for the school to prepare |

---

## Part 11: Which Subjects Can Share Structure and Which Cannot

### Cannot Share: Art, Music, DT

These three subjects each need their own typed label because:

1. **Art** topics are artist + medium + technique triples. No other subject has this structure.
2. **Music** topics are piece + activity_focus + musical_elements triples. The three-strand (performing/composing/listening) structure is unique to Music.
3. **DT** topics are design_brief + strand + materials triples. The five NC strands make DT internally heterogeneous in a way no other subject is.

These three subjects share nothing structurally with each other or with any other subject. Their "topics" are fundamentally different kinds of things.

### Can Share: Computing, RS, Citizenship, Drama

These four subjects can all use generic `TopicSuggestion` with subject-specific optional properties because:

1. Their topics are knowledge-based or enquiry-based, not material-specification-based
2. Each needs only 2-4 additional properties beyond the universal set
3. The total number of TopicSuggestions per subject is small (10-20 each)
4. The additional properties are genuinely optional -- a generic `themes` array gives the AI enough to work with for basic content generation, even if the specialist properties give better results

### Minimal Need: PE, Business, Food, Media Studies

These subjects can use generic `TopicSuggestion` with `themes` alone, with at most 1-2 additional optional properties. Their topic-suggestion needs are either minimal (PE: activities, not topics) or well-served by `themes` (Business, Media: knowledge-based subjects with straightforward topic structures).

### Summary Table

| Structural Family | Subjects | Label | Subject-Specific Properties |
|---|---|---|---|
| **Own typed label** | Art & Design | `ArtTopicSuggestion` | `artist`, `artist_dates`, `art_movement`, `medium`, `techniques`, `visual_elements`, `unit_type`, `cultural_context` |
| **Own typed label** | Music | `MusicTopicSuggestion` | `composer`, `piece`, `genre`, `musical_elements`, `activity_focus`, `instrument`, `notation_level`, `listening_repertoire`, `mmc_reference` |
| **Own typed label** | Design & Technology | `DTTopicSuggestion` | `dt_strand`, `design_brief`, `materials`, `tools`, `techniques`, `safety_notes`, `evaluation_criteria`, `food_allergens`, `food_skills` |
| **Generic + extensions** | Computing | `TopicSuggestion` | `computational_concept`, `programming_paradigm`, `software_tool`, `output_type` |
| **Generic + extensions** | Religious Studies | `TopicSuggestion` | `religion`, `ethical_issue`, `sacred_texts`, `rs_strand` |
| **Generic + extensions** | Citizenship | `TopicSuggestion` | `civic_domain`, `activity_type` |
| **Generic + extensions** | Drama | `TopicSuggestion` | `performance_style`, `practitioner`, `set_text` |
| **Generic minimal** | PE | `TopicSuggestion` | `pe_activity`, `equipment`, `safety_notes` |
| **Generic minimal** | Business | `TopicSuggestion` | `business_context` |
| **Generic minimal** | Food Prep | `TopicSuggestion` | `food_allergens`, `food_skills`, `nutrition_focus` |
| **Generic minimal** | Media Studies | `TopicSuggestion` | `media_form` |

---

## Part 12: VehicleTemplate Assignments by Subject

The FINAL-SCHEMA proposes 24 VehicleTemplates. For foundation subjects, the key templates are:

| Template | Primary Foundation Subjects | Session Structure | Notes |
|---|---|---|---|
| `creative_response` | **Art** (primary template) | exemplar_exposure -> technique_exploration -> planning -> creating -> critique | Art-centric. Works for Art observational drawing, artist response work, sculpture. |
| `performance` | **Music** (performing), **Drama**, PE | warm_up -> skill_building -> rehearsal -> performance -> evaluation | The performing arts template. |
| `design_make_evaluate` | **DT** (all strands) | explore -> design -> plan -> make -> test -> evaluate -> improve | The mandated DT process. |
| `practical_application` | DT (secondary), **Computing**, Food Prep | context -> skill_rehearsal -> design -> make_or_solve -> evaluate | For projects that are more "apply knowledge" than "creative expression". |
| `ethical_enquiry` | **RS**, **Citizenship** | stimulus -> identify_issue -> explore_perspectives -> construct_argument -> evaluate_positions -> personal_response | Structured ethical reasoning for GCSE-level work. |
| `discussion_and_debate` | RS, Citizenship, Drama | stimulus -> research -> structured_discussion -> writing -> reflection | Lighter-weight than ethical_enquiry. KS1-KS3 RS/Citizenship. |
| `topic_study` | RS (beliefs/teachings), Citizenship | hook -> context -> source_analysis -> interpretation -> argument | For RS systematic theology units. |
| `comparison_study` | RS (comparing religions) | introduce_examples -> systematic_comparison -> analysis -> evaluation | For RS cross-religion comparison. |
| `observation_over_time` | Art (observational drawing) | observation -> recording -> classifying -> pattern_identification | For sustained sketchbook/observational work. |
| `research_enquiry` | Computing (internet research), RS | question -> source_selection -> note_taking -> synthesis -> presentation | For research-based units. |

### Template Gaps for Foundation Subjects

I see no missing templates for foundation subjects after the FINAL-SCHEMA additions. The `performance`, `design_make_evaluate`, and `ethical_enquiry` templates (all new in the FINAL-SCHEMA) close the gaps I identified in my previous review.

One consideration: **Music composing lessons** do not perfectly fit any existing template. The composing process is:
`listen_to_stimulus -> improvise -> structure -> notate -> rehearse -> perform -> evaluate`

This is closest to `creative_response` but with an improvisation phase that `creative_response` lacks (its "technique_exploration" is about learning skills, not free improvisation). For now, Music composing can use `creative_response` with a Music-specific `TEMPLATE_FOR` prompt that inserts the improvisation phase. If Music composing TopicSuggestions become numerous, consider a `composition` template.

---

## Part 13: Relationship Model Summary (All Foundation Subjects)

### Universal Relationships (all TopicSuggestion types)

```cypher
// Core teaching link -- which concepts does this topic deliver?
(ts)-[:DELIVERS_VIA {primary: bool}]->(c:Concept)

// Pedagogical pattern -- which VehicleTemplate does this topic use?
(ts)-[:USES_TEMPLATE]->(vt:VehicleTemplate)

// Domain convenience -- which domain contains this topic?
(:Domain)-[:HAS_SUGGESTION]->(ts)

// Cluster integration -- which clusters suggest this topic?
(:ConceptCluster)-[:SUGGESTED_TOPIC {rank: int}]->(ts)
```

### Additional Relationships

```cypher
// VehicleTemplate age-banded prompts (already in FINAL-SCHEMA)
(:VehicleTemplate)-[:TEMPLATE_FOR {agent_prompt: str}]->(:KeyStage)

// Art choice alternatives (optional -- can use choice_group property instead)
(:ArtTopicSuggestion)-[:ALTERNATIVE_TO]->(:ArtTopicSuggestion)
```

No other foundation-subject-specific relationships are needed. The property model carries sufficient information. Graph relationships should encode **structural** information (what connects to what), not **descriptive** information (metadata about a node). Properties like `artist`, `medium`, `dt_strand` are metadata about the TopicSuggestion node, not connections to other graph entities.

### Why I Am Not Proposing Separate `:Artist`, `:Composer`, `:Piece`, `:Material` Nodes

The brief asks me to consider whether these should be separate nodes. My answer is no, for now, and here is my reasoning:

1. **Query pattern**: The AI tutor's primary query is "give me everything I need to generate a lesson for this concept cluster". This is a single traversal from ConceptCluster through SUGGESTED_TOPIC to TopicSuggestion. All information should be available on the TopicSuggestion node itself, without additional joins.

2. **Node proliferation**: Adding `:Artist` (~50), `:Composer` (~30), `:Piece` (~80), `:Medium` (~12), `:Material` (~30) nodes adds ~200 nodes and ~400+ relationships to the graph. These nodes would have very thin schemas (name, dates, nationality) and serve a narrow use case (cross-topic repertoire analysis).

3. **When to reconsider**: If the platform develops a "curriculum map visualisation" that needs to show "which artists appear across which key stages" or "which composers connect to which historical periods", then extracting `:Artist` and `:Composer` into separate nodes would enable these queries efficiently. But that is a future use case, not a current need.

4. **Data portability**: All the information that would go into separate nodes (artist name, dates, nationality) is stored as properties on the TopicSuggestion. It can be extracted into separate nodes later without data loss.

---

## Part 14: Open Questions

### 1. Art Progression Model

The NC does not specify a KS1-KS2 art progression beyond "develop and share ideas" (KS1) to "improve their mastery" (KS2). School practice typically follows:
- **KS1**: Explore materials, experiment with techniques, begin to describe what they see and make
- **Lower KS2**: Develop techniques with growing control, use sketchbooks, begin to evaluate
- **Upper KS2**: Master techniques, refine work through evaluation, create sustained projects

Should this progression be encoded in the graph? If so, where? Options:
- **DifficultyLevel** -- already exists per concept, already encodes progression
- **A `progression_stage` property** on ArtTopicSuggestion -- e.g. `explore`, `develop`, `master`
- **ConceptCluster SEQUENCED_AFTER chains** -- already encode lesson ordering

My inclination: DifficultyLevel + ConceptCluster sequencing already handles this. No additional property needed.

### 2. Model Music Curriculum Authority

The MMC is non-statutory but widely adopted (~70-80% of schools). Should MMC-aligned TopicSuggestions be `teacher_convention` or should we create a new `curriculum_status` value like `non_statutory_guidance`? The distinction matters: `convention` implies "schools happen to do this", while `non_statutory_guidance` implies "the government recommends this but doesn't require it".

My recommendation: Add `non_statutory_guidance` to the `curriculum_status` enum. The MMC is more authoritative than a mere convention but less authoritative than a statutory requirement. This status also applies to some History topics (e.g. the Historical Association's suggested schemes of work).

### 3. DT Safety Escalation

DT safety requirements escalate dramatically from KS1 (scissors, glue) to KS4 (lathes, soldering irons, brazing, table saws). Should `safety_notes` be a required property at KS3-4 for DT? And should there be a `hazard_level` property (matching Science's `hazard_level`) that the AI uses to calibrate safety language intensity?

My recommendation: Yes to both. Make `safety_notes` required for DT at KS3-4. Add `hazard_level` (enum: `low`, `standard`, `elevated`) to DTTopicSuggestion. A Y2 "fruit salad" project is `low` hazard. A Y9 "electronic product with soldering" is `elevated`.

### 4. Music Performance vs Composition vs Listening Units

Should we require that each MusicTopicSuggestion has a single primary `activity_focus`, or is the MMC's integrated model (all three strands in every unit) more appropriate?

My recommendation: Keep `activity_focus` as `string[]` with the primary strand listed first. The MMC integrates all three strands in most units, but each unit has a clear primary focus (e.g. "Livin' on a Prayer" is primarily performing; "The Planets - Mars" is primarily listening). The AI uses the first element for VehicleTemplate routing (`performing` -> `performance` template; `listening` -> `observation_over_time` or `topic_study`; `composing` -> `creative_response`).

### 5. KS3-KS4 Art Without Named Artists

At KS3-KS4, Art becomes more diverse in its artist references (GCSE specifications name no specific artists, leaving schools to choose). Should KS3-4 ArtTopicSuggestions focus on techniques and movements rather than specific artists?

My recommendation: Yes. KS3-4 entries should have `art_movement` and `medium`/`techniques` as the primary organising properties, with `artist` as truly optional (used for exemplar_topic suggestions like "Study Frida Kahlo's self-portraits as an example of expressionist portraiture"). The `unit_type` property can distinguish: KS1-2 entries will mostly be `artist_study`; KS3-4 entries will mostly be `skill_building` or `gallery_response`.

### 6. Cross-Curricular Relationship vs Property

The `cross_curricular_hooks` property stores connections as strings. Should these instead be graph relationships to TopicSuggestions in other subjects? E.g. `(:ArtTopicSuggestion {name: "Hokusai"})-[:CROSS_CURRICULAR {strength: "strong", hook: "Edo period Japan"}]->(:HistoryTopicSuggestion {name: "Shogunate Japan"})`.

My recommendation: Start with the string property. Graph relationships are better for queryable cross-curricular navigation, but they require that both ends of the relationship exist before either can be created. Since TopicSuggestions will be authored subject-by-subject, cross-curricular relationships would require a second pass after all subjects are imported. The string property can be authored immediately and converted to relationships in a future migration if cross-curricular navigation becomes a core use case.

---

## Appendix A: Node Count Estimates

| Label | KS1 | KS2 | KS3 | KS4 | Total |
|---|---|---|---|---|---|
| `ArtTopicSuggestion` | 10 | 12 | 8 | 6 | ~36 |
| `MusicTopicSuggestion` | 8 | 16 | 10 | 6 | ~40 |
| `DTTopicSuggestion` | 6 | 8 | 10 | 8 | ~32 |
| `TopicSuggestion` (Computing) | 4 | 6 | 6 | 4 | ~20 |
| `TopicSuggestion` (RS) | 0 | 0 | 6 | 12 | ~18 |
| `TopicSuggestion` (Citizenship) | 0 | 0 | 8 | 4 | ~12 |
| `TopicSuggestion` (Drama) | 0 | 0 | 0 | 10 | ~10 |
| `TopicSuggestion` (PE) | 4 | 4 | 4 | 0 | ~12 |
| `TopicSuggestion` (Business) | 0 | 0 | 0 | 6 | ~6 |
| `TopicSuggestion` (Food) | 0 | 0 | 0 | 8 | ~8 |
| `TopicSuggestion` (Media) | 0 | 0 | 0 | 6 | ~6 |
| **Foundation total** | | | | | **~200** |

For context, the graph already has ~9,883 nodes. Adding ~200 TopicSuggestion nodes for all foundation subjects is a modest increase (~2%).

## Appendix B: Controlled Vocabulary Reference

### Art: `medium`
`paint`, `drawing`, `collage`, `sculpture`, `clay`, `print`, `textiles`, `digital`, `photography`, `mixed_media`, `natural_materials`

### Art: `visual_elements`
`colour`, `pattern`, `texture`, `line`, `shape`, `form`, `space`, `tone`

### Art: `unit_type`
`artist_study`, `skill_building`, `gallery_response`, `sketchbook_practice`

### Art: `art_movement` (non-exhaustive, expandable)
`De Stijl`, `Impressionism`, `Post-Impressionism`, `Expressionism`, `Cubism`, `Pop Art`, `Surrealism`, `Abstract Expressionism`, `Land Art`, `Op Art`, `Ukiyo-e`, `Arts and Crafts`, `Art Nouveau`, `Bauhaus`, `Street Art`

### Music: `genre`
`western_classical`, `pop`, `rock`, `jazz`, `blues`, `reggae`, `hip_hop`, `r_and_b`, `folk`, `world_african`, `world_indian`, `world_caribbean`, `world_east_asian`, `film_music`, `musical_theatre`, `electronic`, `action_song`

### Music: `musical_elements`
`pulse`, `rhythm`, `pitch`, `melody`, `dynamics`, `tempo`, `timbre`, `texture`, `structure`, `notation`

### Music: `activity_focus`
`performing`, `composing`, `listening`

### Music: `notation_level`
`none`, `graphic`, `rhythm_only`, `staff_intro`, `staff_standard`

### DT: `dt_strand`
`structures`, `mechanisms`, `textiles`, `cooking_and_nutrition`, `electrical_systems`, `digital_world`

### Computing: `computational_concept`
`algorithm`, `sequence`, `selection`, `repetition`, `variable`, `decomposition`, `abstraction`, `pattern_recognition`, `boolean_logic`, `input_output`, `debugging`, `networking`, `data_representation`, `digital_literacy`

### Computing: `programming_paradigm`
`unplugged`, `block_based`, `text_based`, `markup`

### RS: `religion`
`Christianity`, `Islam`, `Judaism`, `Hinduism`, `Buddhism`, `Sikhism`

### RS: `rs_strand`
`beliefs_and_teachings`, `practices`, `ethics`, `religion_and_society`

### Citizenship: `civic_domain`
`democracy`, `law_and_justice`, `human_rights`, `personal_finance`, `community_participation`, `media_literacy`

### Drama: `performance_style`
`naturalistic`, `physical_theatre`, `devised`, `scripted`, `forum_theatre`, `verbatim`

### PE: `pe_activity`
`gymnastics`, `dance`, `swimming`, `athletics`, `team_games`, `oaa`, `fitness`

---

*Foundation ontology design complete. The three typed labels (Art, Music, DT) are the minimum necessary. The remaining foundation subjects share generic `TopicSuggestion` with targeted property extensions. No universal wrapper can serve all 11 foundation subjects, but the typed-label overhead is constrained to the three subjects that genuinely cannot share structure.*

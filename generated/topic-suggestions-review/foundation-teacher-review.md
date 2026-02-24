# Foundation Subjects Specialist Review: TopicSuggestion + VehicleTemplate Schema

**Reviewer**: Foundation Subjects Specialist (Art & Design, Music, DT, Computing, RE/RS, Citizenship, Drama, PE, Business, Food Preparation & Nutrition, Media Studies)
**Date**: 2026-02-24
**Status**: Complete

---

## Executive Summary

The current proposal bundles 11 extremely diverse subjects under a single generic `TopicSuggestion` label with only `themes` as a subject-specific property. This is insufficient. These subjects span practical making (Art, DT, Food), performance (Music, Drama), abstract reasoning (Computing), ethical enquiry (RS, Citizenship), physical activity (PE), and media literacy (Media Studies). A single catch-all cannot serve them all.

**My core recommendation**: Promote **Art & Design**, **Music**, and **Design & Technology** to their own typed labels. Keep the remaining foundation subjects under generic `TopicSuggestion` but with a richer set of optional properties. Add 3 missing VehicleTemplates.

---

## 1. Subject-Specific Property Review

### The Problem with Generic `TopicSuggestion { themes }`

The five core subjects (History, Geography, Science, English, Maths) each get typed labels with 3-6 subject-specific properties. Meanwhile, Art, Music, DT, Computing, RS, Citizenship, Drama, PE, Business, Food, and Media Studies all share a single `themes` array. This creates an asymmetry that will cripple content generation for foundation subjects.

Consider: an AI tutor generating a Y3 Art lesson on "Colour Mixing" needs to know the **medium** (paint, not collage), the **artist reference** (Mondrian's primary colours), and the **technique** (wet-on-wet mixing). None of this can be expressed in `themes: ["colour"]`.

### Recommendation: Three New Typed Labels

#### A. `ArtTopicSuggestion` — **NEW TYPED LABEL**

Art & Design is taught through the study of specific artists, specific media, and specific techniques. This is a fundamentally different structure from all other subjects. The NC requires pupils to "learn about great artists, architects and designers in history" — artist study IS the topic in Art.

| Property | Type | Required | Rationale |
|---|---|---|---|
| `artist` | string | No | The specific artist being studied (e.g. "Piet Mondrian", "Katsushika Hokusai"). Most Art topics ARE artist studies. |
| `art_movement` | string | No | Contextual period/movement (e.g. "De Stijl", "Impressionism", "Pop Art"). Aids cross-curricular history links. |
| `medium` | string[] | Yes | The physical media used: `paint`, `collage`, `sculpture`, `print`, `digital`, `textiles`, `clay`, `mixed_media`, `drawing`, `photography`. Essential for equipment/material planning. |
| `techniques` | string[] | Yes | Specific techniques taught (e.g. "colour mixing", "perspective drawing", "block printing", "weaving", "shading", "pattern making"). The NC explicitly names "techniques" as a key dimension. |
| `visual_elements` | string[] | No | Which formal elements are the focus: `colour`, `pattern`, `texture`, `line`, `shape`, `form`, `space`, `tone`. Maps directly to NC KS1-KS2 language. |
| `themes` | string[] | No | Retained for thematic context (e.g. "nature", "portrait", "landscape", "abstract"). |

**Why a typed label?** Art topics are fundamentally artist+medium+technique triples. Without `medium` and `techniques`, the AI cannot generate an Art lesson that involves any actual art-making. A generic `themes: ["Mondrian"]` tells the AI nothing about whether the child should be painting, printing, or making collage.

**Commonly taught artists** (from school curriculum maps and commercial schemes):
- **KS1**: Mondrian, Kandinsky, Van Gogh (Sunflowers), Lowry, Andy Goldsworthy, Giuseppe Arcimboldo, Henri Matisse (collage), Yayoi Kusama (dots/pattern)
- **KS2**: Hokusai (The Great Wave), Monet (Water Lilies), William Morris (pattern/print), Bridget Riley (Op Art), Frida Kahlo, David Hockney, Barbara Hepworth (sculpture), Banksy
- **KS3-4**: Wider range by GCSE specification — but artist study remains the primary vehicle

These would be `teacher_convention` type TopicSuggestions — the NC does not name specific artists, but school practice is highly convergent on this list.

#### B. `MusicTopicSuggestion` — **NEW TYPED LABEL**

Music is structured around three activities (performing, composing, listening) and the inter-related dimensions of music. The Model Music Curriculum (2021, non-statutory) provides year-by-year repertoire suggestions that most schools follow closely. Music topics are fundamentally tied to specific pieces, composers, genres, and musical elements in a way that `themes` cannot capture.

| Property | Type | Required | Rationale |
|---|---|---|---|
| `composer` | string | No | Specific composer (e.g. "J.S. Bach", "Beethoven", "Holst"). MMC suggests specific composers per year. |
| `piece` | string | No | Specific piece of music (e.g. "The Planets - Mars", "Brandenburg Concerto No. 5", "In the Hall of the Mountain King"). |
| `genre` | string | No | Musical genre/tradition (e.g. "Western Classical", "Blues", "Jazz", "West African drumming", "Indian raga", "Pop", "Film music"). |
| `musical_elements` | string[] | Yes | Which inter-related dimensions are the focus: `pulse`, `rhythm`, `pitch`, `melody`, `dynamics`, `tempo`, `timbre`, `texture`, `structure`, `notation`. These are the NC's own dimensions. |
| `activity_focus` | string[] | Yes | Which of the three NC strands: `performing`, `composing`, `listening`. A topic might focus on one or span all three. |
| `instrument` | string[] | No | Instruments involved (e.g. "glockenspiel", "recorder", "djembe", "ukulele", "voice"). Important for equipment planning. |
| `themes` | string[] | No | Retained for thematic links (e.g. "storytelling", "weather", "animals"). |

**Why a typed label?** Music lessons are structured around the performing-composing-listening triad and the inter-related dimensions. Without `activity_focus` and `musical_elements`, the AI has no idea whether to generate a singing lesson, a composition task, or a listening analysis. Without `composer`/`piece`, it cannot reference the Model Music Curriculum repertoire that most schools follow.

**Model Music Curriculum** — This DfE publication (2021) is non-statutory but widely adopted. It suggests specific pieces for each year group:
- **Year 1**: Hey You! (hip-hop), Rhythm in the Way We Walk (action songs), simple songs
- **Year 2**: Hands, Feet, Heart (South African music), Ho Ho Ho (Christmas), Zootime
- **Year 3**: Let Your Spirit Fly (R&B), Glockenspiel Stage 1, Three Little Birds (Reggae)
- **Year 4**: Mamma Mia (Pop), Glockenspiel Stage 2, Stop! (Grime)
- **Year 5**: Livin' on a Prayer (Rock), Classroom Jazz 1, Make You Feel My Love (Pop ballad)
- **Year 6**: Happy (Pop), Classroom Jazz 2, A New Year Carol (Benjamin Britten)

These should be `teacher_convention` TopicSuggestions. Additionally, the listening repertoire includes Bach, Handel, Haydn, Beethoven, Mozart, Vivaldi, Holst, Grieg, Puccini — creating rich cross-curricular hooks to History.

#### C. `DTTopicSuggestion` — **NEW TYPED LABEL**

Design & Technology is project-based and structured around five curriculum strands (Structures, Mechanisms, Textiles, Cooking & Nutrition, Electrical Systems). DT topics are fundamentally design briefs — they specify a challenge, materials, and technical focus. This is radically different from knowledge-based subjects.

| Property | Type | Required | Rationale |
|---|---|---|---|
| `dt_strand` | string | Yes | The NC strand: `structures`, `mechanisms`, `textiles`, `cooking_and_nutrition`, `electrical_systems`, `digital_world`. Determines the entire nature of the project. |
| `design_brief` | string | Yes | The challenge or context (e.g. "Design and make a moving picture book using sliders and levers", "Design a healthy sandwich for a class picnic"). DT IS design briefs. |
| `materials` | string[] | Yes | Materials needed (e.g. "card", "split pins", "fabric", "wood", "food ingredients", "electrical components"). Essential for planning and safety. |
| `tools` | string[] | No | Tools used (e.g. "scissors", "needle", "saw", "glue gun", "soldering iron"). Safety-critical at KS3-4. |
| `techniques` | string[] | Yes | Making techniques (e.g. "cutting", "joining", "sewing running stitch", "soldering", "programming"). |
| `evaluation_criteria` | string[] | No | How the product will be assessed against the design brief. Maps to the NC Evaluate domain. |
| `safety_notes` | string | No | Safety information for tools/materials. Critical for DT. |
| `themes` | string[] | No | Retained for thematic context (e.g. "playground", "vehicles", "healthy eating"). |

**Why a typed label?** DT is the only subject where the topic IS a making project. Without `design_brief`, `materials`, and `dt_strand`, the AI cannot generate a DT lesson at all — it would not know whether the child is sewing, sawing, cooking, or coding. The five DT strands are as structurally important to DT as `enquiry_type` is to Science.

**Common DT projects** (from school schemes and D&T Association):
- **KS1**: Moving pictures (sliders/levers), puppets (textiles), fruit salad (cooking), freestanding structures, vehicles with wheels/axles
- **KS2**: Mechanical toys (cams), torches (electrical circuits), stuffed toys (textiles), bread making, frame structures, programmed products
- **KS3**: Electronic products, CAD/CAM, food preparation, smart textiles, architectural models

### D. Remaining Foundation Subjects — KEEP as Generic `TopicSuggestion`

The following subjects should stay under generic `TopicSuggestion` but with an expanded set of optional properties beyond just `themes`:

#### Computing
Add: `computational_concept` (string[]) — e.g. `algorithm`, `sequence`, `selection`, `repetition`, `variable`, `decomposition`, `abstraction`, `networking`, `boolean_logic`
Add: `programming_paradigm` (string) — e.g. `block_based`, `text_based`, `unplugged`
Add: `software_tool` (string) — e.g. `Scratch`, `Python`, `HTML/CSS`, `spreadsheet`

Computing is borderline for its own typed label, but its topic suggestions will be fewer in number than Art/Music/DT. The three properties above, added as optional fields on generic `TopicSuggestion`, are sufficient. If Computing TopicSuggestions grow beyond ~30 nodes, reconsider.

#### Religious Studies
Add: `religion` (string[]) — e.g. `Christianity`, `Islam`, `Judaism`, `Hinduism`, `Buddhism`, `Sikhism`
Add: `ethical_issue` (string) — e.g. `euthanasia`, `war_and_peace`, `environmental_ethics`, `equality`

RS at KS4 (GCSE) has specific content requiring study of at least two religions. The `religion` property is essential. Most schools teach Christianity + Islam (the dominant GCSE combination). These would be `prescribed_topic` (Christianity is mandatory) and `exemplar_topic` (Islam as most common second religion, with Judaism, Hinduism, Buddhism, Sikhism as alternatives).

#### Citizenship
Add: `civic_domain` (string) — e.g. `democracy`, `law_and_justice`, `human_rights`, `personal_finance`, `community_participation`
Add: `activity_type` (string) — e.g. `discussion`, `debate`, `mock_election`, `mock_trial`, `campaign_project`, `research`

Citizenship is highly discussion/activity-based. The `activity_type` helps the AI choose between a structured debate, a mock parliament, or a community action project.

#### Drama (KS4 only)
Add: `performance_style` (string) — e.g. `naturalistic`, `physical_theatre`, `devised`, `scripted`, `forum_theatre`
Add: `practitioner` (string) — e.g. `Stanislavski`, `Brecht`, `Artaud`, `Berkoff`

Drama at GCSE requires study of specific practitioners. Similar to Art's artist study pattern.

#### PE, Business, Food, Media Studies
`themes` is genuinely sufficient for these subjects. PE topics are activity-based (the InteractionType layer already handles this). Business and Media are knowledge-heavy and well-served by `themes` + `definitions`. Food Preparation could share DT's `materials`/`techniques` properties but is better served by the `practical_application` VehicleTemplate.

### Summary Table: Recommended Label Architecture

| Label | Subjects | Subject-Specific Properties |
|---|---|---|
| `ArtTopicSuggestion` | Art & Design | `artist`, `art_movement`, `medium`, `techniques`, `visual_elements`, `themes` |
| `MusicTopicSuggestion` | Music | `composer`, `piece`, `genre`, `musical_elements`, `activity_focus`, `instrument`, `themes` |
| `DTTopicSuggestion` | Design & Technology | `dt_strand`, `design_brief`, `materials`, `tools`, `techniques`, `evaluation_criteria`, `safety_notes`, `themes` |
| `TopicSuggestion` | Computing, RS, Citizenship, Drama, PE, Business, Food, Media Studies | `themes` + extended optional properties (see above) |

This gives us **8 typed labels** total (5 original + 3 new). This is manageable — the graph already has 10+ node types per layer.

---

## 2. Universal Property Review

### KEEP (no changes needed)

| Property | Verdict | Notes |
|---|---|---|
| `suggestion_id` | KEEP | Format works. Art: `TS-AD-KS1-001`, Music: `TS-MU-KS2-001`, DT: `TS-DT-KS1-001` |
| `name` | KEEP | Essential |
| `suggestion_type` | KEEP | All 7 types apply to foundation subjects |
| `subject` | KEEP | Essential |
| `key_stage` | KEEP | Essential |
| `curriculum_status` | KEEP | Essential — especially important for Art/Music where most topics are `convention` not `prescribed` |
| `choice_group` | KEEP | Useful for RS (second religion choice) and Art (artist alternatives) |
| `curriculum_reference` | KEEP | Useful but will be null for many foundation topics — the NC is very sparse for Art/Music |
| `pedagogical_rationale` | KEEP | Essential |
| `common_pitfalls` | KEEP | Highly useful for Art (e.g. "pupils copy Mondrian's grid rather than understanding geometric abstraction") |
| `cross_curricular_hooks` | KEEP | Vital — see Section 6 |
| `definitions` | KEEP | Key vocabulary for every subject |
| `display_*` | KEEP | Standard infrastructure |

### ADD to Universal Properties

| Property | Type | Required | Rationale |
|---|---|---|---|
| `year_groups` | string[] | No | Some foundation topics are strongly year-associated even within a KS. Art KS2 is taught differently in Y3 vs Y6. Music MMC is year-by-year. Adding `["Y3", "Y4"]` helps the AI generate age-appropriate content. Other subjects (History, Geography) also benefit but it's especially critical for Art/Music where the NC gives KS-level only but school practice is year-specific. |
| `duration_lessons` | int | No | How many lessons this topic typically spans. DT projects run 4-6 lessons. Art topics run 4-6 lessons. History topics run 6-12 lessons. This varies hugely by subject and affects lesson planning. Currently only on VehicleTemplate — but teachers think about it per topic too. |

### MODIFY

- `curriculum_reference` — change from `string` to `string[]`. Some foundation topics map to multiple NC statements (e.g. a DT project might reference both "design purposeful products" and "select from a range of tools"). Array is more flexible.

---

## 3. VehicleTemplate Critique

### Existing Templates — Assessment

| # | Template | Verdict | Notes |
|---|---|---|---|
| 1 | `topic_study` | KEEP | Works for RS thematic studies |
| 2 | `case_study` | KEEP | Works for Business |
| 3 | `fair_test` | KEEP | N/A for foundation subjects |
| 4 | `observation_enquiry` | KEEP | Works for Art observational drawing |
| 5 | `pattern_seeking` | KEEP | N/A for most foundation subjects |
| 6 | `research_enquiry` | KEEP | Works for RS, Citizenship research |
| 7 | `text_study` | KEEP | Works for Drama script study |
| 8 | `worked_example_set` | KEEP | Possible for Computing algorithms |
| 9 | `investigation_design` | KEEP | N/A for most foundation subjects |
| 10 | `fieldwork` | KEEP | N/A for foundation subjects |
| 11 | `discussion_and_debate` | KEEP | Works well for RS, Citizenship, Drama — but see below |
| 12 | `creative_response` | **MODIFY** | See detailed critique below |
| 13 | `practical_application` | KEEP | Works for DT, Computing, Food |
| 14 | `comparison_study` | KEEP | Works for RS comparing religions |

### Template #12 `creative_response` — MODIFY

Current session structure: `exemplar_exposure -> technique_exploration -> planning -> creating -> critique`

This template tries to serve Art, Music, DT, Drama, and English — five subjects with fundamentally different creative processes. The session structure is Art-centric (look at exemplar, learn technique, plan, make, evaluate).

**Problem**: This doesn't work for Music. A composing lesson follows: `listening -> improvisation -> structuring -> rehearsal -> performance -> reflection`. A performing lesson follows: `warm_up -> technique -> rehearsal -> performance -> evaluation`. Neither of these maps to "exemplar_exposure -> technique_exploration -> planning -> creating -> critique".

**Recommendation**: Keep `creative_response` but acknowledge it is primarily for Art and visual DT. Add two new templates (see below).

### MISSING Templates — ADD These

#### Template #15: `performance` (Music, Drama, PE)

```
warm_up -> skill_building -> rehearsal -> performance -> evaluation
```

**Subjects**: Music (performing), Drama, PE
**Rationale**: Performance subjects follow a warm-up → practise → perform → evaluate cycle that is fundamentally different from the create-a-product cycle of `creative_response`. Music performing, Drama devised/scripted work, and PE skill acquisition all follow this pattern. The AI tutor needs to know this is a performance lesson, not a making lesson.

**Session structure detail**:
- `warm_up`: Physical/vocal/musical preparation (scales, vocal exercises, physical warm-up)
- `skill_building`: Focused technique practice (rhythmic patterns, character work, ball skills)
- `rehearsal`: Applying skills in context (rehearsing the piece/scene/routine)
- `performance`: Presenting to an audience (even if just the class)
- `evaluation`: Self and peer assessment against criteria

#### Template #16: `design_make_evaluate` (DT specifically)

```
explore -> design -> plan -> make -> test -> evaluate -> improve
```

**Subjects**: Design & Technology (all strands)
**Rationale**: DT follows a specific iterative design process that is mandated by the NC: "design, make, evaluate". This is not the same as `creative_response` (which is about artistic expression) or `practical_application` (which is about applying knowledge). The DT process includes explicit design criteria, technical drawing/modelling, material selection, making with tools, testing against criteria, and iterative improvement. The `practical_application` template is close but misses the design and evaluation phases that are central to DT's identity as a subject.

**Session structure detail**:
- `explore`: Investigate existing products (NC Evaluate domain)
- `design`: Generate ideas through drawing, modelling, CAD
- `plan`: Select materials, sequence steps, identify tools
- `make`: Construct using appropriate tools and techniques
- `test`: Test product against design criteria
- `evaluate`: Assess fitness for purpose, suggest improvements
- `improve`: Iterate on design (if time allows)

#### Template #17: `ethical_enquiry` (RS, Citizenship, PSHE)

```
stimulus -> identify_issue -> explore_perspectives -> construct_argument -> evaluate_positions -> personal_response
```

**Subjects**: Religious Studies, Citizenship, PSHE (and some History/English)
**Rationale**: The `discussion_and_debate` template is close but too generic. RS and Citizenship at KS3-4 require structured ethical reasoning — not just "discuss". GCSE RS requires pupils to "evaluate the significance and coherence of different beliefs from both insider and outsider perspectives" and "construct and evaluate ethical arguments using religious and non-religious perspectives". This needs a more rigorous enquiry structure than stimulus → discussion → reflection.

**Session structure detail**:
- `stimulus`: Present the ethical dilemma or issue (case study, news story, sacred text, thought experiment)
- `identify_issue`: Name the ethical question precisely
- `explore_perspectives`: Examine religious and non-religious viewpoints systematically
- `construct_argument`: Build a reasoned position with evidence
- `evaluate_positions`: Assess strengths/weaknesses of different positions
- `personal_response`: Formulate a justified personal view (required for GCSE AO2)

### Updated VehicleTemplate Count: 17

This is a modest increase (14 → 17) and each new template serves a genuine pedagogical gap. The AI tutor cannot generate a good Music performance lesson, DT design project, or RS ethical enquiry using the existing 14 templates.

---

## 4. TopicSuggestion Inventory

### Art & Design

#### KS1 (`ArtTopicSuggestion`)

| Name | Type | Medium | Artist | Curriculum Status |
|---|---|---|---|---|
| Colour Mixing | `prescribed_topic` | paint | — | `mandatory` (NC: "using colour") |
| Drawing from Observation | `prescribed_topic` | drawing | — | `mandatory` (NC: "develop and share ideas") |
| Collage Making | `prescribed_topic` | collage | — | `mandatory` (NC: "range of materials") |
| Sculpture and 3D | `prescribed_topic` | clay, sculpture | — | `mandatory` (NC: "sculpture") |
| Printing | `teacher_convention` | print | — | `convention` |
| Mondrian Colour Study | `teacher_convention` | paint | Piet Mondrian | `convention` |
| Kandinsky Circles | `teacher_convention` | paint, collage | Wassily Kandinsky | `convention` |
| Van Gogh Sunflowers | `teacher_convention` | paint | Vincent van Gogh | `convention` |
| Lowry Matchstick Men | `teacher_convention` | paint, drawing | L.S. Lowry | `convention` |
| Arcimboldo Portraits | `teacher_convention` | collage, mixed_media | Giuseppe Arcimboldo | `convention` |

#### KS2 (`ArtTopicSuggestion`)

| Name | Type | Medium | Artist | Curriculum Status |
|---|---|---|---|---|
| Sketchbook Practice | `prescribed_topic` | drawing | — | `mandatory` (NC: "create sketch books") |
| Perspective Drawing | `teacher_convention` | drawing | — | `convention` |
| Hokusai The Great Wave | `teacher_convention` | paint, print | Katsushika Hokusai | `convention` |
| Monet Water Lilies | `teacher_convention` | paint | Claude Monet | `convention` |
| William Morris Pattern | `teacher_convention` | print, textiles | William Morris | `convention` |
| Bridget Riley Op Art | `teacher_convention` | paint, drawing | Bridget Riley | `convention` |
| Hepworth Sculpture | `teacher_convention` | sculpture, clay | Barbara Hepworth | `convention` |
| Frida Kahlo Self-Portrait | `teacher_convention` | paint | Frida Kahlo | `convention` |
| Andy Goldsworthy Nature Art | `teacher_convention` | natural materials | Andy Goldsworthy | `convention` |

Each of these needs `medium`, `techniques`, and `visual_elements` populated — these are not optional luxuries, they are the core data the AI needs.

### Music

#### KS1-KS2 (`MusicTopicSuggestion`)

The Model Music Curriculum provides year-by-year repertoire. These should be `teacher_convention` TopicSuggestions:

| Name | Year | Activity Focus | Genre | Curriculum Status |
|---|---|---|---|---|
| Hey You! | Y1 | performing, listening | Hip-hop | `convention` (MMC) |
| Rhythm in the Way We Walk | Y1 | performing | Action song | `convention` (MMC) |
| Hands, Feet, Heart | Y2 | performing, listening | South African | `convention` (MMC) |
| Let Your Spirit Fly | Y3 | performing, composing | R&B | `convention` (MMC) |
| Glockenspiel Stage 1 | Y3 | performing | Instrumental | `convention` (MMC) |
| Three Little Birds | Y3 | performing, listening | Reggae | `convention` (MMC) |
| Mamma Mia | Y4 | performing, listening | Pop | `convention` (MMC) |
| Livin' on a Prayer | Y5 | performing, listening | Rock | `convention` (MMC) |
| Classroom Jazz 1 | Y5 | performing, composing | Jazz | `convention` (MMC) |
| Happy | Y6 | performing, listening | Pop | `convention` (MMC) |
| A New Year Carol | Y6 | performing, listening | Classical | `convention` (MMC) |

**Classical listening repertoire** (cross-year, from MMC appendices):
| Name | Type | Composer | Curriculum Status |
|---|---|---|---|
| The Planets - Mars | `teacher_convention` | Holst | `convention` |
| In the Hall of the Mountain King | `teacher_convention` | Grieg | `convention` |
| The Four Seasons - Spring | `teacher_convention` | Vivaldi | `convention` |
| Symphony No. 5 (opening) | `teacher_convention` | Beethoven | `convention` |
| Carnival of the Animals | `teacher_convention` | Saint-Saens | `convention` |
| Nessun Dorma | `teacher_convention` | Puccini | `convention` |
| Brandenburg Concerto No. 5 | `teacher_convention` | J.S. Bach | `convention` |

### Design & Technology

#### KS1 (`DTTopicSuggestion`)

| Name | DT Strand | Design Brief | Curriculum Status |
|---|---|---|---|
| Moving Pictures | `mechanisms` | Design a picture book page with a slider or lever | `teacher_convention` |
| Freestanding Structures | `structures` | Build a structure that can stand on its own and support weight | `prescribed_topic` (NC: "build structures") |
| Fruit Salad | `cooking_and_nutrition` | Plan and make a healthy fruit salad | `teacher_convention` |
| Hand Puppets | `textiles` | Design and make a hand puppet using a template | `teacher_convention` |
| Vehicles with Wheels | `mechanisms` | Make a vehicle that moves using wheels and axles | `teacher_convention` |
| Healthy Wraps | `cooking_and_nutrition` | Design a healthy wrap or sandwich | `teacher_convention` |

#### KS2 (`DTTopicSuggestion`)

| Name | DT Strand | Design Brief | Curriculum Status |
|---|---|---|---|
| Mechanical Toys (Cams) | `mechanisms` | Design a toy that uses a cam mechanism | `teacher_convention` |
| Torches | `electrical_systems` | Design and make a torch with a working circuit | `teacher_convention` |
| Bread Making | `cooking_and_nutrition` | Follow and adapt a bread recipe | `prescribed_topic` (NC: "prepare and cook... savoury dishes") |
| Stuffed Toys | `textiles` | Design and make a stuffed toy using backstitch | `teacher_convention` |
| Frame Structures | `structures` | Design a frame structure for a specific purpose | `teacher_convention` |
| Programmed Products | `electrical_systems` | Create a product that uses programming/control | `teacher_convention` |
| Sewing a Tote Bag | `textiles` | Design and make a bag with decorative stitching | `teacher_convention` |

### Computing (generic `TopicSuggestion` with extended properties)

| Name | Type | Computational Concept | Paradigm | Curriculum Status |
|---|---|---|---|---|
| Algorithms and Sequences | `prescribed_topic` | algorithm, sequence | unplugged, block_based | `mandatory` |
| Debugging Programs | `prescribed_topic` | debugging, logical_reasoning | block_based | `mandatory` |
| Selection (If-Then) | `prescribed_topic` | selection, boolean_logic | block_based | `mandatory` |
| Repetition (Loops) | `prescribed_topic` | repetition, iteration | block_based | `mandatory` |
| Variables | `prescribed_topic` | variable, input_output | block_based, text_based | `mandatory` |
| Internet and Networks | `prescribed_topic` | networking | — | `mandatory` |
| Online Safety | `prescribed_topic` | digital_literacy | — | `mandatory` |
| Scratch Animation | `teacher_convention` | sequence, repetition, event | block_based (Scratch) | `convention` |
| Python Introduction | `teacher_convention` | sequence, variable, selection | text_based (Python) | `convention` |
| HTML/CSS Web Design | `teacher_convention` | markup, structure | text_based (HTML/CSS) | `convention` |

### Religious Studies (generic `TopicSuggestion` with `religion` + `ethical_issue`)

| Name | Type | Religion(s) | Curriculum Status |
|---|---|---|---|
| Christianity: Beliefs & Teachings | `prescribed_topic` | Christianity | `mandatory` (GCSE: Christianity compulsory) |
| Islam: Beliefs & Practices | `exemplar_topic` | Islam | `exemplar` (most common 2nd religion ~70%) |
| Judaism: Beliefs & Practices | `exemplar_topic` | Judaism | `exemplar` (common in London/Manchester) |
| Hinduism: Beliefs & Practices | `exemplar_topic` | Hinduism | `exemplar` (some specifications) |
| Buddhism: Beliefs & Practices | `exemplar_topic` | Buddhism | `exemplar` (some specifications) |
| Medical Ethics | `prescribed_topic` | Christianity, Islam | `mandatory` (GCSE thematic study) |
| War and Peace | `prescribed_topic` | Christianity, Islam | `mandatory` (GCSE thematic study) |
| Crime and Punishment | `prescribed_topic` | Christianity, Islam | `mandatory` (GCSE thematic study) |
| Religion and Life | `prescribed_topic` | Christianity, Islam | `mandatory` (GCSE thematic study) |
| Pilgrimage and Holy Places | `teacher_convention` | Christianity, Islam | `convention` |

### Citizenship (generic `TopicSuggestion` with `civic_domain` + `activity_type`)

| Name | Type | Civic Domain | Curriculum Status |
|---|---|---|---|
| Parliamentary Democracy | `prescribed_topic` | democracy | `mandatory` |
| The Justice System | `prescribed_topic` | law_and_justice | `mandatory` |
| Human Rights | `prescribed_topic` | human_rights | `mandatory` |
| Elections and Voting | `prescribed_topic` | democracy | `mandatory` |
| Personal Finance and Tax | `prescribed_topic` | personal_finance | `mandatory` |
| Mock Election | `teacher_convention` | democracy | `convention` (activity_type: mock_election) |
| Mock Trial | `teacher_convention` | law_and_justice | `convention` (activity_type: mock_trial) |

---

## 5. Content Generation Requirements

### What the AI Needs Per Subject

#### Art Lesson Generation
The AI needs:
1. **Artist reference** with enough context to explain their work to a child (not just a name)
2. **Medium** to specify materials in the lesson plan (you can't say "paint like Hepworth" — she's a sculptor)
3. **Techniques** with age-appropriate step-by-step guidance
4. **Visual elements** to focus the learning (this lesson is about line and shape, not colour)
5. **DifficultyLevel** integration: "entry" = copy a Mondrian grid; "expected" = create original geometric composition inspired by Mondrian; "greater_depth" = explain how Mondrian's use of primary colours creates visual balance

**Without the typed label**: The AI would receive `themes: ["Mondrian"]` and have no idea whether to generate a painting lesson, a collage lesson, or an art history discussion. It would not know which visual elements to focus on. It could not differentiate difficulty levels meaningfully.

#### Music Lesson Generation
The AI needs:
1. **Activity focus** — is this a singing, composing, or listening lesson?
2. **Musical elements** — which dimensions are being taught?
3. **Piece/composer** — for listening lessons, what are we listening to? For performing, what are we learning?
4. **Instrument** — glockenspiel and recorder lessons are very different from singing lessons
5. **DifficultyLevel** integration: "entry" = keep the pulse while singing; "expected" = sing in tune with expression; "greater_depth" = sing in a round or two-part harmony

**Without the typed label**: The AI would receive `themes: ["rhythm"]` and generate a generic rhythm discussion. With the typed label, it knows this is a performing lesson using djembe drums focusing on pulse and rhythm through West African polyrhythmic patterns.

#### DT Lesson Generation
The AI needs:
1. **Design brief** — the challenge that frames the entire project
2. **DT strand** — determines whether this is a making, cooking, or coding project
3. **Materials and tools** — for safety planning and resource lists
4. **Techniques** — specific making skills being practised
5. **Evaluation criteria** — how pupils will assess their products

**Without the typed label**: The AI would receive `themes: ["mechanisms"]` and have no basis for generating a multi-lesson DT project with design criteria, material lists, safety notes, and evaluation rubrics.

#### Video Script Generation
For Art: needs artist images (copyright considerations!), technique demonstration steps, visual element identification
For Music: needs audio references (licensing!), notation if appropriate, instrument technique demonstrations
For DT: needs materials close-up, tool use demonstration, step-by-step making process
For RS: needs sacred text references, religious practice footage context, ethical scenario dramatisation

#### Assessment Generation
With DifficultyLevels already in the graph, the AI can generate differentiated assessments. But it needs subject-specific properties to make these meaningful:
- Art: "At developing level, mix secondary colours. At expected level, mix tertiary colours and explain warm/cool colour theory."
- DT: "At entry level, follow a given design. At expected level, design to meet criteria. At greater depth, iterate on design after testing."

---

## 6. Cross-Curricular Hooks

Foundation subjects are rich in cross-curricular connections. The `cross_curricular_hooks` property on TopicSuggestion should capture these:

### Art & Design
- **History**: Artist study maps to historical period (Mondrian → 1920s De Stijl; William Morris → Victorian Arts & Crafts; Hokusai → Edo period Japan)
- **Geography**: Landscape painting → local/contrasting environments; Goldsworthy → environmental art
- **Science**: Colour mixing → light and colour; materials → properties of materials
- **Maths**: Tessellation → geometry; perspective → scale/proportion; Mondrian → right angles and parallel lines
- **DT**: Textiles techniques shared; sculpture → structures

### Music
- **History**: Composers map to historical periods (Handel → Georgian; Beethoven → Napoleonic era; Holst → WW1; Britten → 20th century Britain)
- **Maths**: Rhythm → fractions and patterns; notation → number lines; tempo → speed/rate
- **Science**: Sound → vibrations, pitch, frequency; instruments → materials and sound production
- **Geography**: World music → places and cultures (West African drumming, Indian raga, Caribbean reggae)
- **English**: Song lyrics → poetry; opera → storytelling; ballads → narrative

### Design & Technology
- **Science**: Electrical circuits → electrical systems; forces → mechanisms; materials → properties; nutrition → healthy eating
- **Maths**: Measurement → making accurately; geometry → structures; data → evaluation
- **Computing**: Programming → control technology; CAD → digital design
- **Art**: Textile techniques overlap; aesthetic design considerations
- **Geography**: Sustainable materials → environmental geography; food miles → trade

### Computing
- **Maths**: Algorithms → logical reasoning; variables → algebra; data → statistics
- **Science**: Data logging → fair tests; simulations → modelling
- **English**: Blogging → writing for audience; digital storytelling

### Religious Studies
- **History**: Religious history maps to historical periods; Reformation → Tudor/Stuart; Crusades → medieval
- **Geography**: Pilgrimage routes; distribution of world religions
- **English**: Sacred texts as literature; ethical argument → persuasive writing
- **Citizenship**: Human rights → religious freedom; ethics → law and morality
- **Art**: Religious art (stained glass, Islamic geometric patterns, Hindu mandalas)

### Citizenship
- **History**: Development of democracy; Magna Carta; suffrage; civil rights movements
- **Geography**: Global governance; migration; trade; environmental policy
- **Maths**: Personal finance → budgeting, percentages, interest rates
- **English**: Media literacy → persuasive writing; debate skills

---

## 7. Stress Test Scenarios

### Scenario 1: Y3 Art — "Study Hokusai's Great Wave, then create a printing block inspired by waves"

**What the AI needs from the graph:**
- `ArtTopicSuggestion`: name="Hokusai The Great Wave", artist="Katsushika Hokusai", art_movement="Ukiyo-e", medium=["print"], techniques=["block printing", "colour layering"], visual_elements=["line", "pattern", "shape", "form"], themes=["water", "nature", "Japan"]
- `VehicleTemplate`: `creative_response` — exemplar_exposure (study the print) -> technique_exploration (practise cutting/rolling) -> planning (design wave pattern) -> creating (print) -> critique (evaluate)
- Cross-curricular hooks: Geography (Japan), History (Edo period), Science (waves/water)
- DifficultyLevel: entry=simple wave shape stamp; developing=multi-colour layered print; expected=composition with foreground/background; greater_depth=edition printing with registration

**Does the current schema handle this?** NO — without `medium`, the AI might generate a painting lesson. Without `techniques`, it won't know to include printing-specific instructions (cutting lino, rolling ink, pressing). Without `artist`, it has no reference point for the exemplar study.

**With proposed schema?** YES — all required information is in the typed `ArtTopicSuggestion` node.

### Scenario 2: Y5 Music — "Perform 'Livin' on a Prayer' with glockenspiel accompaniment, focusing on structure and dynamics"

**What the AI needs from the graph:**
- `MusicTopicSuggestion`: name="Livin' on a Prayer", composer="Bon Jovi", piece="Livin' on a Prayer", genre="Rock", musical_elements=["structure", "dynamics", "tempo"], activity_focus=["performing"], instrument=["glockenspiel", "voice"], themes=["determination", "working together"]
- `VehicleTemplate`: `performance` — warm_up (vocal exercises, glockenspiel scales) -> skill_building (learn verse melody, practise dynamics) -> rehearsal (put together with accompaniment) -> performance (class performance) -> evaluation (did we control dynamics?)
- DifficultyLevel: entry=keep the pulse while performing; developing=perform melody accurately; expected=perform with expression and dynamic contrast; greater_depth=add an improvised glockenspiel counter-melody

**Does the current schema handle this?** NO — `themes: ["rock music"]` gives the AI almost nothing. The `creative_response` template has the wrong session structure (it's for making, not performing). There's no way to specify which musical elements are the focus.

**With proposed schema?** YES — the typed `MusicTopicSuggestion` plus the `performance` VehicleTemplate covers everything.

### Scenario 3: Y2 DT — "Design and make a moving picture book using sliders and levers"

**What the AI needs from the graph:**
- `DTTopicSuggestion`: name="Moving Pictures", dt_strand="mechanisms", design_brief="Design a picture book page with moving parts using sliders and levers", materials=["card", "split pins", "paper fasteners", "straws", "cardboard strips"], tools=["scissors", "hole punch", "ruler"], techniques=["cutting", "joining with split pins", "creating slider tracks", "lever mechanisms"], safety_notes="Adult supervision for hole punch. Ensure split pin points are flattened.", themes=["storytelling", "animals"]
- `VehicleTemplate`: `design_make_evaluate` — explore (look at existing moving books) -> design (draw plan with moving parts marked) -> plan (choose materials) -> make (cut, assemble, test mechanism) -> test (does the slider move smoothly?) -> evaluate (does it tell the story?) -> improve (adjust if needed)

**Does the current schema handle this?** NO — `themes: ["mechanisms"]` provides no design brief, no materials list, no safety information. The `practical_application` template doesn't include the explore/design/evaluate phases that are core to DT.

**With proposed schema?** YES — the typed `DTTopicSuggestion` plus the `design_make_evaluate` VehicleTemplate provides everything for a multi-lesson DT project.

### Scenario 4: Y10 RS — "Evaluate whether euthanasia can ever be morally justified, comparing Christian and Islamic perspectives"

**What the AI needs from the graph:**
- `TopicSuggestion`: name="Medical Ethics: Euthanasia", themes=["sanctity of life", "quality of life", "autonomy", "compassion"], religion=["Christianity", "Islam"], ethical_issue="euthanasia", curriculum_status="mandatory"
- `VehicleTemplate`: `ethical_enquiry` — stimulus (case study of terminally ill patient) -> identify_issue (is euthanasia ever justified?) -> explore_perspectives (Christian: sanctity of life, God as giver/taker; Islamic: Allah determines death, suffering as test; Secular: autonomy, utilitarian reduction of suffering) -> construct_argument (write a reasoned paragraph) -> evaluate_positions (strengths/weaknesses of each) -> personal_response (justify own view with evidence)
- DifficultyLevel: emerging=describe one religious view; developing=explain two contrasting views; secure=evaluate with reasons; mastery=construct a sustained, balanced argument with textual references

**Does the current schema handle this?** PARTIALLY — `themes` could capture the ethical concepts, but without `religion` the AI doesn't know which traditions to draw on. Without `ethical_enquiry` template, it would use `discussion_and_debate` which is less rigorous for GCSE-level ethical reasoning.

**With proposed schema?** YES — the extended `TopicSuggestion` with `religion` and `ethical_issue` properties, plus the `ethical_enquiry` VehicleTemplate, provides the structured data needed for GCSE RS content generation.

---

## 8. Summary: Top 3 Recommendations

### 1. Add Three Typed Labels: `ArtTopicSuggestion`, `MusicTopicSuggestion`, `DTTopicSuggestion`

**Impact: Critical**

These three subjects have fundamentally different topic structures from all other subjects and from each other. Art topics are artist+medium+technique triples. Music topics are piece+activity+element triples. DT topics are design_brief+strand+material triples. None of these can be expressed as `themes: [string]`. Without typed labels, the AI cannot generate meaningful lessons for these subjects — it would produce generic discussions about art rather than actual art-making lessons.

The NC Art curriculum explicitly requires "drawing, painting and sculpture" and "colour, pattern, texture, line, shape, form and space" — these are medium and visual element properties. The NC Music curriculum is structured around "performing, composing, listening" and "the inter-related dimensions of music" — these are activity_focus and musical_elements properties. The NC DT curriculum is structured around "design, make, evaluate" across five technical strands — these are the design_brief, dt_strand, and evaluation_criteria properties.

This is not over-engineering. This is reading the NC and modelling what it actually says.

### 2. Add Three VehicleTemplates: `performance`, `design_make_evaluate`, `ethical_enquiry`

**Impact: High**

The existing 14 templates miss three major pedagogical patterns:
- **Performance** (warm_up -> skill_building -> rehearsal -> performance -> evaluation) — required for Music performing, Drama, and PE
- **Design-Make-Evaluate** (explore -> design -> plan -> make -> test -> evaluate -> improve) — the mandated DT process
- **Ethical Enquiry** (stimulus -> identify_issue -> explore_perspectives -> construct_argument -> evaluate_positions -> personal_response) — required for GCSE RS and KS3-4 Citizenship ethical reasoning

Without these, the AI tutor would force Music performance lessons into an art-making template, DT projects into a generic practical template, and GCSE ethical arguments into a casual discussion format. Each of these would produce pedagogically incorrect lessons.

### 3. Extend Generic `TopicSuggestion` with Subject-Keyed Optional Properties

**Impact: Medium**

For the remaining foundation subjects (Computing, RS, Citizenship, Drama, PE, Business, Food, Media Studies), adding a small set of optional properties to the generic label prevents the need for 8+ more typed labels while still giving the AI enough subject-specific data:
- Computing: `computational_concept`, `programming_paradigm`, `software_tool`
- RS: `religion`, `ethical_issue`
- Citizenship: `civic_domain`, `activity_type`
- Drama: `performance_style`, `practitioner`

These can be implemented as optional properties on the generic `TopicSuggestion` label without creating additional labels. The alternative — forcing these subjects into `themes`-only — would mean the AI tutor couldn't distinguish a Python programming lesson from a digital literacy lesson, or a Christianity lesson from an Islam lesson.

---

## Appendix: Property Count Comparison

| Approach | Labels | Max Properties Per Label | Total Properties Across All Labels |
|---|---|---|---|
| Current proposal (5 typed + 1 generic) | 6 | 6 (History) | ~30 |
| This recommendation (8 typed + extended generic) | 8 | 8 (DT) | ~55 |
| Full typed (1 per subject) | 17 | 8 (DT) | ~100+ |

The recommended approach adds 2 labels and ~25 properties. This is a modest increase for a very large gain in content generation quality for foundation subjects that cover approximately 40% of curriculum time.

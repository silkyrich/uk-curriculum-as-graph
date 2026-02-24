# History Ontology Design: A Subject-Specific Graph Model

**Author**: KS2 + KS3 History Specialist
**Date**: 2026-02-24
**Status**: DESIGN PROPOSAL -- for review by curriculum lead and content architect

---

## 1. Why History Needs Its Own Ontology

The universal `TopicSuggestion` wrapper failed History for three structural reasons:

1. **History topics are not suggestions.** A "topic suggestion" implies optionality. But Stone Age to Iron Age, Roman Britain, and the Holocaust are statutory requirements. The NC prescribes them. What varies is not WHETHER to teach them but HOW -- which sources to use, which enquiry questions to foreground, which interpretations to explore. The node should model the topic itself, not a suggestion about it.

2. **History topics have internal temporal structure.** Roman Britain is not a blob of content -- it runs from 43 AD to 410 AD with a chronological spine of events. The Vikings follow the Anglo-Saxons, which follow the Romans. This chronological ordering is not a convenience -- it is the subject's foundational organising principle. No universal schema captured this.

3. **History has a distinctive disciplinary grammar.** Every History topic foregrounds particular second-order (disciplinary) concepts: cause and consequence, change and continuity, similarity and difference, significance, evidence and interpretation, chronology. These determine what KIND of thinking the AI should demand. A Science topic foregrounds enquiry types. A Maths topic foregrounds CPA stages. These are not interchangeable.

The proposal below gives History exactly what it needs: nodes that model what History topics actually are, relationships that capture how they connect chronologically and thematically, and properties that give an AI tutor everything it needs to generate disciplined historical thinking.

---

## 2. Node Labels

### Three labels, each serving a distinct purpose.

| Label | Purpose | Count (est.) | Why not collapse? |
|---|---|---|---|
| `HistoryStudy` | The historical topic/period/theme being studied | ~50 (KS1-KS3) | This is the core unit: Roman Britain, the Holocaust, Florence Nightingale & Mary Seacole. It carries all the rich subject-specific metadata. |
| `DisciplinaryConcept` | The six second-order historical thinking concepts | 6 | These are the intellectual backbone of History education. They exist independently of any topic and apply across all key stages. Making them nodes (not just string arrays) enables querying: "Which KS2 topics foreground cause and consequence?" |
| `HistoricalSource` | Named canonical sources used across topics | ~80-120 | The Bayeux Tapestry appears in both Medieval Britain (KS3) and Vikings (KS2 context). The Anglo-Saxon Chronicle appears in Anglo-Saxons and Vikings. Making sources nodes eliminates duplication and enables "Which topics use this source?" queries. |

### Why `HistoryStudy` and not `HistoryTopicSuggestion`?

The word "study" comes from the NC itself: "a local history study", "a depth study of one of the following", "a study of an aspect or theme." This is the NC's own vocabulary. The word "suggestion" implies the platform is recommending something optional. "Study" is neutral and accurate -- it models the curriculum requirement, whether prescribed, exemplar, or open-slot.

### Why `DisciplinaryConcept` as a node?

In the universal schema, `disciplinary_concepts` was a string array property on the topic. This works for simple queries but fails when you need:
- "Show me all topics that foreground cause and consequence, ordered by key stage" (requires filtering across all nodes)
- "How does the emphasis on evidence and interpretation develop from KS1 to KS3?" (requires comparing across topics linked to the same concept)
- "Which disciplinary concepts does this pupil need more practice with?" (requires aggregating across their learning history)

Six small, permanent nodes with rich properties solve all three. The `FOREGROUNDS` relationship from `HistoryStudy` to `DisciplinaryConcept` carries `rank` (1 = primary) and `ks_guidance` (how this concept looks at this key stage).

### Why `HistoricalSource` as a node?

Sources are the evidence base of History. They are reusable across topics, they have their own properties (type, provenance, date, museum location), and they are the basis for the `source_enquiry` VehicleTemplate. Making them nodes enables:
- "Which topics use primary written sources?" (filter by source type)
- "Show me all sources from the British Museum collection" (filter by location)
- "The Vindolanda tablets -- which topics reference them?" (reverse lookup)

This is not over-engineering. The existing ContentVehicle data already names ~60 distinct sources across KS2-KS3. Promoting them to nodes adds query power at minimal cost.

---

## 3. Property Tables

### 3.1 HistoryStudy

| Property | Type | Required | Rationale |
|---|---|---|---|
| **`study_id`** | string | Yes | Unique ID. Format: `HS-{KS}-{NNN}`. e.g. `HS-KS2-001` |
| **`name`** | string | Yes | Display name. e.g. "Stone Age to Iron Age Britain" |
| **`study_type`** | string (enum) | Yes | See controlled vocabulary below. Captures the NC's own categorisation of what kind of study this is. |
| **`subject`** | string | Yes | Always `"History"`. Enables cross-label queries via `display_category`. |
| **`key_stage`** | string | Yes | `"KS1"`, `"KS2"`, `"KS3"` |
| **`curriculum_status`** | string (enum) | Yes | `mandatory`, `menu_choice`, `exemplar`, `convention`. Identical to universal schema -- this works. |
| **`choice_group`** | string | No | Groups mutually exclusive NC choices. e.g. `"ks2_ancient_civ_depth_study"`, `"ks2_non_european_contrast"`. Null for mandatory/convention topics. |
| **`curriculum_reference`** | string[] | No | Direct quotes from the NC Programme of Study. |
| **`period`** | string | Yes | Human-readable period string. e.g. `"c.800,000 BC - 43 AD"`, `"Varies by locality"` |
| **`period_start_year`** | integer | No | Machine-readable. Negative for BCE. e.g. `-800000`, `43`, `1066`. Null for open-slot topics. |
| **`period_end_year`** | integer | No | Machine-readable. Null for ongoing or open-slot. |
| **`significance_claim`** | string | Yes | 1-2 sentences explaining why this topic matters historically. This is not a pedagogical rationale (why teach it) but a historical claim (why it is significant). The AI uses this to frame lesson introductions and assessment questions. |
| **`pedagogical_rationale`** | string | Yes | Why this topic works pedagogically at this key stage. What skills it develops, what prior knowledge it builds on. |
| **`enquiry_questions`** | string[] | No (recommended) | The overarching historical questions that frame teaching. These are the questions a teacher plans a sequence around. e.g. `["Why did the Romans invade Britain?", "How far did the Romans change Britain?"]` |
| **`key_figures`** | string[] | No | Historical figures central to this study. For KS1 paired studies, the figures appear here AND in `comparison_pairs`. |
| **`comparison_pairs`** | object[] | No | KS1 paired figure studies only. Each: `{ "figure_a": str, "figure_b": str, "comparison_focus": str }`. Captures the NC's explicit requirement for paired comparison. |
| **`key_events`** | string[] | No | Events that form the chronological spine. Ordered chronologically. |
| **`perspectives`** | string[] | Yes | Contemporary viewpoints -- how people AT THE TIME experienced events. e.g. `["Roman coloniser", "Briton", "Roman soldier", "enslaved person"]`. The AI uses these for empathy activities ("Write from the perspective of...") and multi-perspective source analysis. |
| **`interpretations`** | string[] | No | Historiographical debates -- how HISTORIANS have subsequently understood the past. e.g. `["Was Romanisation beneficial or destructive for British culture?"]`. Required for KS3, optional for KS2. The AI uses these for analytical essay questions and discussion/debate activities. |
| **`source_types`** | string[] | Yes | Controlled vocabulary (see below). The types of evidence available for this topic. Even open-slot topics can specify expected source types. The AI uses this to determine the pedagogical approach: archaeological sources demand inference activities, written sources demand provenance analysis. |
| **`definitions`** | string[] | Yes | Substantive vocabulary (centurion, pharaoh) AND disciplinary vocabulary (chronology, significance). Pre-teaching targets. |
| **`common_pitfalls`** | string[] | No | Teacher-identified mistakes when teaching this topic. Direct guidance for the AI tutor on what NOT to do. |
| **`cross_curricular_hooks`** | object[] | No | Structured: `{ "subject": str, "hook": str, "strength": "strong"|"moderate"|"light" }`. Enables the AI to make meaningful cross-curricular connections. |
| **`sensitive_content_notes`** | string[] | No | Safeguarding and pedagogical sensitivity guidance. This platform serves children aged 5-14. An AI generating a Holocaust lesson or a slavery lesson without sensitivity guidance is a safeguarding failure. |
| **`year_groups`** | string[] | No | Typical year groups this is taught in. e.g. `["Y3", "Y4"]`. |
| **`duration_lessons`** | integer | No | Typical number of lessons for this study. |
| **`display_category`** | string | Yes | `"History Study"` |
| **`display_color`** | string | Yes | `"#059669"` (Emerald-600, matching Topic layer) |
| **`display_icon`** | string | Yes | `"auto_stories"` (Material Icons -- book/story, appropriate for History) |

### `study_type` Controlled Vocabulary (7 values)

| Value | Meaning | KS | Examples |
|---|---|---|---|
| `period_study` | Chronological study of a defined historical period | KS2, KS3 | Stone Age to Iron Age, Roman Britain, Medieval Britain 1066-1509 |
| `civilisation_study` | Depth study of an ancient or non-European civilisation | KS2, KS3 | Ancient Egypt, The Shang Dynasty, Early Islamic Civilisation, Mughal India |
| `thematic_study` | Study of a theme or aspect across a period | KS2, KS3 | British History Beyond 1066, Ideas Power Industry and Empire |
| `significant_individual` | Study of a named individual or paired individuals | KS1 | Florence Nightingale, Edith Cavell |
| `paired_figure_study` | NC-specified paired comparison of individuals | KS1 | Nightingale & Seacole, Elizabeth I & Victoria, Columbus & Armstrong |
| `event_study` | Study of a specific event and its significance | KS1, KS2 | Great Fire of London, Moon Landings |
| `local_history_study` | Enquiry rooted in the pupil's own locality | KS1, KS2 | "Significant Local History", "Local History Study" |

These are not interchangeable with the universal `suggestion_type` values. They reflect how History actually categorises its curriculum units. The distinction between `period_study` and `civilisation_study` matters because they have different pedagogical patterns: period studies are chronological narratives; civilisation studies are thematic explorations of achievement.

### `source_types` Controlled Vocabulary

```
primary_written, primary_visual, primary_archaeological, primary_cartographic,
primary_statistical, primary_legal, primary_administrative, primary_artistic,
primary_audiovisual, primary_technological, oral_tradition, oral_testimony,
built_heritage, museum_artefact, secondary_written, testimony
```

### 3.2 DisciplinaryConcept

| Property | Type | Required | Rationale |
|---|---|---|---|
| **`concept_id`** | string | Yes | `DC-001` through `DC-006` |
| **`name`** | string | Yes | e.g. "Cause and Consequence" |
| **`slug`** | string | Yes | Machine-readable: `cause_and_consequence`, `chronology`, etc. |
| **`description`** | string | Yes | What this concept means in History education. |
| **`key_question`** | string | Yes | The question this concept asks. e.g. "Why did this happen, and what were the effects?" |
| **`ks1_guidance`** | string | Yes | How this concept looks at KS1. e.g. "Focus on simple before/after sequencing and personal timelines." |
| **`ks2_guidance`** | string | Yes | How this concept looks at KS2. |
| **`ks3_guidance`** | string | Yes | How this concept looks at KS3. |
| **`agent_prompt`** | string | Yes | Direct instruction for the AI tutor. e.g. "When generating questions for this concept, always ask WHY something happened and WHAT resulted, not just WHAT happened." |
| **`question_stems`** | string[] | Yes | Reusable question frames. e.g. `["Why did ___ happen?", "What were the consequences of ___?", "Was ___ the most important cause of ___?"]` |
| **`display_category`** | string | Yes | `"History Study"` |
| **`display_color`** | string | Yes | `"#7C3AED"` (Violet-600, matching ThinkingLens layer) |
| **`display_icon`** | string | Yes | `"psychology"` (Material Icons -- thinking/brain) |

**The six concepts:**

| # | Name | Slug | Key Question |
|---|---|---|---|
| 1 | Chronology | `chronology` | When did this happen, and how does it fit into the wider timeline? |
| 2 | Cause and Consequence | `cause_and_consequence` | Why did this happen, and what were the effects? |
| 3 | Change and Continuity | `change_and_continuity` | What changed, what stayed the same, and why? |
| 4 | Similarity and Difference | `similarity_and_difference` | How was this similar to or different from other times, places, or peoples? |
| 5 | Significance | `significance` | Why does this matter, and to whom? |
| 6 | Evidence and Interpretation | `evidence_and_interpretation` | How do we know about this, and how do historians disagree? |

### 3.3 HistoricalSource

| Property | Type | Required | Rationale |
|---|---|---|---|
| **`source_id`** | string | Yes | `HSRC-{NNN}`. e.g. `HSRC-001` |
| **`name`** | string | Yes | e.g. "Vindolanda Tablets" |
| **`source_type`** | string | Yes | From controlled vocabulary above. e.g. `"primary_written"` |
| **`date_description`** | string | No | Human-readable date range. e.g. "c.85-130 AD" |
| **`date_start_year`** | integer | No | Machine-readable. |
| **`date_end_year`** | integer | No | Machine-readable. |
| **`provenance`** | string | No | Who created it, when, and why. Essential for source analysis activities. |
| **`location`** | string | No | Where it can be seen today. e.g. "British Museum", "Vindolanda Museum" |
| **`url`** | string | No | Link to a digital version or museum page. |
| **`pedagogical_use`** | string | Yes | How an AI tutor should use this source. e.g. "Ask pupils to read the tablet and infer what daily life was like for a Roman soldier. Then ask what the tablet CANNOT tell us." |
| **`key_stage_suitability`** | string[] | Yes | Which key stages this source is appropriate for. e.g. `["KS2", "KS3"]` |
| **`sensitivity_notes`** | string | No | If the source requires careful handling. e.g. Holocaust photographs. |
| **`display_category`** | string | Yes | `"History Study"` |
| **`display_color`** | string | Yes | `"#B45309"` (Amber-700 -- evokes archival materials) |
| **`display_icon`** | string | Yes | `"source"` (Material Icons) |

---

## 4. Relationship Model

### 4.1 Relationships from HistoryStudy

```
// Curriculum integration (connects to existing graph)
(:Domain)-[:HAS_STUDY]->(:HistoryStudy)
(:HistoryStudy)-[:DELIVERS_VIA {primary: bool}]->(:Concept)
(:HistoryStudy)-[:USES_TEMPLATE]->(:VehicleTemplate)

// Disciplinary thinking
(:HistoryStudy)-[:FOREGROUNDS {rank: int, ks_guidance: str}]->(:DisciplinaryConcept)
    // rank=1 is the primary disciplinary focus. A topic typically foregrounds 3-4 concepts.
    // ks_guidance explains how this concept manifests at this topic's key stage.

// Evidence base
(:HistoryStudy)-[:USES_SOURCE {purpose: str}]->(:HistoricalSource)
    // purpose explains WHY this source is used for this topic.
    // e.g. "Primary evidence of daily life in Roman Britain"

// Chronological ordering (the spine of History)
(:HistoryStudy)-[:CHRONOLOGICALLY_FOLLOWS]->(:HistoryStudy)
    // Within a key stage's British chronology:
    // Stone Age -> Roman Britain -> Anglo-Saxons -> Vikings (KS2)
    // Medieval -> Church/State 1509-1745 -> Elizabethan -> Industry/Empire -> Challenges 1901+ (KS3)
    // This is NOT mere sequence -- it models that Anglo-Saxons FOLLOW Romans historically.

// Cross-KS progression (chronological continuity)
(:HistoryStudy {study_id: 'HS-KS2-004'})-[:CHRONOLOGICALLY_FOLLOWS]->(:HistoryStudy {study_id: 'HS-KS3-001'})
    // Vikings (KS2, ends 1066) -> Medieval Britain (KS3, starts 1066)
    // This models the NC's explicit chronological progression from KS2 to KS3.

// Thematic connections (not chronological)
(:HistoryStudy)-[:THEMATICALLY_LINKED {theme: str}]->(:HistoryStudy)
    // e.g. Roman Britain -[:THEMATICALLY_LINKED {theme: "empire and resistance"}]-> Ideas/Power/Empire
    // e.g. Ancient Egypt -[:THEMATICALLY_LINKED {theme: "river civilisations"}]-> Ancient Sumer
    // These are bidirectional in intent but stored as directed relationships for graph convention.

// Comparison pairs (KS2 non-European contrast requirement)
(:HistoryStudy)-[:CONTRASTS_WITH {comparison_focus: str}]->(:HistoryStudy)
    // e.g. Early Islamic Civilisation -[:CONTRASTS_WITH {comparison_focus: "while Anglo-Saxon England was
    //       politically fragmented, Baghdad was the world's greatest centre of learning"}]-> Anglo-Saxons
    // Models the NC requirement that non-European societies "provide contrasts with British history"
```

### 4.2 Relationships from DisciplinaryConcept

```
// Progression between key stages (how the concept develops)
(:DisciplinaryConcept)-[:DEVELOPS_THROUGH {from_ks: str, to_ks: str, progression_note: str}]->(:DisciplinaryConcept)
    // Self-relationship with different key stage metadata.
    // Actually, since DisciplinaryConcept nodes are key-stage-independent, this is better
    // modelled as a property on the FOREGROUNDS relationship (ks_guidance).
    // So no explicit inter-DC relationships needed.
```

### 4.3 Relationships from HistoricalSource

```
// Sources are linked to topics via USES_SOURCE (see above)
// Sources can also link to each other:
(:HistoricalSource)-[:CORROBORATES]->(:HistoricalSource)
    // e.g. Vindolanda Tablets CORROBORATES Roman coins (both provide evidence of Roman daily life)
    // OPTIONAL -- only add where the corroboration is pedagogically useful

(:HistoricalSource)-[:CONTRADICTS {note: str}]->(:HistoricalSource)
    // e.g. Anglo-Saxon Chronicle CONTRADICTS Viking sagas (different perspectives on the same events)
    // This enables the AI to create source comparison activities: "These two sources describe
    // the same event differently. Why might that be?"
```

### 4.4 Relationship Diagram (ASCII)

```
                                    (:VehicleTemplate)
                                          ^
                                          |
                                     USES_TEMPLATE
                                          |
(:Domain)--HAS_STUDY-->(:HistoryStudy)--DELIVERS_VIA-->(:Concept)
                            |    |    |
                            |    |    +--FOREGROUNDS {rank, ks_guidance}-->(:DisciplinaryConcept)
                            |    |
                            |    +--USES_SOURCE {purpose}-->(:HistoricalSource)
                            |
                            +--CHRONOLOGICALLY_FOLLOWS-->(:HistoryStudy)
                            +--THEMATICALLY_LINKED {theme}-->(:HistoryStudy)
                            +--CONTRASTS_WITH {comparison_focus}-->(:HistoryStudy)
```

---

## 5. Example Instances

### 5.1 KS1 Paired Figure Study: Florence Nightingale & Mary Seacole

```json
{
  "study_id": "HS-KS1-005",
  "name": "Florence Nightingale & Mary Seacole",
  "study_type": "paired_figure_study",
  "subject": "History",
  "key_stage": "KS1",
  "curriculum_status": "exemplar",
  "choice_group": null,
  "curriculum_reference": [
    "NC KS1 History: 'the lives of significant individuals in the past who have contributed to national and international achievements. Some should be used to compare aspects of life in different periods [for example, Elizabeth I and Queen Victoria, Christopher Columbus and Neil Armstrong, William Caxton and Tim Berners-Lee, Pieter Bruegel the Elder and LS Lowry, Rosa Parks and Emily Davison, Mary Seacole and/or Florence Nightingale and Edith Cavell]'"
  ],
  "period": "1820-1910",
  "period_start_year": 1820,
  "period_end_year": 1910,
  "significance_claim": "Nightingale transformed nursing into a respected evidence-based profession. Seacole's parallel achievements, long overlooked due to racial prejudice, reveal how historical recognition is shaped by social context.",
  "pedagogical_rationale": "The pairing develops the disciplinary concept of significance: both women contributed to healthcare, but their recognition differed dramatically. This comparison introduces KS1 pupils to the idea that history involves selection and that some people are overlooked. It also develops similarity and difference through comparing two contemporaries from different backgrounds.",
  "enquiry_questions": [
    "Why are Florence Nightingale and Mary Seacole both significant?",
    "Why was Florence Nightingale famous in her lifetime while Mary Seacole was forgotten?"
  ],
  "key_figures": ["Florence Nightingale", "Mary Seacole"],
  "comparison_pairs": [
    {
      "figure_a": "Florence Nightingale",
      "figure_b": "Mary Seacole",
      "comparison_focus": "Both contributed to nursing in the Crimean War, but their backgrounds, methods and recognition differed dramatically. Explore why."
    }
  ],
  "key_events": ["Crimean War 1853-56", "Nightingale at Scutari Hospital", "Seacole's British Hotel near Balaclava"],
  "perspectives": ["Florence Nightingale", "Mary Seacole", "wounded soldier", "Victorian society"],
  "interpretations": null,
  "source_types": ["primary_visual", "primary_written"],
  "definitions": ["significant", "nurse", "Crimean War", "hospital", "contribution", "recognition", "prejudice"],
  "common_pitfalls": [
    "Reducing the lesson to biography recitation rather than exploring WHY these figures are significant",
    "Treating Seacole as an add-on to Nightingale's story rather than a significant figure in her own right",
    "Avoiding discussion of racial prejudice, which is central to understanding why Seacole was forgotten"
  ],
  "sensitive_content_notes": [
    "Seacole experienced racial prejudice; discuss age-appropriately as unfairness based on skin colour",
    "War involves injury and death; focus on the caring response rather than the violence"
  ],
  "cross_curricular_hooks": [
    {"subject": "English", "hook": "Writing recounts and diary entries from Nightingale or Seacole's perspective", "strength": "strong"},
    {"subject": "Science", "hook": "Hygiene and handwashing: why did Nightingale insist on cleanliness?", "strength": "moderate"}
  ],
  "year_groups": ["Y1", "Y2"],
  "duration_lessons": 6,
  "display_category": "History Study",
  "display_color": "#059669",
  "display_icon": "auto_stories"
}
```

**Relationships:**
- `FOREGROUNDS` -> DC "Significance" (rank 1, ks_guidance: "At KS1, significance means asking 'Why do we remember this person?' and 'What difference did they make?'")
- `FOREGROUNDS` -> DC "Similarity and Difference" (rank 2, ks_guidance: "At KS1, compare two people: what was the same and what was different about their lives?")
- `USES_SOURCE` -> "Photograph of Mary Seacole" (purpose: "Compare with Nightingale portraits to discuss how each was represented")
- `USES_SOURCE` -> "Nightingale's Notes on Nursing" (purpose: "Simplified extract showing her evidence-based approach to hygiene")
- `DELIVERS_VIA` -> HI-KS1-C003 "Significant Individuals and Their Impact" (primary: true)
- `DELIVERS_VIA` -> HI-KS1-C001 "Time and Chronology" (primary: false)

### 5.2 KS2 Prescribed Period Study: Roman Britain

```json
{
  "study_id": "HS-KS2-002",
  "name": "Roman Britain",
  "study_type": "period_study",
  "subject": "History",
  "key_stage": "KS2",
  "curriculum_status": "mandatory",
  "choice_group": null,
  "curriculum_reference": [
    "NC KS2 History: 'The Roman Empire and its impact on Britain'"
  ],
  "period": "43 AD - 410 AD",
  "period_start_year": 43,
  "period_end_year": 410,
  "significance_claim": "The Roman occupation fundamentally transformed Britain's infrastructure, culture and identity, leaving a legacy of roads, towns, language and law that shaped subsequent British history.",
  "pedagogical_rationale": "Roman Britain provides an outstanding case study for cause and consequence: why did the Romans invade, and what were the lasting effects? The rich primary source base (Vindolanda tablets, coins, archaeological remains) makes this ideal for developing evidence skills.",
  "enquiry_questions": [
    "Why did the Romans invade Britain, and what were the consequences?",
    "What can the Vindolanda tablets tell us about everyday life in Roman Britain?",
    "How significant was the Roman legacy in modern Britain?"
  ],
  "key_figures": ["Boudicca", "Julius Caesar", "Claudius", "Hadrian"],
  "comparison_pairs": null,
  "key_events": [
    "Roman invasion 43 AD",
    "Boudicca's revolt 60-61 AD",
    "Building of Hadrian's Wall 122 AD",
    "Roman withdrawal c.410 AD"
  ],
  "perspectives": ["Roman coloniser", "Briton", "Roman soldier", "enslaved person"],
  "interpretations": [
    "Historians debate whether Romanisation was imposed by force or adopted willingly by British elites seeking status",
    "The reasons for the Roman withdrawal remain contested: economic decline, military pressure, or political fragmentation?"
  ],
  "source_types": ["primary_written", "primary_archaeological", "built_heritage"],
  "definitions": ["centurion", "legion", "Romanisation", "villa", "amphitheatre", "mosaic", "aqueduct", "revolt", "empire"],
  "common_pitfalls": [
    "Presenting the Romans as unambiguously civilising rather than examining the violence and exploitation of conquest",
    "Neglecting the perspective of the indigenous Britons",
    "Reducing Boudicca to a simple hero narrative without examining the complexity of her revolt"
  ],
  "sensitive_content_notes": [
    "Slavery was integral to the Roman economy; discuss with appropriate sensitivity",
    "The conquest involved significant violence against indigenous peoples; present balanced perspectives"
  ],
  "cross_curricular_hooks": [
    {"subject": "English", "hook": "Diary writing as a Roman soldier or Boudicca; Latin roots in English vocabulary", "strength": "strong"},
    {"subject": "Mathematics", "hook": "Roman numerals; measuring distances along Roman roads", "strength": "moderate"},
    {"subject": "Design & Technology", "hook": "Roman building techniques: arches, aqueducts, mosaics", "strength": "strong"},
    {"subject": "Geography", "hook": "Roman roads and settlement patterns", "strength": "moderate"}
  ],
  "year_groups": ["Y3", "Y4"],
  "duration_lessons": 12,
  "display_category": "History Study",
  "display_color": "#059669",
  "display_icon": "auto_stories"
}
```

**Relationships:**
- `FOREGROUNDS` -> DC "Cause and Consequence" (rank 1)
- `FOREGROUNDS` -> DC "Significance" (rank 2)
- `FOREGROUNDS` -> DC "Evidence and Interpretation" (rank 3)
- `FOREGROUNDS` -> DC "Change and Continuity" (rank 4)
- `USES_SOURCE` -> "Vindolanda Tablets" (purpose: "Evidence of daily life for ordinary Roman soldiers in northern Britain")
- `USES_SOURCE` -> "Hadrian's Wall" (purpose: "Physical evidence of the frontier of Roman power and its defensive needs")
- `USES_SOURCE` -> "Roman coins and pottery" (purpose: "Evidence of trade, economy and Romanisation across Britain")
- `CHRONOLOGICALLY_FOLLOWS` -> HS-KS2-001 "Stone Age to Iron Age Britain"
- `CHRONOLOGICALLY_FOLLOWS` is followed by -> HS-KS2-003 "Anglo-Saxon and Scots Settlement"
- `THEMATICALLY_LINKED` -> HS-KS3-004 "Ideas, Power, Industry and Empire" (theme: "empire, colonisation and resistance")
- `DELIVERS_VIA` -> HI-KS2-C005 "Historical Skills and Source Analysis" (primary: true)
- `DELIVERS_VIA` -> HI-KS2-C001 "Cause and Consequence" (primary: false)
- `HAS_STUDY` from Domain HI-KS2-D002 "British History"

### 5.3 KS3 Statutory Sensitive Topic: The Holocaust

```json
{
  "study_id": "HS-KS3-006",
  "name": "The Holocaust",
  "study_type": "thematic_study",
  "subject": "History",
  "key_stage": "KS3",
  "curriculum_status": "mandatory",
  "choice_group": null,
  "curriculum_reference": [
    "NC KS3 History: 'the Holocaust'",
    "The only specific historical event named as a mandatory standalone topic in the KS3 curriculum"
  ],
  "period": "1933 - 1945",
  "period_start_year": 1933,
  "period_end_year": 1945,
  "significance_claim": "The Holocaust is the defining moral catastrophe of the twentieth century, and understanding how it happened is essential for developing the vigilance and values needed to prevent future genocides.",
  "pedagogical_rationale": "Teaching about the Holocaust develops pupils' understanding of how ideology, propaganda, dehumanisation and bureaucracy can combine to produce genocide. It connects to broader themes of human rights, prejudice and the responsibilities of citizenship. The UCL Centre for Holocaust Education provides evidence-based guidance on effective teaching approaches.",
  "enquiry_questions": [
    "How did persecution escalate from discrimination to genocide, and could it have been stopped?",
    "What can testimony tell us that other historical sources cannot?",
    "Why does the Holocaust matter today, and what is our responsibility to remember?"
  ],
  "key_figures": ["Anne Frank", "Primo Levi", "Oskar Schindler", "Kindertransport children"],
  "comparison_pairs": null,
  "key_events": [
    "Nuremberg Laws 1935",
    "Kristallnacht 1938",
    "Kindertransport 1938-39",
    "Wannsee Conference 1942",
    "Liberation of Auschwitz 1945"
  ],
  "perspectives": ["Jewish victim", "rescuer", "bystander", "perpetrator", "liberator"],
  "interpretations": [
    "The question of when the Nazi regime decided on the 'Final Solution' (intentionalist vs functionalist debate) remains a central historiographical discussion",
    "Historians debate the extent to which ordinary Germans knew about and participated in the Holocaust"
  ],
  "source_types": ["primary_written", "testimony", "primary_legal", "primary_visual"],
  "definitions": ["antisemitism", "Holocaust", "genocide", "persecution", "ghetto", "concentration camp", "Kindertransport", "remembrance"],
  "common_pitfalls": [
    "Jumping straight to death camps without teaching the gradual escalation from discrimination to genocide",
    "Reducing the Holocaust to statistics rather than using individual testimony to establish the human reality",
    "Treating the Holocaust as inevitable rather than examining choices made at each stage",
    "Using graphic imagery without pedagogical justification; the UCL Centre advises against shock tactics"
  ],
  "sensitive_content_notes": [
    "This topic requires particular sensitivity and careful planning; follow UCL Centre for Holocaust Education and Holocaust Educational Trust guidance",
    "Be aware of Jewish pupils who may have family connections to the Holocaust",
    "Avoid comparisons that trivialise the Holocaust; use precise historical language",
    "The perpetrator/bystander/rescuer framework should not be a simple moral judgement exercise",
    "Some pupils may find testimony and images distressing; prepare them and provide support",
    "Roma, disabled, LGBT+ and other victim groups should not be omitted from the narrative"
  ],
  "cross_curricular_hooks": [
    {"subject": "English", "hook": "Anne Frank's diary and Primo Levi's testimony as both literature and historical source", "strength": "strong"},
    {"subject": "Religious Studies", "hook": "The moral and theological questions raised by the Holocaust", "strength": "strong"},
    {"subject": "Citizenship", "hook": "Human rights frameworks developed in response to the Holocaust; genocide prevention", "strength": "strong"}
  ],
  "year_groups": ["Y8", "Y9"],
  "duration_lessons": 8,
  "display_category": "History Study",
  "display_color": "#059669",
  "display_icon": "auto_stories"
}
```

**Relationships:**
- `FOREGROUNDS` -> DC "Cause and Consequence" (rank 1, ks_guidance: "At KS3, pupils should construct multi-causal explanations showing how ideology, propaganda, bureaucracy and individual choices combined to produce genocide")
- `FOREGROUNDS` -> DC "Evidence and Interpretation" (rank 2, ks_guidance: "At KS3, pupils must learn to use testimony as a distinct source type, understanding its strengths (personal experience, emotional truth) and limitations (memory, selectivity)")
- `FOREGROUNDS` -> DC "Significance" (rank 3)
- `USES_SOURCE` -> "Anne Frank's Diary" (purpose: "Personal testimony showing the human reality of persecution and hiding", sensitivity_notes present)
- `USES_SOURCE` -> "Nuremberg Trial Transcripts" (purpose: "Legal/documentary evidence of the mechanics of genocide and the concept of crimes against humanity")
- `THEMATICALLY_LINKED` -> HS-KS3-005 "Challenges 1901 to Present Day" (theme: "The Holocaust is contextualised within the broader 20th-century challenge theme")

### 5.4 KS2 Open Slot: Local History Study

```json
{
  "study_id": "HS-KS2-005",
  "name": "Local History Study",
  "study_type": "local_history_study",
  "subject": "History",
  "key_stage": "KS2",
  "curriculum_status": "mandatory",
  "choice_group": null,
  "curriculum_reference": [
    "NC KS2 History: 'a local history study'"
  ],
  "period": "Varies by locality",
  "period_start_year": null,
  "period_end_year": null,
  "significance_claim": "Local history demonstrates that every community has a past worth studying, and that national historical forces are experienced and shaped at the local level.",
  "pedagogical_rationale": "Local history makes the abstract concrete by connecting historical concepts to places pupils know. It provides the most accessible route to primary sources (census records, old maps, local museum artefacts) and develops skills of historical enquiry in a personally meaningful context.",
  "enquiry_questions": [
    "How has our local area changed over time, and why?",
    "What can local primary sources tell us that national history books cannot?",
    "Who are the most significant people in the history of our area?"
  ],
  "key_figures": [],
  "comparison_pairs": null,
  "key_events": [],
  "perspectives": ["Local resident (past)", "Local resident (present)", "Historian/archaeologist"],
  "interpretations": [
    "Different community groups may have contrasting memories and interpretations of local change",
    "The selection of which local history to teach itself reflects judgements about what matters"
  ],
  "source_types": ["primary_written", "primary_cartographic", "museum_artefact", "primary_visual", "oral_testimony"],
  "definitions": ["primary source", "secondary source", "census", "Ordnance Survey", "archive", "oral history", "heritage"],
  "common_pitfalls": [
    "Choosing a topic too broad (entire history of the town) rather than a specific aspect or period",
    "Relying solely on secondary sources when local primary sources are often readily available",
    "Failing to connect the local study to the broader national narrative"
  ],
  "sensitive_content_notes": [
    "Local history may uncover difficult aspects including poverty, industrial exploitation or displacement",
    "Oral history from community elders may raise sensitive personal or family memories"
  ],
  "cross_curricular_hooks": [
    {"subject": "Geography", "hook": "Map skills: comparing old and new OS maps of the local area", "strength": "strong"},
    {"subject": "Mathematics", "hook": "Census data analysis: population change, occupations, household sizes", "strength": "moderate"},
    {"subject": "English", "hook": "Writing a local history guide; conducting and recording oral history interviews", "strength": "strong"}
  ],
  "year_groups": ["Y3", "Y4", "Y5", "Y6"],
  "duration_lessons": 8,
  "display_category": "History Study",
  "display_color": "#059669",
  "display_icon": "auto_stories"
}
```

**Relationships:**
- `FOREGROUNDS` -> DC "Evidence and Interpretation" (rank 1)
- `FOREGROUNDS` -> DC "Change and Continuity" (rank 2)
- `FOREGROUNDS` -> DC "Significance" (rank 3)
- `USES_TEMPLATE` -> VT "source_enquiry" (for census/map analysis activities)
- `USES_TEMPLATE` -> VT "local_history_enquiry" (proposed new template)
- No `CHRONOLOGICALLY_FOLLOWS` -- local history sits outside the chronological spine
- No `USES_SOURCE` for specific sources -- the open-slot nature means sources are locality-dependent

---

## 6. What This Enables That the Universal TopicSuggestion Could Not

### 6.1 Chronological querying

```cypher
// "Show me the KS2 British History chronological sequence"
MATCH (s1:HistoryStudy)-[:CHRONOLOGICALLY_FOLLOWS]->(s2:HistoryStudy)
WHERE s1.key_stage = 'KS2' AND s1.study_type = 'period_study'
RETURN s1.name, s2.name
ORDER BY s1.period_start_year
```

The universal schema had no mechanism for chronological ordering between topics. In History, this is foundational -- you cannot understand the Anglo-Saxons without knowing the Romans came first.

### 6.2 Disciplinary concept progression

```cypher
// "How does 'cause and consequence' develop from KS1 to KS3?"
MATCH (s:HistoryStudy)-[f:FOREGROUNDS]->(dc:DisciplinaryConcept {slug: 'cause_and_consequence'})
WHERE f.rank = 1
RETURN s.key_stage, s.name, f.ks_guidance
ORDER BY s.key_stage
```

This query is impossible with a string array property. Promoting disciplinary concepts to nodes with the `FOREGROUNDS` relationship enables curriculum-wide analysis of how historical thinking develops.

### 6.3 Source reuse and cross-reference

```cypher
// "Which topics use the Bayeux Tapestry, and for what purpose?"
MATCH (s:HistoryStudy)-[u:USES_SOURCE]->(src:HistoricalSource {name: 'Bayeux Tapestry'})
RETURN s.name, s.key_stage, u.purpose
```

The universal schema stored sources as a flat string array. This ontology enables the AI to say: "You studied the Bayeux Tapestry when you learned about the Vikings. Now in KS3, we're going to look at it again, but this time we'll analyse it as propaganda rather than just a narrative."

### 6.4 Sensitive content filtering

```cypher
// "Show all topics with sensitivity notes for the AI content filter"
MATCH (s:HistoryStudy)
WHERE s.sensitive_content_notes IS NOT NULL AND size(s.sensitive_content_notes) > 0
RETURN s.name, s.sensitive_content_notes
```

This was technically possible with the universal schema too, but having `sensitive_content_notes` as a first-class property on a dedicated label makes it visible and auditable -- essential for a platform serving children.

### 6.5 AI lesson generation with disciplinary framing

The universal schema gave the AI a flat list of properties. This ontology gives the AI a structured query path:

1. Fetch the `HistoryStudy` node for the topic
2. Follow `FOREGROUNDS` to get the ranked disciplinary concepts with age-banded guidance
3. Follow `USES_SOURCE` to get specific sources with pedagogical instructions
4. Follow `CHRONOLOGICALLY_FOLLOWS` to situate the topic in the broader narrative
5. Follow `THEMATICALLY_LINKED` to suggest connections to other topics
6. Read `sensitive_content_notes` to apply safeguarding guardrails
7. Read `enquiry_questions` to frame the lesson around genuine historical investigation

This is the difference between "tell me about the Romans" and "explain WHY the Romans invaded Britain, using evidence from the Vindolanda tablets, while being sensitive to the fact that the conquest involved significant violence against indigenous peoples."

### 6.6 Contrast pairs for cross-cultural comparison

```cypher
// "What should I compare Early Islamic Civilisation with?"
MATCH (s1:HistoryStudy {study_id: 'HS-KS2-012'})-[c:CONTRASTS_WITH]->(s2:HistoryStudy)
RETURN s2.name, c.comparison_focus
```

The NC explicitly requires non-European societies to "provide contrasts with British history." This relationship makes that pedagogical requirement queryable.

---

## 7. Relationship to Existing Graph Nodes

### ContentVehicle: Replace or Coexist?

The existing `ContentVehicle` nodes for History carry much of the same data as the proposed `HistoryStudy` nodes (period, key_figures, sources, perspectives, etc.). The question is whether `HistoryStudy` replaces `ContentVehicle` for History or sits alongside it.

**My recommendation: Replace.**

The `ContentVehicle` was designed as a teaching pack wrapper. For History, the teaching pack IS the topic study. There is a 1:1 mapping between "Roman Britain as a ContentVehicle" and "Roman Britain as a HistoryStudy." Having both creates redundancy and confusion about which node carries authoritative data.

The `HistoryStudy` node carries everything the `ContentVehicle` carried plus:
- Disciplinary concepts (via `FOREGROUNDS` relationship)
- Chronological ordering (via `CHRONOLOGICALLY_FOLLOWS`)
- Proper historiographical debate (via `interpretations`)
- Separated sources as nodes (via `USES_SOURCE`)
- Sensitivity notes and significance claims

The `ContentVehicle` label can be retired for History. The `VehicleTemplate` nodes remain -- they model the HOW (session structure, pedagogical pattern) while `HistoryStudy` models the WHAT (content, evidence, thinking).

### ConceptCluster: How does HistoryStudy relate?

`ConceptCluster` groups concepts into teachable lesson-sized units. `HistoryStudy` groups concepts into topic-sized units (typically 8-12 lessons). They operate at different scales:

```
(:Domain)-[:HAS_STUDY]->(:HistoryStudy)    // topic scale (8-12 lessons)
(:Domain)-[:HAS_CLUSTER]->(:ConceptCluster)  // lesson scale (1-2 lessons)
```

A `HistoryStudy` encompasses multiple `ConceptClusters`. The relationship could be:

```
(:HistoryStudy)-[:ENCOMPASSES]->(:ConceptCluster)
```

But this might be over-specified. The link is already implicit through shared Domain membership. I would NOT add this relationship at launch -- keep the ontology lean and add it if query patterns demand it.

### ThinkingLens: Overlap with DisciplinaryConcept?

The existing `ThinkingLens` nodes (10 cross-subject cognitive lenses) overlap with `DisciplinaryConcept` in some cases:
- ThinkingLens "Cause and Effect" closely maps to DC "Cause and Consequence"
- ThinkingLens "Patterns" maps loosely to DC "Similarity and Difference"
- ThinkingLens "Evidence and Argument" maps to DC "Evidence and Interpretation"

**My recommendation: Keep both.** ThinkingLens nodes are cross-subject and already integrated with ConceptClusters via `APPLIES_LENS`. DisciplinaryConcept nodes are History-specific and carry History-specific age-banded guidance and question stems. They serve different purposes at different scales. An `ALIGNS_WITH` relationship between the two would be a useful future addition:

```
(:DisciplinaryConcept {slug: 'cause_and_consequence'})-[:ALIGNS_WITH]->(:ThinkingLens {lens_id: 'cause-and-effect'})
```

---

## 8. Open Questions

### 8.1 KS4 History (GCSE)

This design covers KS1-KS3. KS4 (GCSE) History is exam-board-specific (AQA, Edexcel, OCR) with set texts, paper structures and mark schemes. The `HistoryStudy` model could extend to KS4 with additional properties (`exam_board`, `paper_number`, `mark_scheme_reference`), but this needs separate design work. The core model -- disciplinary concepts, sources, chronological ordering -- transfers cleanly.

### 8.2 How many HistoricalSource nodes?

The existing CV data names ~60 distinct sources. A complete audit might produce 80-120 nodes. This is manageable but needs curation. Questions:
- Should we include only canonical named sources (Bayeux Tapestry, Magna Carta) or also source TYPES used generically ("Roman coins")?
- Should modern secondary sources (UCL Centre guidance, museum websites) be nodes or just URL properties?

**My recommendation**: Named canonical sources only (Vindolanda Tablets: yes; "Roman coins": no -- that is a source type, not a specific source). Modern pedagogical resources are URL properties, not graph nodes.

### 8.3 Should `CHRONOLOGICALLY_FOLLOWS` cross to non-History subjects?

Roman Britain (History) is contemporaneous with certain Geography and Science topics. Should chronological relationships cross subject boundaries? Probably not -- the `THEMATICALLY_LINKED` relationship handles cross-subject connections better. Chronology is a specifically historical organising principle.

### 8.4 Migration path from existing ContentVehicle data

If `HistoryStudy` replaces `ContentVehicle` for History, we need a migration that:
1. Creates `HistoryStudy` nodes from the enriched topic suggestion JSONs (which already have all the needed properties)
2. Creates `DisciplinaryConcept` nodes (6 fixed nodes)
3. Creates `HistoricalSource` nodes (curated from CV source lists)
4. Creates all relationships
5. Removes History `ContentVehicle` nodes
6. Updates `graph_query_helper.py` and `query_cluster_context.py` to query `HistoryStudy` instead of `ContentVehicle`

The existing topic suggestion JSONs (`history_ks2.json`, `history_ks3.json`) are already 90% there in terms of data completeness. The migration is primarily a structural transformation, not a data creation exercise.

### 8.5 KS1 coverage

The current topic suggestion files only cover KS2 and KS3. KS1 History topics (Changes Within Living Memory, Great Fire of London, paired figure studies, local history) need to be extracted into `history_ks1.json`. The `HistoryStudy` model handles KS1 cleanly -- the `paired_figure_study` type and `comparison_pairs` property were designed specifically for the KS1 pattern.

---

## 9. Summary: What This Ontology Gives an AI Tutor

For any History lesson generation request, the AI can query:

| Need | Source in this ontology |
|---|---|
| What to teach | `HistoryStudy` node: key_figures, key_events, definitions |
| Why it matters | `significance_claim` |
| What kind of thinking to develop | `FOREGROUNDS` -> `DisciplinaryConcept` with rank and ks_guidance |
| What evidence to use | `USES_SOURCE` -> `HistoricalSource` with pedagogical_use |
| What perspectives to explore | `perspectives` (contemporary viewpoints) |
| What debates to introduce | `interpretations` (historiographical debates) |
| How to frame the enquiry | `enquiry_questions` |
| What NOT to do | `common_pitfalls`, `sensitive_content_notes` |
| Where this sits in the timeline | `CHRONOLOGICALLY_FOLLOWS` chain |
| What to connect it to | `THEMATICALLY_LINKED`, `CONTRASTS_WITH`, `cross_curricular_hooks` |
| How to structure the session | `USES_TEMPLATE` -> `VehicleTemplate` |
| What difficulty level to target | `DELIVERS_VIA` -> `Concept` -> `HAS_DIFFICULTY_LEVEL` -> `DifficultyLevel` |

This is a complete brief for generating a historically rigorous, age-appropriate, source-based, multi-perspective History lesson. The universal `TopicSuggestion` schema got about 60% of the way there. This ontology gets to 95%.

The remaining 5% is the human teacher's contextual knowledge of their class, their locality, and their pupils' prior experiences. That is as it should be. The graph provides the curriculum intelligence; the teacher provides the pedagogical wisdom.

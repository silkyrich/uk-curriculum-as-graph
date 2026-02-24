# History Teacher Review: HistoryTopicSuggestion Schema

**Reviewer**: KS2 + KS3 History Specialist
**Date**: 2026-02-24
**Scope**: HistoryTopicSuggestion schema, VehicleTemplates for History, KS1-KS3 coverage

---

## 1. Subject-Specific Property Review

### `period` (string, required) — MODIFY

**Verdict**: Keep but supplement with machine-readable fields.

The existing ContentVehicle data uses strings like `"c.800,000 BC - 43 AD"` and `"1066 - 1509"`. This is perfect for human display but useless for timeline generation — one of the key downstream uses of this data.

**Proposed change**: Keep `period` as a human-readable display string. Add:

| Property | Type | Required | Notes |
|---|---|---|---|
| `period_start_year` | integer | No | Machine-readable. Negative for BCE. e.g. `-800000`, `43`, `1066` |
| `period_end_year` | integer | No | Machine-readable. `null` for ongoing (e.g. "1901 to present") |

**Rationale**: An AI tutor generating a Year 3 timeline needs to programmatically sort Roman Britain (43–410) before Anglo-Saxons (410–793). String parsing of "c.800,000 BC - 43 AD" is fragile. For open_slot topics (Local History Study, Beyond 1066), these fields can be null — the `period` string can say "Varies by locality".

For KS1 "Changes within Living Memory," `period` = `"Within living memory (c.1940s-present)"` with `period_start_year` = null. This gracefully handles the KS1 case where no fixed period exists.

### `key_figures` (string[], optional) — KEEP with modification

**Verdict**: Keep, but add `comparison_pairs` for KS1.

`key_figures` works well for KS2 period studies (Boudicca, Julius Caesar) and KS3 thematic studies (Elizabeth I, Francis Drake). The existing CV data is strong here.

**Problem**: KS1 "significant individuals" topics ARE the key figures — Florence Nightingale IS the topic, not a figure within a topic. And the NC explicitly requires paired comparison: "some should be used to compare aspects of life in different periods [for example, Elizabeth I and Queen Victoria, Christopher Columbus and Neil Armstrong]."

**Proposed addition**:

| Property | Type | Required | Notes |
|---|---|---|---|
| `comparison_pairs` | object[] | No | KS1 paired figures. Each: `{ "figure_a": str, "figure_b": str, "comparison_focus": str }` |

Example:
```json
"comparison_pairs": [
  { "figure_a": "Florence Nightingale", "figure_b": "Mary Seacole", "comparison_focus": "contributions to nursing and healthcare, recognition and race" },
  { "figure_a": "Elizabeth I", "figure_b": "Queen Victoria", "comparison_focus": "life in different periods, role of the monarch" }
]
```

This tells the AI tutor exactly what the NC intends: compare these two figures and focus on these aspects. Without this, the AI has no signal that Nightingale and Seacole are a pedagogical pair.

### `key_events` (string[], optional) — KEEP as-is

Works well across all key stages. The existing CV data demonstrates good coverage. Optional is correct — Local History and some KS1 topics have no pre-specified key events.

### `sources` (string[], optional) — MODIFY to required for prescribed/exemplar topics

**Verdict**: Should be conditionally required — mandatory for `prescribed_topic` and `exemplar_topic`, optional for `open_slot` and `convention`.

**Rationale**: You cannot teach History without engaging with historical evidence. The NC requires source work at every key stage:
- KS1: "asking and answering questions using a range of historical sources"
- KS2: "asking and answering historically valid questions, choosing and using parts of stories and other sources"
- KS3: "understand how evidence is used rigorously to make historical claims"

For prescribed topics like Roman Britain, we know the canonical sources (Vindolanda tablets, Roman coins). For open_slot topics (Local History), the sources depend on locality and cannot be pre-specified.

**Practical proposal**: Keep `sources` optional in the schema, but add a validation rule: if `curriculum_status` is `mandatory` or `menu_choice`, then `sources` should be non-empty. Add a `source_quality` note to the briefing.

### `source_types` (string[], optional) — MODIFY to required

**Verdict**: Make required. This is MORE important than named sources for AI generation.

**Rationale**: An AI tutor generating a lesson needs to know it should create activities around "primary written" sources vs "archaeological remains" vs "oral testimony." The source type determines the pedagogical approach:
- Primary written → transcription, interpretation, provenance analysis
- Archaeological → inference from physical evidence, what can/cannot be determined
- Visual (paintings, tapestries) → composition analysis, propaganda awareness
- Oral testimony → reliability, memory, emotion

The existing CV data has excellent source_type taxonomies. Even for open_slot topics, we can specify the TYPES of sources expected (local history: "census records, maps, photographs, oral history").

**Proposed controlled vocabulary**:
```
primary_written, primary_visual, primary_archaeological, primary_cartographic,
primary_statistical, primary_legal, primary_administrative, primary_artistic,
primary_audiovisual, oral_tradition, oral_testimony, built_heritage,
museum_artefact, secondary_written, testimony
```

### `perspectives` (string[], required) — MODIFY

**Verdict**: Keep required, but rename to `viewpoints` and add `interpretations` as a separate property.

**Rationale**: In History education, there is a crucial distinction between:
1. **Perspectives/viewpoints** — how people at the time saw events (a Roman coloniser vs a Briton; a factory owner vs a child worker)
2. **Interpretations** — how historians have subsequently understood and debated the past (Was the Norman Conquest a catastrophe or a modernisation? Was the British Empire beneficial or exploitative?)

The NC names both explicitly:
- KS2: "they should understand how our knowledge of the past is constructed from a range of sources"
- KS3: "understand how different types of historical sources are used rigorously to make historical claims and discern how and why contrasting arguments and interpretations of the past have been constructed"

The existing CV data conflates these — "archaeologist (modern)" appears alongside "pharaoh" in the Ancient Egypt perspectives. These serve different pedagogical functions.

**Proposed change**:

| Property | Type | Required | Notes |
|---|---|---|---|
| `perspectives` | string[] | Yes | Contemporary viewpoints — how people at the time experienced events |
| `interpretations` | string[] | No | Historiographical debates. Required for KS3, optional for KS2. e.g. "Was the Roman Empire beneficial for Britain?" |

Example (Roman Britain):
```json
"perspectives": ["Roman coloniser", "Briton", "Roman soldier", "enslaved person"],
"interpretations": ["Was Romanisation beneficial or destructive for British culture?", "To what extent did the Romans 'civilise' Britain?"]
```

This gives the AI tutor two distinct lesson-generation pathways: "Write from the perspective of a Roman soldier at Hadrian's Wall" (creative empathy) vs "Evaluate the interpretation that the Roman Empire was beneficial for Britain" (analytical argument).

### NEW PROPERTY: `disciplinary_concepts` (string[], required) — ADD

**This is the single most important addition to the schema.**

**Rationale**: Every History topic foregrounds certain second-order (disciplinary) concepts. The NC explicitly names these as the intellectual backbone of History education:
- **Chronology** — ordering events and periods in time
- **Cause and consequence** — why things happened and what resulted
- **Change and continuity** — what changed and what stayed the same
- **Similarity and difference** — comparing across periods, places, peoples
- **Significance** — why events/people/developments matter
- **Evidence and interpretation** — how we know about the past and how we debate it

These are not optional enrichments — they determine what kind of thinking the AI should demand from the child. A Roman Britain lesson foregrounding "cause and consequence" asks "Why did the Romans invade?" A Roman Britain lesson foregrounding "evidence and interpretation" asks "What can this Vindolanda tablet tell us about daily life?"

| Property | Type | Required | Notes |
|---|---|---|---|
| `disciplinary_concepts` | string[] | Yes | Ordered by prominence for this topic. Controlled vocabulary below. |

**Controlled vocabulary** (from NC + Historical Association):
```
chronology, cause_and_consequence, change_and_continuity,
similarity_and_difference, significance, evidence_and_interpretation
```

**Examples**:
- Stone Age to Iron Age: `["change_and_continuity", "chronology", "evidence_and_interpretation"]`
- Roman Britain: `["cause_and_consequence", "evidence_and_interpretation", "significance"]`
- The Holocaust: `["cause_and_consequence", "significance", "evidence_and_interpretation"]`
- Significant Individuals (KS1): `["significance", "similarity_and_difference", "chronology"]`

**Impact**: This is the property that transforms a generic AI tutor into one that develops genuine historical thinking. Without it, the AI generates "tell me about the Romans" lessons. With it, the AI generates "explain why the Romans invaded Britain, using evidence from at least two sources" lessons.

### NEW PROPERTY: `significance_claim` (string, required) — ADD

**Rationale**: The `pedagogical_rationale` explains why this topic works for the curriculum concepts it delivers. But it does NOT explain why this topic matters in History — why it is worth studying, what it tells us about the human experience, what lasting consequences it had.

An AI tutor needs this to generate assessment questions ("Explain why the Norman Conquest was significant"), to frame the topic introduction ("We're studying the Industrial Revolution because it changed how everyone in Britain lived"), and to connect topics across the curriculum ("The abolition of slavery was significant because...").

| Property | Type | Required | Notes |
|---|---|---|---|
| `significance_claim` | string | Yes | 1-2 sentences explaining the historical significance of this topic. Why does it matter? |

**Examples**:
- Roman Britain: "The Roman occupation transformed Britain's infrastructure, language, law, and culture, and its legacy remains visible in roads, towns, and institutions today."
- The Holocaust: "The Holocaust represents the most systematic genocide in modern history and raises fundamental questions about human rights, prejudice, and the responsibilities of individuals and states."
- Florence Nightingale: "Nightingale's work transformed nursing from a low-status occupation into a respected profession and established the principle that healthcare should be based on evidence and data."

### NEW PROPERTY: `sensitive_content_notes` (string[], optional) — ADD

**Rationale**: This is a safeguarding issue. An AI tutor for children aged 5-14 MUST know when a topic involves content that requires careful handling. The platform serves children — the ICO Children's Code and the project's ethical framework demand age-appropriate content.

Topics requiring sensitivity notes include:
- **The Holocaust** — genocide, antisemitism, mass murder (UCL Centre for Holocaust Education provides specific guidance)
- **Slavery and the Atlantic slave trade** — dehumanisation, violence, racism
- **British Empire and colonialism** — exploitation, racism, violence
- **Religious persecution** — Reformation, recusants, martyrdom
- **Warfare** — violence, death, civilian suffering (especially WW1/WW2)
- **Benin Bronzes** — repatriation debates, colonial theft, ongoing political sensitivity

| Property | Type | Required | Notes |
|---|---|---|---|
| `sensitive_content_notes` | string[] | No | Specific content warnings and pedagogical guidance. References to external guidance where applicable. |

**Example** (The Holocaust):
```json
"sensitive_content_notes": [
  "Requires particular sensitivity in language and source selection — follow UCL Centre for Holocaust Education guidance",
  "Do not use graphic atrocity images with KS3 pupils — use testimony and documentary evidence instead",
  "Present victims as individuals with full lives, not anonymous masses",
  "Address antisemitism as a long historical phenomenon, not just a Nazi invention",
  "Be aware that pupils may have family connections to the Holocaust or to contemporary antisemitism"
]
```

**Example** (British Empire):
```json
"sensitive_content_notes": [
  "Present multiple perspectives including colonised peoples — avoid presenting empire as solely beneficial",
  "Be sensitive to pupils whose heritage connects to colonised nations",
  "Slavery content should centre the experiences and agency of enslaved people, not only the actions of enslavers"
]
```

### NEW PROPERTY: `enquiry_questions` (string[], optional but recommended) — ADD

**Rationale**: Good History teaching is driven by enquiry questions — the big questions that frame a sequence of lessons. The Historical Association and leading History education researchers (e.g., Christine Counsell, Michael Riley) emphasise the enquiry question as the single most important planning decision a History teacher makes.

| Property | Type | Required | Notes |
|---|---|---|---|
| `enquiry_questions` | string[] | No | 1-3 overarching enquiry questions for this topic. Should be genuinely debatable and historically valid. |

**Examples**:
- Roman Britain: `["Why did the Romans invade Britain?", "How far did the Romans change Britain?", "Was the Roman occupation good for Britain?"]`
- The Holocaust: `["How did the Holocaust happen?", "What choices did people face during the Holocaust?", "Why does the Holocaust matter today?"]`
- Stone Age to Iron Age: `["What was the biggest change in people's lives from the Stone Age to the Iron Age?", "How do we know about life in prehistoric Britain?"]`

**Impact**: Enquiry questions give the AI tutor a framework for structuring a multi-lesson sequence, rather than generating disconnected factual lessons. They also model the kind of historical thinking we want children to develop.

---

## 2. Universal Property Review

### `suggestion_type` values — MODIFY

The proposed values are: `prescribed_topic`, `exemplar_topic`, `open_slot`, `exemplar_figure`, `exemplar_event`, `exemplar_text`, `teacher_convention`.

For History, I'd add:
- **`paired_figure_study`** — for KS1 comparison pairs (Nightingale vs Seacole). These are neither simple "exemplar_figure" nor "prescribed_topic" — they are a specific pedagogical pattern.

And I'd rename:
- `exemplar_event` → keep (works for Great Fire of London, Moon Landings)
- `exemplar_figure` → keep (works for individual figures like Rosa Parks, Neil Armstrong)

### `curriculum_status` — KEEP, but clarify `convention` vs `exemplar`

For History:
- `mandatory` = Stone Age to Iron Age, Roman Britain, Anglo-Saxons, Vikings, Ancient Greece, Holocaust
- `menu_choice` = Ancient Egypt/Sumer/Indus/Shang (pick one), Maya/Benin/Islamic (pick one)
- `exemplar` = Nightingale, Seacole, Great Fire of London (NC names them as examples)
- `convention` = WW2 at KS2 Beyond 1066 (56% of schools, not named in NC); Tudors at KS2 (28%)

This is clear and well-designed.

### `definitions` — KEEP but ensure subject-specific precision

History definitions should include both **substantive vocabulary** (centurion, pharaoh, ziggurat) and **disciplinary vocabulary** (chronology, cause, consequence, significance, evidence, interpretation). The existing CV data handles this well.

### `common_pitfalls` — KEEP, this is excellent

For History, common pitfalls include:
- Teaching the topic as a narrative rather than developing disciplinary thinking
- Using anachronistic moral judgements ("the Romans were bad because they had slaves")
- Relying on myths and popular culture over historical evidence (Horrible Histories as the only lens)
- Presenting a single narrative without multiple perspectives
- For KS1: turning "significant individuals" into biography recitations rather than significance analysis

### `cross_curricular_hooks` — KEEP but add structure

For History, these are genuinely valuable:
- Roman Britain → Latin roots in English vocabulary, Roman numerals in Maths, Roman buildings in DT
- Ancient Egypt → Geography of the Nile, Science of mummification/preservation, Art of tomb painting
- Industrial Revolution → Science of steam engines, Geography of urbanisation, English of reform literature
- The Holocaust → English (diary writing, testimony), RS (moral philosophy), Citizenship (human rights)

Should these be simple strings or structured objects with `{ subject, connection_description }`? I'd prefer structured — it lets the AI tutor generate meaningful cross-curricular links rather than vague mentions.

---

## 3. VehicleTemplate Critique

### Existing templates that work for History

| Template | History use | Verdict |
|---|---|---|
| `topic_study` | Primary pattern for period studies (KS2 British History, KS3 thematic) | KEEP — this is the workhorse |
| `comparison_study` | Comparing civilisations, comparing perspectives | KEEP — essential for History |
| `research_enquiry` | Extended enquiry using multiple sources | KEEP but modify session structure |
| `discussion_and_debate` | KS3 argumentative History (Was empire beneficial?) | KEEP |

### Templates that need History-specific modifications

**`research_enquiry`** — The session structure `question -> source_selection -> note_taking -> synthesis -> presentation` is too generic for History. History research enquiry requires explicit source criticism:

**Proposed History variant**: `question -> source_identification -> provenance_analysis -> cross_referencing -> argument_construction -> presentation`

The key difference: History enquiry doesn't just "take notes from sources" — it interrogates them. Who wrote this? When? Why? Can we trust it? What does it NOT tell us?

### Missing templates for History

**`source_enquiry`** — STRONGLY RECOMMEND ADDING

This is the signature History pedagogical pattern. It's distinct from `research_enquiry` because the sources themselves are the focus, not a question that sources help answer.

| Property | Value |
|---|---|
| `template_type` | `source_enquiry` |
| Subjects | History |
| Session structure | `source_presentation -> observation -> questioning -> contextualisation -> inference -> evaluation` |
| Description | Structured analysis of one or more primary sources. Pupils develop skills of observation, inference, and evaluation through progressive engagement with historical evidence. |

**Example use**: Analysing the Bayeux Tapestry, reading Vindolanda tablets, examining Benin Bronzes, studying propaganda posters from WW1/WW2.

**`significance_enquiry`** — RECOMMEND ADDING

| Property | Value |
|---|---|
| `template_type` | `significance_enquiry` |
| Subjects | History |
| Session structure | `event_introduction -> criteria_establishment -> evidence_gathering -> argument_construction -> evaluation` |
| Description | Structured investigation of historical significance. Pupils establish criteria for significance (impact, duration, remembered-ness, relevance) and apply them to evaluate events, people, or developments. |

**Example use**: "Was the Norman Conquest the most significant event in British History?", "Why is Florence Nightingale significant?", "Was the abolition of slavery a turning point?"

**`local_history_enquiry`** — RECOMMEND ADDING

| Property | Value |
|---|---|
| `template_type` | `local_history_enquiry` |
| Subjects | History, Geography |
| Session structure | `place_observation -> question_generation -> local_source_investigation -> oral_history_collection -> synthesis -> community_presentation` |
| Description | Enquiry rooted in the pupil's own locality. Uses local sites, buildings, maps, census records, and community testimony. |

This is a statutory requirement at both KS1 and KS2 and has a distinctive pedagogical pattern that doesn't fit `topic_study` or `research_enquiry`.

### Template that doesn't quite fit History

**`case_study`** — listed as Geography/Business/Science. The session structure (`introduction -> data_collection -> analysis -> comparison -> evaluation`) is too data-oriented for History. History uses case studies but in a narrative/analytical rather than data-driven mode. I'd keep this for Geography but note that History topics that look like case studies should use `topic_study` or `comparison_study` instead.

---

## 4. TopicSuggestion Inventory

### KS1 History

| suggestion_id | name | suggestion_type | curriculum_status |
|---|---|---|---|
| TS-HI-KS1-001 | Changes Within Living Memory | open_slot | mandatory |
| TS-HI-KS1-002 | The Great Fire of London | exemplar_event | exemplar |
| TS-HI-KS1-003 | The First Aeroplane Flight | exemplar_event | exemplar |
| TS-HI-KS1-004 | Moon Landings | exemplar_event | exemplar |
| TS-HI-KS1-005 | Florence Nightingale & Mary Seacole | paired_figure_study | exemplar |
| TS-HI-KS1-006 | Elizabeth I & Queen Victoria | paired_figure_study | exemplar |
| TS-HI-KS1-007 | Christopher Columbus & Neil Armstrong | paired_figure_study | exemplar |
| TS-HI-KS1-008 | Rosa Parks & Emily Davison | paired_figure_study | exemplar |
| TS-HI-KS1-009 | William Caxton & Tim Berners-Lee | paired_figure_study | exemplar |
| TS-HI-KS1-010 | Pieter Bruegel the Elder & LS Lowry | paired_figure_study | exemplar |
| TS-HI-KS1-011 | Edith Cavell | exemplar_figure | exemplar |
| TS-HI-KS1-012 | Significant Local History | open_slot | mandatory |
| TS-HI-KS1-013 | Remembrance Day / Commemorations | teacher_convention | convention |
| TS-HI-KS1-014 | Grace Darling | teacher_convention | convention |
| TS-HI-KS1-015 | Samuel Pepys (Great Fire of London) | teacher_convention | convention |
| TS-HI-KS1-016 | Gunpowder Plot (1605) | teacher_convention | convention |

**Note on KS1**: The NC names all the paired figures explicitly — these are NOT school choices but NC exemplars. The pairing IS the pedagogical point (comparing aspects of life in different periods). The schema must capture this.

### KS2 History

| suggestion_id | name | suggestion_type | curriculum_status |
|---|---|---|---|
| TS-HI-KS2-001 | Stone Age to Iron Age Britain | prescribed_topic | mandatory |
| TS-HI-KS2-002 | Roman Britain | prescribed_topic | mandatory |
| TS-HI-KS2-003 | Anglo-Saxon and Scots Settlement | prescribed_topic | mandatory |
| TS-HI-KS2-004 | Vikings and Anglo-Saxon England | prescribed_topic | mandatory |
| TS-HI-KS2-005 | Local History Study | open_slot | mandatory |
| TS-HI-KS2-006 | British History Beyond 1066 | open_slot | mandatory |
| TS-HI-KS2-007 | Ancient Greece | prescribed_topic | mandatory |
| TS-HI-KS2-008 | Ancient Egypt | exemplar_topic | menu_choice |
| TS-HI-KS2-009 | Ancient Sumer | exemplar_topic | menu_choice |
| TS-HI-KS2-010 | The Indus Valley | exemplar_topic | menu_choice |
| TS-HI-KS2-011 | The Shang Dynasty | exemplar_topic | menu_choice |
| TS-HI-KS2-012 | Early Islamic Civilisation (Baghdad c.900) | exemplar_topic | menu_choice |
| TS-HI-KS2-013 | Mayan Civilisation (c.900) | exemplar_topic | menu_choice |
| TS-HI-KS2-014 | Benin (West Africa c.900-1300) | exemplar_topic | menu_choice |
| TS-HI-KS2-015 | World War 2 (Beyond 1066 choice) | teacher_convention | convention |
| TS-HI-KS2-016 | The Tudors (Beyond 1066 choice) | teacher_convention | convention |
| TS-HI-KS2-017 | The Victorians (Beyond 1066 choice) | teacher_convention | convention |
| TS-HI-KS2-018 | Crime and Punishment (Beyond 1066 choice) | teacher_convention | convention |

**Convention data** (from Historical Association survey + briefing data):
- Ancient civ depth study: Ancient Egypt 77%, Shang 10%, Sumer 3%, Indus rare
- Non-European: Maya 45%, Benin 17%, Islamic 13%
- Beyond 1066: WW2 56%, Victorians 32%, Tudors 28%, Crime & Punishment 11%

### KS3 History

| suggestion_id | name | suggestion_type | curriculum_status |
|---|---|---|---|
| TS-HI-KS3-001 | Medieval Britain 1066-1509 | prescribed_topic | mandatory |
| TS-HI-KS3-002 | Church, State and Society 1509-1745 | prescribed_topic | mandatory |
| TS-HI-KS3-003 | The Elizabethan Age | prescribed_topic | mandatory |
| TS-HI-KS3-004 | Ideas, Power, Industry and Empire 1745-1901 | prescribed_topic | mandatory |
| TS-HI-KS3-005 | Challenges 1901 to Present Day | prescribed_topic | mandatory |
| TS-HI-KS3-006 | The Holocaust | prescribed_topic | mandatory |
| TS-HI-KS3-007 | World History Study | open_slot | mandatory |
| TS-HI-KS3-008 | Atlantic Slave Trade | teacher_convention | convention |
| TS-HI-KS3-009 | Mughal India | exemplar_topic | menu_choice |
| TS-HI-KS3-010 | Aztec/Inca Empires | exemplar_topic | menu_choice |
| TS-HI-KS3-011 | Ming Dynasty China | exemplar_topic | menu_choice |
| TS-HI-KS3-012 | 20th Century USA | exemplar_topic | menu_choice |
| TS-HI-KS3-013 | Communist States in the 20th Century | exemplar_topic | menu_choice |
| TS-HI-KS3-014 | English Civil War (within 1509-1745) | teacher_convention | convention |
| TS-HI-KS3-015 | Black Peoples of the Americas | teacher_convention | convention |

**Note**: The KS3 PoS is deliberately broad — "the development of Church, state and society in Medieval Britain 1066-1509" is a single statutory requirement that schools break into many sub-topics. The TopicSuggestion for this should capture the whole statutory requirement, with `enquiry_questions` breaking it into teachable chunks.

---

## 5. Content Generation Requirements

### What does the AI need to generate a good History lesson?

**For a Year 3 Roman Britain lesson** (first encounter, DifficultyLevel: entry/developing):
1. The topic's `period` and `period_start_year`/`period_end_year` — to place on a timeline
2. `key_figures` — to introduce Boudicca, Claudius as characters
3. `key_events` — to structure the narrative chronologically
4. `sources` and `source_types` — to create a "What can we learn from this source?" activity
5. `disciplinary_concepts` — to know this lesson should foreground "cause and consequence" (WHY did the Romans invade?) not just narrative
6. `perspectives` — to create a "How would a Roman soldier and a Briton see this differently?" activity
7. `definitions` — to pre-teach vocabulary (centurion, legion, Romanisation)
8. The linked DifficultyLevel data — to calibrate the complexity of questions
9. `significance_claim` — to frame the lesson ("We're learning about the Romans because their impact on Britain is still visible today")
10. VehicleTemplate session structure — to structure the lesson flow

**For a Year 8 Industrial Revolution essay** (DifficultyLevel: secure/mastery):
1. `disciplinary_concepts` — to know this should be an analytical "cause and consequence" essay, not a narrative
2. `perspectives` — to ensure the essay considers multiple viewpoints (factory owner, child worker, colonial subject)
3. `interpretations` — to frame the essay question ("To what extent did the Industrial Revolution improve life in Britain?")
4. `enquiry_questions` — to provide the essay question itself
5. `source_types` — to generate appropriate source-based activities (factory commission reports, census data, photographs)
6. `sensitive_content_notes` — to handle child labour, slavery, and colonialism content appropriately
7. DifficultyLevel data — to differentiate between "describe two causes" (developing) and "evaluate relative importance of causes" (mastery)

### For a video script:
- `significance_claim` — the hook: WHY should the viewer care?
- `key_events` in chronological order — the narrative spine
- `key_figures` — characters to bring to life
- `sources` — visual assets to show on screen
- `perspectives` — to structure a "but what did the other side think?" narrative turn

### For assessment generation:
- `disciplinary_concepts` — determines the TYPE of question (chronology = sequence, cause/consequence = explain why, significance = evaluate importance)
- `DifficultyLevel` data — determines the DEPTH of the expected answer
- `enquiry_questions` — provides the overarching question that the assessment should align to

---

## 6. Cross-Curricular Hooks

### High-value cross-curricular connections for History

| History Topic | Subject | Connection |
|---|---|---|
| Roman Britain | English | Latin roots in English vocabulary; writing persuasive accounts |
| Roman Britain | Mathematics | Roman numerals; measurement of distances (Hadrian's Wall) |
| Roman Britain | DT | Roman building techniques (arches, aqueducts) |
| Ancient Egypt | Geography | The Nile: river systems, flooding, irrigation |
| Ancient Egypt | Science | Mummification: preservation, materials, chemical change |
| Ancient Egypt | Art | Tomb painting: composition, symbolism, perspective |
| Stone Age to Iron Age | Science | Properties of materials (stone, bronze, iron) |
| Stone Age to Iron Age | Geography | Settlement patterns, landscape change |
| Anglo-Saxons | English | Anglo-Saxon literature (Beowulf extracts), place names |
| Vikings | Geography | Migration routes, Scandinavian geography |
| Ancient Greece | English | Greek myths as narrative texts |
| Ancient Greece | Mathematics | Greek mathematicians, geometry origins |
| Ancient Greece | Citizenship | Democracy — origins and modern comparisons |
| Industrial Revolution | Science | Steam engines, materials science |
| Industrial Revolution | Geography | Urbanisation, population change, trade routes |
| Industrial Revolution | English | Dickens, reform literature, journalistic writing |
| The Holocaust | English | Diary writing (Anne Frank), testimony as genre |
| The Holocaust | RS | Moral philosophy, human rights |
| The Holocaust | Citizenship | Genocide prevention, human rights law |
| WW1/WW2 | English | War poetry (Owen, Sassoon), propaganda analysis |
| Benin | Art | Bronze casting techniques, metalwork |
| Islamic Civilisation | Mathematics | Algebra origins (Al-Khwarizmi), number systems |

**Recommendation**: Capture these as structured objects: `{ "subject": "English", "hook": "Latin roots in English vocabulary from Roman occupation", "strength": "strong" }`. The `strength` field (strong/moderate/light) tells the AI how substantial the cross-curricular link is — "Roman numerals" is a light link, "Greek democracy and Citizenship" is a strong one.

---

## 7. Stress Test Scenarios

### Scenario 1: Year 1 — Florence Nightingale and Mary Seacole (KS1 paired figure study)

**The lesson**: A Year 1 class (age 5-6) learning about significant individuals. The NC requires comparing Nightingale and Seacole to develop understanding of how context shapes significance.

**Does the schema capture everything needed?**
- `comparison_pairs` (proposed): YES — captures the pairing and comparison focus
- `perspectives`: Partially — but at KS1, "perspectives" means something simpler: "What was life like for Florence?" not "Whose perspective is represented in this source?"
- `disciplinary_concepts`: `["significance", "similarity_and_difference"]` — YES, this tells the AI to ask "Why is Florence Nightingale significant?" not just "What did she do?"
- `period`: `"1820-1910"` — covers both figures' lifetimes
- `sensitive_content_notes`: NEEDED — Seacole's experiences with racial prejudice should be handled age-appropriately
- `source_types`: `["primary_visual", "primary_written"]` — portraits, photographs, letters
- VehicleTemplate: Neither `topic_study` nor `research_enquiry` quite fits. KS1 significant individuals is closer to **`biography_comparison`** but there's no template for this. The closest is `comparison_study`, which could work if the session structure is age-adapted.

**Verdict**: Schema works IF `comparison_pairs` is added and a KS1-appropriate VehicleTemplate is available. The age-banded `TEMPLATE_FOR` prompts on VehicleTemplate would need to radically simplify the session structure for KS1.

### Scenario 2: Year 4 — Ancient Egypt depth study (KS2 menu choice)

**The lesson**: A Year 4 class (age 8-9) studying Ancient Egypt as their earliest civilisations depth study. The teacher wants to focus on the Nile's role in sustaining civilisation.

**Does the schema capture everything needed?**
- `period`: "c.3100 BC - 30 BC" with `period_start_year: -3100`, `period_end_year: -30` — YES, allows timeline placement
- `key_figures`: Tutankhamun, Cleopatra, Hatshepsut, Howard Carter — YES
- `key_events`: Building of Great Pyramid, Discovery of Tutankhamun's tomb — YES
- `sources`: Rosetta Stone, tomb artefacts — YES
- `source_types`: primary written, primary archaeological, built heritage — YES, tells the AI what types of activities to generate
- `disciplinary_concepts`: `["evidence_and_interpretation", "significance", "cause_and_consequence"]` — YES
- `enquiry_questions`: `["How do we know about Ancient Egypt?", "Why did the Nile make civilisation possible?"]` — YES
- `significance_claim`: "Ancient Egypt was one of the earliest and longest-lasting civilisations, whose achievements in writing, engineering, and governance influenced subsequent Mediterranean cultures." — YES
- `cross_curricular_hooks`: Geography (Nile), Science (mummification), Art (tomb painting) — YES
- DifficultyLevel integration: Year 4 concepts at "entry" through "expected" — YES

**Verdict**: Schema works well for this mainstream case. The existing CV data for Ancient Egypt is strong and maps cleanly to the new schema.

### Scenario 3: Year 8 — The Holocaust (KS3 statutory, sensitive)

**The lesson**: A Year 8 class (age 12-13) studying the Holocaust. This is statutory and requires extreme pedagogical care.

**Does the schema capture everything needed?**
- `sensitive_content_notes`: CRITICAL — must reference UCL Centre for Holocaust Education guidance, must warn against graphic imagery, must note that pupils may have family connections
- `disciplinary_concepts`: `["cause_and_consequence", "significance", "evidence_and_interpretation"]` — YES
- `perspectives`: "Jewish victim, rescuer, bystander, perpetrator, liberator" — YES, but needs careful framing (the AI must not ask pupils to "imagine you are a perpetrator")
- `interpretations`: "How did the Holocaust happen? Was it inevitable? What were the stages of persecution?" — YES
- `enquiry_questions`: "How did discrimination escalate to genocide?", "What choices did people face?" — YES
- `sources`: Anne Frank's diary, Primo Levi's testimony, Nuremberg trial transcripts — YES
- `source_types`: testimony, primary written, primary legal, primary visual — YES, and critically, the AI needs to know that "primary visual" in this context means "use with extreme care"
- VehicleTemplate: `topic_study` with `discussion_and_debate` elements. The standard session structure needs modification — the "hook" stage cannot be a provocation or a shocking image. It should be a personal story or a pre-war photograph of normal life.

**Verdict**: Schema works IF `sensitive_content_notes` is present AND the VehicleTemplate age-banded prompt for KS3 Holocaust includes explicit guidance about atrocity imagery, testimony handling, and the UCL Centre's recommended pedagogical approaches. The `sensitive_content_notes` property is not a nice-to-have — it is a child safeguarding requirement.

### Scenario 4: Year 5 — Local History Study (KS2 open slot)

**The lesson**: A Year 5 class studying the history of their town's Victorian cotton mill.

**Does the schema capture everything needed?**
- `suggestion_type`: `open_slot` — YES, this is a framework not a specific topic
- `period`: `null` or "Varies by locality" — works
- `key_figures`, `key_events`, `sources`: all empty/generic — this is correct for an open_slot
- `source_types`: `["census_records", "historic_maps", "photographs", "oral_history", "built_heritage"]` — YES, these are the types of sources available for ANY local history study
- `enquiry_questions`: Generic: `["How has our local area changed over time?", "What can local sources tell us about the past?", "Why is our local heritage significant?"]` — YES
- VehicleTemplate: Needs `local_history_enquiry` (proposed above) — the standard `topic_study` doesn't capture the fieldwork and community engagement elements
- `disciplinary_concepts`: `["change_and_continuity", "evidence_and_interpretation", "significance"]` — YES

**Verdict**: The schema handles open_slot topics adequately because the universal properties (VehicleTemplate, source_types, disciplinary_concepts) provide enough structure for the AI to generate a pedagogically sound local history lesson, even though the specific content is unknown. The proposed `local_history_enquiry` template is essential here.

---

## 8. Summary: Top 3 Recommendations

### 1. ADD `disciplinary_concepts` (string[], required) — HIGHEST IMPACT

**Why**: This is the difference between an AI tutor that generates factual quizzes and one that develops historical thinking. The six second-order concepts (chronology, cause and consequence, change and continuity, similarity and difference, significance, evidence and interpretation) are the intellectual backbone of History education from KS1 to KS4. Without this property, the AI has no signal about what KIND of thinking to develop. With it, every generated lesson, assessment, and video script can be framed around genuine historical reasoning.

**Effort**: Low. The controlled vocabulary is fixed (6 values). Each HistoryTopicSuggestion needs 2-4 concepts in priority order. Can be generated from existing CV assessment_guidance text.

### 2. ADD `sensitive_content_notes` (string[], optional) and `significance_claim` (string, required) — HIGH IMPACT

**Why `sensitive_content_notes`**: This platform serves children aged 5-14. Topics like the Holocaust, slavery, colonialism, and religious persecution require explicit pedagogical guardrails. An AI tutor that generates a "write from the perspective of a Holocaust perpetrator" activity for a 12-year-old is not just bad pedagogy — it is a safeguarding failure. This property is mandatory for child safety.

**Why `significance_claim`**: Assessment in History is fundamentally about significance — why does this matter? Without this property, the AI generates "what happened?" questions. With it, the AI generates "why does this matter?" questions — the hallmark of good History teaching.

**Effort**: Medium. Sensitive content notes needed for ~8-10 topics (Holocaust, slavery, empire, religious persecution, warfare). Significance claims needed for all topics but are 1-2 sentences each.

### 3. ADD `comparison_pairs` for KS1 + `source_enquiry` VehicleTemplate — MEDIUM-HIGH IMPACT

**Why `comparison_pairs`**: KS1 History is fundamentally different from KS2/KS3. The NC explicitly names paired figure comparisons (Nightingale/Seacole, Elizabeth I/Victoria, Columbus/Armstrong). Without `comparison_pairs`, the schema cannot represent the most distinctive feature of KS1 History. An AI generating a KS1 "significant individuals" lesson without knowing the comparison structure will miss the pedagogical point entirely.

**Why `source_enquiry` template**: Source analysis is the signature activity of History education. The existing templates handle narrative studies (topic_study), debates (discussion_and_debate), and research (research_enquiry), but none captures the distinctive pattern of "here is a primary source — observe, question, infer, evaluate." This is used in every History lesson from KS1 (looking at old photographs) to KS3 (analysing propaganda posters). Adding this template significantly expands the AI's pedagogical repertoire for History.

**Effort**: Low-medium. `comparison_pairs` is a simple object array added to KS1 suggestions only. `source_enquiry` is one new VehicleTemplate with a clear session structure.

---

## Appendix: Complete Proposed HistoryTopicSuggestion Property Table

| Property | Type | Required | Source |
|---|---|---|---|
| `period` | string | Yes | Existing (keep) |
| `period_start_year` | integer | No | **NEW** |
| `period_end_year` | integer | No | **NEW** |
| `key_figures` | string[] | No | Existing (keep) |
| `comparison_pairs` | object[] | No | **NEW** (KS1) |
| `key_events` | string[] | No | Existing (keep) |
| `sources` | string[] | No | Existing (keep, recommend non-empty for prescribed/exemplar) |
| `source_types` | string[] | Yes | Existing (upgrade to required) |
| `perspectives` | string[] | Yes | Existing (keep, clarify = contemporary viewpoints) |
| `interpretations` | string[] | No | **NEW** (historiographical debates, required KS3+) |
| `disciplinary_concepts` | string[] | Yes | **NEW** (controlled vocab, ordered by prominence) |
| `significance_claim` | string | Yes | **NEW** |
| `sensitive_content_notes` | string[] | No | **NEW** |
| `enquiry_questions` | string[] | No | **NEW** (recommended for all prescribed topics) |

Plus all universal properties from the briefing.

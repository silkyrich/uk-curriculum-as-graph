# English Teacher Review: EnglishTopicSuggestion Schema

**Reviewer**: KS2 + KS4 English Specialist
**Date**: 2026-02-24
**Data reviewed**: BRIEFING.md, english_y4.json (existing CVs), English_Y4_extracted.json, English_Literature_KS4_extracted.json, English_Language_KS4_extracted.json, GCSE set text data (AQA, Edexcel, OCR)

---

## 1. Subject-Specific Property Review

### Proposed: `genre` (string, required) — MODIFY

**Verdict**: KEEP but enforce a **controlled vocabulary** and make it an **array** (`string[]`), not a single string.

**Rationale**: A single Year 4 text study commonly straddles genres. The existing CV `EN-Y4-CV008` has genre `"balanced discussion text"` but its teaching involves spoken language, debate AND writing — it touches persuasion, discussion AND recount. A Y10 Macbeth study is simultaneously drama, tragedy, and poetry (blank verse). Forcing one genre loses information.

**Proposed controlled vocabulary** (aligned to NC text type expectations):

Primary genres (KS1-KS2):
- `narrative` (adventure, mystery, historical, sci-fi, fantasy)
- `traditional_tale` (fairy tale, myth, legend, fable, folk tale)
- `poetry` (performance, form study, anthology)
- `playscript`
- `recount` (diary, biography, autobiography, newspaper report)
- `report` (non-chronological report)
- `instruction`
- `explanation`
- `persuasion` (letter, advertisement, speech)
- `discussion` (balanced argument)
- `information` (reference, encyclopaedia)

Secondary genres (KS3-KS4):
- `fiction` (literary fiction, genre fiction, short story)
- `drama` (tragedy, comedy, history, modern drama)
- `poetry` (anthology, unseen, comparison)
- `literary_nonfiction` (travel writing, memoir, essay, journalism)
- `transactional` (article, letter, speech, review, report)
- `creative_writing` (narrative, descriptive)

**Implementation**: `genre: string[]` with values from the controlled vocab. First element = primary genre.

### Proposed: `text_features` (string[], required) — KEEP

**Verdict**: KEEP as-is. This is one of the strongest properties in the existing CVs. The Y4 data shows excellent use: `["problem-resolution structure", "vivid description", "dialogue to advance plot", "building suspense"]` for adventure narrative. This directly tells the AI tutor what textual features to teach and assess.

**One addition**: Consider renaming to `text_features_to_teach` for clarity — these aren't just features of the suggested text, they're the *teaching objectives* expressed as text features.

### Proposed: `suggested_texts` (string[], optional) — MODIFY

**Verdict**: MODIFY to **structured objects**, not plain strings.

**Problem**: `"The Iron Man by Ted Hughes"` as a string is parseable but fragile. More critically, for KS4 set texts, you need exam board, text status, and edition information. And for fairy tales or myths, a bare title is ambiguous — "Cinderella" could be Perrault, Brothers Grimm, or a modern retelling.

**Proposed structure**:
```json
"suggested_texts": [
  {
    "title": "The Iron Man",
    "author": "Ted Hughes",
    "publication_year": 1968,
    "text_type": "novel",
    "suitability": "Y3-Y5",
    "note": "Core text — rich vocabulary, clear narrative structure"
  }
]
```

For KS4, the structure needs additional fields (see `exam_board_status` below).

### MISSING: `reading_level` — ADD (required)

**Verdict**: ADD. This is **critical** and its omission from the proposed schema is the single biggest gap.

**Evidence**: Every single existing CV in `english_y4.json` has `reading_level: "Year 4"`. The briefing says these are "runtime content" — they absolutely are not. Reading level is a **curriculum design property**, not runtime content. The Iron Man is a Year 3-5 text. Macbeth is a KS4 text. This is not generated at runtime — it's an inherent property of the suggestion.

**Proposed**: `reading_level: string` — values like `"Y3-Y4"`, `"Y5-Y6"`, `"KS3"`, `"KS4"`. This is the age band the text/topic is appropriate for, which may differ from the key_stage of the suggestion (a Y6 class might study a Y5 text for consolidation).

### MISSING: `writing_outcome` — ADD (required)

**Verdict**: ADD. Every English lesson has a **writing product**. The existing CVs all have this: `"Write an adventure narrative (500-700 words) with clear problem-resolution structure, vivid description, and dialogue"`. This tells the AI tutor exactly what the child should produce.

Without this, the AI has no idea whether a Y4 "Greek Myths" study should result in a retelling, an information text about ancient Greece, a diary entry from Theseus's perspective, or a comparative essay. These are completely different lessons.

**Proposed**: `writing_outcome: string` — the expected written output with approximate length and key features.

### MISSING: `grammar_focus` — ADD (required for KS1-KS3)

**Verdict**: ADD. The National Curriculum **explicitly** links grammar to year groups. Year 4 must cover fronted adverbials, expanded noun phrases, direct speech punctuation. These aren't optional — they're statutory. The existing CVs all have `grammar_focus` arrays.

An AI tutor generating a Y4 lesson without knowing the grammar focus will produce either: (a) generic grammar, (b) grammar from the wrong year group, or (c) no grammar at all. All three are failures.

**Proposed**: `grammar_focus: string[]` — required for KS1-KS3 where grammar is year-specific, optional for KS4 where grammar is embedded in writing quality assessment.

### MISSING: `text_type` — ADD (required)

**Verdict**: ADD as a higher-level classifier above `genre`.

**Proposed controlled vocabulary**: `fiction`, `non_fiction`, `poetry`, `drama`, `mixed`

**Rationale**: An AI tutor needs to know immediately whether it's dealing with a fiction or non-fiction study. The pedagogical approach is fundamentally different. A fiction text study uses inference, characterisation, empathy. A non-fiction study uses retrieval, organisation, evaluation. Genre alone doesn't cleanly separate these — `"report"` is always non-fiction, but `"recount"` could be fiction (diary of a fictional character) or non-fiction (autobiography).

### MISSING: `spoken_language_focus` — ADD (optional)

**Verdict**: ADD. Spoken language is a statutory cross-cutting requirement in KS1-KS4 English. The existing CV `EN-Y4-CV008` (Discussion and Debate) is primarily a spoken language activity. Many text studies include performance (reading aloud, drama, debate). The NC requires this but the schema ignores it.

**Proposed**: `spoken_language_focus: string` — e.g. `"performance reading"`, `"structured debate"`, `"dramatic role play"`, `"formal presentation"`. Optional because not every text study has an explicit spoken language component.

### MISSING: `exam_board_status` (KS4 only) — ADD

**Verdict**: ADD for KS4 English Literature suggestions. GCSE texts are SET by exam boards. Schools choose their exam board, then the texts are mandatory within that board's specification.

**Evidence from research**:
- AQA Shakespeare: Macbeth, Romeo & Juliet, The Tempest, Merchant of Venice, Much Ado About Nothing, Julius Caesar
- AQA 19th C: Great Expectations, Jane Eyre, Pride & Prejudice, Jekyll & Hyde, Christmas Carol, Frankenstein, Sign of Four
- AQA Modern: Inspector Calls, Blood Brothers, History Boys, DNA, Curious Incident, Lord of the Flies, Animal Farm, Never Let Me Go, Anita and Me, Pigeon English, My Name is Leon

Popularity: Macbeth 70-76%, Inspector Calls 56-84%, Christmas Carol + Jekyll & Hyde co-dominant for 19th C.

**Proposed**:
```json
"exam_board_status": [
  { "board": "AQA", "category": "shakespeare", "status": "set_text" },
  { "board": "Edexcel", "category": "shakespeare", "status": "set_text" },
  { "board": "OCR", "category": "shakespeare", "status": "set_text" }
]
```

This allows the AI tutor to filter by exam board and understand that "Macbeth" is a set text choice, not a free recommendation.

---

## 2. Universal Property Review

### `suggestion_type` — MODIFY for English

The proposed values `prescribed_topic`, `exemplar_topic`, `open_slot`, `exemplar_figure`, `exemplar_event`, `exemplar_text`, `teacher_convention` need English-specific additions:

- **`set_text`** — GCSE set text (mandatory once exam board is chosen). This is different from `prescribed_topic` because it's board-specific, not NC-mandated.
- **`exemplar_text`** already fits well for KS1-KS3 (e.g. "The Iron Man is a good choice for adventure narrative").
- **`genre_requirement`** — the NC says "pupils should write in a range of genres including...". The genre is prescribed; the specific text/topic within it is not. This is different from `open_slot` because it's genre-constrained.

### `curriculum_reference` — KEEP but note English complexity

In History, a curriculum reference is clean: "a study of an aspect of British history beyond 1066". In English, the reference is often spread across multiple places: the main Programme of Study, the spelling appendix, the grammar appendix, and the writing composition expectations. A single string may not suffice.

**Proposal**: Keep as string but allow references to multiple NC sections separated by `;`. E.g. `"Writing - Composition (Y3-4); English Appendix 2 (Y4 grammar); Reading - Comprehension (Y3-4)"`.

### `pedagogical_rationale` — KEEP, essential

This is excellent. For English, the rationale should explain WHY this text/genre is placed at this year group. E.g. "The Iron Man works for Y4 adventure narrative because its clear three-act structure models the problem-resolution pattern that Y4 writers need to internalise, its vocabulary is rich but accessible, and its themes (fear of the unknown, friendship) engage 8-9 year olds without being emotionally overwhelming."

### `definitions` — KEEP but distinguish literary terms from topic vocabulary

In History, definitions are content vocabulary ("empire", "pharaoh"). In English, definitions split into:
1. **Literary terminology** the child must learn to use: "protagonist", "metaphor", "stanza"
2. **Text-specific vocabulary** from the suggested text: "iron", "space-bat-angel-dragon" (Iron Man)

These serve different pedagogical purposes. The AI tutor needs literary terms for teaching and assessing; text-specific vocabulary is part of comprehension support.

**Proposal**: Either (a) add a `literary_terms: string[]` property separate from `definitions`, or (b) accept that `definitions` in English = literary terminology and text vocabulary is runtime.

### `common_pitfalls` — KEEP, add English-specific defaults

Useful. For English, common pitfalls include:
- Teaching grammar in isolation (not embedded in reading/writing)
- Spending too long on reading with no writing output
- Setting writing tasks that don't match the genre being studied
- Using texts that are too difficult/easy for the year group
- Neglecting spoken language in text study lessons

### `cross_curricular_hooks` — KEEP

Essential for English. Every English text study can hook into another subject: Greek Myths → History (Ancient Greece), Persuasive Writing → Geography (environmental issues), Information Texts → Science (topic reports). These hooks are bidirectional — English ALSO benefits from subject knowledge.

---

## 3. VehicleTemplate Critique

### Existing templates that work for English:

| # | Template | Verdict | Notes |
|---|---|---|---|
| 7 | `text_study` | KEEP | Core English template. Session structure is good: shared_reading → analysis → vocabulary → planning → drafting → editing. But needs variant for KS4 closed-book literature study (different structure). |
| 11 | `discussion_and_debate` | KEEP | Good for oracy-focused English work. Session structure works. |
| 12 | `creative_response` | KEEP | Works for creative writing and poetry performance. |

### Templates that need MODIFICATION for English:

**`text_study` needs TWO variants:**

1. **`text_study_primary`** (KS1-KS3): shared_reading → analysis → vocabulary → planning → drafting → editing → publishing
   - This is the "reading into writing" model used in all good primary English teaching
   - The writing outcome is the purpose; the reading is the model

2. **`text_study_literature`** (KS4): introduction → close_reading → analysis → contextualisation → essay_planning → essay_writing → peer_review
   - KS4 Literature is analytical, not creative — students write ABOUT texts, not inspired BY them
   - Closed-book exam means memorisation of quotations is part of the template
   - Context (AO3) is a specific assessed skill, not just background

### Templates MISSING for English:

| # | Proposed template | Subjects | Session structure | Rationale |
|---|---|---|---|---|
| 15 | `writers_workshop` | English | mini_lesson → independent_writing → conferencing → sharing → revision | The dominant primary writing pedagogy (Calkins/Graves model). Different from text_study because the starting point is the child's own writing, not a model text. Essential for extended writing units. |
| 16 | `grammar_in_context` | English | text_exploration → pattern_identification → rule_articulation → guided_practice → independent_application | Grammar MUST be taught in context (NC statutory guidance). This template ensures grammar isn't taught as isolated exercises but embedded in meaningful reading and writing. |
| 17 | `reading_for_pleasure` | English | book_talk → independent_reading → reading_journal → discussion → recommendation | Statutory requirement: "develop positive attitudes to reading and understanding of what they read" (KS2 NC). Not assessed, but essential for reading culture. |
| 18 | `spoken_language_performance` | English, Drama | text_selection → rehearsal → technique_practice → performance → evaluation | Covers poetry performance, dramatic reading, storytelling, presentation — all statutory spoken language requirements. |
| 19 | `unseen_analysis` | English | first_reading → annotation → structural_analysis → language_analysis → comparative_writing | KS4-specific. Unseen poetry and unseen prose are exam components requiring a specific analytical workflow that differs from studied text analysis. |

---

## 4. TopicSuggestion Inventory

### A. Naming: Should it be `EnglishTopicSuggestion` or `EnglishTextSuggestion`?

**Strong opinion**: English teaching is organised around **texts and genres**, not topics. A History teacher teaches "The Romans" (topic). An English teacher teaches "Adventure Narrative using The Iron Man" (genre + text). The "topic" in English IS the genre/text combination.

However, for schema consistency across the graph, I accept `EnglishTopicSuggestion` with the understanding that in English, a "topic suggestion" means "a genre + text pairing". The `name` property should reflect this: not "Adventure Stories" (too vague) but "Adventure Narrative: The Iron Man" (genre: text pattern, matching existing CV naming).

### B. KS1-KS2 Inventory (genres are the organising principle)

#### Year 1-2 (KS1)

| Name | Type | Genre | Curriculum basis |
|---|---|---|---|
| Traditional Tales: The Three Billy Goats Gruff | `exemplar_text` | `traditional_tale` | NC: "listening to and discussing a wide range of... traditional tales" |
| Fairy Tales: Cinderella | `exemplar_text` | `traditional_tale` | NC: "fairy stories" explicitly named |
| Poetry Recitation: Action Poems | `genre_requirement` | `poetry` | NC: "learning to appreciate rhymes and poems, and to recite some by heart" |
| Labels, Lists and Captions | `genre_requirement` | `instruction`, `information` | NC: "sequencing sentences to form short narratives... writing for different purposes" |
| Recount: My Weekend | `genre_requirement` | `recount` | NC: "write about real events" |
| Stories by Familiar Authors | `exemplar_text` | `narrative` | NC: "stories... by significant children's authors" — Julia Donaldson, Michael Rosen |

#### Year 3-4 (Lower KS2)

| Name | Type | Genre | Curriculum basis |
|---|---|---|---|
| Adventure Narrative: The Iron Man | `exemplar_text` | `narrative` | Genre convention; text is widely used |
| Myths and Legends: Greek Myths | `teacher_convention` | `traditional_tale` | NC: "myths, legends" in reading; cross-curricular with History KS2 Ancient Greece |
| Fairy Tale Retellings | `genre_requirement` | `traditional_tale` | NC: "increasing their familiarity with a wide range of books, including fairy stories" |
| Persuasive Writing: Formal Letter | `genre_requirement` | `persuasion` | NC: "composing and rehearsing sentences orally... progressively building a varied and rich vocabulary" + writing for purpose |
| Poetry: Performance and Form | `genre_requirement` | `poetry` | NC: "preparing poems and play scripts to read aloud and to perform... showing understanding through intonation, tone, volume and action" |
| Non-Chronological Report | `genre_requirement` | `report` | NC: "retrieve and record information from non-fiction" + cross-curricular writing |
| Discussion Text: Balanced Argument | `genre_requirement` | `discussion` | NC: "listening to and discussing a wide range of fiction, poetry, plays, non-fiction and reference books" |
| Spelling and Vocabulary Study | `prescribed_topic` | N/A | NC: statutory Y3-4 word list + English Appendix 1 spelling rules |

#### Year 5-6 (Upper KS2)

| Name | Type | Genre | Curriculum basis |
|---|---|---|---|
| Classic Fiction: Shakespeare Retelling | `prescribed_topic` | `drama`, `narrative` | NC: "Shakespeare (2 plays)" — statutory at KS2. Usually simplified retellings (Leon Garfield, Andrew Matthews, Marcia Williams) |
| Narrative: Suspense and Mystery | `genre_requirement` | `narrative` | NC: "plan their writing... noting and developing initial ideas, drawing on reading" |
| Biography and Autobiography | `genre_requirement` | `recount` | NC: "distinguish between statements of fact and opinion... retrieve, record and present information" |
| Formal Report Writing | `genre_requirement` | `report` | NC: "use further organisational and presentational devices" |
| Debate and Spoken Argument | `genre_requirement` | `discussion` | NC: "participate in discussions... use spoken language to develop understanding" |
| Poetry: Comparison and Analysis | `genre_requirement` | `poetry` | NC: "learn a wider range of poetry by heart... prepare poems and plays to read aloud" |
| Newspaper Report | `teacher_convention` | `recount` | Not statutory but near-universal in Y5-6 teaching |
| Explanation Text | `genre_requirement` | `explanation` | Cross-curricular; NC requires writing for different purposes |

### C. KS3 Inventory

| Name | Type | Genre | Curriculum basis |
|---|---|---|---|
| Gothic Fiction | `teacher_convention` | `fiction` | Near-universal KS3 unit; preparation for KS4 19th-C novel |
| War Poetry | `teacher_convention` | `poetry` | NC KS3: "seminal world literature"; Wilfred Owen, Siegfried Sassoon |
| Shakespeare: A Midsummer Night's Dream | `exemplar_text` | `drama` | NC: "two Shakespeare plays" at KS3 |
| Shakespeare: The Tempest | `exemplar_text` | `drama` | NC: "two Shakespeare plays" at KS3 |
| Dystopian Fiction | `teacher_convention` | `fiction` | Popular KS3 unit (Animal Farm, Noughts and Crosses, The Giver) |
| Travel Writing | `genre_requirement` | `literary_nonfiction` | NC KS3: "literary non-fiction" |
| Spoken Language: Debate | `genre_requirement` | `discussion` | NC KS3: "speak confidently and effectively" |
| Creative Writing Portfolio | `genre_requirement` | `creative_writing` | NC KS3: "write accurately, fluently, effectively and at length for pleasure and information" |

### D. KS4 English Literature Inventory (set texts)

These are organised by GCSE assessment component, not by genre. Each exam board offers a menu; schools choose one text per category.

#### Shakespeare (all boards require one play)

| Name | Type | Boards | Popularity |
|---|---|---|---|
| Macbeth | `set_text` | AQA, Edexcel, OCR, Eduqas | 70-76% |
| Romeo and Juliet | `set_text` | AQA, Edexcel, OCR, Eduqas | ~20% |
| The Tempest | `set_text` | AQA, Edexcel | ~3% |
| Merchant of Venice | `set_text` | AQA, Edexcel, OCR, Eduqas | ~2% |
| Much Ado About Nothing | `set_text` | AQA, Edexcel, OCR, Eduqas | ~2% |
| Julius Caesar | `set_text` | AQA | <1% |
| Twelfth Night | `set_text` | Edexcel, Eduqas | <2% |
| Othello | `set_text` | Eduqas | <1% |

#### 19th-Century Novel (all boards require one)

| Name | Type | Boards | Popularity |
|---|---|---|---|
| A Christmas Carol | `set_text` | AQA, Edexcel, OCR, Eduqas | Co-dominant |
| Jekyll and Hyde | `set_text` | AQA, Edexcel, OCR, Eduqas | Co-dominant |
| Great Expectations | `set_text` | AQA, Edexcel, OCR | Moderate |
| Jane Eyre | `set_text` | AQA, Edexcel, OCR, Eduqas | Moderate |
| Frankenstein | `set_text` | AQA, Edexcel | Growing |
| Pride and Prejudice | `set_text` | AQA, Edexcel, OCR, Eduqas | Moderate |
| The Sign of Four | `set_text` | AQA | Low |
| Silas Marner | `set_text` | Edexcel, Eduqas | Low |
| War of the Worlds | `set_text` | OCR, Eduqas | Moderate |

#### Modern Text (post-1914, all boards require one)

| Name | Type | Boards | Popularity |
|---|---|---|---|
| An Inspector Calls | `set_text` | AQA, Edexcel, OCR, Eduqas | 56-84% |
| Blood Brothers | `set_text` | AQA, Edexcel, Eduqas | Moderate |
| Lord of the Flies | `set_text` | AQA, Edexcel, Eduqas | Moderate |
| Animal Farm | `set_text` | AQA, Edexcel, OCR | Moderate |
| DNA | `set_text` | AQA, OCR | Low |
| Never Let Me Go | `set_text` | AQA, OCR | Growing |
| Anita and Me | `set_text` | AQA, Edexcel, OCR, Eduqas | Growing |
| The History Boys | `set_text` | AQA | Low |
| Curious Incident | `set_text` | AQA | Moderate |
| Pigeon English | `set_text` | AQA | Low |
| My Name is Leon | `set_text` | AQA | New |

#### Poetry Anthology (board-specific clusters)

| Name | Type | Board | Notes |
|---|---|---|---|
| Power and Conflict (AQA) | `set_text` | AQA | 15 poems, dominant choice |
| Love and Relationships (AQA) | `set_text` | AQA | 15 poems |
| Worlds and Lives (AQA) | `set_text` | AQA | 15 poems, new for 2025 |
| Relationships (Edexcel) | `set_text` | Edexcel | |
| Conflict (Edexcel) | `set_text` | Edexcel | |
| Time and Place (Edexcel) | `set_text` | Edexcel | |
| Belonging (Edexcel) | `set_text` | Edexcel | |

### E. KS4 English Language (no set texts, but genre requirements)

English Language doesn't use set texts. Instead, it requires students to write in specific forms:

| Name | Type | Genre | Assessment |
|---|---|---|---|
| Narrative and Descriptive Writing | `genre_requirement` | `creative_writing` | Paper 1 Section B |
| Transactional Writing: Article | `genre_requirement` | `transactional` | Paper 2 Section B |
| Transactional Writing: Letter | `genre_requirement` | `transactional` | Paper 2 Section B |
| Transactional Writing: Speech | `genre_requirement` | `transactional` | Paper 2 Section B |
| Transactional Writing: Review | `genre_requirement` | `transactional` | Paper 2 Section B |
| Unseen Fiction Analysis | `genre_requirement` | `fiction` | Paper 1 Section A |
| Unseen Non-Fiction Comparison | `genre_requirement` | `literary_nonfiction` | Paper 2 Section A |

---

## 5. Content Generation Requirements

### What the AI tutor needs to generate a good Y4 "Adventure Narrative" lesson:

1. **Genre** (`narrative`) + **text_features** (`["problem-resolution structure", "vivid description", "dialogue to advance plot"]`) — tells the AI WHAT to teach
2. **Suggested text** (The Iron Man, Ted Hughes) — gives a specific anchor text for shared reading
3. **Writing outcome** ("Write an adventure narrative of 500-700 words...") — tells the AI what the child produces
4. **Grammar focus** (`["fronted adverbials", "expanded noun phrases", "direct speech punctuation"]`) — the statutory grammar to embed
5. **Reading level** ("Y3-Y5") — prevents the AI selecting a text that's too hard or easy
6. **Definitions/literary terms** (`["protagonist", "antagonist", "climax"]`) — vocabulary to introduce
7. **VehicleTemplate** (`text_study_primary`) — the session structure
8. **DifficultyLevel** from the graph — tells the AI whether this is entry/developing/expected/greater_depth work
9. **Pedagogical rationale** — WHY this text works for these concepts (the AI can explain this to parents)
10. **ThinkingLens** — the cognitive framing (e.g. "Structure & Function" for narrative structure)

### What the AI needs for a Y10 "Macbeth Act 3 Scene 1" analysis:

1. **Text** (Macbeth, Shakespeare) with **exam_board_status** (AQA set text, Shakespeare category)
2. **Genre** (`drama`) + **text_type** (`drama`)
3. **Text features** — irrelevant at this level; replaced by assessment objectives: AO1 (response + evidence), AO2 (language, form, structure), AO3 (context)
4. **Writing outcome** ("Write an analytical essay (600-800 words) exploring how Shakespeare presents the theme of ambition in Act 3 Scene 1, using quotations and contextual knowledge")
5. **Grammar focus** — not year-specific at KS4; embedded in writing quality (AO4)
6. **Key quotations** — the AI needs to know which quotations are essential for this scene (closed-book exam)
7. **Context points** — Jacobean kingship, the Gunpowder Plot, the Great Chain of Being
8. **VehicleTemplate** (`text_study_literature`) — the analytical study structure
9. **DifficultyLevel** — emerging/developing/secure/mastery maps to grade boundaries

### What the AI needs for a video script:

Everything above PLUS:
- **Spoken language focus** — is this a performance piece? Dramatic reading? Analytical explanation?
- **Cross-curricular hooks** — can the video reference History, Geography, Science connections?
- The **pedagogical_rationale** becomes the script's "why this matters" section

### What the AI needs for assessment:

- **DifficultyLevel** nodes provide `example_task`, `example_response`, `common_errors` — essential
- **Writing outcome** defines what the assessment task IS
- **Grammar focus** defines what to mark for (at KS1-KS3)
- **Text features** define the success criteria
- The AI should generate assessment at the right DifficultyLevel, not one-size-fits-all

---

## 6. Cross-Curricular Hooks

English is the most cross-curricular subject. Every topic in every other subject requires English skills. The hooks should be **bidirectional** and **specific**:

### English → Other Subjects

| English suggestion | Links to | Hook |
|---|---|---|
| Greek Myths (Y3-4) | History: Ancient Greece | Shared vocabulary, historical context enriches reading |
| Persuasive Letter (Y3-4) | Geography: Local area study | Real-world purpose for persuasive writing |
| Non-Chronological Report (Y3-5) | Science: any topic | Cross-curricular writing; report structure transfers |
| Biography (Y5-6) | History: any period | Historical figures provide writing subjects |
| Explanation Text (Y5-6) | Science: forces, materials, light | Scientific processes need explanation text structure |
| Macbeth (KS4) | History: Jacobean England, divine right of kings | AO3 context is essentially a history question |
| Inspector Calls (KS4) | History: Edwardian England, welfare state | Social and historical context drives interpretation |
| War Poetry (KS3) | History: WWI | Impossible to teach one without the other |
| Christmas Carol (KS4) | History: Victorian poverty, workhouses | Dickens as social reformer requires historical knowledge |

### Other Subjects → English

| Other subject suggestion | English skills required | Hook |
|---|---|---|
| Any History source analysis | Reading: inference, evaluating reliability | Historical sources ARE texts |
| Any Geography fieldwork report | Writing: report structure, technical vocabulary | Fieldwork write-up IS non-chronological report |
| Any Science investigation | Writing: explanation, method, conclusion | Scientific writing IS a genre |
| RS: ethical debates | Spoken language: structured discussion, balanced argument | Debate skills transfer directly |

---

## 7. Stress Test Scenarios

### Scenario 1: Year 4 pupil, adventure narrative unit, developing level

**The query**: "Generate a 3-lesson sequence on adventure narrative for a Y4 class, most pupils at developing level."

**What the schema must provide**:
- `EnglishTopicSuggestion`: Adventure Narrative: The Iron Man
- `genre`: `["narrative"]`, `text_type`: `"fiction"`
- `text_features`: `["problem-resolution structure", "vivid description", "dialogue to advance plot", "building suspense"]`
- `writing_outcome`: "Write an adventure narrative (500-700 words) with clear problem-resolution structure"
- `grammar_focus`: `["fronted adverbials", "expanded noun phrases", "direct speech punctuation"]`
- `reading_level`: `"Y3-Y5"`
- `VehicleTemplate`: `text_study_primary` — shared_reading → analysis → vocabulary → planning → drafting → editing
- `DifficultyLevel`: developing (level 2) — the AI scaffolds more, provides sentence starters, models structures
- `ThinkingLens`: Structure & Function — "How does the author build this story? What are the parts?"

**Does the proposed schema handle this?** PARTIALLY. Missing `writing_outcome`, `grammar_focus`, `reading_level`. Without these, the AI doesn't know what the child should produce, which grammar to embed, or whether The Iron Man is age-appropriate.

### Scenario 2: Year 10 pupil, Macbeth revision, secure level, AQA exam board

**The query**: "Generate a revision activity on Macbeth Act 1 Scene 7 for a Y10 student at secure level, AQA board."

**What the schema must provide**:
- `EnglishTopicSuggestion`: Macbeth (Shakespeare)
- `exam_board_status`: `[{board: "AQA", category: "shakespeare", status: "set_text"}]`
- `genre`: `["drama"]`, `text_type`: `"drama"`
- `text_features`: `["soliloquy", "blank verse", "dramatic irony", "supernatural elements"]` (play-level features)
- `writing_outcome`: "Write an analytical paragraph responding to: How does Shakespeare present Macbeth's internal conflict in Act 1 Scene 7?"
- `VehicleTemplate`: `text_study_literature` — close_reading → analysis → contextualisation → essay_writing
- `DifficultyLevel`: secure (level 3) — expects independent analysis with embedded quotations, some contextual links
- Key context: Lady Macbeth's manipulation, the concept of masculinity, Jacobean honour codes

**Does the proposed schema handle this?** POORLY. No `exam_board_status`, no `writing_outcome`, no way to distinguish "Macbeth as a KS4 set text for close analytical study" from "Macbeth as a KS2 simplified retelling for reading enjoyment". The `suggestion_type` values don't include `set_text`.

### Scenario 3: Year 6 pupil, SATs preparation, non-fiction reading comprehension

**The query**: "Generate a reading comprehension practice for Y6 SATs prep, using a non-fiction text."

**What the schema must provide**:
- This is an English Language / Reading skill, not a text study
- The AI needs: `text_type`: `"non_fiction"`, `genre`: `["report", "explanation"]`
- SATs assess: retrieval (2a), inference (2d), vocabulary in context (2a), summarising (2c), comparing (2h)
- The AI generates an appropriate text at Y6 reading level and then writes SATs-style questions
- `VehicleTemplate`: `unseen_analysis` — first_reading → annotation → question_response → review

**Does the proposed schema handle this?** NO. There's no mechanism for assessment-focused suggestions that aren't tied to a specific text. Y6 SATs reading uses UNSEEN texts — the AI must generate or select a text and then create questions. This is a fundamentally different use case from "study The Iron Man".

**Proposal**: Add `assessment_mode` property: `formative` (in-lesson checks), `summative` (end-of-unit), `exam_practice` (SATs/GCSE style). This tells the AI whether to generate teaching activities or assessment tasks.

### Scenario 4: Reception/Year 1 transition, phonics-based reading

**The query**: "Generate a shared reading session for a Y1 class using a decodable text."

**What the schema must provide**:
- Y1 English is dominated by PHONICS, not genres. The text must match the phonics phase.
- `reading_level`: `"Phase 5"` (Letters and Sounds phonics framework)
- `text_type`: `"fiction"` (decodable reader)
- `text_features`: `["CVC words", "digraphs", "adjacent consonants", "high-frequency tricky words"]`

**Does the proposed schema handle this?** POORLY. The `reading_level` property I proposed (e.g. "Y1") is too coarse for KS1. For Y1-Y2, reading level should reference the phonics phase or a book band (e.g. "Book Band: Orange / Phase 5"). This is a KS1-specific refinement.

---

## 8. Summary: Top 3 Recommendations

### 1. ADD the three missing essential properties: `writing_outcome`, `grammar_focus`, `reading_level`

**Impact**: CRITICAL. These are the three properties that make the difference between "the AI knows English is a subject" and "the AI can actually generate an English lesson". Every existing ContentVehicle has them. They were present in the data that teachers reviewed and rated 6.6/10. Removing them would drop content generation readiness back to 3/10 or below.

- `writing_outcome: string` (required) — what the child produces
- `grammar_focus: string[]` (required KS1-KS3, optional KS4) — year-specific statutory grammar
- `reading_level: string` (required) — age-appropriateness of the text/content

### 2. ADD `exam_board_status` for KS4 and change `genre` to `string[]`

**Impact**: HIGH. Without `exam_board_status`, the schema cannot represent the most fundamental fact of KS4 English teaching: texts are set by exam boards. 84% of AQA students study Inspector Calls — this isn't a "suggestion", it's a curricular fact. The AI tutor MUST know which board the school uses to generate relevant revision content.

Changing `genre` from `string` to `string[]` with a controlled vocabulary prevents the proliferation of ad-hoc genre labels (the existing CVs already show inconsistency: "adventure narrative", "myth and legend", "persuasive letter", "balanced discussion text" — these mix form, purpose, and tradition).

### 3. ADD `text_study_literature`, `writers_workshop`, and `grammar_in_context` VehicleTemplates

**Impact**: HIGH. The current `text_study` template assumes the primary "reading into writing" model. This works for KS1-KS3 but is wrong for KS4 Literature, where students write ABOUT texts analytically, not creatively inspired by them. Two separate templates prevent the AI from generating Y10 Macbeth lessons that end with "Now write your own tragedy!" (a real and embarrassing failure mode).

`writers_workshop` is the dominant primary writing pedagogy — omitting it means the graph has no template for the 40-50% of English lessons that start from the child's own writing rather than a model text. `grammar_in_context` prevents the worst sin in English teaching: isolated grammar worksheets disconnected from reading and writing.

---

## Appendix: Complete Proposed EnglishTopicSuggestion Schema

| Property | Type | Required | Notes |
|---|---|---|---|
| `suggestion_id` | string | Yes | Format: `TS-EN-{KS}-{number}` or `TS-ELT-{KS}-{number}` for Literature |
| `name` | string | Yes | Pattern: "{Genre}: {Text/Theme}" e.g. "Adventure Narrative: The Iron Man" |
| `suggestion_type` | string | Yes | `prescribed_topic`, `exemplar_text`, `genre_requirement`, `set_text`, `teacher_convention`, `open_slot` |
| `text_type` | string | Yes | `fiction`, `non_fiction`, `poetry`, `drama`, `mixed` |
| `genre` | string[] | Yes | From controlled vocabulary (see Section 1). First element = primary. |
| `text_features` | string[] | Yes | Textual/genre features to teach and assess |
| `suggested_texts` | object[] | No | `{title, author, publication_year, text_type, suitability, note}` |
| `reading_level` | string | Yes | Year-based ("Y3-Y5"), phonics-based ("Phase 5"), or KS-based ("KS4") |
| `writing_outcome` | string | Yes | Expected written output with approximate length and key features |
| `grammar_focus` | string[] | Yes (KS1-3) | Year-specific statutory grammar to embed |
| `spoken_language_focus` | string | No | Performance, debate, presentation, dramatic role play |
| `exam_board_status` | object[] | No (KS4 only) | `{board, category, status}` for GCSE set texts |
| `assessment_mode` | string | No | `formative`, `summative`, `exam_practice` |
| `literary_terms` | string[] | No | Subject-specific terminology to introduce |
| *Plus all universal properties from briefing* | | | `subject`, `key_stage`, `curriculum_status`, `pedagogical_rationale`, `definitions`, `common_pitfalls`, `cross_curricular_hooks`, display props |

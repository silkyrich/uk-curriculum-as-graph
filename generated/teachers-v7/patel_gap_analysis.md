# Gap Analysis: Y3 English — Knowledge Graph Readiness

**Teacher:** Ms. Patel, Y3 Class Teacher & English Lead (10 years, Leicester)
**Cluster reviewed:** EN-Y3-D004-CL001 — Apply prefixes, suffixes and doubling rules to spell derived words
**Date:** 2026-02-23

---

## Overall Readiness Score: 5.5 / 10

The graph understands the STRUCTURE of Y3 English very well — 7 domains, 20 clusters, clear sequencing, accurate curriculum alignment. The concept descriptions, teaching guidance, and misconception data are genuinely excellent. But the graph fundamentally lacks CONTENT for English: no texts, no word lists, no model sentences, no content vehicles, no difficulty levels. English is a content-hungry subject — you cannot teach a spelling lesson without actual words, or a reading lesson without an actual text. The structure is solid but the cupboard is bare.

For comparison: the graph appears to have content vehicles for Y4 English (8 text studies) and Y3 Maths (difficulty levels). Y3 English has neither. This makes it the least "teach-ready" of the subjects I'd expect to be priorities.

---

## Y3 English-Specific Gaps

### 1. The Phonics-to-Spelling Bridge (Critical Gap)

Y3 is THE transition year — children move from "learning to read" to "reading to learn." The graph has 53 KS1 English concepts and 41+ Y3 English concepts, which is structurally correct. But the prerequisite links between KS1 and Y3 spelling are incomplete:

**What's linked:**
- KS1 Contractions → Y3 Prefix/suffix rules ✓
- KS1 Possessive apostrophes → Y3 Prefix/suffix rules ✓
- KS1 Spelling using phonemes → Y3 Homophones ✓
- KS1 Homophones → Y3 Homophones ✓
- KS1 Spelling patterns → Y3 Statutory word list ✓

**What's missing:**
- KS1 Suffixes (C027) → Y3 Prefix/suffix rules (C034) — NOT linked
- KS1 Prefixes (C028) → Y3 Prefix/suffix rules (C034) — NOT linked
- KS1 Root words (C029) → Y3 Prefix/suffix rules (C034) — NOT linked
- KS1 Segmenting (C005) → Y3 Suffix doubling (C035) — NOT linked (segmenting into syllables is essential for stress identification)
- KS1 Syllables (C012) → Y3 Suffix doubling (C035) — NOT linked (children must understand syllables to apply the doubling rule)

These are not obscure connections — they are the most direct conceptual prerequisites. A child who doesn't know what a suffix is cannot learn suffix doubling rules. The graph links to contractions and possessive apostrophes instead, which are from the same domain but are tangential to morphological spelling.

### 2. No Text Recommendations or Reading Levels for Y3

The content guidelines give a Lexile range (150–350L) and FK grade max (2), which is useful for AI-generated content. But for English specifically, teachers need:
- **Recommended texts** for guided reading and shared reading (the curriculum says "read widely across fiction, poetry and non-fiction")
- **Reading level guidance** — which book bands map to the 150–350L range?
- **Genre lists** — what genres should Y3 be encountering? The graph has a reading comprehension cluster (EN-Y3-D003-CL002) that mentions "themes, conventions and language in fiction and poetry" but no specific genre or text recommendations

The Y4 English content vehicles include named texts (The Iron Man, Greek Myths, etc.) — Y3 English has nothing equivalent.

### 3. No Writing Scaffolds or Model Texts

The writing composition domain (EN-Y3-D006) has 3 clusters covering planning, paragraphing, and evaluating. The teaching guidance says "Plan writing from model texts and generate ideas." But the graph provides:
- No model texts
- No writing frames
- No genre-specific scaffolds (narrative, recount, instruction, explanation, persuasion)
- No example paragraphs showing Y3-standard writing

For English, model texts aren't supplementary — they ARE the curriculum. You cannot teach "organise writing into paragraphs" without showing children what a well-paragraphed piece looks like.

### 4. No Difficulty Levels for English

The DifficultyLevel layer has been piloted for Y3 Maths (41 concepts, ~150 difficulty nodes with entry/developing/expected/greater_depth). Y3 English has zero difficulty levels. For a spelling concept like EN-Y3-C034, I would expect:

- **Entry:** Add un- to happy, kind, fair (common single-syllable roots)
- **Developing:** Add dis-, mis-, re- to familiar words (disagree, misplace, rewrite)
- **Expected:** Add super-, anti-, auto- to less familiar roots (supermarket, antiseptic, autograph)
- **Greater depth:** Recognise that adding a prefix never changes root word spelling, even when it creates double letters (misspell, unnecessary)

Without these, the graph has no concept of differentiation within a concept — every child gets the same level.

### 5. Interaction Types Are Subject-Agnostic

The learner profile provides Y3 interaction types that work well for some subjects (drag_categorise, matching_pairs, multi_choice) but the secondary list includes maths-specific tools (area_model_multiplication, column_subtraction, fraction_visualizer, place_value_blocks) that are irrelevant for English. Missing English-specific interactions:
- Sentence builder / word builder
- Cloze procedure (fill the gap in a sentence)
- Dictation / write from memory
- Spelling test / look-cover-write-check
- Read-aloud with TTS comparison
- Handwriting practice tool

The graph's writing from dictation concept (EN-Y3-C041) describes dictation as a learning activity but there is no corresponding dictation interaction type.

### 6. No Phonics Consolidation Layer

Y3 English still requires phonics consolidation for lower attainers — roughly 20-30% of a typical Y3 class. The graph treats phonics as a KS1 concept (correctly) but has no mechanism for flagging which Y3 children need phonics intervention or which specific GPCs they might still be shaky on. There is no link between the KS1 phonics concepts and Y3 spelling concepts that says "if the child hasn't mastered KS1-C003 (GPC), they will struggle with Y3-C037 (etymology-based spelling patterns)."

### 7. No Grammar-Spelling Integration

In practice, Y3 spelling and grammar are taught together — prefixes change meaning AND word class, suffixes change word class (happy → happily, adjective → adverb). The graph has these in separate domains (D004 Spelling, D007 Grammar) with separate clusters. The grammar cluster EN-Y3-D007-CL003 covers "noun formation using prefixes" (EN-Y3-C060) and the spelling cluster EN-Y3-D004-CL001 covers "prefix spelling rules" (EN-Y3-C034). These are the SAME prefixes taught for two different purposes, but there is no CO_TEACHES or cross-domain link between them. A teacher would naturally combine these; the graph separates them.

---

## What the Graph Does Well for Y3 English

To be fair, several things are genuinely strong:

1. **Misconception data** — the best I've seen in any planning resource. Specific, per-concept, with actual error examples (e.g., "dissappoint" not "disappoint"). This alone would save me planning time.

2. **Curriculum context** — the domain-level curriculum_context property gives an accurate overview of what Y3 spelling is about and where it fits in the progression. Reads like a confident curriculum document.

3. **Cluster sequencing** — the three spelling clusters (rules → patterns → application) follow a sensible teaching progression. The SEQUENCED_AFTER chain is correct.

4. **Thinking lens fit** — "Patterns" is exactly the right lens for morphological spelling. The rationale explains why, and the question stems are directly usable: "What rule connects these examples?" is a good spelling investigation question.

5. **Pedagogy profile** — the session sequence (challenge → guided exploration → worked example → practice → retrieval) matches evidence-based spelling teaching. Productive failure is correctly flagged as appropriate for Y3.

6. **Feedback guidance** — the "specific competence" approach is right for spelling. Naming the rule the child applied is much better than "Well done!" The avoid-phrases list (no "Wrong", no "Amazing!") matches current best practice.

---

## Top 5 Data Additions

### 1. Y3 English Content Vehicles (Priority: Critical)
Create text_study vehicles for Y3 English, similar to the Y4 set. At minimum:
- Narrative text study (e.g., "The Hodgeheg" by Dick King-Smith or "The Twits" by Roald Dahl)
- Traditional tale/myth text study (e.g., "The Pied Piper" or Anansi stories)
- Poetry text study (e.g., Michael Rosen or Joseph Coelho)
- Non-fiction text study (e.g., information text about animals or historical events)
- Spelling investigation pack (word sorts, dictation passages, prefix/suffix games)

Each should include `genre`, `grammar_focus`, `reading_level`, and `text_recommendations` properties — just as Y4 vehicles have.

### 2. Fix KS1→Y3 Spelling Prerequisite Links (Priority: Critical)
Add the missing PREREQUISITE_OF relationships:
- EN-KS1-C027 (Suffixes) → EN-Y3-C034 (Prefix/suffix spelling rules)
- EN-KS1-C028 (Prefixes) → EN-Y3-C034 (Prefix/suffix spelling rules)
- EN-KS1-C029 (Root words) → EN-Y3-C034 (Prefix/suffix spelling rules)
- EN-KS1-C012 (Syllables) → EN-Y3-C035 (Suffix doubling rules)
- EN-KS1-C005 (Segmenting) → EN-Y3-C035 (Suffix doubling rules)
- EN-KS1-C027 (Suffixes) → EN-Y3-C035 (Suffix doubling rules)

These are direct conceptual dependencies, not optional links.

### 3. Difficulty Levels for Y3 English (Priority: High)
Extend the DifficultyLevel pilot from Y3 Maths to Y3 English. Start with the spelling domain (D004) — 8 concepts with 3-4 levels each would give ~30 DifficultyLevel nodes. Each level needs:
- `description` — what the child can do at this level
- `example_task` — a specific spelling task
- `example_response` — a correct response
- `common_errors` — typical mistakes at this level

### 4. Cross-Domain CO_TEACHES for Spelling ↔ Grammar (Priority: High)
Add CO_TEACHES relationships between:
- EN-Y3-C034 (prefix/suffix spelling) ↔ EN-Y3-C060 (noun formation using prefixes)
- EN-Y3-C034 (prefix/suffix spelling) ↔ EN-Y3-C062 (word families)
- EN-Y3-C035 (suffix doubling) ↔ EN-Y3-C057 (present perfect tense) — doubling applies when forming past participles

### 5. English-Specific Interaction Types (Priority: Medium)
Add interaction types for English/literacy:
- `cloze_procedure` — fill the gap in a sentence (essential for grammar and spelling in context)
- `word_builder` — combine morphemes to build words (prefix + root + suffix)
- `dictation_tool` — listen and write (links to EN-Y3-C041)
- `look_cover_write_check` — the standard spelling practice method
- `sentence_reorder` — drag words into correct sentence order (grammar)

---

## Specific New Entities/Properties Wanted

### New Node Properties:
| Property | Node Type | Purpose |
|----------|-----------|---------|
| `success_criteria` (array of strings) | ConceptCluster | Pre-formed "I can..." statements for each cluster |
| `text_recommendations` (array of objects) | ConceptCluster or Domain | Named texts with reading level, genre, and curriculum links |
| `word_lists` (object) | Concept | Curated word lists for spelling concepts — grouped by difficulty |
| `model_sentences` (array of strings) | Concept | Example sentences showing the concept in use |
| `book_band_range` | ContentGuideline | Map Lexile to UK book bands (Turquoise/Purple/Gold etc.) |
| `phonics_phase_assumed` | Concept | Which Letters and Sounds phase must be secure for this concept |
| `ks2_test_domain_code` | Concept | Link to assessment layer content domain codes |

### New Relationship Types:
| Relationship | From → To | Purpose |
|-------------|-----------|---------|
| `CONSOLIDATES` | Y3 Concept → KS1 Concept | "This Y3 concept requires ongoing consolidation of this KS1 skill" (for phonics/handwriting) |
| `CONTEXTUALISES_VOCABULARY_FOR` | English Concept → Subject | Cross-subject vocabulary links (e.g., prefix "re-" used in Science: reversible, renewable) |
| `ASSESSED_BY` | Concept → ContentDomainCode | Direct concept → KS2 test framework link |

### New Nodes:
| Node Type | Purpose |
|-----------|---------|
| `TextRecommendation` | Named text with metadata: title, author, genre, reading level, year group, curriculum links |
| `WritingFrame` | Genre-specific scaffold: narrative, recount, explanation, instruction, persuasion, discussion |
| `SpellingPattern` | Curated pattern with word list: e.g., "-tion words", "silent k words", "French ch words" |

---

## Comparison with V5 Review Findings

The V5 teacher review (generated/teachers-v4/) identified similar themes:
- Content generation readiness improved from 3.7/10 to 6.6/10 with content vehicles — but those vehicles are Y4, not Y3
- "No worked examples" was a consensus finding — confirmed for Y3 English
- "Incomplete vehicle coverage" — Y3 English has zero vehicles
- "Thinking Lens rationales age-inappropriate for KS1" — for Y3, the Patterns lens rationale is appropriate

My 5.5/10 is lower than the V5 average of 6.6/10 because Y3 English specifically lacks the content vehicles that boosted other subjects' scores.

---

## Teaching Artefacts Needed

What would I actually need to walk from "lesson plan on screen" to "ready to teach this spelling lesson at 9:15 on Monday morning"? Here are my top 5, in order, specific to Y3 English and this spelling cluster.

### 1. Word Cards / Word Mats (Priority: Essential)

**What it is:** Printed cards with root words, prefixes, and suffixes that children physically manipulate — snap together, sort, build.

**Why it matters for Y3 English spelling specifically:** Morphological spelling is PHYSICAL at this age. Children need to see "dis" as a separate chunk they attach to "appear" to make "disappear." A word mat on every table showing the Y3 prefixes (un-, dis-, mis-, re-, super-, sub-, anti-, auto-) with their meanings is the single most-used resource in my spelling lessons. I laminate one per table and they stay up for the half-term.

**What I'd want generated:**
- Prefix cards (one per prefix, with meaning on the reverse)
- Root word cards that pair with each prefix (6-8 per prefix)
- Suffix cards (-ing, -ed, -er, -est, -ly, -ous, -tion, -sion)
- A word mat showing all Y3 prefixes, their meanings, and 2-3 example words each
- A "doubling rule" reference card: stressed syllable → double, unstressed → don't

**Graph data available:** The concept descriptions list all the relevant prefixes and suffixes, plus example words. The teaching guidance mentions "word-sorting and word-building activities." The raw data is there — it just needs formatting into printable card sets.

### 2. Differentiated Practice Sheets (Priority: Essential)

**What it is:** Three versions of a practice worksheet — support (working towards), core (expected), and extension (greater depth) — that children work through independently or in guided groups.

**Why it matters for Y3 English spelling:** In a typical Y3 class of 30, I'll have 5-6 children still consolidating KS1 phonics, 18-20 at expected level, and 4-5 ready for greater depth. A single worksheet doesn't work. The support version needs fewer words, all 2-syllable, with the prefix/suffix already printed as a separate element. The extension version needs 3-syllable words, words where doubling creates unusual-looking spellings (misspell, unnecessary), and an investigative element.

**What I'd want generated:**
- **Support:** 8 questions, prefixes only (un-, dis-, re-), root word given, child writes the combined word. Visual scaffolding — root word in black, prefix in blue.
- **Core:** 12 questions mixing prefixes and suffix doubling. Root word given, child adds the correct prefix/suffix and explains the rule.
- **Extension:** 8 questions with trickier words (occur→occurring, prefer→preferred vs preference), plus a "spelling detective" investigation: "Find 3 words in the dictionary that use the prefix anti-. What do they all have in common?"

**Graph data available:** The misconception data tells me exactly what errors to design distractors around. The teaching guidance describes activity types. But there are no actual word lists graded by difficulty — the DifficultyLevel layer hasn't been built for English.

### 3. Knowledge Organiser (Priority: High)

**What it is:** A single A4 sheet summarising everything a child needs to know about this topic — key vocabulary, rules, examples, and common errors. Goes in the front of their English book and on the working wall.

**Why it matters for Y3 English:** Knowledge organisers are now standard practice in most primary schools. For spelling, they serve as a permanent reference — children check their KO before asking "how do you spell...?" A good spelling KO includes the rules, 5-6 example words per rule, and the 2-3 most common mistakes to avoid. Children refer to it during independent writing across ALL subjects, not just English lessons.

**What I'd want generated:**
- Title: "Y3 Spelling: Prefixes, Suffixes and Doubling Rules"
- Section 1: Prefix rules with examples (the root word NEVER changes)
- Section 2: Suffix doubling rule with the "clap test" for stress
- Section 3: Key vocabulary with child-friendly definitions
- Section 4: "Watch out!" — the 5 most common errors from the misconception data
- Section 5: Statutory word list words that use these rules (e.g., disappear, different, separate)

**Graph data available:** Excellent. The concept descriptions, key vocabulary, and misconception data provide almost everything needed. The statutory word list (EN-Y3-C038) gives the word list. This is the artefact the graph is CLOSEST to being able to generate right now.

### 4. Interactive Whiteboard Slides (Priority: High)

**What it is:** 10-15 slides for the lesson — not a PowerPoint presentation to read from, but prompts, word displays, sorting activities, and worked examples projected on the interactive whiteboard.

**Why it matters for Y3 English:** I teach spelling from the front for the introduction and guided exploration, then children work in groups/pairs. The IWB is where I display the challenge problem, model the worked example, run the "I Notice / I Wonder" activity, and show the sorting categories. Without slides, I'm writing everything by hand on the board in real time, which eats into teaching time.

**What I'd want generated:**
- Slide 1: Challenge problem — "Add -ing to these words" (no answers)
- Slides 2-3: "I Notice / I Wonder" — display the correct spellings for pattern discovery
- Slides 4-6: Worked examples for prefix rules (animated: root word appears, prefix slides in, combined word appears)
- Slides 7-9: Worked examples for doubling rule (with clapping syllable visual)
- Slide 10: Sorting activity categories displayed
- Slide 11: Independent practice instructions
- Slides 12-13: Plenary matching pairs
- Slide 14: Exit ticket questions

**Graph data available:** The pedagogy sequence (challenge → guided exploration → worked example → practice → retrieval) gives the slide structure. The concept descriptions give the content. But the graph has no concept of visual presentation — no slide templates, no animation logic, no display formatting beyond Neo4j Bloom styling.

### 5. Marking Rubric / Assessment Grid (Priority: Medium-High)

**What it is:** A simple grid I use while circulating during independent practice and marking books afterwards. Shows what "working towards," "expected," and "greater depth" look like for THIS specific lesson's objectives.

**Why it matters for Y3 English:** I assess formatively every lesson and formally every half-term against the Y3 spelling expectations. Without a rubric specific to this lesson, I'm making holistic judgements that are hard to moderate with my year group partner. The rubric also feeds into my spelling tracker — which children have secured prefix rules? Which still need the doubling rule revisited?

**What I'd want generated:**
- 3 columns: Working Towards / Expected / Greater Depth
- 2 rows: Prefix Rules / Suffix Doubling Rules
- Each cell: 2-3 "I can..." descriptors + example of what correct work looks like + typical errors at this level
- A tick-list version I can use while circulating (child names down the side, criteria across the top)

**Graph data available:** The misconception data is ideal for the "typical errors" column. The teaching guidance describes what secure understanding looks like. But there are no formal assessment descriptors, no DifficultyLevel nodes for English, and no link to the KS2 test framework content domain codes that I'd use for summative assessment.

### Honourable Mentions (Not Top 5 but Would Use)

- **Dictation passages** — 3-4 sentences incorporating the lesson's target spellings, read aloud for children to write from memory. The graph has a concept for this (EN-Y3-C041: Writing from dictation) but no actual passages.
- **Homework sheet** — a lighter version of the core practice sheet, 6-8 questions, for parents to support. Must include parent-facing instructions ("Your child is learning to add prefixes to words. The key rule is...").
- **Spelling test template** — 10 words from today's lesson for the weekly spelling test (Friday in most schools). The statutory word list is in the graph but not formatted as a test.
- **Working wall display** — A3 versions of the key rules and examples for the classroom wall. Same content as the knowledge organiser but large-format.
- **Reading comprehension passage** — a short text (150-250 words, Lexile 200-300) that uses many of the lesson's target spellings in context, for a follow-up reading lesson linking spelling to comprehension.

### What This Means for the Platform

The graph currently gets me from "nothing" to "I know what to teach and what misconceptions to expect" — that's roughly 30% of lesson preparation. The remaining 70% is creating the artefacts above. If the platform could generate even the top 3 (word cards, differentiated worksheets, knowledge organiser), it would save me 45-60 minutes per new spelling topic. The knowledge organiser is the quickest win — the graph already has almost all the data needed.

The artefact generation order should mirror difficulty:
1. **Knowledge organiser** — text-only, data mostly exists in graph (EASY)
2. **Word cards / word mats** — text-only, needs curated word lists per concept (MEDIUM)
3. **Differentiated worksheets** — needs difficulty levels + word lists (MEDIUM)
4. **IWB slides** — needs presentation layer + visual design (HARD)
5. **Marking rubric** — needs assessment framework + difficulty levels (HARD)

## Bottom Line

The graph is an excellent CURRICULUM REFERENCE for Y3 English — I could use it to check coverage, verify progression, and understand misconceptions. But it is not yet a LESSON PLANNING TOOL for English. The subject is uniquely content-dependent: you need actual texts, actual words, actual sentences. The graph knows this (it describes "model texts" and "word sorting activities" in teaching guidance) but doesn't provide the content to make it happen.

Priority order for Y3 English:
1. Fix prerequisite links (quick win — data correction)
2. Add content vehicles for Y3 English (medium effort — mirrors Y4 pattern)
3. Add difficulty levels (medium effort — mirrors Y3 Maths pattern)
4. Add cross-domain CO_TEACHES for spelling ↔ grammar (quick win)
5. Add English-specific interaction types (design work needed)

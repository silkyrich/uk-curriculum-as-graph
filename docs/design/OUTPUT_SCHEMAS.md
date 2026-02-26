# Output Schema Specifications

**Three compilation targets from the same knowledge graph.**

Each schema defines what data is pulled from the graph, how it's structured, and what the output contract looks like. All three compile from the same underlying data; the difference is audience, tone, and constraint strictness.

---

## Schema A: Teacher Planner

**Audience:** Qualified teacher (QTS/PGCE) planning a lesson or sequence of lessons.
**Purpose:** "Here's everything you need to plan and deliver teaching on this topic."
**Generation method:** Procedural (deterministic query — no LLM needed).
**Input:** `(cluster_id)` or `(domain_id)` — teacher selects scope.

### Output contract

```
TEACHER_PLANNER
├── header
│   ├── subject                     # e.g. "Geography"
│   ├── year_group                  # e.g. "Y3-Y4" (from Key Stage)
│   ├── domain                      # e.g. "Human and Physical Geography"
│   ├── cluster_name                # e.g. "Understand climate zones, biomes and the water cycle"
│   ├── cluster_type                # introduction | practice
│   ├── estimated_lessons           # from cluster lesson_count or topic suggestion duration_lessons
│   ├── nc_reference                # statutory objectives (verbatim)
│   └── source_document             # DfE reference + URL
│
├── concepts[]                      # 1-4 concepts in this cluster
│   ├── concept_id
│   ├── concept_name
│   ├── concept_type                # knowledge | skill | procedure | understanding
│   ├── teaching_weight             # 1-6 (higher = more lesson time)
│   ├── description                 # what pupils learn (full prose)
│   ├── teaching_guidance           # how to teach it (full prose)
│   ├── key_vocabulary              # terms pupils must learn
│   ├── common_misconceptions       # what pupils get wrong (full prose)
│   ├── prerequisites[]             # what must be secure before teaching this
│   │   ├── concept_id
│   │   ├── concept_name
│   │   ├── relationship_type       # logical | developmental | procedural
│   │   └── rationale
│   ├── difficulty_levels[]         # ALL 4 levels — teacher uses for differentiation
│   │   ├── label                   # entry | developing | expected | greater_depth
│   │   ├── description             # what mastery looks like at this level
│   │   ├── example_task            # concrete assessment task
│   │   ├── example_response        # model answer
│   │   └── common_errors[]         # typical mistakes at this level
│   └── representation_stages[]     # CPA stages (primary maths only)
│       ├── stage                   # concrete | pictorial | abstract
│       ├── description
│       ├── resources[]             # physical manipulatives needed
│       ├── example_activity
│       └── transition_cue          # observable behaviour = ready for next stage
│
├── sequencing
│   ├── previous_cluster            # what came before (null if first)
│   ├── next_clusters[]             # what comes after
│   ├── co_teaches[]                # concepts that pair well within/across domains
│   │   ├── concept_id
│   │   ├── concept_name
│   │   └── reason
│   └── interleave_candidates[]     # previously-taught concepts suitable for retrieval practice
│
├── thinking_lens                   # primary lens for this cluster
│   ├── lens_name
│   ├── key_question                # e.g. "What are the parts of this system?"
│   ├── rationale                   # why this lens fits this cluster
│   ├── question_stems[]            # 4-5 age-appropriate question openers
│   └── alternative_lenses[]        # rank > 1 lenses, same structure
│
├── suggested_vehicle               # best-fit topic suggestion for this cluster
│   ├── study_name                  # e.g. "Climate Zones, Biomes and Vegetation Belts"
│   ├── study_type                  # place_study | thematic_study | enquiry | ...
│   ├── curriculum_status           # mandatory | optional | flexible
│   ├── enquiry_question            # central question
│   ├── duration_lessons
│   ├── success_criteria[]          # observable learning outcomes
│   ├── assessment_guidance
│   ├── common_pitfalls[]           # mistakes to avoid
│   ├── fieldwork_potential         # null if not applicable
│   ├── sensitive_content_notes     # null if not applicable
│   ├── subject_references[]        # GeoPlace, HistoricalSource, Genre, etc.
│   └── cross_curricular_links[]    # connections to other subjects
│       ├── target_name
│       ├── target_subject
│       ├── hook                    # the teaching connection
│       └── strength                # strong | moderate
│
├── vehicle_template                # pedagogical pattern for this study type
│   ├── template_name               # e.g. "Topic Study"
│   ├── session_structure[]         # ordered phases: hook → context → analysis → ...
│   ├── agent_prompt                # age-banded prompt for this KS
│   ├── question_stems[]            # age-appropriate openers
│   └── assessment_approach
│
├── epistemic_skills[]              # disciplinary skills to weave through
│   ├── skill_name
│   ├── skill_type                  # mapwork | enquiry | fieldwork | ...
│   └── description
│
└── notes
    ├── domain_curriculum_context   # what this domain covers and why it matters
    └── cluster_rationale           # why these concepts cluster together
```

### What is NOT included (available on request)

- Learner profile (teacher already knows their year group's capabilities)
- Interaction types (irrelevant for classroom teaching)
- Feedback profiles (teacher provides feedback, not a system)
- Full topic suggestion list (only the best-fit vehicle is shown; teacher can browse others)

### Rendering notes

- **Prose, not JSON.** Teachers read markdown, not data structures.
- **Professional shorthand.** Can use terms like "scaffold", "interleave", "productive failure" without explanation.
- **Differentiation is the headline.** Difficulty levels presented as a differentiation table: Entry/Support → Developing/Core → Expected → Greater Depth/Extension.
- **Vocabulary as a printable word mat.** Key vocabulary formatted for direct classroom use.
- **Success criteria as assessment checklist.** From topic suggestion success_criteria.

---

## Schema B: LLM Child Session Prompt

**Audience:** LLM that will interact directly with a child.
**Purpose:** "Teach this child this concept right now, obeying these rules exactly."
**Generation method:** Procedural (deterministic query assembles the prompt; LLM executes it).
**Input:** `(cluster_id, difficulty_target, topic_suggestion_id)` — adaptive engine has already decided what to teach, at what level, using which vehicle.

### Output contract

The prompt is structured as a **priority stack** — sections at the top take precedence over sections below. If any instruction conflicts, the higher section wins.

```
LLM_CHILD_SESSION_PROMPT
│
├── 1_HARD_CONSTRAINTS              # MUST obey. Non-negotiable.
│   ├── session_length_max_minutes   # e.g. 20
│   ├── activities_count             # e.g. 4
│   ├── max_sentence_length_words    # e.g. 14
│   ├── avg_sentence_length_words    # e.g. 9
│   ├── vocabulary_level             # e.g. "curriculum_vocabulary_supported"
│   ├── academic_vocabulary_ok       # e.g. false → "Avoid — use everyday language"
│   ├── number_range                 # e.g. "0–1000, simple fractions"
│   ├── tts_available                # e.g. true (offer if child requests)
│   ├── gamification_ban             # "No progress bars, badges, leaderboards, streaks, or expected rewards."
│   ├── comparative_feedback_ban     # "Never compare to other children or previous performance."
│   ├── avoid_phrases[]              # e.g. ["Wrong", "Incorrect", "Well done!", "Amazing!"]
│   ├── sensitive_content_notes      # from topic suggestion (null if none)
│   └── prerequisite_gate            # "Child has demonstrated [X]. Do not re-teach [X]."
│
├── 2_OUTPUT_SCHEMA                  # Exact structure the adaptive engine expects back.
│   ├── session_meta
│   │   ├── concept_ids[]            # concepts being taught
│   │   ├── difficulty_target        # e.g. "developing"
│   │   ├── lens_used                # e.g. "Systems and System Models"
│   │   ├── vehicle_template         # e.g. "topic_study"
│   │   └── time_minutes             # total session length
│   ├── activities[]                 # exactly N activities (from activities_count)
│   │   ├── activity_type            # from session_sequence: challenge | worked_example | practice | retrieval
│   │   ├── interaction_type         # MUST be from allowed_interactions list
│   │   ├── time_minutes             # per activity
│   │   ├── prompt_text              # what the child sees (obey sentence/vocab constraints)
│   │   ├── correct_response         # expected answer(s)
│   │   ├── misconception_traps[]    # which misconceptions this activity surfaces
│   │   │   ├── symptom              # what wrong answer looks like
│   │   │   └── counter_prompt       # what to say if child gives this answer
│   │   ├── hints[]                  # exactly hint_tiers_max hints
│   │   │   ├── tier                 # 1, 2, or 3
│   │   │   └── text                 # the hint (obey sentence/vocab constraints)
│   │   └── interleaved              # true if this retrieves a prior concept
│   ├── mastery_check
│   │   ├── items[]                  # 2-3 quick-fire items
│   │   │   ├── prompt_text
│   │   │   ├── correct_response
│   │   │   └── interaction_type
│   │   └── pass_threshold           # e.g. "2 of 3 correct"
│   └── feedback_templates
│       ├── correct_pattern          # e.g. "You spotted the pattern — [specific skill]."
│       └── incorrect_pattern        # e.g. "That one got you — [specific error]. Here's how: [correction]."
│
├── 3_PEDAGOGY_ALGORITHM             # Exact session flow. Follow this order.
│   ├── session_sequence[]           # e.g. ["challenge_problem", "guided_exploration", "worked_example", "independent_practice", "retrieval_practice"]
│   ├── productive_failure           # true/false + notes (e.g. "Let child attempt for 2-3 min before instruction")
│   ├── worked_example_style         # e.g. "Text + diagram narrated. Step-by-step with child input."
│   ├── interleaving_instruction     # e.g. "Mix with 2-3 previously mastered concepts in retrieval phase"
│   ├── spacing_note                 # e.g. "This concept last practised N days ago"
│   └── mastery_threshold            # e.g. "5 correct in 7 days (80%)"
│
├── 4_ALLOWED_INTERACTIONS[]         # Only these interaction types may appear in activities.
│   ├── interaction_id               # e.g. "drag_categorise"
│   ├── name                         # e.g. "Drag to Categorise"
│   ├── input_method                 # e.g. "touch_or_mouse"
│   └── when_to_use                  # from agent_prompt: "Used for classification tasks"
│
├── 5_CONCEPT_CONTENT                # What to teach. One block per concept in scope.
│   ├── concept_id
│   ├── concept_name
│   ├── description                  # COMPRESSED: child-accessible summary, not full prose
│   ├── key_vocabulary[]             # allowed terms (use these, not synonyms)
│   ├── difficulty_target            # the SINGLE level this child is working at
│   │   ├── label                    # e.g. "developing"
│   │   ├── description              # what success looks like
│   │   ├── example_task             # reference task at this level
│   │   └── common_errors[]          # errors to watch for at THIS level
│   ├── difficulty_stretch           # next level up (for children who fly through)
│   │   ├── label
│   │   ├── example_task
│   │   └── common_errors[]
│   ├── misconceptions[]             # top 3-6 most likely for this concept + level
│   │   ├── symptom                  # what the wrong answer looks like
│   │   ├── counter_prompt           # one-sentence correction
│   │   └── distractor_use           # "Use as MCQ option B" / "Use as drag-to-wrong-bucket"
│   └── representation_stage         # CPA stage if primary maths (null otherwise)
│       ├── stage                    # concrete | pictorial | abstract
│       ├── resources[]              # what the child interacts with
│       └── transition_cue           # when to advance
│
├── 6_LENS_REQUIREMENT               # Observable output the lens demands (not just framing).
│   ├── lens_name
│   ├── must_include                 # e.g. "a flow chart OR input/output list"
│   ├── question_stems[]             # e.g. "What goes in? What comes out?"
│   └── mapping_rationale            # why this lens fits (for context, not output)
│
├── 7_CONCEPT_SCOPE                  # Prevent scope creep.
│   ├── teach_these[]                # concept_ids for THIS session
│   ├── interleave_with[]            # concept_ids for retrieval practice only (do NOT re-teach)
│   └── do_not_teach[]               # concept_ids that are out of scope
│
├── 8_FEEDBACK_RULES                 # How to respond to child answers.
│   ├── ai_tone                      # e.g. "warm_competence_focused"
│   ├── feedback_style               # e.g. "specific_competence"
│   ├── agent_feedback_prompt        # full instruction block
│   ├── normalize_struggle           # e.g. true → "That one took longer — your brain was making new connections."
│   ├── post_error_approach          # e.g. "Explain the specific error and model the correct reasoning"
│   ├── counter_misconceptions       # e.g. false → correct gently, don't label as misconception
│   ├── example_correct              # concrete example
│   ├── example_incorrect            # concrete example
│   └── delight_frequency            # e.g. "semi_random" → occasional surprise moments
│
└── 9_AGENT_INSTRUCTIONS             # Aggregated from all agent_prompt fields.
    ├── content_instructions         # from ContentGuideline.agent_content_prompt
    ├── pedagogy_instructions        # from PedagogyProfile.agent_pedagogy_prompt
    └── vehicle_instructions         # from VehicleTemplate age-banded agent_prompt
```

### What is NOT included

- Full topic suggestion details (the engine already selected the vehicle; only the enquiry question and relevant content is injected)
- Cross-curricular links (out of scope for a single session)
- Epistemic skills list (woven into activities, not listed)
- Source documents (reference only, not pupil-facing)
- Cluster rationale (routing decision, not content)
- Alternative topic suggestions (engine already chose)

### Rendering notes

- **Sections 1-3 are the spine.** If the LLM gets nothing else right, obeying constraints + output schema + pedagogy algorithm produces a functional session.
- **Section 5 is the meat.** Concept content with misconceptions wired to activities is what makes the session educational rather than generic.
- **Section 4 is the rendering contract.** The LLM can only produce interaction types the UI can display. If `drag_categorise` isn't in the list, it can't appear in the output.
- **Total target: 3-5KB.** Enough for grounded generation, small enough to leave room for the LLM's output.

### Misconception compilation

Since misconceptions are currently prose (not structured), the procedural query must parse them. Two approaches:

**Immediate (no graph changes):** The query extracts `common_misconceptions` prose + `DifficultyLevel.common_errors[]` and injects them as-is under each concept. The LLM interprets them during generation. This works but relies on LLM quality.

**Target state (requires extraction):** Misconceptions become structured nodes with `symptom`, `counter_prompt`, `distractor_template` fields. The query injects them pre-structured. The LLM maps them to activities deterministically. This is more reliable but requires a data extraction pass across all 1,298 concepts.

**Hybrid (recommended first step):** Use `DifficultyLevel.common_errors[]` (already structured as arrays of specific error strings per level) as the primary misconception source for session generation. These are level-specific, concrete, and already in the graph. Supplement with the prose `common_misconceptions` field as background context.

---

## Schema C: Parent / Home Educator Guide

**Audience:** Non-specialist adult (parent, NVQ student, teaching assistant, homeschooling family).
**Purpose:** "Here's how to teach your child this topic today, step by step."
**Generation method:** LLM-generated from a structured prompt (the parent guide needs warm, plain-English prose that a procedural template can't produce well).
**Input:** `(cluster_id, difficulty_target)` — parent selects topic; system determines child's level.

### Generation prompt structure

The LLM that generates the parent guide receives a **compilation prompt** assembled procedurally from the graph. The compilation prompt is NOT the parent guide — it's the instructions for generating it.

```
PARENT_GUIDE_COMPILATION_PROMPT
│
├── 1_OUTPUT_RULES                   # What the generated guide must look like.
│   ├── tone                         # "Warm, encouraging, zero jargon. Write as if explaining to a friend."
│   ├── reading_level                # "The ADULT reader: assume GCSE-level English, no teaching training."
│   ├── format                       # "Numbered steps. Each step ≤ 3 sentences. Include what to SAY."
│   ├── length                       # "800-1200 words total."
│   └── must_include_sections[]      # see output contract below
│
├── 2_OUTPUT_CONTRACT                # Exact sections the guide must contain.
│   ├── what_were_learning           # 2-3 sentences: topic + why it matters
│   ├── what_youll_need              # bullet list: household items, printables, devices
│   ├── before_you_start             # what the child should already know (in plain English)
│   ├── the_lesson                   # step-by-step script with timings
│   │   ├── step_1_warm_up           # 2-3 min: activate prior knowledge
│   │   ├── step_2_new_learning      # 5-8 min: introduce concept
│   │   ├── step_3_practice          # 5-8 min: child tries with support
│   │   └── step_4_check             # 2-3 min: quick check + celebration
│   ├── if_they_find_it_easy         # stretch activity (next difficulty level)
│   ├── if_they_find_it_hard         # simpler version (previous difficulty level)
│   ├── common_mistakes              # dialogue scripts for misconceptions
│   │   ├── "If your child says X..."
│   │   └── "You could say: Y"
│   ├── how_youll_know_it_worked     # success criteria in parent language
│   └── whats_next                   # what this leads to (next cluster)
│
├── 3_CONCEPT_DATA                   # From graph — injected for LLM to compile.
│   ├── concept_name
│   ├── description                  # full prose (LLM simplifies for parent)
│   ├── teaching_guidance            # full prose (LLM converts to step-by-step)
│   ├── key_vocabulary[]             # terms the child should learn
│   ├── common_misconceptions        # full prose (LLM converts to dialogue scripts)
│   ├── difficulty_levels[]          # all 4 levels
│   │   ├── label + description + example_task + example_response + common_errors
│   │   └── (LLM uses target level for main lesson, level below for "if hard", level above for "if easy")
│   └── representation_stages[]     # CPA if primary maths
│       └── (LLM converts resources to household equivalents: "Dienes blocks → dried pasta")
│
├── 4_THINKING_LENS                  # Converted to parent-friendly questions.
│   ├── lens_name                    # (not shown to parent — used by LLM)
│   ├── key_question                 # LLM adapts for parent: "Ask your child: ..."
│   └── question_stems[]             # LLM selects 2-3 most concrete ones
│
├── 5_TOPIC_CONTEXT                  # From topic suggestion — gives the lesson a shape.
│   ├── enquiry_question             # LLM uses as lesson hook
│   ├── success_criteria[]           # LLM converts to "how you'll know it worked"
│   ├── common_pitfalls[]            # LLM converts to "avoid doing X" advice
│   ├── fieldwork_potential          # LLM converts to "you could try this at home/outside"
│   └── sensitive_content_notes      # LLM includes a parent note if relevant
│
├── 6_VEHICLE_TEMPLATE               # Session structure for the LLM to follow.
│   ├── template_name
│   ├── session_structure[]          # ordered phases → LLM maps to numbered steps
│   └── agent_prompt                 # age-banded (LLM adapts language for parent)
│
├── 7_SAFETY_CONSTRAINTS             # Non-negotiable rules for the generated guide.
│   ├── no_gamification              # "Do not suggest reward charts, sticker systems, or competitive games."
│   ├── no_comparison                # "Do not suggest comparing with siblings, classmates, or 'where they should be'."
│   ├── normalize_struggle           # "Include: 'It's completely normal if they find this hard at first.'"
│   ├── session_length_max           # "Keep total time under N minutes."
│   └── positive_error_framing       # "Mistakes are learning. Never say 'wrong'."
│
└── 8_CONTEXT_FOR_LLM                # Background the LLM needs but the parent doesn't see.
    ├── year_group                   # so LLM knows age-appropriate language
    ├── subject
    ├── prerequisites_met            # what we know the child already knows
    └── nc_reference                 # so LLM can ground claims in curriculum
```

### What the generated guide looks like (example structure)

```markdown
# Rivers and the Water Cycle
## Geography — Years 3-4

### What we're learning
Your child is going to learn how water moves around the Earth in a never-ending
cycle, and how rivers shape the land. By the end, they'll be able to explain
why it rains and what happens to that water as it flows downhill.

### What you'll need
- A clear glass or jar
- Cling film
- Warm water and ice cubes
- A baking tray or large plate
- Paper and coloured pencils

### Before you start
Your child should already know:
- The four seasons and basic weather patterns
- That water can be solid (ice), liquid (water), or gas (steam)

If they're not sure about these, spend 5 minutes chatting about them first.

### The lesson (about 20 minutes)

**Step 1: Start with a question (3 minutes)**
Ask: "Where does rain come from? And where does it go after it lands?"
Let them guess. There's no wrong answer here — you're finding out what they
already think. Write down or draw their ideas.

**Step 2: Make a mini water cycle (8 minutes)**
Pour warm water into the glass. Cover with cling film. Put ice cubes on top.
Watch what happens. Ask: "What can you see on the cling film? Where did that
come from?"

The warm water evaporates (turns to gas), rises, hits the cold cling film,
and condenses back into drops. That's the water cycle in a glass.

**Step 3: Draw and label (5 minutes)**
Together, draw a big water cycle: sea → evaporation → clouds → rain → river → sea.
Use these words: **evaporation**, **condensation**, **precipitation**.
Say each word together and talk about what it means.

**Step 4: Quick check (3 minutes)**
Ask these three questions:
1. "What makes water go up into the sky?" (heat — evaporation)
2. "What makes clouds turn into rain?" (cooling — condensation)
3. "Where does river water end up?" (the sea — and then the cycle starts again)

### If they find it easy
Ask: "What would happen if it stopped raining for a whole year? What would
happen to the rivers?" This pushes them to think about cause and effect.

### If they find it hard
Focus just on evaporation. Wet a plate, put it in the sun, check it in 30
minutes. "Where did the water go?" Keep it concrete and observable.

### Common mistakes (and what to say)
- **If your child says "clouds are made of steam":**
  Say: "Really good thinking — steam and clouds are similar! Clouds are actually
  made of tiny, tiny water droplets, so small they float in the air. Steam is
  water vapour you can't even see."

- **If your child thinks rivers flow uphill sometimes:**
  Say: "Water always flows downhill — it's gravity pulling it. Even when a river
  looks flat, it's actually going very slightly downhill. That's why rivers
  always end up at the sea, which is the lowest point."

### How you'll know it worked
Your child can:
- Name the three stages (evaporation, condensation, precipitation)
- Explain that the water cycle is a loop — it never stops
- Point to a river on a map and explain which way the water flows

### What's next
Next time, we'll look at how rivers change the shape of the land — carving
valleys, creating meanders, and building up beaches at the coast.
```

### Why LLM generation is necessary for this output

1. **Household resource substitution.** The graph says "Dienes blocks" — a parent needs "dried pasta for ones, penne tubes for tens." This requires contextual reasoning, not lookup.
2. **Dialogue scripts for misconceptions.** Converting "Pupils often think deserts are always hot" into "If your child says 'deserts are hot', you could say: 'That's a great thought...'" requires natural language generation.
3. **Tone calibration.** The guide must feel warm and achievable, not clinical. A template can't do this — it needs to vary sentence structure, use encouragement naturally, and adjust complexity to the topic.
4. **Adaptive branching.** The "if easy / if hard" sections require the LLM to genuinely understand the difficulty levels and produce different activities, not just label them.

### Quality controls

The procedural layer validates the LLM output before serving:
- **Word count:** 800-1200 words (reject if outside range)
- **Section completeness:** all required sections present
- **Vocabulary check:** key terms from graph appear in the guide
- **Banned phrase check:** none of the `avoid_phrases` appear
- **Session timing:** total time ≤ session_length_max_minutes
- **No gamification language:** no "reward", "star", "badge", "streak", "points"

---

## Comparison: What each schema pulls from the graph

| Graph data | Teacher Planner | LLM Session | Parent Guide |
|------------|:-:|:-:|:-:|
| Concept description | Full | Compressed | LLM simplifies |
| Teaching guidance | Full | Omitted (in agent instructions) | LLM converts to steps |
| Key vocabulary | Full list | Allowed terms only | LLM weaves into lesson |
| Common misconceptions (prose) | Full | Background context | LLM → dialogue scripts |
| DifficultyLevel (all 4) | All (differentiation table) | Target + stretch only | Target + easy/hard branches |
| DifficultyLevel.common_errors | All levels | Target level only | LLM → "common mistakes" |
| RepresentationStage (CPA) | Full with resources | Active stage only | LLM → household materials |
| Prerequisites | Listed with rationale | Gate check only | "Before you start" in plain English |
| CO_TEACHES | Listed | Interleave candidates | Omitted |
| ConceptCluster sequencing | Full chain | Scope control only | "What's next" sentence |
| ThinkingLens | Full with rationale | Observable requirement | LLM → parent questions |
| Topic Suggestion (all) | Best-fit only | Pre-selected | Pre-selected |
| Topic Suggestion details | Full properties | Enquiry question + pitfalls | LLM uses for lesson shape |
| Subject References | Full | Omitted | Omitted |
| Cross-curricular links | Listed | Omitted | Omitted |
| Vehicle Template | Full | Session structure only | LLM follows structure |
| Epistemic Skills | Listed | Omitted | Omitted |
| Source Document | DfE ref + URL | Omitted | Omitted |
| ContentGuideline | Omitted | Hard constraints | LLM uses for child language |
| PedagogyProfile | Omitted | Pedagogy algorithm | LLM uses for step timing |
| FeedbackProfile | Omitted | Feedback rules | Safety constraints only |
| InteractionTypes | Omitted | Allowed pick-list | Omitted |
| PedagogyTechniques | Omitted | Implementation rules | Omitted |
| Learner Profile (full) | Omitted | Sections 1, 3, 4, 8 | Sections 1, 7 |

---

## Token budget estimates

| Schema | Estimated size | Notes |
|--------|---------------|-------|
| **Teacher Planner** | 4-8 KB | Depends on concept count. All prose, no LLM overhead. |
| **LLM Session Prompt** | 3-5 KB | Compressed. Must leave room for LLM output (~3-4 KB). |
| **Parent Guide Compilation Prompt** | 4-6 KB | Input to LLM. Output is ~800-1200 words (~2-3 KB). |
| **Parent Guide (final)** | 2-3 KB | What the parent sees. Clean markdown. |

---

## Implementation order

| Step | What | Effort | Depends on |
|------|------|--------|------------|
| 1 | **Session-scoped graph query** | Medium | Nothing — new query function |
| | `get_session_context(cluster_id, difficulty_target, topic_suggestion_id)` returns only what's needed | | |
| 2 | **Teacher Planner renderer** | Low | Step 1 |
| | Procedural: query → markdown. No LLM. | | |
| 3 | **LLM Session Prompt assembler** | Medium | Step 1 |
| | Procedural: query → priority-stacked prompt. Includes output schema. | | |
| 4 | **Parent Guide compilation prompt assembler** | Medium | Step 1 |
| | Procedural: query → LLM prompt. LLM generates the guide. | | |
| 5 | **Parent Guide validator** | Low | Step 4 |
| | Post-generation checks: word count, sections, banned phrases, timing. | | |
| 6 | **Thinking lens → observable requirements** | Low | Nothing |
| | Rewrite 40 prompt strings in `thinking_lens_ks_prompts.json`. | | |
| 7 | **Structured misconceptions (optional, high-leverage)** | High | Nothing |
| | Extract from prose → structured nodes with symptom/counter/distractor fields. | | |

Step 1 is the foundation — all three schemas share the same underlying query. Build it once, render three ways.

---

## Open questions for review

1. **Should the Teacher Planner include the learner profile?** Currently excluded on the assumption that qualified teachers know their year group. But NQTs and supply teachers might benefit from it. Could be an optional "appendix" section.

2. **Should the Parent Guide offer multiple difficulty levels?** Currently it targets one level with "if easy/hard" branches. An alternative is to generate three variants (support/core/extension) and let the parent choose. But this triples generation cost and may overwhelm the parent.

3. **How should the LLM Session Prompt handle multi-concept clusters?** A cluster with 3 concepts can't be covered in one 15-minute session. The adaptive engine needs to decide: teach concept 1 today, concept 2 tomorrow? Or introduce all 3 lightly? This is a routing decision upstream of the prompt.

4. **Misconception compilation strategy.** The hybrid approach (use `DifficultyLevel.common_errors[]` as primary, prose as backup) works today without graph changes. Is that sufficient for v1, or is structured misconception extraction a prerequisite?

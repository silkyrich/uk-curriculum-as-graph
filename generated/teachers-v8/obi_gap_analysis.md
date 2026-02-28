# Gap Analysis: Mr. Obi — Geography (KS2)

**Planner:** Rivers and the Water Cycle
**Date:** February 2026 (V8 review)
**V7 score:** 4.0/10 -> **V8 score:** 6.5/10

---

## Top 5 Data Additions That Would Improve This Planner

### 1. Location and Case Study Data on GeoStudy Nodes (HIGH PRIORITY)

The "Locations" section of the planner lists "River Thames" with a blank description. This is the thinnest part of the planner and represents the biggest gap between what Geography requires and what the graph provides.

A rivers unit needs at minimum ONE detailed case study river with: physical geography data (length, source location, mouth location, major tributaries, key landforms along its course), human geography context (settlements along it, economic uses, flood history, management), and comparison opportunities (how does this river differ from the school's local river?).

**What I need on GeoStudy nodes:**

```
study.case_study_locations = [
  {
    name: 'River Thames',
    type: 'primary_case_study',
    coordinates: {source: '51.6944N, 2.0299W', mouth: '51.4505N, 0.7217E'},
    length_km: 346,
    key_features: ['source at Thames Head, Gloucestershire', 'meanders through Oxford', 'tidal from Teddington Lock', 'Thames Barrier flood defence'],
    settlements: ['Oxford', 'Reading', 'Windsor', 'London'],
    human_uses: ['drinking water supply', 'trade and transport', 'tourism', 'flood management'],
    flood_history: ['1953 North Sea flood', '2014 winter floods in Surrey'],
    comparison_prompts: ['Compare with your local river', 'Compare with the Nile — how are they similar and different?']
  }
]
```

The GeoPlace nodes exist in the per-subject ontology (255 reference nodes include GeoPlace). If the planner is not pulling GeoPlace data through, the generator needs to follow the LOCATED_IN relationship from the GeoStudy to its GeoPlace nodes and surface that data.

**Impact:** Would transform the "Locations" section from a blank field to a usable case study foundation. This single addition would close the most Geography-specific gap in the planner.

### 2. Thinking Lens Restoration (HIGH PRIORITY)

The V7 cluster context included "Systems and System Models" as the recommended thinking lens with structured question stems. The V8 planner has no thinking lens at all. This is a regression that affects the pedagogical depth of every activity in the planner.

For this rivers unit, the Systems lens is not just decorative — it fundamentally shapes how children think about the water cycle. Without it, the water cycle is a diagram to memorise. With it, children ask: "What are the inputs to this system? What are the outputs? What happens if precipitation increases?" These are the questions that move Geography from description to analysis.

**What I need:** The planner generator should query the APPLIES_LENS relationship from the relevant ConceptCluster (or from the GeoStudy node itself if study-level lens assignments exist) and include the lens name, key question, and age-banded question stems.

The data already exists in the graph: 10 ThinkingLens nodes, 1,222 APPLIES_LENS relationships, 40 PROMPT_FOR relationships with age-banded prompts. The planner generator is simply not querying it.

**Impact:** Would restore the analytical depth that made V7's lesson plan genuinely geographical rather than descriptive. No new data needed — just a generator fix.

### 3. Fieldwork Planning Scaffold (MEDIUM PRIORITY)

The planner's fieldwork potential description — "Local river or stream study measuring width, depth, and flow velocity at different points; observing erosion and deposition features; water quality testing" — is specific enough to know what to do, but not detailed enough to plan from.

**What I need on GeoStudy nodes:**

```
study.fieldwork = {
  type: 'data_collection',
  location_type: 'local_river_or_stream',
  equipment: ['metre rulers', 'measuring tape', 'stopwatch', 'orange peel (for float method)', 'clipboards', 'recording sheets', 'wellies', 'waders (optional)'],
  measurements: [
    {variable: 'width', method: 'Stretch tape across river at three sites', unit: 'metres'},
    {variable: 'depth', method: 'Use metre ruler at five points across width', unit: 'centimetres'},
    {variable: 'velocity', method: 'Float method: time orange peel over 10m, repeat x3', unit: 'seconds per 10m'}
  ],
  risk_assessment_notes: [
    'Adult supervision ratio 1:6 minimum near water',
    'Children must wear wellies, not school shoes',
    'Check river level on Environment Agency website before visit',
    'No child enters water above ankle depth',
    'Identify safe access and exit points before visit'
  ],
  data_recording_template: 'Table with columns: Site number, Width (m), Depth at 5 points (cm), Float time x3 (s), Average velocity',
  follow_up: 'Plot width, depth and velocity data on graphs. Do they change from upstream to downstream? Why?'
}
```

This is Geography-specific infrastructure that no other subject needs. Science has equipment lists on investigation nodes; Geography needs fieldwork scaffolds on GeoStudy nodes.

**Impact:** Would make fieldwork planning realistic rather than aspirational. Currently, the planner says "do fieldwork" without providing the practical detail that makes it happen safely.

### 4. Vocabulary Definitions with Geographical Precision (MEDIUM PRIORITY)

The 13-term word mat needs definitions that are both child-accessible AND geographically precise. This is harder than it sounds. "Erosion" is not just "wearing away" — it is "the wearing away and removal of rock and soil by water, wind, or ice." The "removal" part matters because without it, children conflate erosion with weathering (breaking down without removal).

**What I need:**

| Term | Child-friendly definition (max 18 words) | Geographical precision note |
|------|------------------------------------------|---------------------------|
| source | The place where a river starts, often a spring or the top of a hill | NOT "where it comes from" — specify spring/hilltop |
| meander | A large bend in a river, caused by erosion on the outside and deposition on the inside | Must include process, not just shape |
| erosion | When water, wind, or ice wears away and carries away rock and soil | Must include "carries away" to distinguish from weathering |
| deposition | When a river drops the material it has been carrying, often where it slows down | Must include "where it slows down" for causation |
| drainage basin | The area of land where all the rain flows into one river and its tributaries | A conceptual term — needs diagram support |
| flood plain | Flat land on either side of a river that floods when the river gets too high | Must connect to flooding, not just describe flatness |

Two terms from the concept description are missing from the word mat: **infiltration** and **run-off**. Both are essential water cycle vocabulary. Their absence is an oversight.

**Impact:** Would make the vocabulary section a usable classroom resource rather than a blank template.

### 5. Lesson Sequence Mapped to the 8-Lesson Duration (LOWER PRIORITY)

The planner estimates 8 lessons but does not sequence them. For a Geography teacher, the lesson order matters because concepts build on each other: the water cycle must come before river processes (you need to understand precipitation and run-off before erosion makes sense), and river processes must come before landforms (you need to understand erosion and deposition before meanders and floodplains make sense).

**What I need:**

| Lesson | Focus | Key concept | Activity type |
|--------|-------|-------------|---------------|
| 1 | What is the water cycle? | GE-KS2-C003 | Diagram, labelling, discussion |
| 2 | How does water get into rivers? | GE-KS2-C003 | Precipitation, run-off, infiltration |
| 3 | River systems: source to mouth | GE-KS2-C003 | Map work, tracing the Thames |
| 4 | How do rivers shape the land? (erosion) | GE-KS2-C003 | Photographs, diagrams, modelling |
| 5 | River landforms: meanders and floodplains | GE-KS2-C003 | OS map skills, cross-sections |
| 6 | How do people use and manage rivers? | GE-KS2-C003 | Case study, data analysis |
| 7 | Fieldwork: Our local river | GE-KS2-C005 | Data collection, observation |
| 8 | Assessment and review | All | Enquiry write-up, retrieval quiz |

This could be generated from the concept structure (water cycle -> river systems -> landforms -> human interaction -> fieldwork) and the differentiation levels (which imply a teaching sequence from Entry to Greater Depth).

**Impact:** Would turn the planner from a unit overview into a scheme of work.

---

## What the Auto-Generator Does Well

1. **Geography-specific study scope metadata.** Map types, data sources, fieldwork potential, scale, and themes are all new and represent the per-subject ontology working as designed. In V7, Geography had zero subject-specific metadata. Now I know I need "river basin map, OS map, cross section, satellite image" — I still have to find them, but I know what to find. This is the single biggest structural improvement.

2. **DifficultyLevel differentiation for all four concepts.** V7 had no differentiation data for Geography. Now, every concept has four levels with example tasks and common errors. The primary concept's differentiation is particularly strong — the progression from labelling a diagram (Entry) to evaluating human-river interaction (Greater Depth) is a genuine geographical progression, not just "do the same task with harder numbers" as some differentiation frameworks produce.

3. **Cross-curricular links are present and correct.** The Science-Geography water cycle link (states of matter as phase changes) was the single link I most wanted to see in V7. It is here, correctly identified as "Strong." The History link (settlement near rivers) and English link (river poetry) are both valid. Three links is better than V7's zero, even though the subject field is broken.

4. **Success criteria are assessable.** "Draw and label the water cycle with correct vocabulary," "Explain at least 2 river landforms" — these are statements I could write on the board, give as self-assessment criteria, or use as exit ticket prompts. They are specific (not "understand rivers") and measurable (not "appreciate the water cycle").

5. **Pitfalls show pedagogical understanding.** "Teaching the water cycle as a closed diagram without connecting it to real rivers" is the kind of insight that comes from watching rivers lessons go wrong. These are not generic warnings.

6. **Common misconceptions across all four concepts.** The misconception data was already strong in V7; it remains strong in V8. "Rivers flow uphill," "deserts are always hot," "reading northings before eastings" — these are real, specific, and actionable.

7. **Enquiry question frames the unit geographically.** "How does water shape the landscape?" is a genuine geographical enquiry question, not a knowledge recall question. It invites investigation rather than memorisation.

8. **Named data sources.** Environment Agency, Ordnance Survey, Met Office, Google Earth — these are the actual sources I use. Naming them saves me the "where do I find reliable KS2 data?" problem.

---

## What the Auto-Generator Gets Wrong

1. **Source document is wrong.** "KS2 English Grammar, Punctuation and Spelling Test Framework 2016" is not a Geography source document. This is a persistent generator error across all subjects.

2. **Location section is nearly empty.** "River Thames:" with nothing after it is worse than no section at all — it signals that the generator tried to populate this field and failed. Either populate it with case study data or remove it.

3. **Subject field in cross-curricular table is "None."** All three links correctly describe the connection but list "None" as the subject. "States of Matter and the Water Cycle" should say "Science." This is a data quality bug.

4. **Missing year group.** The header says "Key Stage: KS2" but not Y3, Y4, Y5, or Y6. The differentiation levels are KS2-wide, which works, but a teacher needs to know which year group this is planned for so they can pull the right learner profile and cross-reference with other subjects.

5. **Thinking lens absent.** The per-subject ontology planner does not include thinking lens data that the ConceptCluster context provided. The data exists in the graph — the generator does not query it.

6. **Secondary concepts may be over-inclusive.** Latitude/Longitude and Climate Zones are conceptually related to rivers but are substantial units in their own right. Including full differentiation tables for these within a Rivers planner makes the document feel like it is planning three units at once. The focus should be on the primary concept (River Systems and Water Cycle) with secondary concepts presented more briefly.

7. **No "Leads to" in sequencing.** The planner shows what unit precedes this one (Weather Patterns) but not what follows. For medium-term planning, I need both directions.

8. **Infiltration and run-off missing from word mat.** Both are named in the concept description as key vocabulary but do not appear on the word mat. The generator is not fully synchronising concept vocabulary with the word mat section.

---

## Comparison: Hand-Written vs Auto-Generated Planner

| Aspect | My current planning (from scratch) | V8 auto-generated planner |
|--------|-------------------------------------|---------------------------|
| Time to create | 4-5 hours for an 8-lesson unit | 0 minutes |
| Curriculum accuracy | Good (I check the NC) | Excellent — statutory reference is precise |
| Differentiation | Based on my class knowledge, often ad hoc | Structured four-level tables for all concepts — superior |
| Map resources | I source from Digimap, OS, Google Earth | Named but not provided |
| Data for enquiry | I build from Environment Agency, Met Office | Sources named but no data |
| Fieldwork plan | I write from scratch, including risk assessment | Described but not scaffolded |
| Vocabulary | 15-20 terms with definitions and diagrams on the working wall | 13 terms, no definitions |
| Case study | I research one river in depth (usually the Trent for local relevance) | "River Thames" with blank description |
| Lesson sequence | Full 8-lesson breakdown with activities and resources | 8-lesson estimate, no breakdown |
| Assessment | Rubric based on school assessment framework | 4 success criteria + differentiation tables |
| Cross-curricular | I plan with Science and History colleagues | 3 links (1 strong, 2 moderate) |
| Thinking lens | I did not use before V7 — now I do, and I got the idea from the graph | Missing from V8 planner |

**Summary:** The auto-generated planner gives me a stronger curriculum and differentiation foundation than my hand-written plans (especially the four-level differentiation tables — these are better than anything I create manually). But it gives me a weaker teaching plan (no lesson sequence, no maps, no data, no fieldwork scaffold, no case study detail). The planner saves me the first 90 minutes of a 5-hour planning process — the curriculum research and differentiation design. The remaining 3.5 hours — sourcing maps, building data packs, planning fieldwork, creating vocabulary displays, and writing the lesson sequence — still falls to me.

---

## Verdict

The V8 planner is a 2.5-point improvement over V7 for Geography, which is the largest score increase of any subject across the V7-V8 transition. This is because V7 Geography was the worst-served subject in the graph (zero content vehicles, zero differentiation, zero subject-specific metadata), and V8 addresses the most critical gaps: DifficultyLevel differentiation, Geography-specific study scope, enquiry questions, cross-curricular links, and success criteria.

The improvement is structural, not cosmetic. The per-subject ontology (GeoStudy) provides metadata — map types, data sources, fieldwork potential, scale, themes — that the generic ConceptCluster context could not. This vindicates the architectural decision to replace generic Topics and Content Vehicles with typed per-subject nodes. GeoStudy is not just a renamed TopicSuggestion; it carries Geography-specific properties that make the planner more useful.

What remains is the resource gap. Geography is the most resource-dependent subject in the primary curriculum. A rivers lesson without maps is not a Geography lesson. A water cycle lesson without data is not geographical enquiry. The planner now NAMES the resources I need (river basin map, OS map, Environment Agency data) without PROVIDING them. This is progress — in V7, the planner did not even acknowledge that resources were needed. But it means the planner is a planning tool, not a teaching tool. The distinction matters: I can plan FROM this planner, but I cannot teach FROM it without 3-4 hours of additional resource sourcing.

The path from 6.5 to 8.5:

1. **Populate location data** (+0.5) — case study detail for the River Thames and ideally a second contrasting river
2. **Restore thinking lens** (+0.5) — the data already exists, the generator just needs to query it
3. **Add vocabulary definitions** (+0.25) — geographically precise, child-accessible definitions for all terms
4. **Add lesson sequence** (+0.25) — map the 8 lessons to concepts, activity types, and resources
5. **Add fieldwork scaffold** (+0.5) — equipment, measurements, risk assessment, data recording template

These five additions require modest data work (location data is the heaviest lift; thinking lens requires zero new data). If all five were implemented, the planner would move from "plan from this" to "nearly teach from this" — the remaining gap being the actual map files, photograph files, and data files that no graph database can provide.

**V7: 4.0/10 -> V8: 6.5/10.** A 2.5-point improvement driven by the per-subject ontology and DifficultyLevel data. The next 2 points require location data, thinking lens restoration, and fieldwork scaffolds.

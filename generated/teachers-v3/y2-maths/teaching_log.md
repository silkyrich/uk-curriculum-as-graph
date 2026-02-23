# Teaching Log -- Year 2 Mathematics (Number, Addition & Subtraction, Multiplication & Division)

**Teacher:** Mrs Henderson, Year 2 Class Teacher & Maths Lead
**School:** Two-form entry primary, West Midlands
**Date:** February 2026
**Planning scope:** MA-Y2-D001, MA-Y2-D002, MA-Y2-D003 (12 concepts, 7 clusters, ~30 lessons across autumn and spring terms)

---

## 1. Initial Observations on the Graph Data

### What I have

Twelve concepts across three domains, now grouped into seven curated clusters:

| Domain | Concepts | Clusters |
|--------|----------|----------|
| MA-Y2-D001 Number & Place Value | 5 (C001, C002, C003, C011, C021) | 3 |
| MA-Y2-D002 Addition & Subtraction | 4 (C004, C005, C006, C007) | 2 |
| MA-Y2-D003 Multiplication & Division | 3 (C008, C009, C010) | 2 |

Total curated clusters: 7. That is down from 10 in the previous version. Every cluster is now typed as either "introduction" or "practice" -- no assessment clusters at all.

### What has changed since I last looked

Two significant structural changes:

**1. Assessment clusters have been removed entirely.** The old data had a separate assessment cluster per domain (D001-CL004, D002-CL002, D003-CL002) that duplicated concept lists and added 15 lessons of standalone "assessment" blocks. Those are gone. I was quite vocal that they were the single biggest structural problem last time -- they inflated the total from about 25 usable lessons to 47 -- and removing them was absolutely the right call. The cluster system now describes teaching sequence, not assessment schedule, which is how it should be. Assessment is my professional judgement, not something a graph should dictate in multi-lesson blocks.

**2. Cross-domain CO_TEACHES relationships now exist with rationales.** This is the change I am most interested in. Last time, the clusters were strictly domain-bound and I had to infer every cross-domain connection myself. Now the context file includes a "Cross-Domain CO_TEACHES" section for each domain, with typed reasons (prerequisite_gap, feeds_into, parallel_concept, shared_context, extracted) and prose rationales. Several of these are attributed to "Henderson," which I assume means they have been curated from teacher input -- including, it appears, my own feedback from the last round. That is gratifying.

### First impressions

The data is leaner and more useful than the previous version. Seven clusters instead of ten. Clear rationales. Cross-domain links with reasoning I can actually use in planning. The concept descriptions, teaching guidance, and misconceptions sections remain excellent -- they were already the strongest part of the data and they have not been degraded.

My one immediate concern is that the cluster structure has become quite sparse. Three clusters for Number and Place Value, two each for the other domains. With only "introduction" and "practice" types, some clusters feel like they are doing too much work -- particularly MA-Y2-D002-CL001, which bundles number fact recall (C004) and two-digit calculation (C005) into a single introduction cluster marked KEYSTONE. That is a lot of ground to cover in one cluster. More on this below.

---

## 2. Domain-by-Domain Cluster Analysis

### D001: Number and Place Value (5 concepts, 3 clusters)

**MA-Y2-D001-CL001** -- Extend the counting sequence and recognise odd and even numbers
Type: introduction | Concepts: C001, C011

*Verdict: FOLLOW exactly.*

This groups counting in steps (C001) with odd and even numbers (C011). The rationale is that they share the same structural insight about the number system, which is exactly right: counting in 2s generates the even numbers, so odd/even is a natural extension. The within-domain CO_TEACHES link between C001 and C011 confirms the pairing.

I will allocate **4 lessons**: two on counting in steps (revising 2s and 5s, introducing 3s as genuinely new) and two on odd and even (concrete exploration, then the digit rule and pattern investigation). This is enough because counting in 2s and 5s is revision from Year 1 -- I need time on 3s specifically, but the rest is consolidation.

The cross-domain CO_TEACHES links from this cluster are strong:
- C001 to C008 (2, 5, 10 times tables) with reason "prerequisite_gap" -- this was a gap I flagged last time. Counting in steps is the direct precursor to times table recall. The graph has now captured this as a curated connection rather than a formal prerequisite, which is an acceptable compromise. I will use it: when I reach the multiplication unit, I will open by connecting back to this counting work explicitly.
- C011 to C008 with reason "feeds_into" and the rationale "Even numbers are multiples of 2" -- again, something I flagged. This is a genuine pedagogical connection I make every year. When teaching the 2 times table, I always ask: "What do you notice about all these answers? They are all even."
- C021 (patterns) to C008 with reason "shared_context" -- arrays as patterns. This is a more subtle connection that I would not have prioritised in planning, but it is not wrong. I will note it but it will not change my sequencing.

**MA-Y2-D001-CL002** -- Understand place value in two-digit numbers
Type: practice | Concepts: C002, C003 | Sequenced after: CL001

*Verdict: FOLLOW, but I question the "practice" label.*

C002 (place value of tens and ones) and C003 (comparing and ordering using symbols) are correctly paired. You cannot compare two-digit numbers until you understand tens and ones, and comparison work reinforces place value. The CO_TEACHES link confirms this.

However, calling this cluster "practice" is misleading. This is almost entirely new content for these children. Place value of two-digit numbers is not practising something they already know -- it is the foundational concept of KS1 mathematics. Comparing with the formal < > = symbols is also new. If "practice" means "the second cluster in the sequence, so it builds on earlier counting work," I can see the logic, but for a teacher reading this cold, "practice" implies consolidation of previously-taught material. I would label this "introduction" or "new_content."

I will allocate **4-5 lessons**: two on partitioning and representing two-digit numbers (Dienes, place value charts, numeral cards, flexible partitioning), two on comparing and ordering with symbols, and possibly one more on place value if the class needs it. Place value is the concept I least want to rush. The cross-domain CO_TEACHES from C002 to C004 (derived facts) and C002 to C005 (two-digit calculation) tell me that if place value is not secure, both addition domains will suffer. That dependency is real and the graph captures it clearly.

**MA-Y2-D001-CL003** -- Order and arrange numbers and objects in patterns and sequences
Type: practice | Concepts: C021 | Sequenced after: CL002

*Verdict: FOLLOW with repositioning.*

C021 (patterns and sequences) is correctly identified as a standalone strand. It sits slightly apart from the rest of the number domain -- it is more about early algebraic thinking than about place value or calculation. The rationale acknowledges this: "a distinct strand in the NC that crosses number and shape."

I will allocate **2 lessons**, but I will NOT teach them consecutively after the place value block. Patterns work is better woven into the year: one lesson early on (linked to counting sequences from CL001), and one later (linked to arrays and multiplication patterns from D003). The cross-domain CO_TEACHES from C021 to C008 (patterns to times tables, reason: shared_context) supports this repositioning -- if I teach patterns work entirely before multiplication, I miss the opportunity to connect them.

**Lesson count for D001: 10 lessons** (4 + 4-5 + 2, with overlap and one patterns lesson deferred to the multiplication unit)

### D002: Addition and Subtraction (4 concepts, 2 clusters)

**MA-Y2-D002-CL001** -- Recall and use addition and subtraction facts to 20 and 100 [KEYSTONE]
Type: introduction | Concepts: C004, C005

*Verdict: FOLLOW with expansion and internal restructuring.*

This is the most important cluster in the data and it is correctly marked as a keystone. C004 (recall of facts to 20, derived facts to 100) and C005 (adding and subtracting two-digit numbers) are rightly paired -- the rationale says they "mutually co-teach" and that this pairing "drives fluency across the rest of the domain." True.

But this is a very heavy cluster. C005 alone has teaching_weight 3, covers four distinct calculation types (TU + U, TU + T, TU + TU, and three one-digit numbers), and involves progression from concrete to pictorial to column recording. The curriculum demands work with and without bridging through ten, both addition and subtraction. Bundling all of that with number fact recall and derivation into a single cluster is asking one cluster to do too much.

I will allocate **9 lessons** internally structured as:
- Phase 1 (3 lessons): Number bonds recall, derived facts using place value (cross-domain link to C002)
- Phase 2 (5 lessons): Two-digit calculation -- one lesson per calculation type, plus one mixed practice
- Checkpoint (1 lesson): Short written assessment to replace the old standalone assessment cluster

This is a significant expansion from what the cluster implies but it reflects reality. C005 is where the attainment gap widens in Year 2. I cannot teach four calculation types in two or three lessons and expect mastery. The graph's teaching_weight of 3 for C005 is accurate in relative terms but the absolute lesson count needs to be higher.

The cross-domain CO_TEACHES links from this cluster are all useful:
- C005 to C002 (place value) -- reason: extracted. Confirmed. I explicitly teach derived facts through the lens of place value.
- C005 to C023 (asking and answering questions about data, Statistics domain) -- reason: extracted. This is interesting. I had not considered linking addition/subtraction to the statistics domain for Year 2 planning, but it makes sense: data-handling questions often require calculation. I will note this for when I teach statistics later in the year.
- C006 to C010 (commutativity of addition parallels commutativity of multiplication) -- reason: parallel_concept. This is the connection I explicitly requested last time. The rationale says "Teach as deliberate pair, referencing addition work when reaching multiplication." That is exactly what I do, and it is good to see it formalised.

**MA-Y2-D002-CL002** -- Understand properties and relationships of addition and subtraction
Type: practice | Concepts: C006, C007 | Sequenced after: CL001

*Verdict: FOLLOW with reduced lesson count.*

C006 (commutativity and associativity) and C007 (inverse relationship) are well paired. These are properties of operations that pupils demonstrate through their calculation work rather than learn in isolation. The within-domain CO_TEACHES web here is very dense -- C004, C006, and C007 all co-teach with each other through inverse_operations links.

The "practice" label is more appropriate here than for D001-CL002, because these concepts build on the calculation work in CL001. Pupils need to have done addition and subtraction before they can meaningfully explore whether the order matters.

I will allocate **4 lessons**: two on commutativity (including using reordering as a checking strategy), two on the inverse relationship (fact families and missing number problems). The missing number work in particular connects back to the inverse relationship -- if ? - 5 = 13, use the inverse: 13 + 5 = 18. This is consistently one of the hardest problem types in Year 2 and needs proper teaching time.

**Lesson count for D002: 13 lessons** (9 + 4, including one checkpoint)

### D003: Multiplication and Division (3 concepts, 2 clusters)

**MA-Y2-D003-CL001** -- Recall the 2, 5 and 10 times tables and write multiplication and division statements [KEYSTONE]
Type: introduction | Concepts: C008, C009

*Verdict: FOLLOW with internal structuring.*

Another correctly identified keystone. C008 (times table recall) has the highest teaching_weight in the data at 4, and it is rightly paired with C009 (writing formal statements). You learn the tables by writing the facts, and writing the facts consolidates the tables.

I will allocate **7 lessons** structured as:
- 2 lessons on the 2 times table (including related division facts and formal notation, linking back to counting in 2s from D001)
- 2 lessons on the 5 times table (connecting to clock face and 5p coins)
- 2 lessons on the 10 times table (connecting to place value, linking the three tables together)
- 1 consolidation lesson: mixed practice across all three tables, rapid recall games

The cross-domain CO_TEACHES links into this cluster are the most numerous and the most useful:
- C008 to C016 (telling time to five minutes) -- reason: extracted. This is a genuine classroom connection: the 5 times table and clock reading reinforce each other. I teach them in the same half-term deliberately.
- C001 to C008 (counting in steps to times tables) -- reason: prerequisite_gap. Already discussed. I will open the multiplication unit by connecting back to counting work.
- C011 to C008 (odd/even to 2 times table) -- reason: feeds_into. Already discussed. "What do you notice about all the answers in the 2 times table?"
- C021 to C008 (patterns to arrays) -- reason: shared_context. This is where I will teach my deferred patterns lesson -- using arrays as a context for pattern recognition.

**MA-Y2-D003-CL002** -- Understand commutativity of multiplication and non-commutativity of division
Type: practice | Concepts: C010 | Sequenced after: CL001

*Verdict: FOLLOW exactly.*

C010 is correctly placed after the tables work. You need to know the facts before you can reason about commutativity. As a standalone concept in a practice cluster, 3 lessons is appropriate: one on commutativity with arrays (physically rotating them), one on non-commutativity of division (with sharing contexts), and one on applying these properties including fact families and missing number problems.

The cross-domain CO_TEACHES from C006 to C010 (parallel_concept) is the link I will make most explicit: "Remember when we found out that addition is commutative but subtraction is not? The same pattern happens with multiplication and division."

**Lesson count for D003: 10 lessons** (7 + 3)

---

## 3. Cross-Domain Planning

### How I will use the cross-domain CO_TEACHES links

The new cross-domain connections are the single biggest improvement in this version of the data. Last time I had to infer every one of these connections myself. Now they are formalised with reasons and rationales, which means:

1. **I can plan deliberate bridging moments.** When lesson 21 opens the multiplication unit, I will start with: "Do you remember counting in 2s, 5s, and 10s? Today we are going to turn those counting patterns into something new." This is the C001-to-C008 link (prerequisite_gap) made concrete.

2. **I can make structural parallels explicit.** The C006-to-C010 link (parallel_concept) gives me a specific moment in my sequence where I deliberately echo earlier learning. Lesson 27 (commutativity of multiplication) will explicitly reference lesson 18 (commutativity of addition). Same structure, different operation. This is the kind of connection that deepens mathematical understanding.

3. **I can justify my sequencing choices.** The C002-to-C004 link (feeds_into) confirms that place value must be secure before derived facts. The C002-to-C005 link (extracted) confirms that place value must be secure before two-digit calculation. These are not surprises, but having them formalised in the data means I can show my headteacher or Ofsted inspector exactly why I sequence things this way.

### Do the rationales make sense?

Yes, mostly. The rationales are clear and match my classroom experience. Some specific comments:

- **"prerequisite_gap" for C001 to C008** -- the rationale says this was a "within-Year-2 prerequisite missing from the graph." This is correct. Counting in steps IS a prerequisite for table recall, not just a co-teaching connection. The graph still does not have it as a formal PREREQUISITE_OF relationship (only as a CO_TEACHES), which feels slightly wrong. If a child cannot count in 2s, they cannot learn the 2 times table. That is a dependency, not a co-teaching suggestion.

- **"feeds_into" for C002 to C004** -- the rationale says "Understanding tens and ones allows derivation of number facts: 3+7=10 leads to 30+70=100." Exactly right. This is one of the most important cross-domain bridges in Year 2 maths and it governs my lesson 10 (derived facts).

- **"parallel_concept" for C006 to C010** -- well-stated. This is not a dependency but a structural echo. I would not change my sequencing based on this link, but I will change my teaching language to make the parallel visible.

- **"shared_context" for C021 to C008** -- the weakest of the connections, but not wrong. Arrays are patterns, and recognising patterns supports array work. I will use it lightly.

- **"extracted" for C005 to C023 (statistics)** -- useful but outside my current planning scope. I will return to this when I plan the statistics unit.

### Connections still missing

Three gaps remain:

1. **C007 (inverse of +/-) to C008/C009 (times tables and division).** The inverse relationship between multiplication and division is structurally parallel to the inverse relationship between addition and subtraction. I teach these as a deliberate pair: "Remember fact families for addition? Multiplication has them too." The graph has C006-to-C010 (commutativity parallel) but not C007-to-C008/C009 (inverse parallel). This should be a cross-domain CO_TEACHES with reason "parallel_concept."

2. **C005 (two-digit +/-) to C008 (times tables) via problem-solving.** Two-step word problems often combine addition and multiplication: "I buy 3 packs of 5 pencils at 20p each. How much change from 50p?" The graph does not represent this kind of application-level connection, and I am not sure it should -- it might be too fine-grained -- but it is a real planning consideration.

3. **No link to the Fractions domain.** The curriculum explicitly connects multiplication to fractions: "They begin to relate these to fractions and measures (for example, 40 / 2 = 20, 20 is a half of 40)." The context file covers only D001-D003, so fractions links are invisible. If I were planning the full year, I would need to see the C008-to-fractions connections.

---

## 4. Overall Assessment

### Rating: 7.5 out of 10

This is a significant improvement from the previous version, which I would have rated about 5.5. The removal of assessment clusters and addition of cross-domain CO_TEACHES links address the two biggest problems I identified last time. The data is now genuinely useful as a planning starting point rather than just a reference document.

### Top 3 remaining gaps

1. **Cluster granularity for heavy concepts.** MA-Y2-D002-CL001 bundles two concepts (C004 and C005) that together require 8-9 lessons. The cluster does not acknowledge the internal phasing needed: fact recall first, then calculation strategies, with different concrete resources for each. A sub-cluster or phasing mechanism -- even just a note saying "teach C004 before C005 within this cluster" -- would help. The prerequisite chain says C004 feeds C005, but the cluster presents them as a co-taught pair, which is not quite how I would teach them.

2. **The "practice" label is misleading.** MA-Y2-D001-CL002 is labelled "practice" but contains place value (C002) and comparison symbols (C003), which are substantial new content. If the types only allow "introduction" and "practice," then "practice" needs a definition -- perhaps "builds on prior cluster" rather than "consolidation of previously-taught material." Better yet, add a third type: "extension" or "development" for clusters that introduce new content that depends on earlier clusters.

3. **No suggested lesson counts or time allocation.** The old assessment clusters at least implied a lesson count (even if it was wrong). The current clusters have no lesson count at all. For a teacher picking this up for the first time, there is no signal about how long each cluster should take. I can work this out from the teaching_weight values and my experience, but a newer teacher might not. A simple "estimated_lessons: 3-5" field per cluster would help significantly.

### Specific recommendations for improvement

1. **Add estimated_lessons to each cluster.** Use teaching_weight sums as a starting point: a cluster with total teaching_weight of 6 might suggest 4-6 lessons. This is guidance, not prescription.

2. **Reclassify or define "practice."** Either add a third cluster type ("development" for new content that builds on earlier clusters) or add a description field that clarifies what "practice" means for each specific cluster. MA-Y2-D001-CL002 being "practice" while containing the foundational concept of KS1 maths is confusing.

3. **Promote the strongest CO_TEACHES links to formal prerequisite_gap connections.** The C001-to-C008 link (counting in steps to times tables) is not really a co-teaching suggestion -- it is a dependency. If a child cannot count in 2s, they cannot learn the 2 times table. The "prerequisite_gap" reason type is correct but it sits alongside weaker "shared_context" connections with no distinction in status.

4. **Add the C007-to-C008 inverse parallel.** The graph captures the commutativity parallel (C006-C010) but misses the inverse parallel (C007-C008). Both are structurally important and both should be flagged for teachers.

5. **Consider a "thread" tag for woven concepts.** C021 (patterns) and C004 (fact recall) are not best taught in a single block -- they are practised repeatedly throughout the year. A "thread" tag would signal to teachers that these concepts should be woven across the teaching sequence rather than confined to one cluster's timeslot.

### What I will actually use in my planning

- The **concept descriptions, teaching guidance, and misconceptions** -- these are excellent and I will reference them when writing my medium-term plan and preparing resources.
- The **cross-domain CO_TEACHES with rationales** -- these will shape my bridging moments and my sequencing of lessons across domains. The C001-C008, C011-C008, and C006-C010 links in particular will appear explicitly in my planning.
- The **prerequisite chains** -- these confirm my sequencing. Place value before calculation. Facts before strategies. Counting before tables.
- The **cluster groupings** as starting points -- I will follow 5 of the 7 clusters as-is (CL001 and CL003 from D001, CL002 from D002, CL001 and CL002 from D003). I will expand D002-CL001 internally and reposition D001-CL003.
- The **teaching_weight values** -- these confirm my time allocation instincts. C008 at weight 4 gets the most lessons. C005 at weight 3 gets the most within addition/subtraction. The lower-weight concepts (C001, C003, C021 at weight 2) get fewer dedicated lessons.

### What I will not use

- The **"Inspired by" Common Core references** -- still not useful for UK planning. CC Math 3.OA.C.7 references Year 3 fluency expectations, which is confusing when planning Year 2. I understand these exist for curriculum comparison purposes but they add noise for classroom teachers.
- The **cluster types as-is** -- the "practice" label does not match my understanding of the word. I will use my own phasing (new content, consolidation, application, checkpoint) within and across clusters.

### Final reflection

This data is now at the point where I would recommend it to a colleague as a planning aid, with caveats. The concept-level detail is genuinely excellent -- better than most published schemes of work for the teaching guidance and misconceptions. The cluster structure is a reasonable skeleton. The cross-domain links are the breakthrough feature in this version: they make connections visible that are often implicit in experienced teachers' planning but invisible to newer teachers.

For this to become a tool I would use instead of (rather than alongside) my existing medium-term plan, it needs lesson count estimates, clearer cluster type definitions, and a way to represent threaded concepts that run across the teaching sequence. But as a professional reference for understanding curriculum structure and planning domain connections, it is already useful. I will be using the cross-domain CO_TEACHES rationales directly in my autumn term planning meeting with my NQT colleague next door.

---

*Mrs Henderson, Year 2, February 2026*

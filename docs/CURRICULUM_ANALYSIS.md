# UK Curriculum Knowledge Graph - Analysis Report

**Generated:** 2026-02-16
**Database:** Neo4j @ localhost:7687
**Coverage:** KS1-3 (Ages 5-14, Years 1-9)

---

## Executive Summary

This analysis reveals the structure and interconnections within the UK National Curriculum knowledge graph containing **1,395 concepts** across **22 subjects** with **1,355 prerequisite relationships**.

### Key Findings

1. **Most Foundational Concepts**: Number recognition, counting, and past/present distinction are the building blocks
2. **Deepest Learning Chains**: Fractions concepts require up to 10 prerequisite steps
3. **Dominant Concept Types**: Knowledge (44%) and Skills (38%) make up 82% of concepts
4. **Complexity Distribution**: Most concepts (80%) are complexity levels 2-3 (developing/expected)
5. **Cross-Key-Stage Links**: 15+ explicit prerequisite connections from KS1/2 to KS3

---

## 1. Most Foundational Concepts

**These concepts support the most other concepts (critical building blocks):**

### Top 15 Foundation Concepts

| Rank | Concept | Subject | Dependents | Why It Matters |
|------|---------|---------|------------|----------------|
| 1 | Number recognition to 100 | Maths Y1 | 8 | Underpins all arithmetic |
| 2 | Counting forwards | Maths Y1 | 8 | Core numerical fluency |
| 3 | Past and Present | History KS1 | 8 | Foundation for chronological understanding |
| 4 | Extended vocabulary range | Languages KS3 | 7 | Enables all language production |
| 5 | Inter-relationship of Musical Dimensions | Music KS3 | 7 | Connects all music concepts |
| 6 | Coordination | PE KS1 | 6 | Required for all physical skills |
| 7 | Present tense structures | Languages KS3 | 6 | Grammar foundation |
| 8 | Concrete objects for calculation | Maths Y1 | 6 | Conceptual understanding before abstract |
| 9 | Locating places | Geography KS1 | 6 | Spatial awareness foundation |
| 10 | Close Observation | Science KS1 | 6 | Scientific enquiry basis |
| 11 | Binary Number System | Computing KS3 | 6 | Digital literacy foundation |
| 12 | Textual Programming Languages | Computing KS3 | 6 | Computing capability |
| 13 | Wide Listening Repertoire | Music KS3 | 5 | Musical appreciation |
| 14 | Democratic Government | Citizenship KS3 | 5 | Political understanding |
| 15 | Counting data categories | Maths Y2 | 5 | Statistical thinking |

**Insight for EdTech:** These are your **diagnostic priority concepts**. If a student struggles with advanced topics, test these foundational concepts first. Mastering these unlocks large parts of the curriculum.

---

## 2. Deepest Concepts (Longest Learning Chains)

**These concepts require the longest prerequisite chains to reach:**

### Top 15 Deepest Concepts

| Rank | Concept | Subject | Chain Depth | Implication |
|------|---------|---------|-------------|-------------|
| 1-6 | Counting in fractions | Maths Y2 | 8-10 steps | Complex multi-step learning journey |
| 7 | Emerging Privacy Protection | Computing KS4 | 9 steps | Builds on extensive prior digital literacy |
| 8 | Advanced Concern Reporting | Computing KS4 | 9 steps | Requires maturity + technical understanding |
| 9 | Jacobite rebellions | History KS3 | 9 steps | Deep historical context needed |
| 10 | Creative Computing Solutions | Computing KS4 | 9 steps | Culmination of computational thinking |
| 11-15 | Three quarters (3/4), Non-unit fractions, Fractions of quantities | Maths Y2 | 8-9 steps | Fraction concepts are hierarchical |

**Insight for EdTech:** These are **advanced concepts** that require mastery of long prerequisite chains. If students fail these:
- Don't just re-teach the concept
- Trace the 8-10 prerequisite chain backward
- Identify the actual gap (might be 6-7 steps back)
- Targeted remediation at the real breakdown point

**Fractions are challenging** because they require:
1. Number recognition → 2. Counting → 3. Place value → 4. Equal parts → 5. Unit fractions → 6. Non-unit fractions → 7. Fractions of quantities → 8. Counting in fractions

---

## 3. Cross-Cutting Concepts

**Concepts that appear across multiple domains/subjects:**

### Key Cross-Cutting Concepts (Selected)

| Concept | Type | Appears In | Educational Value |
|---------|------|------------|-------------------|
| Abstraction | Process | Computing, Maths, Science | Fundamental thinking skill |
| Accuracy and precision | Skill | Science, Maths, Music | Cross-disciplinary standard |
| Analysing trends | Skill | History, Geography, Science, Maths | Data interpretation |
| Asking perceptive questions | Skill | History, Science, English | Critical thinking |
| Appropriate Technology Use | Skill | Computing, D&T | Digital competence |
| Performance analysis | Process | PE, Music, D&T | Self-improvement cycle |
| Active Lifestyle Promotion | Attitude | PE (cross-cutting) | Health and wellbeing |
| Computational Thinking | Process | Computing, Maths | Problem-solving approach |

**Total identified:** 20+ cross-cutting concepts

**Insight for EdTech:** These concepts can be **reinforced across subjects**:
- Student masters "Analysing trends" in Maths → Highlight when it appears in Geography
- AI tutor: "You already know how to analyze trends from Maths. Let's apply it to population data!"
- Cross-subject reinforcement = deeper understanding + transfer of learning

---

## 4. Concept Type Distribution

**How concepts break down by type:**

```
Knowledge    : 616 concepts (44%) - Facts to remember
Skill        : 527 concepts (38%) - Abilities to perform
Process      : 138 concepts (10%) - Procedures to follow
Content      :  65 concepts ( 5%) - Specific study areas
Attitude     :  49 concepts ( 4%) - Dispositions to develop
```

**Insight for EdTech:**

- **Knowledge concepts** (44%): Best for flashcards, recall practice, spaced repetition
  - Example: "Plants need water to grow", "Capital of France is Paris"

- **Skill concepts** (38%): Need practice problems, exercises, demonstrations
  - Example: "Add two-digit numbers", "Play scales on instrument"

- **Process concepts** (10%): Need step-by-step guidance, procedural practice
  - Example: "Scientific enquiry method", "Iterative design process"

- **Attitude concepts** (4%): Hard to test directly, measured through engagement
  - Example: "Curiosity", "Resilience", "Musical confidence"

**Implication:** Your AI tutor needs **different pedagogical strategies** for different concept types. One-size-fits-all won't work.

---

## 5. Complexity Level Distribution

**How concepts are rated for difficulty (1=basic, 5=advanced for key stage):**

```
Level 1:  109 concepts ( 8%) █████
Level 2:  552 concepts (40%) ███████████████████████████
Level 3:  502 concepts (36%) █████████████████████████
Level 4:  206 concepts (15%) ██████████
Level 5:   26 concepts ( 2%) █
```

**Insight for EdTech:**

- **Levels 2-3** (76% of concepts): The "main body" of the curriculum
- **Level 1** (8%): Foundational concepts - master these first
- **Levels 4-5** (17%): Advanced/stretch concepts - for high achievers

**Adaptive learning strategy:**
1. Start students at their assessed level
2. Only advance when 80%+ mastery at current level
3. Offer Level 4-5 as "challenge mode" for confident students
4. Never skip Level 1 concepts - they're critical foundations

---

## 6. Subject Coverage Analysis

**Concepts and objectives per subject:**

### Largest Subjects (by objectives)

| Subject | Domains | Objectives | Notes |
|---------|---------|------------|-------|
| **Science KS3** | 16 | 156 | Largest single subject |
| **English KS1** | 7 | 116 | Phonics, spelling, grammar detail |
| **Mathematics KS3** | 9 | 83 | Comprehensive secondary maths |
| **Mathematics KS1-2** | 15 | 65 | Year 1 + Year 2 combined |
| **Science KS1** | 6 | 29 | Foundation science |

### Smallest Subjects (by objectives)

| Subject | Domains | Objectives | Notes |
|---------|---------|------------|-------|
| **Art & Design KS1** | 4 | 4 | High teacher autonomy |
| **Music KS1** | 5 | 4 | Practical, less prescriptive |
| **Music KS3** | 7 | 6 | Continues to be flexible |

**Insight for EdTech:**

- **Core subjects** (Maths, English, Science) have the most detailed specifications → easiest to build comprehensive content
- **Arts subjects** (Art, Music) have fewer explicit objectives → more room for creativity, but harder to assess objectively
- **KS3 Science** is the most complex single subject (156 objectives across 16 domains) → significant market opportunity if you can make it accessible

---

## 7. Cross-Key-Stage Prerequisite Links

**Concepts from earlier key stages that directly lead to later ones:**

### Sample Cross-KS Links (KS1 → KS2)

| From (KS1/Y1) | To (KS2/Y2) | Strength | Subject |
|---------------|-------------|----------|---------|
| Counting forwards | Counting in steps of 2 | 0.90 | Maths |
| Number recognition to 100 | Place value (ones) | 0.90 | Maths |
| Number line representation | Number bonds to 20 | 0.90 | Maths |
| Counting backwards | Place value (tens) | 0.90 | Maths |
| Concrete objects for calculation | Standard units (length) | 0.90 | Maths |
| Quarter as fraction | Time to five minutes | 0.90 | Maths |

**Identified explicit links:**
- Computing KS1-2 → KS3-4: 10 links
- Mathematics KS2 → KS3: 20 links
- Languages KS2 → KS3: 14 links
- Science KS1 → KS3: 4 links
- English KS1-2 → KS3: 15 links

**Total: 53+ explicit cross-key-stage prerequisites**

**Insight for EdTech:**

These are the **progression pathways** from primary to secondary:
- A Year 6 student struggling with KS3 Maths? Check their Year 2 foundations (20 explicit links)
- Languages teacher starting KS3? Know exactly which KS2 concepts students should have (14 links)
- Your AI tutor can **trace back across years** to find the real gap

**Example learning journey:**
```
Year 1: Counting forwards
   ↓
Year 2: Counting in steps of 2
   ↓
Year 2: Understanding multiples
   ↓
Year 3: Times tables
   ↓
KS3: Prime factorization
```

---

## 8. Pedagogical Insights for AI Tutoring

### A. Diagnostic Assessment Strategy

**Based on prerequisite depth:**

1. **Quick Screener** (5-10 min):
   - Test the 15 most foundational concepts (from Section 1)
   - If student fails any → deep dive on that concept's prerequisites

2. **Subject Deep-Dive** (15-20 min):
   - Test concepts at student's supposed year level
   - For each failure → test its immediate prerequisites
   - Continue until you find what they DO know

3. **Adaptive Difficulty**:
   - Student passes Level 2 concepts → try Level 3
   - Student fails Level 3 → more Level 2 practice
   - Never jump levels without mastery

### B. Intelligent Remediation

**When student fails a concept:**

```python
def remediate(failed_concept):
    prerequisites = get_prerequisites(failed_concept)

    for prereq in prerequisites:
        if not student_has_mastered(prereq):
            # Found the gap!
            return create_practice_session(prereq)

    # All prerequisites mastered, student just needs practice
    return create_practice_session(failed_concept, difficulty="easier")
```

**Example:**
- Student fails: "Multiplying fractions" (KS3)
- Trace prerequisites:
  - ✓ "Understanding fractions" (mastered)
  - ✗ "Multiplying whole numbers fluently" (NOT mastered)
- **Remediation:** Practice multiplication fluency, THEN return to fractions

### C. Content Generation Guidelines

**By concept type:**

| Concept Type | Best Content Format | AI Prompting Strategy |
|--------------|---------------------|----------------------|
| **Knowledge** | Multiple choice, flashcards, fill-in-blank | "Generate 10 quiz questions testing recall of [concept]" |
| **Skill** | Practice problems, worked examples | "Create 5 progressive exercises for [skill] from easy to challenging" |
| **Process** | Step-by-step guides, checklists | "Break down [process] into numbered steps with examples" |
| **Attitude** | Reflection prompts, scenarios | "Create a scenario where [attitude] would be helpful" |

**Complexity calibration:**
- Level 1-2: Short problems, concrete examples, scaffolded hints
- Level 3: Standard exam-style questions
- Level 4-5: Multi-step problems, open-ended challenges

### D. Progress Visualization

**Student dashboard could show:**

```
Curriculum Map for [Student Name]
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Mathematics Year 2:
  ████████░░ 80% Complete

  ✓ Number & Place Value (100%)
  ✓ Addition & Subtraction (95%)
  ⧗ Multiplication & Division (60%) ← Current focus
  ░ Fractions (0%) ← Blocked by Multiplication

Next up: Master "Times tables 2, 5, 10" to unlock Fractions!

Learning Path:
Year 1: Counting → Grouping → Repeated Addition
Year 2: Times Tables ← YOU ARE HERE
Year 2: Fractions ← NEXT (blocked)
```

---

## 9. Business Insights

### Market Opportunities

**Based on curriculum structure:**

1. **Maths KS1-2** (169 concepts, clear progressions)
   - Largest single subject at primary
   - Very structured (9/10, 8/10 ratings)
   - Clear prerequisite chains → ideal for adaptive learning
   - **Recommendation:** Strong MVP candidate

2. **Science KS3** (171 concepts, 156 objectives)
   - Largest secondary subject
   - Well-structured (8/10 rating)
   - Current offerings (IXL, etc.) struggle with practical science
   - **Recommendation:** High value if you can handle practicals

3. **English KS1** (77 concepts, 116 objectives)
   - Phonics-heavy (systematic synthetic phonics)
   - Government-mandated Phonics Screening Check (Year 1)
   - Parents highly motivated to support reading
   - **Recommendation:** High demand, competitive market

4. **Cross-Subject Skills** (20+ cross-cutting concepts)
   - Computational thinking, analyzing trends, critical questioning
   - No current product teaches these explicitly across subjects
   - **Recommendation:** Unique differentiator vs. IXL

### Competitive Differentiation

**What your graph enables that IXL can't do:**

| Feature | IXL | Your Potential |
|---------|-----|----------------|
| **Prerequisite-aware remediation** | ❌ Retry same level | ✅ Trace back to actual gap |
| **Cross-subject reinforcement** | ❌ Siloed subjects | ✅ "You learned this in Maths!" |
| **Exact concept targeting** | ❌ Broad topics | ✅ 1,395 specific concepts |
| **Learning path visualization** | ❌ Hidden structure | ✅ Show student their journey |
| **Curriculum compliance reporting** | ✅ Basic | ✅ Detailed (621 objectives tracked) |
| **AI content generation** | ❌ Hand-authored | ✅ Generate on-demand from graph |
| **Adaptive difficulty** | ✅ Basic | ✅ Graph-informed (5 complexity levels) |

### Pricing Implications

**Your graph enables value-based pricing:**

- **Diagnostic precision:** "Know exactly where your child's gaps are" (worth £££)
- **Time efficiency:** "Only practice what they actually need" (vs. wasting time on mastered concepts)
- **Cross-subject intelligence:** "Learning that transfers across subjects" (unique value)
- **Progress visibility:** "See exactly what they've mastered" (parent peace of mind)

**Suggested tiers:**
1. **Free**: Basic diagnostic (test foundational concepts only)
2. **Premium** (£9.99/month): Full adaptive learning, one subject
3. **Family** (£19.99/month): All subjects, cross-subject insights, progress reports
4. **Schools** (£199/year per class): Teacher dashboard, curriculum compliance, bulk access

---

## 10. Next Steps: Research Questions

**To validate and refine your graph:**

### A. Teacher Validation
- Are prerequisite relationships pedagogically sound?
- Are concepts at the right granularity for lesson planning?
- What's missing? What's wrong?

### B. Student Testing
- Pick 20 students across Year 1-9
- Diagnostic test using your graph
- Does it correctly identify gaps?
- Does remediation work?

### C. Content Viability
- Can AI generate quality practice questions for all 1,395 concepts?
- Which concept types are hardest for AI?
- What human curation is needed?

### D. Market Validation
- Will parents pay for this vs. free resources?
- Will schools adopt it?
- What's the customer acquisition cost?

---

## Appendix: Technical Queries

### Query 1: Find All Prerequisites for a Concept
```cypher
MATCH path = (prereq:Concept)-[:PREREQUISITE_OF*]->(target:Concept)
WHERE target.concept_id = 'MA-Y2-C050' // e.g., "Counting in fractions"
RETURN path
```

### Query 2: Student Mastery Gap Analysis
```cypher
// Given a student's mastered concepts, find what they should learn next
MATCH (mastered:Concept)
WHERE mastered.concept_id IN ['MA-Y1-C001', 'MA-Y1-C002', ...] // Student's mastery list

MATCH (next:Concept)
WHERE NOT next.concept_id IN ['MA-Y1-C001', 'MA-Y1-C002', ...] // Not yet mastered

MATCH (prereq:Concept)-[:PREREQUISITE_OF]->(next)
WHERE prereq.concept_id IN ['MA-Y1-C001', 'MA-Y1-C002', ...] // Prerequisites ARE mastered

// Only include concepts where ALL prerequisites are mastered
WITH next, collect(prereq) as prereqs
MATCH (all_prereqs:Concept)-[:PREREQUISITE_OF]->(next)
WITH next, prereqs, count(all_prereqs) as total_prereqs
WHERE size(prereqs) = total_prereqs

RETURN next.concept_name, next.concept_id, next.complexity_level
ORDER BY next.complexity_level
LIMIT 10
```

### Query 3: Curriculum Coverage Report
```cypher
// For a given student, what % of Year 2 Maths have they mastered?
MATCH (c:Concept)
WHERE c.concept_id STARTS WITH 'MA-Y2'
WITH count(c) as total_concepts

MATCH (mastered:Concept)
WHERE mastered.concept_id IN ['MA-Y2-C001', 'MA-Y2-C003', ...] // Student's mastery
WITH total_concepts, count(mastered) as mastered_concepts

RETURN mastered_concepts, total_concepts,
       toFloat(mastered_concepts) / total_concepts * 100 as percentage_complete
```

---

**Analysis Complete**
**Date:** 2026-02-16
**Next:** Build POC or validate with teachers?

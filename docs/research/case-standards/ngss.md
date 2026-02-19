# Next Generation Science Standards (NGSS)

**Framework ID:** `ngss-science-2013`
**Jurisdiction:** US-NGSS (national, published by Achieve Inc)
**Subject:** Science
**Published:** 2013
**Licence:** CC-BY
**CASE endpoint:** `https://casenetwork.imsglobal.org/ims/case/v1p0`

---

## Overview

NGSS is a set of K–12 science standards developed through a state-led process coordinated
by Achieve Inc, with input from the National Research Council, NSTA, and AAAS. It is based
on the NRC Framework for K–12 Science Education (2012).

As of 2024, approximately 20 states have fully adopted NGSS. A further ~10 use modified
versions. States that rejected NGSS include Texas, Virginia, South Carolina, Wyoming
(initially), and Oklahoma.

---

## The Three-Dimensional Learning Model

NGSS organises science learning around three interlocking dimensions:

### 1. Science and Engineering Practices (SEPs)

Eight practices that describe what scientists and engineers actually do:

| SEP | Title |
|---|---|
| SEP.1 | Asking Questions and Defining Problems |
| SEP.2 | Developing and Using Models |
| SEP.3 | Planning and Carrying Out Investigations |
| SEP.4 | Analysing and Interpreting Data |
| SEP.5 | Using Mathematics and Computational Thinking |
| SEP.6 | Constructing Explanations and Designing Solutions |
| SEP.7 | Engaging in Argument from Evidence |
| SEP.8 | Obtaining, Evaluating, and Communicating Information |

**UK comparison:** These map directly to the UK KS3 Working Scientifically programme of
study. The vocabulary differs (NGSS uses "Argument from Evidence"; UK uses "evaluate data
and methods") but the underlying skills are closely aligned. This is the primary alignment
target in `ngss_to_uk_science.json`.

### 2. Crosscutting Concepts (CCCs)

Seven concepts that apply across all science disciplines:
Patterns; Cause and Effect; Scale, Proportion, and Quantity; Systems and System Models;
Energy and Matter; Structure and Function; Stability and Change.

**UK comparison:** The UK curriculum does not have an explicit crosscutting concepts
framework, though similar ideas appear implicitly (e.g. "cause and effect" in biology,
"scale" in geography). This structural gap is interesting: the UK embeds these ideas
in subject content; NGSS makes them explicit.

### 3. Disciplinary Core Ideas (DCIs)

Content knowledge in four domains:
- Life Science (LS)
- Physical Science (PS)
- Earth and Space Science (ESS)
- Engineering, Technology, and Applications of Science (ETS)

**UK comparison:** Maps broadly to UK KS3 Biology, Chemistry, Physics domains.

---

## Controversial Content

NGSS includes explicit coverage of:
- **Evolution** — integrated throughout life science from grade 3 upwards
- **Human-caused climate change** — explicit in ESS3 (Earth and Human Activity)
- **Age of the universe and Earth** — explicit in ESS1

These are sources of political controversy in several states:

- **Oklahoma** rejected NGSS in 2014, with legislators citing concerns about evolution
  and climate content. Oklahoma created its own standards that include evolution but
  with weakened language.
- **South Carolina** rejected NGSS repeatedly due to climate change content.
- **Wyoming** initially removed climate change language from their adopted version (2016)
  before restoring it (2020).

In contrast, the **UK National Curriculum** mandates evolution (KS3, KS4) and
includes climate as part of KS3 Earth Science content. There is no political mechanism
for local removal of national curriculum content.

---

## Comparison Queries

```cypher
-- All NGSS items mentioning climate
MATCH (j:Jurisdiction {jurisdiction_id: 'US-NGSS'})-[:PUBLISHES]->(d:CFDocument)
      -[:CONTAINS_ITEM]->(i:CFItem)
WHERE i.full_statement CONTAINS 'climate'
RETURN i.human_coding_scheme, i.full_statement
ORDER BY i.human_coding_scheme

-- NGSS Science Practices aligned to UK curriculum
MATCH (i:CFItem)-[:ALIGNS_TO]->(target)
WHERE i.cf_doc_id STARTS WITH 'ngss'
  AND i.item_type = 'Science and Engineering Practice'
RETURN i.human_coding_scheme, i.abbreviated_statement, labels(target), target.concept_name

-- Grade band coverage comparison
MATCH (i:CFItem)<-[:CONTAINS_ITEM]-(d:CFDocument)<-[:PUBLISHES]-(j:Jurisdiction)
WHERE j.jurisdiction_id = 'US-NGSS'
RETURN i.education_level AS grade_band, count(i) AS items
ORDER BY size(i.education_level)
```

---

## Sources

- NGSS official site: https://www.nextgenscience.org/
- NRC Framework: https://www.nap.edu/catalog/13165
- Achieve Inc CASE package: via IMS CASE Network
- Adoption status: https://www.nextgenscience.org/lead-state-process

# Wyoming Science Standards

**Framework ID:** `wyoming-science-2016`
**Jurisdiction:** US-WY (Wyoming Department of Education)
**Subject:** Science
**Key revisions:** 2016 (initial adoption, climate removed), 2020 (climate restored)
**Licence:** Public domain (state government)
**CASE endpoint:** Wyoming DOE or IMS CASE Network (check availability at fetch time)

---

## Overview

Wyoming's science standards are among the most politically significant in the
US because they provide a clear, documented case study of a state government
removing specific scientific content from curriculum standards under political
pressure, and subsequently restoring it.

---

## The Climate Change Controversy

### 2016 adoption

The Wyoming Board of Education adopted science standards based on NGSS but with
a key modification: all references to human-caused climate change were removed.

The state legislature had previously (2014) passed a budget footnote blocking
adoption of any standards that "would teach or explore the causes and effects of
climate change" — an unprecedented legislative intervention into curriculum content.

The rationale given: protecting Wyoming's coal and natural gas industries, which
employ a significant portion of the state workforce and fund state education budgets
through severance taxes.

Affected content included:
- ESS3-5 (Ask questions to clarify evidence of the factors that have caused
  the rise in global temperatures over the past century)
- ESS3-C (Human Impacts on Earth Systems)
- Multiple middle school standards on the greenhouse effect and global warming

### 2020 revision

Under a new state superintendent, Wyoming's science standards were revised.
Climate change content was restored, largely matching NGSS language.
The 2016 episode had attracted significant national attention and criticism from
the scientific community, and the restoration was seen as a course correction.

---

## Why This Matters for the Curriculum Graph

Wyoming's standards history is a perfect case study for the graph's comparative
layer because:

1. **The same physical phenomenon exists** (climate change) in both UK and US
   standards — but political will to include it varies by jurisdiction
2. **The 2016 vs 2020 comparison** could eventually be represented as two
   Jurisdiction-versioned CFDocuments, showing the same content absent then present
3. **The contrast with the UK** is stark: no equivalent mechanism exists in England
   for local authorities to remove national curriculum content

---

## Wyoming Curriculum Context

Wyoming is a sparsely populated state (population ~580,000) with a
resource-extraction economy. Education funding is unusually dependent on mineral
severance taxes — meaning the coal and gas industries directly fund schools.
This creates a structural incentive for state politicians to avoid curriculum
content that might be seen as threatening those industries.

This economic-curriculum linkage is specific to Wyoming's context; other states
that rejected climate content (e.g. South Carolina) did so on different grounds
(philosophical opposition to federal standards, concerns about cost of implementation).

---

## Comparison Queries

```cypher
-- Wyoming items mentioning climate (should be present post-2020 restoration)
MATCH (j:Jurisdiction {jurisdiction_id: 'US-WY'})-[:PUBLISHES]->(d:CFDocument)
      -[:CONTAINS_ITEM]->(i:CFItem)
WHERE i.full_statement CONTAINS 'climate'
RETURN i.human_coding_scheme, i.full_statement

-- Compare Wyoming vs NGSS climate coverage
MATCH (j:Jurisdiction)-[:PUBLISHES]->(d:CFDocument)-[:CONTAINS_ITEM]->(i:CFItem)
WHERE j.jurisdiction_id IN ['US-WY', 'US-NGSS']
  AND i.full_statement CONTAINS 'climate'
RETURN j.name, count(i) AS climate_items
ORDER BY j.name
```

---

## Sources

- Wyoming Department of Education science standards:
  https://edu.wyoming.gov/educators/standards/science/
- 2014 Wyoming budget footnote blocking climate standards:
  Coverage in Science magazine, Nature News, NCSE
- NCSE Wyoming page: https://ncse.ngo/wyoming
- 2016 adoption controversy: https://www.scientificamerican.com/article/
  wyoming-becomes-first-state-to-reject-next-generation-science-standards/

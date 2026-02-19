# Texas Essential Knowledge and Skills — Science (TEKS)

**Framework ID:** `texas-teks-science`
**Jurisdiction:** US-TX (Texas Education Agency)
**Subject:** Science
**Most recent revision:** 2024 (phased implementation 2025–2026)
**Licence:** Public domain (state government)
**CASE endpoint:** Texas Education Agency (TEA) — `https://tea.texas.gov/ims/case/v1p0`

---

## Overview

Texas maintains its own curriculum standards (TEKS — Texas Essential Knowledge and
Skills) and did not adopt NGSS. The TEA publishes TEKS in CASE format, making
machine-readable comparison possible.

Texas is one of the largest textbook markets in the US, which means Texas TEKS
have historically influenced the content of nationally distributed textbooks.
This amplifies their significance beyond Texas itself.

---

## Science TEKS Structure

Unlike NGSS's three-dimensional model, TEKS uses a more traditional
content-domain structure:

**Grade K–8:** Earth and Space Science, Life Science, Physical Science, plus
"Scientific and Engineering Practices" (introduced in 2024 revision)

**High school courses:** Biology, Chemistry, Physics, Earth and Space Science,
Aquatic Science, Astronomy, Environmental Systems, etc.

**Texas Science and Engineering Practices (TSEP):**
The 2024 revision introduced explicit practices mirroring some NGSS SEPs,
but with Texas-specific framing and additional engineering focus aligned
to the Texas economy (energy, technology).

---

## The Evolution Question

Texas TEKS include evolution, but the history of how they do so is instructive:

**2009 revision (controversial):** The State Board of Education (SBOE) voted to
include language requiring students to "analyse and evaluate" the "strengths and
weaknesses" of evolutionary theory. Critics argued this was a backdoor mechanism
to introduce creationism; supporters framed it as scientific rigour.
The language was applied to evolution but not other theories (e.g. gravity, plate tectonics).

**2013 revision:** The SBOE attempted to adopt biology textbooks that included
creationist claims. After significant public pressure, the books were adopted with
corrections, but the episode illustrated ongoing tension.

**2024 revision:** The "strengths and weaknesses" language was removed. Evolution
is now covered in Biology TEKS with standard scientific framing, though some
board members continue to express reservations.

**UK comparison:** The UK National Curriculum mandates evolution at KS3 (Year 8/9)
with no equivalent political controversy at the national level. Evolution has been
a settled curriculum question in England since 2014, when it was added to KS2.

---

## The Climate Change Question

Texas TEKS do include climate change content in Earth and Space Science, but:
- The 2009 revision introduced language about "climate change" that was considered
  weaker than NGSS equivalent content
- The term "human-caused" or "anthropogenic" appeared inconsistently across revisions
- Texas's energy sector interests (oil, gas, coal) have historically influenced
  the framing of energy and climate content

**UK comparison:** UK KS3 science explicitly includes the greenhouse effect,
global warming, and climate change as mandatory content.

---

## Comparison Queries

```cypher
-- Compare evolution coverage: Texas vs NGSS
MATCH (j:Jurisdiction)-[:PUBLISHES]->(d:CFDocument)-[:CONTAINS_ITEM]->(i:CFItem)
WHERE j.jurisdiction_id IN ['US-TX', 'US-NGSS']
  AND i.full_statement CONTAINS 'evolution'
RETURN j.name, count(i) AS evo_items, collect(i.human_coding_scheme)[..5] AS examples
ORDER BY j.name

-- Texas items by education level
MATCH (j:Jurisdiction {jurisdiction_id: 'US-TX'})-[:PUBLISHES]->(d:CFDocument)
      -[:CONTAINS_ITEM]->(i:CFItem)
UNWIND i.education_level AS level
RETURN level, count(i) AS items
ORDER BY level
```

---

## Sources

- Texas Education Agency: https://tea.texas.gov/
- TEKS online: https://texreg.sos.state.tx.us/public/readtac$ext.ViewTAC?tac_view=3&ti=19&pt=2&ch=112
- 2009 SBOE controversy: NCSE coverage at https://ncse.ngo/texas
- 2024 TEKS Science revision: https://tea.texas.gov/academics/curriculum-standards

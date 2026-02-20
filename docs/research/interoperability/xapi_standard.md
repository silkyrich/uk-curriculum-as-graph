# xAPI: Experience API (IEEE 9274.1.1-2023)
**Citation:** ADL Initiative / 1EdTech Consortium. Experience API (xAPI), IEEE 9274.1.1-2023. (Technical standard; xAPI 1.0 published 2013; IEEE standardised as v2.0, 2020+.)
**Source:** https://adlnet.gov/projects/xapi/
**Fetched:** 2026-02-18
**Type:** standard
**Access:** page summary fetched

## Summary
xAPI (Experience API), now standardised as IEEE 9274.1.1-2023 (xAPI 2.0), defines a triple-structure statement format — Actor, Verb, Object — for capturing and sharing human performance and learning data across diverse environments. Statements are stored in a Learning Record Store (LRS), a server that receives, stores, and provides access to xAPI records. Multiple LRSs can federate, enabling cross-system data aggregation. xAPI is the most widely adopted standard for granular learner event capture in K-12 and workplace learning contexts.

## Key findings
- Core statement model: Actor → Verb → Object, plus context extensions (timestamp, authority, results, extensions)
- Learning Record Store (LRS): server receiving, storing, and providing access to xAPI statements; multiple LRSs can federate
- Tracks virtually any learning activity; content-delivery agnostic
- Three dimensions of interoperability: structural (format compliance), operational (data transfer), semantic (shared vocabularies via xAPI Profiles)
- Version history: Project Tin Can (2011) → xAPI 1.0 (2013) → IEEE standardisation as v2.0 (October 2023)
- xAPI Profiles extend the base vocabulary with domain-specific verbs and activity types, enabling semantic interoperability
- Governed by the ADL Initiative and maintained by 1EdTech; widely deployed in K-12 (more so than Caliper Analytics)
- xAPI is a data transport and storage standard — it says nothing about curriculum structure, prerequisite relationships, or how to compute mastery

## Direct quotes
From the briefing summary based on page access:

"Statement model: Actor → Verb → Object + context (timestamp, authority, results)"

"Learning Record Store (LRS): server receiving, storing, providing access to xAPI records; multiple LRSs can federate"

"xAPI is a data transport/storage standard, not a knowledge model." (Briefing interpretation)

## Relevance to platform
The platform should emit xAPI statements as its canonical learner event format, storing Neo4j concept node GUIDs in the context extension field; this creates future school MIS interoperability and GDPR audit capability while mapping naturally to the domain model — `{ actor: student_id, verb: "answered", object: question_id, result: { success: true }, context: { concept_node: "fractions/equivalent" } }`.

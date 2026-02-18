# CASE: Competencies and Academic Standards Exchange
**Citation:** 1EdTech Consortium. CASE (Competencies and Academic Standards Exchange) Specification. (Technical standard; v1.0 and v1.1.)
**Source:** https://www.1edtech.org/standards/case
**Fetched:** 2026-02-18
**Type:** standard
**Access:** page summary fetched

## Summary
CASE is a 1EdTech (formerly IMS Global) technical specification for machine-readable hierarchical academic standards. It replaces static PDF curriculum documents with API-accessible, UUID-identified standards trees expressed as JSON-LD linked data. CASE defines three core elements: CFItems (individual objectives with globally unique identifiers), Rubrics (optional depth-of-knowledge descriptors), and Associations (cross-framework alignment relationships between items). It is designed to enable content publishers, assessment vendors, and learning management systems to align their materials to curriculum standards programmatically.

## Key findings
- CASE provides machine-readable hierarchical academic standards with GUIDs (globally unique identifiers) per item
- Three core elements: Items (learning objectives with GUIDs), Rubrics (optional DOK descriptors), Associations (cross-framework alignment links between items)
- Enables: standards tagging of content and questions, progress tracking against curriculum objectives, data portability across platforms, credential linking
- Transforms static PDF curriculum documents into structured, API-accessible standards trees
- Part of the 1EdTech ecosystem alongside LTI (content integration), OneRoster (rostering), and Open Badges (credentials)
- CASE is hierarchical (a tree), not a graph — it does not natively represent prerequisite relationships, co-requisite skills, or epistemic skill types
- A JSON-LD binding allows curriculum standards to be expressed as linked data

## Direct quotes
From the briefing summary based on page access:

"CASE = Competencies and Academic Standards Exchange; machine-readable hierarchical academic standards with GUIDs"

"Transforms static PDFs into structured, API-accessible standards"

"CASE is hierarchical (a tree of standards), not a graph. It does not natively represent prerequisite relationships." (Briefing note)

## Relevance to platform
The Neo4j graph is more expressive than CASE; however, publishing a CASE-compatible view of the curriculum (flattening prerequisites into parent-child relationships) would allow the platform's content to be referenced by third-party tools aligned to the UK National Curriculum — a useful interoperability layer for school integrations, not the core data model.

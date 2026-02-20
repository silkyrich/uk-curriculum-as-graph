# Large Language Models in Education: A Systematic Review
**Citation:** Author(s) not confirmed from fetch. (2025). Large language models in education: A systematic review. *Computers and Education: Artificial Intelligence* (ScienceDirect), S2666920X25001699.
**Source:** https://www.sciencedirect.com/article/pii/S2666920X25001699
**Fetched:** 2026-02-18
**Type:** systematic review
**Access:** briefing summary only

## Summary
This 2025 systematic review examines the evidence base for large language model applications in education, with particular attention to conversational AI tutors and hint generation systems. It identifies both the promising capabilities of LLM-based tutors (conversational flexibility, Socratic questioning capacity, on-demand availability) and the critical quality control problem: a substantial proportion of LLM-generated hints in evaluated systems were pedagogically unhelpful or actively harmful to learning.

## Key findings
- Conversational LLM tutors are promising but quality control of generated content is an unsolved problem
- 35% of hints in evaluation studies were too general, incorrect, or solution-revealing — a substantial failure rate for a primary learning interaction
- LLMs do not natively maintain a persistent student model; each conversation starts fresh without explicit architectural mechanisms to carry forward student state
- LLMs can confidently produce incorrect content in niche curriculum areas, including specialist UK curriculum domains (WorkingScientifically, HistoricalThinking, etc.)
- Most productive architecture: LLM over a structured domain model — the graph provides structured curriculum and learner model (what is known, prerequisite chain, recent attempts); the LLM provides natural language generation for hints and encouragement
- Neither LLM alone nor structured model alone is sufficient for K-12 curriculum-aligned tutoring

## Direct quotes
From the briefing summary:

"35% of hints in evaluation studies were too general, incorrect, or solution-revealing."

"LLMs do not natively maintain persistent student models without explicit architecture."

"Productive architecture: LLM over structured domain model." (Briefing design principle)

## Relevance to platform
This review directly validates the platform's intended architecture: the Neo4j curriculum graph and BKT-derived learner model provide the structured knowledge state that LLMs lack natively; the LLM layer sits on top of this structure, constrained by it, generating natural language that is anchored to specific concept nodes and prerequisite states rather than generating curriculum content from scratch.

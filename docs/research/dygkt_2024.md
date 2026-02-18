# DyGKT: Dynamic Graph-Based Knowledge Tracing
**Citation:** Author(s) not confirmed from fetch. (2024). DyGKT: Dynamic Graph-Based Knowledge Tracing. *arXiv preprint* arXiv:2407.20824.
**Source:** https://arxiv.org/html/2407.20824v1
**Fetched:** 2026-02-18
**Type:** academic paper
**Access:** briefing summary only (fetch failed)

## Summary
DyGKT extends Graph-Based Knowledge Tracing (GKT) by replacing static concept dependency graphs with dynamic graphs that evolve as a student learns. Rather than fixing the graph structure at the start of a session, the graph topology is updated in response to the student's interaction history, allowing the model to capture how the relationships between concepts shift as knowledge is acquired. It represents the current frontier in graph-aware knowledge tracing as of 2024.

## Key findings
- Extends GKT (Nakagawa et al. 2019) to dynamic graph structures that evolve during learning
- Graph topology updates in response to student interaction history rather than remaining fixed
- Captures temporal shifts in concept relationships as the learner's knowledge state changes
- Part of the 2024 wave of 37 deep KT papers identified in a 2024 IEEE Education Society review
- Represents the state of the art in combining graph neural networks with knowledge tracing

## Direct quotes
None available — full text not fetched.

## Relevance to platform
DyGKT demonstrates that the Neo4j prerequisite graph need not be treated as a fixed input to the knowledge tracing model; once the platform has sufficient interaction data, the graph structure itself can become learnable, with edges reflecting empirically observed co-mastery patterns rather than only hand-authored prerequisites.

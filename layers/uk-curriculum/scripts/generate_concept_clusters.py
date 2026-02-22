#!/usr/bin/env python3
"""
Generate ConceptCluster nodes from the enriched UK Curriculum graph.

Produces small, conservative clusters as a default starting scaffold.
Teachers will rearrange and customise — the algorithm provides structure,
not prescription. Follows CC Math's Domain→Cluster→Standard pattern.

Respects:
  - topological ordering (prerequisites before dependents)
  - co-teaching pairs (CO_TEACHES pairs stay together, but capped at 4)
  - domain structure_type (hierarchical, sequential, developmental, mixed)
  - keystone concepts (trigger assessment checkpoints)
  - consolidation / assessment insertion heuristics

Usage:
  python3 generate_concept_clusters.py           # create clusters
  python3 generate_concept_clusters.py --clean    # delete existing clusters first
"""

import argparse
import math
import sys
from collections import defaultdict, deque
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


# ── Graph helpers ────────────────────────────────────────────────────────────

def load_domains(session):
    """Return list of {domain_id, domain_name, structure_type}."""
    result = session.run("""
        MATCH (d:Domain)
        WHERE EXISTS { (d)-[:HAS_CONCEPT]->(:Concept) }
        RETURN d.domain_id AS domain_id,
               d.domain_name AS domain_name,
               coalesce(d.structure_type, 'mixed') AS structure_type
        ORDER BY d.domain_id
    """)
    return [dict(r) for r in result]


def load_domain_concepts(session, domain_id):
    """Return concepts for a domain with their properties."""
    result = session.run("""
        MATCH (d:Domain {domain_id: $domain_id})-[:HAS_CONCEPT]->(c:Concept)
        RETURN c.concept_id AS concept_id,
               c.concept_name AS concept_name,
               coalesce(c.teaching_weight, 1) AS teaching_weight,
               coalesce(c.complexity_level, 1) AS complexity_level,
               coalesce(c.is_keystone, false) AS is_keystone,
               coalesce(c.concept_type, 'knowledge') AS concept_type
        ORDER BY c.concept_id
    """, domain_id=domain_id)
    return [dict(r) for r in result]


def load_domain_prerequisites(session, domain_id):
    """Return PREREQUISITE_OF edges within a domain as (source, target) pairs."""
    result = session.run("""
        MATCH (d:Domain {domain_id: $domain_id})-[:HAS_CONCEPT]->(c1:Concept)
              -[:PREREQUISITE_OF]->(c2:Concept)<-[:HAS_CONCEPT]-(d)
        RETURN c1.concept_id AS source, c2.concept_id AS target
    """, domain_id=domain_id)
    return [(r["source"], r["target"]) for r in result]


def load_domain_co_teaches(session, domain_id):
    """Return CO_TEACHES edges within a domain as (source, target) pairs."""
    result = session.run("""
        MATCH (d:Domain {domain_id: $domain_id})-[:HAS_CONCEPT]->(c1:Concept)
              -[:CO_TEACHES]->(c2:Concept)<-[:HAS_CONCEPT]-(d)
        RETURN c1.concept_id AS source, c2.concept_id AS target
    """, domain_id=domain_id)
    return [(r["source"], r["target"]) for r in result]


# ── Clustering algorithm ────────────────────────────────────────────────────

def topological_sort(concept_ids, prereq_edges):
    """Kahn's algorithm. Returns sorted list; cycles are appended at end."""
    in_degree = {cid: 0 for cid in concept_ids}
    adjacency = defaultdict(list)
    for src, tgt in prereq_edges:
        if src in in_degree and tgt in in_degree:
            adjacency[src].append(tgt)
            in_degree[tgt] += 1

    queue = deque(cid for cid, deg in in_degree.items() if deg == 0)
    ordered = []
    while queue:
        node = queue.popleft()
        ordered.append(node)
        for neighbour in adjacency[node]:
            in_degree[neighbour] -= 1
            if in_degree[neighbour] == 0:
                queue.append(neighbour)

    # Append any remaining (cycle members) at the end
    remaining = [cid for cid in concept_ids if cid not in set(ordered)]
    ordered.extend(remaining)
    return ordered


def build_co_teach_groups(concept_ids, co_teach_edges, max_group_size=4):
    """Union-Find to merge co-teaching pairs into groups.

    Groups are capped at max_group_size to prevent runaway merging
    from aggressive vocabulary-overlap heuristics. If a union would
    create a group larger than the cap, the edge is silently skipped.
    Teachers can always merge clusters manually.
    """
    parent = {cid: cid for cid in concept_ids}
    size = {cid: 1 for cid in concept_ids}

    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            # Cap: don't merge if combined size exceeds limit
            if size[ra] + size[rb] > max_group_size:
                return
            # Union by size
            if size[ra] < size[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            size[ra] += size[rb]

    for src, tgt in co_teach_edges:
        if src in parent and tgt in parent:
            union(src, tgt)

    groups = defaultdict(set)
    for cid in concept_ids:
        groups[find(cid)].add(cid)
    return list(groups.values())


def cluster_concepts(concepts, prereq_edges, co_teach_edges, structure_type):
    """
    Main clustering logic. Returns list of dicts:
      {concept_ids: [...], cluster_type: str, is_keystone_cluster: bool}

    Produces small, conservative clusters (max 4 concepts). The output is
    a suggested scaffold — teachers will rearrange based on their own
    judgement about what goes well together.
    """
    if not concepts:
        return []

    concept_map = {c["concept_id"]: c for c in concepts}
    concept_ids = list(concept_map.keys())

    # Topological order
    topo_order = topological_sort(concept_ids, prereq_edges)

    # Co-teach groups (merged sets, capped at 4 members)
    max_per_cluster = 4 if structure_type in ("hierarchical", "sequential") else 3
    co_groups = build_co_teach_groups(concept_ids, co_teach_edges, max_group_size=max_per_cluster)

    # Map each concept to its group representative
    cid_to_group = {}
    for group in co_groups:
        rep = min(group)  # canonical representative
        for cid in group:
            cid_to_group[cid] = rep

    # Build ordered list of unique groups in topological order
    seen_groups = set()
    ordered_groups = []
    for cid in topo_order:
        rep = cid_to_group.get(cid, cid)
        if rep not in seen_groups:
            seen_groups.add(rep)
            members = sorted(
                [c for c in concept_ids if cid_to_group.get(c, c) == rep],
                key=lambda x: topo_order.index(x)
            )
            ordered_groups.append(members)

    # Pack groups into clusters (respecting max_per_cluster strictly)
    raw_clusters = []
    current = []

    for group_members in ordered_groups:
        # Split oversized groups into sub-clusters of max_per_cluster
        if len(group_members) > max_per_cluster:
            if current:
                raw_clusters.append(current)
                current = []
            for i in range(0, len(group_members), max_per_cluster):
                raw_clusters.append(group_members[i:i + max_per_cluster])
            continue

        if len(current) + len(group_members) > max_per_cluster:
            raw_clusters.append(current)
            current = list(group_members)
        else:
            current.extend(group_members)

    if current:
        raw_clusters.append(current)

    # Classify clusters: first is introduction, rest are practice
    clusters = []
    for i, concept_ids_in_cluster in enumerate(raw_clusters):
        has_keystone = any(
            concept_map[cid]["is_keystone"] for cid in concept_ids_in_cluster
        )
        cluster_type = "introduction" if i == 0 else "practice"
        clusters.append({
            "concept_ids": concept_ids_in_cluster,
            "cluster_type": cluster_type,
            "is_keystone_cluster": has_keystone,
        })

    # ── Insert consolidation clusters (~15-20% of content clusters) ──
    # Only insert if there are enough content clusters to consolidate.
    # Each consolidation cluster recaps concepts from the preceding 2 clusters.
    total_content = len(clusters)
    if total_content >= 4:
        num_consolidation = max(1, round(total_content * 0.18))
        step = max(3, total_content // num_consolidation)
        enriched = []
        inserted = 0
        for i, cluster in enumerate(clusters):
            enriched.append(cluster)
            # Insert consolidation after every `step` content clusters
            if (i + 1) % step == 0 and i > 0 and inserted < num_consolidation:
                # Gather concept_ids from the last 2 content clusters
                prev_ids = []
                for prev in enriched[-(min(2, len(enriched))):]:
                    if prev["cluster_type"] != "consolidation":
                        prev_ids.extend(prev["concept_ids"])
                if prev_ids:
                    enriched.append({
                        "concept_ids": prev_ids[:4],
                        "cluster_type": "consolidation",
                        "is_keystone_cluster": False,
                    })
                    inserted += 1
    else:
        enriched = list(clusters)

    # ── Insert assessment clusters ──
    # After keystone clusters and every 10+ cumulative teaching_weight.
    # Target: ~10-15% of total, not after every content cluster.
    final = []
    cumulative_weight = 0
    last_assessment_weight = 0
    assessment_gap = 10  # minimum teaching_weight between assessments
    for cluster in enriched:
        final.append(cluster)
        weight = sum(
            concept_map[cid]["teaching_weight"]
            for cid in cluster["concept_ids"]
            if cid in concept_map
        )
        cumulative_weight += weight

        # Skip assessment after consolidation or other assessment clusters
        if cluster["cluster_type"] in ("assessment", "consolidation"):
            continue

        needs_assessment = (
            cluster["is_keystone_cluster"]
            and (cumulative_weight - last_assessment_weight >= 4)
        ) or (
            cumulative_weight - last_assessment_weight >= assessment_gap
        )

        if needs_assessment:
            final.append({
                "concept_ids": cluster["concept_ids"],
                "cluster_type": "assessment",
                "is_keystone_cluster": cluster["is_keystone_cluster"],
            })
            last_assessment_weight = cumulative_weight

    return final


# ── Graph writing ────────────────────────────────────────────────────────────

def extract_cluster_prefix(domain_id):
    """Derive cluster prefix from domain_id, e.g. 'MA-Y3-D001' -> 'MA-Y3-D001'.

    Uses the full domain_id to avoid collisions between domains in the
    same subject-year (e.g. MA-Y3-D001 and MA-Y3-D002).
    """
    return domain_id


def write_clusters_to_graph(session, domain_id, clusters, concept_map, stats):
    """Create ConceptCluster nodes and relationships for one domain."""
    prefix = extract_cluster_prefix(domain_id)
    cluster_ids = []

    for i, cluster in enumerate(clusters):
        cluster_id = f"{prefix}-CL{i + 1:03d}"
        cluster_ids.append(cluster_id)

        # Compute derived properties
        concept_ids = cluster["concept_ids"]
        complexities = [
            concept_map[cid]["complexity_level"]
            for cid in concept_ids if cid in concept_map
        ]
        weights = [
            concept_map[cid]["teaching_weight"]
            for cid in concept_ids if cid in concept_map
        ]

        min_c = min(complexities) if complexities else 1
        max_c = max(complexities) if complexities else 1
        complexity_range = f"{min_c}-{max_c}" if min_c != max_c else str(min_c)
        lesson_count = sum(weights) if weights else 1
        teaching_weeks = max(1, round(lesson_count / 3, 1))

        cluster_name = f"{cluster['cluster_type'].title()}: {', '.join(concept_map[cid]['concept_name'] for cid in concept_ids[:3] if cid in concept_map)}"
        if len(concept_ids) > 3:
            cluster_name += f" (+{len(concept_ids) - 3})"

        # Create cluster node
        session.run("""
            MERGE (cc:ConceptCluster {cluster_id: $cluster_id})
            SET cc.cluster_name = $cluster_name,
                cc.cluster_type = $cluster_type,
                cc.teaching_weeks = $teaching_weeks,
                cc.lesson_count = $lesson_count,
                cc.complexity_range = $complexity_range,
                cc.is_keystone_cluster = $is_keystone_cluster,
                cc.display_category = 'UK Curriculum',
                cc.display_color = '#6366F1',
                cc.display_icon = 'view_module',
                cc.name = $cluster_name
        """,
            cluster_id=cluster_id,
            cluster_name=cluster_name,
            cluster_type=cluster["cluster_type"],
            teaching_weeks=teaching_weeks,
            lesson_count=lesson_count,
            complexity_range=complexity_range,
            is_keystone_cluster=cluster["is_keystone_cluster"],
        )
        stats["clusters_created"] += 1
        stats[f"type_{cluster['cluster_type']}"] += 1

        # Domain -> Cluster
        session.run("""
            MATCH (d:Domain {domain_id: $domain_id})
            MATCH (cc:ConceptCluster {cluster_id: $cluster_id})
            MERGE (d)-[:HAS_CLUSTER]->(cc)
        """, domain_id=domain_id, cluster_id=cluster_id)

        # Cluster -> Concepts
        for cid in concept_ids:
            if cid in concept_map:
                session.run("""
                    MATCH (cc:ConceptCluster {cluster_id: $cluster_id})
                    MATCH (c:Concept {concept_id: $concept_id})
                    MERGE (cc)-[:GROUPS]->(c)
                """, cluster_id=cluster_id, concept_id=cid)
                stats["concepts_grouped"] += 1

    # SEQUENCED_AFTER chains within domain
    for i in range(1, len(cluster_ids)):
        session.run("""
            MATCH (a:ConceptCluster {cluster_id: $prev_id})
            MATCH (b:ConceptCluster {cluster_id: $curr_id})
            MERGE (b)-[:SEQUENCED_AFTER]->(a)
        """, prev_id=cluster_ids[i - 1], curr_id=cluster_ids[i])
        stats["sequence_links"] += 1


def clean_existing_clusters(session):
    """Delete all ConceptCluster nodes and their relationships."""
    result = session.run("""
        MATCH (cc:ConceptCluster)
        DETACH DELETE cc
        RETURN count(cc) AS deleted
    """)
    deleted = result.single()["deleted"]
    print(f"  Deleted {deleted} existing ConceptCluster nodes.")
    return deleted


# ── Main ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Generate ConceptCluster nodes")
    parser.add_argument("--clean", action="store_true",
                        help="Delete existing clusters before generating")
    args = parser.parse_args()

    print("=" * 60)
    print("UK Curriculum: Generate ConceptCluster nodes")
    print("=" * 60)

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    stats = defaultdict(int)

    try:
        with driver.session() as session:
            if args.clean:
                print("\n--- Cleaning existing clusters ---")
                clean_existing_clusters(session)

            print("\n--- Loading domains ---")
            domains = load_domains(session)
            print(f"  Domains with concepts: {len(domains)}")

            for domain in domains:
                domain_id = domain["domain_id"]
                structure_type = domain["structure_type"]

                # Load data for this domain
                concepts = load_domain_concepts(session, domain_id)
                if not concepts:
                    continue

                prereq_edges = load_domain_prerequisites(session, domain_id)
                co_teach_edges = load_domain_co_teaches(session, domain_id)
                concept_map = {c["concept_id"]: c for c in concepts}

                # Cluster
                clusters = cluster_concepts(
                    concepts, prereq_edges, co_teach_edges, structure_type
                )

                if clusters:
                    write_clusters_to_graph(
                        session, domain_id, clusters, concept_map, stats
                    )
                    stats["domains_processed"] += 1
                    print(f"  {domain_id}: {len(concepts)} concepts -> {len(clusters)} clusters")

        # ── Summary ──────────────────────────────────────────────────────
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)
        print(f"  Domains processed:      {stats['domains_processed']}")
        print(f"  Clusters created:       {stats['clusters_created']}")
        print(f"    - introduction:       {stats['type_introduction']}")
        print(f"    - practice:           {stats['type_practice']}")
        print(f"    - consolidation:      {stats['type_consolidation']}")
        print(f"    - assessment:         {stats['type_assessment']}")
        print(f"  Concepts grouped:       {stats['concepts_grouped']}")
        print(f"  Sequence links:         {stats['sequence_links']}")
        if stats["clusters_created"] > 0:
            avg = stats["concepts_grouped"] / stats["clusters_created"]
            print(f"  Avg concepts/cluster:   {avg:.1f}")

    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
    finally:
        driver.close()

    print("\nDone.")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Generate MathsUnit JSON data files from existing extraction data and cluster definitions.

Each MathsUnit corresponds to one ConceptCluster (e.g. "Add and subtract using
formal columnar methods"). This follows the many-to-one domain mapping pattern
used by other subjects — multiple units deliver the same domain from different
angles, just as Science has multiple enquiries per domain and History has
multiple thematic studies per domain.

Units are populated with:
  - concept_ids and delivers_via from the cluster definitions
  - concept metadata (description, teaching_guidance) from the extraction JSONs
  - manipulative/representation/context/reasoning links from reference node data
  - appropriate vehicle templates based on cluster/domain type

Usage:
    python3 layers/topic-suggestions/scripts/generate_maths_units.py
    python3 layers/topic-suggestions/scripts/generate_maths_units.py --dry-run
"""

import argparse
import json
import re
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
EXTRACTIONS_DIR = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "extractions"
CLUSTER_DEFS = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "cluster_definitions" / "mathematics.json"
REFERENCE_DIR = PROJECT_ROOT / "layers" / "topic-suggestions" / "data"
OUTPUT_DIR = PROJECT_ROOT / "layers" / "topic-suggestions" / "data" / "maths_units"


def load_extractions() -> dict:
    """Load all Maths extraction JSONs. Returns {domain_id: {domain_info, concepts}}."""
    domains = {}
    for subdir in ["primary", "secondary"]:
        extraction_dir = EXTRACTIONS_DIR / subdir
        if not extraction_dir.exists():
            continue
        for fp in sorted(extraction_dir.glob("Mathematics_*.json")):
            data = json.loads(fp.read_text(encoding="utf-8"))
            meta = data.get("metadata", {})
            ks = meta.get("key_stage", "")
            years = meta.get("years_covered", [])

            # Concepts are at top level with domain_id field
            all_concepts = data.get("concepts", [])
            concepts_by_domain = {}
            for c in all_concepts:
                cdid = c.get("domain_id", "")
                concepts_by_domain.setdefault(cdid, []).append(c)

            for domain in data.get("domains", []):
                did = domain["domain_id"]
                concepts = concepts_by_domain.get(did, [])

                # Determine year_groups
                year_groups = []
                if years:
                    year_groups = [f"Y{y}" for y in years]
                elif "KS3" in did:
                    year_groups = ["Y7", "Y8", "Y9"]
                elif "KS4" in did:
                    year_groups = ["Y10", "Y11"]

                domains[did] = {
                    "domain_id": did,
                    "domain_name": domain.get("domain_name", ""),
                    "description": domain.get("description", ""),
                    "curriculum_context": domain.get("curriculum_context", ""),
                    "key_stage": ks,
                    "year_groups": year_groups,
                    "concepts": concepts,
                }
    return domains


def load_cluster_definitions() -> dict:
    """Load cluster definitions. Returns {domain_id: [clusters]}."""
    if not CLUSTER_DEFS.exists():
        return {}
    data = json.loads(CLUSTER_DEFS.read_text(encoding="utf-8"))
    return data.get("domains", {})


def load_reference_links() -> dict:
    """Load reference node data to map concept_id -> reference nodes."""
    concept_to_refs = {}  # {concept_id: {manipulatives: [], representations: [], contexts: [], reasoning: []}}

    # Manipulatives
    manip_file = REFERENCE_DIR / "maths_manipulatives" / "manipulatives.json"
    if manip_file.exists():
        for item in json.loads(manip_file.read_text(encoding="utf-8")):
            mid = item.get("manipulative_id")
            for cid in item.get("source_concepts", []):
                concept_to_refs.setdefault(cid, {"manipulatives": [], "representations": [], "contexts": [], "reasoning": []})
                if mid not in concept_to_refs[cid]["manipulatives"]:
                    concept_to_refs[cid]["manipulatives"].append(mid)

    # Representations
    repr_file = REFERENCE_DIR / "maths_representations" / "representations.json"
    if repr_file.exists():
        for item in json.loads(repr_file.read_text(encoding="utf-8")):
            rid = item.get("representation_id")
            for cid in item.get("source_concepts", []):
                concept_to_refs.setdefault(cid, {"manipulatives": [], "representations": [], "contexts": [], "reasoning": []})
                if rid not in concept_to_refs[cid]["representations"]:
                    concept_to_refs[cid]["representations"].append(rid)

    # Contexts
    ctx_file = REFERENCE_DIR / "maths_contexts" / "contexts.json"
    if ctx_file.exists():
        for item in json.loads(ctx_file.read_text(encoding="utf-8")):
            cxid = item.get("context_id")
            for cid in item.get("source_concepts", []):
                concept_to_refs.setdefault(cid, {"manipulatives": [], "representations": [], "contexts": [], "reasoning": []})
                if cxid not in concept_to_refs[cid]["contexts"]:
                    concept_to_refs[cid]["contexts"].append(cxid)

    # Reasoning prompt types
    reason_file = REFERENCE_DIR / "maths_reasoning" / "reasoning_prompt_types.json"
    if reason_file.exists():
        for item in json.loads(reason_file.read_text(encoding="utf-8")):
            ptid = item.get("prompt_type_id")
            for cid in item.get("source_concepts", []):
                concept_to_refs.setdefault(cid, {"manipulatives": [], "representations": [], "contexts": [], "reasoning": []})
                if ptid not in concept_to_refs[cid]["reasoning"]:
                    concept_to_refs[cid]["reasoning"].append(ptid)

    return concept_to_refs


def choose_templates(domain_name: str, cluster_name: str, cluster_type: str) -> list[str]:
    """Choose appropriate VehicleTemplates based on domain and cluster type."""
    combined = (domain_name + " " + cluster_name).lower()

    # VT-08 Worked Example Set — core template for all maths
    templates = ["VT-08"]

    # VT-09 Open Investigation — for problem-solving/reasoning/investigation clusters
    if any(kw in combined for kw in ["problem", "investigation", "reasoning", "working mathematically", "open"]):
        templates.append("VT-09")

    # VT-13 Practical Application — for measurement, statistics, geometry, applied contexts
    if any(kw in combined for kw in ["measurement", "statistics", "geometry", "ratio", "probability",
                                      "money", "time", "perimeter", "area", "volume", "data"]):
        templates.append("VT-13")

    # VT-05 Pattern Seeking — for algebra, number patterns, sequences
    if any(kw in combined for kw in ["algebra", "pattern", "sequence", "formula"]):
        templates.append("VT-05")

    return templates


def domain_sort_key(domain_id: str) -> tuple:
    """Sort key for domains: by year number then domain number."""
    # Extract year: Y1-Y11 or KS3/KS4
    m = re.search(r'Y(\d+)', domain_id)
    if m:
        year = int(m.group(1))
    elif 'KS3' in domain_id:
        year = 70  # sort after Y6
    elif 'KS4' in domain_id:
        year = 100
    else:
        year = 999

    # Extract domain number
    m2 = re.search(r'D(\d+)', domain_id)
    dom = int(m2.group(1)) if m2 else 0

    return (year, dom)


def collect_refs(concept_ids: list[str], ref_links: dict) -> dict:
    """Collect reference node links across a set of concept IDs."""
    result = {"manipulatives": [], "representations": [], "contexts": [], "reasoning": []}
    for cid in concept_ids:
        refs = ref_links.get(cid, {})
        for key in result:
            for val in refs.get(key, []):
                if val not in result[key]:
                    result[key].append(val)
    return result


def build_concept_index(domains: dict) -> dict:
    """Build concept_id -> concept metadata index from all domains."""
    index = {}
    for dinfo in domains.values():
        for c in dinfo["concepts"]:
            index[c["concept_id"]] = c
    return index


def generate_units(domains: dict, clusters: dict, ref_links: dict, dry_run: bool = False):
    """Generate MathsUnit JSON files grouped by key stage.

    Creates one MathsUnit per ConceptCluster, following the many-to-one
    domain mapping used by other subjects (Science, History, English, Geography).
    """
    concept_index = build_concept_index(domains)

    # Group domains by key stage
    ks_domains = {}
    for did, dinfo in sorted(domains.items(), key=lambda x: domain_sort_key(x[0])):
        ks = dinfo["key_stage"]
        ks_domains.setdefault(ks, []).append((did, dinfo))

    total_units = 0
    total_files = 0

    for ks, domain_list in sorted(ks_domains.items()):
        units = []
        unit_counter = 0

        for did, dinfo in domain_list:
            year_part = did.split("-")[1]  # Y1, Y2, ..., KS3, KS4
            domain_name = dinfo["domain_name"]
            domain_clusters = clusters.get(did, {}).get("clusters", [])

            if not domain_clusters:
                # Fallback: domain has no clusters — create one unit for the whole domain
                unit_counter += 1
                concept_ids = [c["concept_id"] for c in dinfo["concepts"]]
                refs = collect_refs(concept_ids, ref_links)

                rationale = dinfo.get("curriculum_context", dinfo.get("description", ""))
                if len(rationale) > 500:
                    sentences = rationale.split(". ")
                    rationale = ". ".join(sentences[:2]) + "."

                units.append({
                    "unit_id": f"MU-{year_part}-{unit_counter:03d}",
                    "name": domain_name,
                    "subject": "Mathematics",
                    "key_stage": ks,
                    "year_groups": dinfo["year_groups"],
                    "curriculum_status": "mandatory",
                    "suggestion_type": "curriculum_unit",
                    "unit_type": "domain_unit",
                    "description": dinfo["description"],
                    "pedagogical_rationale": rationale,
                    "duration_lessons": max(3, min(10, len(concept_ids) * 2)),
                    "concept_count": len(concept_ids),
                    "cluster_type": "mixed",
                    "thinking_lenses": [],
                    "delivers_via": [{"concept_id": cid, "primary": i == 0}
                                     for i, cid in enumerate(concept_ids)],
                    "uses_template": choose_templates(domain_name, "", ""),
                    "domain_ids": [did],
                    "uses_manipulative": refs["manipulatives"],
                    "uses_representation": refs["representations"],
                    "uses_context": refs["contexts"],
                    "uses_reasoning_prompt": refs["reasoning"],
                    "cross_curricular_links": [],
                    "display_category": "Topic Suggestion",
                    "display_color": "#3B82F6",
                    "display_icon": "calculate",
                })
                continue

            # One unit per cluster
            for cl in domain_clusters:
                unit_counter += 1
                cluster_name = cl["cluster_name"]
                cluster_type = cl.get("cluster_type", "introduction")
                concept_ids = cl.get("concept_ids", [])

                # Extract thinking lenses
                thinking_lenses = [tl["lens"] for tl in cl.get("thinking_lenses", [])]

                # Build delivers_via
                delivers_via = [{"concept_id": cid, "primary": i == 0}
                                for i, cid in enumerate(concept_ids)]

                # Collect reference links for this cluster's concepts
                refs = collect_refs(concept_ids, ref_links)

                # Build description from concept metadata
                concept_descriptions = []
                for cid in concept_ids:
                    cmeta = concept_index.get(cid, {})
                    cname = cmeta.get("concept_name", cid)
                    concept_descriptions.append(cname)
                description = f"Covers: {'; '.join(concept_descriptions)}."

                # Use cluster rationale as pedagogical_rationale
                rationale = cl.get("rationale", "")

                # Duration based on cluster type and concept count
                n = len(concept_ids)
                if cluster_type == "introduction":
                    duration_lessons = max(3, n * 2)
                else:  # practice
                    duration_lessons = max(2, n + 1)

                templates = choose_templates(domain_name, cluster_name, cluster_type)

                units.append({
                    "unit_id": f"MU-{year_part}-{unit_counter:03d}",
                    "name": cluster_name,
                    "subject": "Mathematics",
                    "key_stage": ks,
                    "year_groups": dinfo["year_groups"],
                    "curriculum_status": "mandatory",
                    "suggestion_type": "curriculum_unit",
                    "unit_type": cluster_type,
                    "domain_name": domain_name,
                    "description": description,
                    "pedagogical_rationale": rationale,
                    "duration_lessons": duration_lessons,
                    "concept_count": n,
                    "cluster_type": cluster_type,
                    "thinking_lenses": thinking_lenses,
                    "delivers_via": delivers_via,
                    "uses_template": templates,
                    "domain_ids": [did],
                    "uses_manipulative": refs["manipulatives"],
                    "uses_representation": refs["representations"],
                    "uses_context": refs["contexts"],
                    "uses_reasoning_prompt": refs["reasoning"],
                    "cross_curricular_links": [],
                    "display_category": "Topic Suggestion",
                    "display_color": "#3B82F6",
                    "display_icon": "calculate",
                })

        # Write file
        file_data = {
            "version": "1.0",
            "subject": "Mathematics",
            "key_stage": ks,
            "authored_by": "maths-unit-generator",
            "authored_date": "2026-03-20",
            "note": f"MathsUnit nodes for {ks}. Auto-generated from cluster definitions. Each unit corresponds to one ConceptCluster, following the many-to-one domain mapping pattern used by other subjects.",
            "units": units,
        }

        filename = f"maths_units_{ks.lower()}.json"
        filepath = OUTPUT_DIR / filename

        if dry_run:
            print(f"  [DRY RUN] Would write {filename}: {len(units)} units")
        else:
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(file_data, f, indent=2, ensure_ascii=False)
            print(f"  Wrote {filename}: {len(units)} units")

        total_units += len(units)
        total_files += 1

    return total_units, total_files


def main():
    parser = argparse.ArgumentParser(description="Generate MathsUnit data files")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be generated")
    args = parser.parse_args()

    print("Loading extraction data...")
    domains = load_extractions()
    print(f"  Found {len(domains)} maths domains")

    print("Loading cluster definitions...")
    clusters = load_cluster_definitions()
    print(f"  Found {len(clusters)} domains with clusters")

    print("Loading reference node links...")
    ref_links = load_reference_links()
    concepts_with_refs = len(ref_links)
    print(f"  Found reference links for {concepts_with_refs} concepts")

    print("\nGenerating MathsUnit files...")
    total_units, total_files = generate_units(domains, clusters, ref_links, dry_run=args.dry_run)

    print(f"\nDone: {total_units} units across {total_files} files")
    if not args.dry_run:
        print(f"Output: {OUTPUT_DIR.relative_to(PROJECT_ROOT)}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Classify every curriculum concept by delivery mode suitability.

Reads concept metadata from extraction JSONs plus supplementary data
(RepresentationStages, concept_skill_links) and applies rule-based
classification to assign each concept a primary delivery mode:

  DM-AI  — AI Direct (computer teaches end-to-end)
  DM-AF  — AI Facilitated (computer + non-specialist facilitator)
  DM-GM  — Guided Materials (non-qualified adult with materials)
  DM-ST  — Specialist Teacher (qualified teacher required)

Outputs per-file JSON files in layers/uk-curriculum/data/delivery_modes/
with one entry per concept. These are imported by import_delivery_modes.py.

Usage:
  python3 layers/uk-curriculum/scripts/classify_delivery_modes.py
  python3 layers/uk-curriculum/scripts/classify_delivery_modes.py --dry-run
"""

import json
import re
import argparse
from pathlib import Path
from collections import Counter, defaultdict

PROJECT_ROOT = Path(__file__).resolve().parents[3]

# Source data directories
PRIMARY_DIR = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "extractions" / "primary"
SECONDARY_DIR = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "extractions" / "secondary"
EYFS_DIR = PROJECT_ROOT / "layers" / "eyfs" / "data" / "extractions"
RS_DIR = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "representation_stages"
CSL_DIR = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "concept_skill_links"
OUTPUT_DIR = PROJECT_ROOT / "layers" / "uk-curriculum" / "data" / "delivery_modes"

# Valid delivery modes (ordered by digital autonomy)
MODES = {
    "ai_direct": "DM-AI",
    "ai_facilitated": "DM-AF",
    "guided_materials": "DM-GM",
    "specialist_teacher": "DM-ST",
}

MODE_ORDER = {"DM-AI": 1, "DM-AF": 2, "DM-GM": 3, "DM-ST": 4}

# Keywords in teaching_guidance that signal physical requirements
PHYSICAL_KEYWORDS = [
    "manipulative", "concrete", "hands-on", "physical", "apparatus",
    "equipment", "practical", "kitchen", "cooking", "instrument",
    "tools", "materials", "cut", "build", "construct", "clay",
    "paint", "draw", "pencil", "ruler", "scissors", "glue",
    "outdoor", "fieldwork", "gymnastic", "swimming", "dance",
]

DISCUSSION_KEYWORDS = [
    "discuss", "debate", "dialogue", "conversation", "talk about",
    "explore views", "ethical", "moral", "sensitive", "empathy",
    "perspective", "interpret", "opinion", "viewpoint",
]

PERFORMANCE_KEYWORDS = [
    "perform", "sing", "play instrument", "ensemble", "recite",
    "present to", "audience", "improvise", "compose and perform",
    "choreograph", "gymnastic routine", "swimming",
]

CREATIVE_ASSESSMENT_KEYWORDS = [
    "creative writing", "compose", "story writing", "poetry writing",
    "artwork", "sculpture", "painting", "design and make",
    "original", "imaginative", "expressive",
]


def load_representation_stages():
    """Load RS data to identify concepts needing physical manipulatives."""
    rs_data = {}  # concept_id -> {has_concrete: bool, concrete_resources: [...]}
    if not RS_DIR.exists():
        return rs_data
    for f in RS_DIR.glob("*.json"):
        with open(f) as fh:
            entries = json.load(fh)
        for entry in entries:
            cid = entry["concept_id"]
            stages = entry.get("stages", [])
            concrete = [s for s in stages if s.get("stage") == "concrete"]
            rs_data[cid] = {
                "has_concrete": len(concrete) > 0,
                "concrete_resources": concrete[0].get("resources", []) if concrete else [],
            }
    return rs_data


def load_concept_skill_links():
    """Load concept-skill links to identify enquiry types."""
    csl_data = {}  # concept_id -> {skill_type, enquiry_type}
    if not CSL_DIR.exists():
        return csl_data
    for f in CSL_DIR.glob("*.json"):
        with open(f) as fh:
            data = json.load(fh)
        for link in data.get("links", []):
            cid = link["concept_id"]
            csl_data[cid] = {
                "skill_type": data.get("skill_type", ""),
                "enquiry_type": link.get("enquiry_type", ""),
            }
    return csl_data


def keyword_score(text, keywords):
    """Count how many keywords appear in text (case-insensitive)."""
    if not text:
        return 0
    text_lower = text.lower()
    return sum(1 for kw in keywords if kw.lower() in text_lower)


def extract_subject_from_id(concept_id):
    """Extract subject prefix from concept ID (e.g. 'MA' from 'MA-Y3-C001')."""
    return concept_id.split("-")[0] if "-" in concept_id else ""


def extract_year_number(concept_id, metadata):
    """Extract year number from concept or metadata."""
    years = metadata.get("years_covered", [])
    if years:
        return years[0]
    # Try to parse from concept_id
    parts = concept_id.split("-")
    for p in parts:
        if p.startswith("Y") and p[1:].isdigit():
            return int(p[1:])
        if p.startswith("KS"):
            ks_map = {"KS1": 2, "KS2": 5, "KS3": 8, "KS4": 10}
            return ks_map.get(p, 0)
    return 0


def get_key_stage(concept_id, metadata):
    """Determine key stage from concept or metadata."""
    ks = metadata.get("key_stage", "")
    if ks:
        return ks
    # Infer from year
    year = extract_year_number(concept_id, metadata)
    if year <= 2:
        return "KS1"
    elif year <= 6:
        return "KS2"
    elif year <= 9:
        return "KS3"
    else:
        return "KS4"


def classify_concept(concept, domain_info, metadata, rs_data, csl_data):
    """
    Classify a single concept into a delivery mode.

    Returns dict with: primary_mode, confidence, rationale, alternative_modes,
    teaching_requirements, notes
    """
    cid = concept["concept_id"]
    ctype = concept.get("concept_type", "knowledge")
    tw = concept.get("teaching_weight", 3)
    subject = metadata.get("subject", "")
    year = extract_year_number(cid, metadata)
    ks = get_key_stage(cid, metadata)
    guidance = concept.get("teaching_guidance", "")
    description = concept.get("description", "")
    misconceptions = concept.get("common_misconceptions", "")
    domain_structure = domain_info.get("structure_type", "")
    is_cross_cutting = concept.get("is_cross_cutting", False)

    # Supplementary data
    rs = rs_data.get(cid, {})
    csl = csl_data.get(cid, {})

    # Accumulate teaching requirements and reasons
    requirements = set()
    reasons = []

    # Score keyword signals
    phys_score = keyword_score(guidance + " " + description, PHYSICAL_KEYWORDS)
    disc_score = keyword_score(guidance + " " + description, DISCUSSION_KEYWORDS)
    perf_score = keyword_score(guidance + " " + description, PERFORMANCE_KEYWORDS)
    crea_score = keyword_score(guidance + " " + description, CREATIVE_ASSESSMENT_KEYWORDS)

    # ---- HARD RULES (override everything) ----

    # PE: almost entirely specialist teacher
    if subject == "Physical Education":
        if ctype == "knowledge":
            # Theory-only PE concepts can be AI-delivered
            return _result(cid, "DM-AF", "high",
                           "PE knowledge concept — factual content deliverable digitally but physical context benefits from facilitator.",
                           ["DM-AI"], ["TR-VIS", "TR-OBJ"], "")
        return _result(cid, "DM-ST", "high",
                       f"Physical Education {ctype} concept — requires physical space, expert technique correction, and safety supervision.",
                       [], ["TR-PER", "TR-APP", "TR-SPK"],
                       "PE skills, processes, and attitudes require embodied teaching.")

    # Drama: specialist teacher
    if subject == "Drama":
        return _result(cid, "DM-ST", "high",
                       "Drama concept — requires embodied performance, devising, and real-time ensemble work.",
                       ["DM-GM"], ["TR-PER", "TR-CRA", "TR-SPK"], "")

    # Attitude concepts: specialist minimum
    if ctype == "attitude":
        return _result(cid, "DM-ST", "medium",
                       f"Attitude concept ({concept.get('concept_name', '')}) — attitudes require human modelling, relationship, and pastoral awareness.",
                       ["DM-GM"], ["TR-PAS", "TR-MOD"],
                       "Some attitudes (e.g. scientific curiosity) could be supported via AI-guided inquiry, but human modelling is primary.")

    # EYFS: children aged 4-5 need adult presence for almost everything
    if cid.startswith("EYFS-") or ks == "EYFS":
        if subject == "PSED" or ctype == "social":
            return _result(cid, "DM-ST", "high",
                           "EYFS PSED/social concept — requires emotionally attuned adult for social-emotional development.",
                           [], ["TR-PAS", "TR-MOD", "TR-OBS"], "")
        if subject in ("Physical Development",):
            return _result(cid, "DM-ST", "high",
                           "EYFS Physical Development — requires physical space and expert safety supervision for young children.",
                           [], ["TR-PER", "TR-APP", "TR-OBS"], "")
        # Most EYFS concepts need at minimum a facilitator
        return _result(cid, "DM-AF", "medium",
                       f"EYFS concept for 4-5 year olds — AI can deliver structured activities via voice/touch but adult facilitates physical tasks and monitors engagement.",
                       ["DM-GM"], ["TR-PHY", "TR-OBS", "TR-AUD"],
                       "Young children benefit from adult presence; voice-based AI interaction is primary digital channel.")

    # ---- SUBJECT-SPECIFIC RULES ----

    # MATHEMATICS
    if subject == "Mathematics":
        return _classify_maths(cid, concept, ctype, tw, year, ks, rs, guidance, description, requirements)

    # ENGLISH (including English Language, English Literature)
    if subject in ("English", "English Language", "English Literature"):
        return _classify_english(cid, concept, ctype, tw, year, ks, domain_info, guidance, description,
                                 disc_score, crea_score, perf_score)

    # SCIENCE (including Biology, Chemistry, Physics)
    if subject in ("Science", "Biology", "Chemistry", "Physics"):
        return _classify_science(cid, concept, ctype, tw, year, ks, csl, guidance, description, phys_score)

    # HISTORY
    if subject == "History":
        return _classify_history(cid, concept, ctype, tw, ks, guidance, description, disc_score)

    # GEOGRAPHY
    if subject == "Geography":
        return _classify_geography(cid, concept, ctype, tw, ks, guidance, description, phys_score)

    # COMPUTING
    if subject == "Computing":
        return _result(cid, "DM-AI", "high",
                       "Computing concept — inherently digital subject with strong tool support.",
                       ["DM-AF"], ["TR-DIG", "TR-OBJ", "TR-SPR"], "")

    # LANGUAGES (MFL)
    if subject == "Languages":
        return _classify_languages(cid, concept, ctype, tw, ks, domain_info, guidance, description)

    # ART AND DESIGN
    if subject == "Art and Design":
        return _classify_art(cid, concept, ctype, tw, ks, guidance, description, crea_score)

    # MUSIC
    if subject == "Music":
        return _classify_music(cid, concept, ctype, tw, ks, guidance, description, perf_score)

    # DESIGN AND TECHNOLOGY
    if subject == "Design and Technology":
        return _classify_dt(cid, concept, ctype, tw, ks, guidance, description, phys_score)

    # FOOD PREPARATION AND NUTRITION
    if subject == "Food Preparation and Nutrition":
        if ctype == "knowledge":
            return _result(cid, "DM-AI", "medium",
                           "Food knowledge concept — nutritional science and food safety theory can be delivered digitally.",
                           ["DM-GM"], ["TR-OBJ", "TR-VIS"], "")
        return _result(cid, "DM-ST", "high",
                       "Food practical concept — requires kitchen equipment, safety supervision, and technique demonstration.",
                       [], ["TR-APP", "TR-OBS", "TR-SPK"], "")

    # RELIGIOUS STUDIES
    if subject == "Religious Studies":
        return _classify_re(cid, concept, ctype, tw, ks, guidance, description, disc_score)

    # CITIZENSHIP
    if subject == "Citizenship":
        if disc_score >= 2:
            return _result(cid, "DM-GM", "medium",
                           "Citizenship discussion concept — requires facilitated debate with structured materials.",
                           ["DM-AF"], ["TR-GDI", "TR-NAR"], "")
        return _result(cid, "DM-AI", "medium",
                       "Citizenship knowledge concept — factual civic content deliverable digitally.",
                       ["DM-GM"], ["TR-OBJ", "TR-VIS"], "")

    # BUSINESS / MEDIA STUDIES
    if subject in ("Business", "Media Studies"):
        return _result(cid, "DM-AI", "medium",
                       f"{subject} knowledge concept — factual/analytical content deliverable digitally.",
                       ["DM-GM"], ["TR-OBJ", "TR-VIS"], "")

    # FALLBACK
    if ctype == "skill":
        return _result(cid, "DM-AF", "low",
                       f"Unclassified skill concept in {subject} — defaulting to AI Facilitated.",
                       ["DM-GM"], ["TR-OBS"], "Needs manual review.")
    return _result(cid, "DM-GM", "low",
                   f"Unclassified concept in {subject} — defaulting to Guided Materials.",
                   ["DM-AI"], ["TR-GDI"], "Needs manual review.")


# ---- Subject-specific classifiers ----

def _classify_maths(cid, concept, ctype, tw, year, ks, rs, guidance, description, requirements):
    """Classify a mathematics concept."""
    has_concrete = rs.get("has_concrete", False)
    concrete_resources = rs.get("concrete_resources", [])

    # KS3-KS4 maths: mostly abstract, AI-friendly
    if ks in ("KS3", "KS4"):
        if ctype == "process":
            return _result(cid, "DM-AF", "medium",
                           "Secondary maths process concept — problem-solving benefits from structured AI delivery with facilitator for extended reasoning.",
                           ["DM-AI"], ["TR-OBJ", "TR-DIG", "TR-SPR", "TR-OBS"], "")
        return _result(cid, "DM-AI", "high",
                       "Secondary maths concept — abstract, procedural, and objectively assessable.",
                       ["DM-AF"], ["TR-OBJ", "TR-DIG", "TR-SPR", "TR-VIS"], "")

    # Primary maths with RepresentationStage data
    if has_concrete and concrete_resources and year <= 3:
        return _result(cid, "DM-AF", "high",
                       f"Primary maths (Y{year}) with concrete stage requiring physical manipulatives ({', '.join(concrete_resources[:2])}). AI delivers instruction; facilitator sets up materials.",
                       ["DM-AI"], ["TR-OBJ", "TR-DIG", "TR-SPR", "TR-PHY"],
                       f"Concrete resources: {', '.join(concrete_resources)}")

    if has_concrete and year >= 4:
        # Y4-Y6: concrete less critical, many children at pictorial/abstract
        return _result(cid, "DM-AI", "high",
                       f"Upper primary maths (Y{year}) — most pupils at pictorial/abstract stage. AI can deliver with virtual representations.",
                       ["DM-AF"], ["TR-OBJ", "TR-DIG", "TR-SPR", "TR-VIS"],
                       "Some pupils may still benefit from concrete at entry level.")

    # Primary maths without RS data
    if ctype == "skill":
        if tw <= 3:
            return _result(cid, "DM-AI", "high",
                           f"Primary maths skill (weight {tw}) — procedural, assessable, digital tools available.",
                           ["DM-AF"], ["TR-OBJ", "TR-DIG", "TR-SPR"], "")
        return _result(cid, "DM-AI", "medium",
                       f"Primary maths skill (weight {tw}) — complex but still procedurally assessable.",
                       ["DM-AF"], ["TR-OBJ", "TR-DIG", "TR-SPR"], "")

    if ctype == "knowledge":
        return _result(cid, "DM-AI", "high",
                       "Maths knowledge concept — understanding deliverable through visual representations and structured practice.",
                       ["DM-AF"], ["TR-OBJ", "TR-VIS", "TR-SPR"], "")

    if ctype == "process":
        return _result(cid, "DM-AF", "medium",
                       "Maths process concept — problem-solving/reasoning benefits from facilitator observation.",
                       ["DM-AI"], ["TR-OBJ", "TR-DIG", "TR-OBS"], "")

    # Fallback for maths
    return _result(cid, "DM-AI", "medium",
                   "Mathematics concept — generally amenable to digital delivery.",
                   ["DM-AF"], ["TR-OBJ", "TR-DIG"], "")


def _classify_english(cid, concept, ctype, tw, year, ks, domain_info, guidance, description,
                       disc_score, crea_score, perf_score):
    """Classify an English / English Language / English Literature concept."""
    domain_name = domain_info.get("domain_name", "").lower()

    # Spoken language: specialist teacher
    if "spoken language" in domain_name or "speaking" in domain_name:
        return _result(cid, "DM-ST", "high",
                       "Spoken language concept — requires live dialogue, social interaction, and performance assessment.",
                       ["DM-GM"], ["TR-PER", "TR-GDI", "TR-SPK"], "")

    # Handwriting: AI facilitated (physical skill)
    if "handwriting" in domain_name:
        return _result(cid, "DM-AF", "high",
                       "Handwriting concept — AI provides letter formation models; facilitator observes physical practice.",
                       [], ["TR-OBS", "TR-PHY", "TR-VIS"], "")

    # Grammar, punctuation, spelling: AI direct
    if any(kw in domain_name for kw in ["grammar", "punctuation", "spelling", "transcription"]):
        if "spelling" in domain_name or "transcription" in domain_name:
            return _result(cid, "DM-AI", "high",
                           "Spelling/transcription concept — rule-based, pattern-based, ideal for spaced repetition and adaptive practice.",
                           [], ["TR-OBJ", "TR-SPR", "TR-DIG"], "")
        return _result(cid, "DM-AI", "high",
                       "Grammar/punctuation concept — rule-based with objectively assessable outcomes.",
                       ["DM-AF"], ["TR-OBJ", "TR-SPR", "TR-DIG"], "")

    # Word reading / phonics: AI direct with audio
    if "word reading" in domain_name or "phonics" in domain_name or "reading" in domain_name:
        if ctype == "skill" and disc_score >= 2:
            return _result(cid, "DM-GM", "medium",
                           "Reading inference/discussion skill — benefits from guided discussion with prepared materials.",
                           ["DM-AF"], ["TR-GDI", "TR-NAR", "TR-AUD"], "")
        if "inference" in description.lower() or "evaluate" in description.lower():
            return _result(cid, "DM-GM", "medium",
                           "Reading comprehension (inference/evaluation) — interpretive skill benefits from discussion.",
                           ["DM-AF"], ["TR-GDI", "TR-NAR"], "")
        return _result(cid, "DM-AI", "high",
                       "Reading/word reading concept — decoding and retrieval skills are digitally assessable.",
                       ["DM-AF"], ["TR-OBJ", "TR-AUD", "TR-DIG", "TR-SPR"], "")

    # Composition: guided materials (creative assessment)
    if "composition" in domain_name or "writing" in domain_name:
        if crea_score >= 2:
            return _result(cid, "DM-ST", "medium",
                           "Creative writing concept — quality of creative expression requires expert assessment and modelling.",
                           ["DM-GM"], ["TR-CRA", "TR-MOD", "TR-SPK"], "")
        return _result(cid, "DM-GM", "medium",
                       "Composition concept — writing process benefits from adult modelling and feedback using structured materials.",
                       ["DM-AF"], ["TR-MOD", "TR-NAR", "TR-GDI"],
                       "Planning and editing stages can be AI-supported; drafting and feedback need human interaction.")

    # English Literature KS4: guided materials (text study, critical analysis)
    if ks == "KS4":
        if disc_score >= 2 or "critical" in description.lower() or "analyse" in description.lower():
            return _result(cid, "DM-GM", "medium",
                           "KS4 English critical analysis — literary interpretation benefits from guided discussion.",
                           ["DM-AF"], ["TR-GDI", "TR-NAR", "TR-SPK"], "")
        return _result(cid, "DM-GM", "medium",
                       "KS4 English concept — text-based study benefits from structured materials and discussion.",
                       ["DM-AF"], ["TR-GDI", "TR-NAR"], "")

    # Default English
    if disc_score >= 2:
        return _result(cid, "DM-GM", "medium",
                       "English concept involving discussion — benefits from facilitated dialogue.",
                       ["DM-AF"], ["TR-GDI", "TR-NAR"], "")
    return _result(cid, "DM-AF", "medium",
                   "English concept — AI can support with facilitator guidance at key moments.",
                   ["DM-AI", "DM-GM"], ["TR-DIG", "TR-NAR"], "")


def _classify_science(cid, concept, ctype, tw, year, ks, csl, guidance, description, phys_score):
    """Classify a science concept."""
    enquiry_type = csl.get("enquiry_type", "")

    # Working Scientifically / process concepts with fair_test or observation
    if ctype == "process" or enquiry_type in ("fair_test", "observation"):
        if enquiry_type == "fair_test" or "fair test" in guidance.lower():
            return _result(cid, "DM-AF", "high",
                           "Science fair test concept — requires physical apparatus and variable control, but AI can structure the enquiry sequence.",
                           ["DM-GM"], ["TR-APP", "TR-OBS", "TR-OBJ"],
                           "AI guides the enquiry cycle; facilitator manages equipment and safety.")
        if enquiry_type == "observation" or "observation over time" in guidance.lower():
            return _result(cid, "DM-AF", "medium",
                           "Science observation concept — requires sustained observation of real phenomena with adult support.",
                           ["DM-GM"], ["TR-OBS", "TR-APP"], "")
        # Generic process
        return _result(cid, "DM-AF", "medium",
                       "Science process concept — enquiry methodology benefits from structured AI guidance with facilitator.",
                       ["DM-GM"], ["TR-OBS", "TR-APP"], "")

    # Classifying / secondary research: AI direct
    if enquiry_type in ("classifying", "secondary_research"):
        return _result(cid, "DM-AI", "high",
                       f"Science {enquiry_type} concept — data-driven activity well-suited to digital delivery.",
                       ["DM-AF"], ["TR-OBJ", "TR-DIG", "TR-VIS"], "")

    # Practical-heavy concepts (high physical keyword score)
    if phys_score >= 3:
        return _result(cid, "DM-AF", "medium",
                       "Science concept with significant practical requirements — AI delivers theory, facilitator manages practical.",
                       ["DM-GM"], ["TR-APP", "TR-OBS", "TR-VIS"], "")

    # KS3-KS4 knowledge concepts (Biology, Chemistry, Physics)
    if ks in ("KS3", "KS4") and ctype == "knowledge":
        return _result(cid, "DM-AI", "high",
                       "Secondary science knowledge concept — factual/theoretical content with clear misconceptions to diagnose.",
                       ["DM-AF"], ["TR-OBJ", "TR-VIS", "TR-SPR"], "")

    # General science knowledge
    if ctype == "knowledge":
        return _result(cid, "DM-AI", "high",
                       "Science knowledge concept — factual content deliverable with visual representations and adaptive quizzing.",
                       ["DM-AF"], ["TR-OBJ", "TR-VIS", "TR-SPR"], "")

    # Science skill (data, measurement)
    if ctype == "skill":
        if phys_score >= 2:
            return _result(cid, "DM-AF", "medium",
                           "Science skill involving measurement/practical work — AI structures, facilitator supervises.",
                           ["DM-GM"], ["TR-OBS", "TR-APP", "TR-DIG"], "")
        return _result(cid, "DM-AI", "medium",
                       "Science data/analysis skill — graph interpretation and data handling are digitally deliverable.",
                       ["DM-AF"], ["TR-OBJ", "TR-DIG", "TR-VIS"], "")

    # Default science
    return _result(cid, "DM-AI", "medium",
                   "Science concept — generally amenable to AI delivery with visual support.",
                   ["DM-AF"], ["TR-OBJ", "TR-VIS"], "")


def _classify_history(cid, concept, ctype, tw, ks, guidance, description, disc_score):
    """Classify a history concept."""
    desc_lower = description.lower()

    # Source analysis, interpretation, perspective
    if any(kw in desc_lower for kw in ["source", "interpret", "perspective", "empathy", "significance"]):
        return _result(cid, "DM-GM", "high",
                       "History interpretive concept — source analysis and perspective-taking require curated materials and facilitated discussion.",
                       ["DM-AF"], ["TR-GDI", "TR-NAR", "TR-MOD"], "")

    # Historical enquiry skills
    if ctype == "skill":
        if disc_score >= 2:
            return _result(cid, "DM-GM", "medium",
                           "History skill requiring discussion — disciplinary thinking benefits from facilitated enquiry.",
                           ["DM-AF"], ["TR-GDI", "TR-NAR"], "")
        return _result(cid, "DM-AF", "medium",
                       "History skill — chronological/evidential thinking can be structured digitally with facilitation.",
                       ["DM-AI"], ["TR-DIG", "TR-NAR", "TR-OBJ"], "")

    # Substantive knowledge (dates, events, civilisations)
    if ctype == "knowledge":
        return _result(cid, "DM-AI", "high",
                       "History knowledge concept — factual content about periods, events, and civilisations deliverable digitally.",
                       ["DM-AF", "DM-GM"], ["TR-OBJ", "TR-VIS", "TR-NAR"], "")

    # Default history
    return _result(cid, "DM-GM", "medium",
                   "History concept — benefits from narrative materials and discussion.",
                   ["DM-AF"], ["TR-GDI", "TR-NAR"], "")


def _classify_geography(cid, concept, ctype, tw, ks, guidance, description, phys_score):
    """Classify a geography concept."""
    desc_lower = description.lower()

    # Fieldwork
    if "fieldwork" in desc_lower or "field" in guidance.lower():
        return _result(cid, "DM-ST", "high",
                       "Geography fieldwork concept — requires real-world data collection, outdoor safety supervision, and specialist planning.",
                       ["DM-GM"], ["TR-APP", "TR-OBS", "TR-SPK"], "")

    # Map skills: highly digital
    if any(kw in desc_lower for kw in ["map", "grid reference", "ordnance survey", "atlas", "globe"]):
        return _result(cid, "DM-AI", "high",
                       "Geography map/spatial skill — digital mapping tools and interactive exercises are highly effective.",
                       ["DM-AF"], ["TR-DIG", "TR-VIS", "TR-OBJ"], "")

    # Locational / place knowledge
    if ctype == "knowledge":
        return _result(cid, "DM-AI", "high",
                       "Geography knowledge concept — locational, place, and process knowledge deliverable with visual resources.",
                       ["DM-AF"], ["TR-OBJ", "TR-VIS", "TR-DIG"], "")

    # Geographical skills (non-fieldwork)
    if ctype == "skill":
        return _result(cid, "DM-AF", "medium",
                       "Geography skill — data interpretation and enquiry can be AI-structured with facilitator support.",
                       ["DM-AI"], ["TR-DIG", "TR-VIS", "TR-OBJ"], "")

    return _result(cid, "DM-AI", "medium",
                   "Geography concept — generally amenable to visual/interactive digital delivery.",
                   ["DM-AF"], ["TR-OBJ", "TR-VIS"], "")


def _classify_languages(cid, concept, ctype, tw, ks, domain_info, guidance, description):
    """Classify a Languages (MFL) concept."""
    domain_name = domain_info.get("domain_name", "").lower()

    if "speaking" in domain_name or "spoken" in description.lower():
        return _result(cid, "DM-AF", "high",
                       "Languages speaking concept — AI provides prompts and models; facilitator or speech recognition supports oral practice.",
                       ["DM-GM"], ["TR-AUD", "TR-OBS", "TR-DIG"], "")

    if "listening" in domain_name:
        return _result(cid, "DM-AI", "high",
                       "Languages listening concept — audio-based exercises are ideal for AI delivery.",
                       ["DM-AF"], ["TR-AUD", "TR-OBJ", "TR-DIG"], "")

    if "reading" in domain_name:
        return _result(cid, "DM-AI", "high",
                       "Languages reading concept — text comprehension exercises deliverable digitally.",
                       ["DM-AF"], ["TR-OBJ", "TR-DIG", "TR-VIS"], "")

    if "writing" in domain_name:
        return _result(cid, "DM-AF", "medium",
                       "Languages writing concept — structured writing exercises with some human feedback for extended responses.",
                       ["DM-AI"], ["TR-OBJ", "TR-DIG", "TR-OBS"], "")

    if "grammar" in domain_name or "grammar" in description.lower():
        return _result(cid, "DM-AI", "high",
                       "Languages grammar concept — rule-based and objectively assessable.",
                       [], ["TR-OBJ", "TR-SPR", "TR-DIG"], "")

    return _result(cid, "DM-AF", "medium",
                   "Languages concept — generally AI-deliverable with some facilitator support for oral components.",
                   ["DM-AI"], ["TR-AUD", "TR-DIG", "TR-OBJ"], "")


def _classify_art(cid, concept, ctype, tw, ks, guidance, description, crea_score):
    """Classify an Art and Design concept."""
    desc_lower = description.lower()

    # Art history / artist knowledge: AI direct
    if any(kw in desc_lower for kw in ["artist", "architect", "designer", "art history", "movement"]):
        return _result(cid, "DM-AI", "high",
                       "Art history/knowledge concept — factual content about artists, movements, and techniques deliverable digitally with visual resources.",
                       ["DM-AF"], ["TR-VIS", "TR-OBJ", "TR-AUD"], "")

    # Making skills (drawing, painting, sculpture, printmaking)
    if any(kw in desc_lower for kw in ["drawing", "painting", "sculpture", "print", "textiles", "collage"]):
        return _result(cid, "DM-ST", "high",
                       "Art making skill — physical technique, material handling, and creative assessment require specialist teacher.",
                       ["DM-GM"], ["TR-CRA", "TR-PHY", "TR-PER", "TR-SPK"],
                       "AI can support art appreciation and analysis; physical making needs expert demonstration and assessment.")

    # Sketchbook / creative process
    if "sketchbook" in desc_lower or "creative" in desc_lower:
        return _result(cid, "DM-GM", "medium",
                       "Art creative process concept — structured materials can guide sketchbook work and creative exploration.",
                       ["DM-ST"], ["TR-PHY", "TR-CRA", "TR-MOD"], "")

    # Default art: specialist
    return _result(cid, "DM-ST", "medium",
                   "Art concept — generally requires physical materials and creative assessment.",
                   ["DM-GM"], ["TR-CRA", "TR-PHY"], "")


def _classify_music(cid, concept, ctype, tw, ks, guidance, description, perf_score):
    """Classify a music concept."""
    desc_lower = description.lower()

    # Music theory, notation, history: AI direct with audio
    if any(kw in desc_lower for kw in ["notation", "theory", "history", "inter-related dimensions",
                                        "tempo", "dynamics", "structure", "texture"]):
        return _result(cid, "DM-AI", "high",
                       "Music theory/knowledge concept — notation, theory, and music history deliverable with audio tools and visual representations.",
                       ["DM-AF"], ["TR-AUD", "TR-VIS", "TR-OBJ", "TR-DIG"],
                       "Computer can synthesise and play back musical examples; interactive notation exercises are effective.")

    # Listening and appraising: AI direct
    if "listen" in desc_lower or "apprais" in desc_lower:
        return _result(cid, "DM-AI", "high",
                       "Music listening/appraising concept — audio playback, guided listening, and structured analysis are ideal for AI delivery.",
                       ["DM-AF"], ["TR-AUD", "TR-OBJ", "TR-VIS"], "")

    # Composition: AI facilitated (digital composition tools exist)
    if "compos" in desc_lower:
        return _result(cid, "DM-AF", "high",
                       "Music composition concept — digital composition tools (GarageBand, Chrome Music Lab) enable AI-guided creation; facilitator supports creative feedback.",
                       ["DM-GM"], ["TR-AUD", "TR-DIG", "TR-CRA"],
                       "Computer can synthesise, play back, and suggest; creative quality assessment benefits from human ear.")

    # Performance, ensemble, improvisation: specialist teacher
    if perf_score >= 1 or any(kw in desc_lower for kw in ["perform", "sing", "instrument", "ensemble",
                                                            "improvise", "play"]):
        return _result(cid, "DM-ST", "high",
                       "Music performance concept — instrumental technique, vocal coaching, and ensemble coordination require specialist teacher.",
                       ["DM-GM"], ["TR-PER", "TR-APP", "TR-SPK"],
                       "Computer cannot replace the feedback loop of hearing a child play and correcting posture, breath, or fingering in real-time.")

    # Default music
    return _result(cid, "DM-AF", "medium",
                   "Music concept — generally benefits from both digital audio tools and human musical guidance.",
                   ["DM-AI", "DM-GM"], ["TR-AUD", "TR-DIG"], "")


def _classify_dt(cid, concept, ctype, tw, ks, guidance, description, phys_score):
    """Classify a Design and Technology concept."""
    desc_lower = description.lower()

    # Cooking / food
    if any(kw in desc_lower for kw in ["cooking", "food", "nutrition", "recipe", "ingredient"]):
        if ctype == "knowledge":
            return _result(cid, "DM-AI", "medium",
                           "DT food knowledge — nutritional science and food safety theory deliverable digitally.",
                           ["DM-GM"], ["TR-OBJ", "TR-VIS"], "")
        return _result(cid, "DM-ST", "high",
                       "DT cooking/food practical — kitchen safety, technique demonstration, and equipment supervision require specialist.",
                       [], ["TR-APP", "TR-OBS", "TR-SPK", "TR-PER"], "")

    # Material knowledge, mechanisms theory, CAD
    if any(kw in desc_lower for kw in ["material properties", "mechanisms", "structures", "cad",
                                        "electronics theory", "system"]):
        return _result(cid, "DM-AI", "medium",
                       "DT knowledge concept — material science, mechanisms theory, and systems knowledge deliverable digitally.",
                       ["DM-AF"], ["TR-OBJ", "TR-VIS", "TR-DIG"], "")

    # Design process
    if any(kw in desc_lower for kw in ["design", "evaluate", "iterative", "user needs", "criteria"]):
        return _result(cid, "DM-GM", "medium",
                       "DT design process concept — structured design briefs and evaluation frameworks guide non-specialist adults.",
                       ["DM-AF"], ["TR-NAR", "TR-MOD", "TR-GDI"], "")

    # Making skills
    if any(kw in desc_lower for kw in ["making", "construct", "assemble", "cut", "join", "finish",
                                        "tool", "technique"]):
        return _result(cid, "DM-ST", "high",
                       "DT making skill — physical tools, material handling, and safety require specialist supervision and technique demonstration.",
                       ["DM-GM"], ["TR-APP", "TR-OBS", "TR-PER", "TR-SPK"], "")

    # Default DT
    if phys_score >= 2:
        return _result(cid, "DM-ST", "medium",
                       "DT concept with practical requirements — defaulting to specialist for safety and technique.",
                       ["DM-GM"], ["TR-APP", "TR-OBS"], "")
    return _result(cid, "DM-GM", "medium",
                   "DT concept — benefits from structured materials and guided making.",
                   ["DM-AF"], ["TR-NAR", "TR-MOD"], "")


def _classify_re(cid, concept, ctype, tw, ks, guidance, description, disc_score):
    """Classify a Religious Studies concept."""
    desc_lower = description.lower()

    # Sensitive / pastoral topics
    if any(kw in desc_lower for kw in ["death", "afterlife", "suffering", "evil", "abortion",
                                        "euthanasia", "war", "persecution"]):
        return _result(cid, "DM-ST", "high",
                       "RE sensitive topic — pastoral awareness and skilled facilitation required for topics touching on suffering, death, or moral controversy.",
                       ["DM-GM"], ["TR-PAS", "TR-GDI", "TR-SPK"], "")

    # Ethical reasoning / discussion
    if disc_score >= 2 or any(kw in desc_lower for kw in ["ethical", "moral", "debate", "argument"]):
        return _result(cid, "DM-GM", "medium",
                       "RE ethical reasoning concept — structured discussion materials enable facilitated moral reasoning.",
                       ["DM-AF"], ["TR-GDI", "TR-NAR"], "")

    # Knowledge of beliefs, practices, teachings
    return _result(cid, "DM-AI", "high",
                   "RE knowledge concept — factual content about beliefs, practices, and sacred texts deliverable digitally.",
                   ["DM-GM"], ["TR-OBJ", "TR-VIS", "TR-NAR"], "")


# ---- Helpers ----

def _result(concept_id, primary_mode, confidence, rationale, alternative_modes, teaching_requirements, notes):
    """Create a classification result dict."""
    return {
        "concept_id": concept_id,
        "primary_mode": {v: k for k, v in MODES.items()}[primary_mode],
        "primary_mode_id": primary_mode,
        "confidence": confidence,
        "rationale": rationale,
        "alternative_modes": [
            {v: k for k, v in MODES.items()}.get(m, m) for m in alternative_modes
        ],
        "teaching_requirements": teaching_requirements,
        "notes": notes,
    }


def process_extraction_file(filepath, rs_data, csl_data):
    """Process one extraction JSON file and return classifications."""
    with open(filepath) as f:
        data = json.load(f)

    metadata = data["metadata"]
    concepts = data.get("concepts", [])
    domains = {d["domain_id"]: d for d in data.get("domains", [])}

    results = []
    for concept in concepts:
        domain_id = concept.get("domain_id", "")
        domain_info = domains.get(domain_id, {})
        result = classify_concept(concept, domain_info, metadata, rs_data, csl_data)
        results.append(result)

    return results


def main():
    parser = argparse.ArgumentParser(description="Classify concepts by delivery mode")
    parser.add_argument("--dry-run", action="store_true", help="Print stats without writing files")
    args = parser.parse_args()

    print("=" * 60)
    print("Delivery Mode Classification")
    print("=" * 60)

    # Load supplementary data
    print("\nLoading supplementary data...")
    rs_data = load_representation_stages()
    print(f"  RepresentationStage data for {len(rs_data)} concepts")
    csl_data = load_concept_skill_links()
    print(f"  Concept-skill links for {len(csl_data)} concepts")

    # Process all extraction files
    all_results = {}  # filename_stem -> [results]
    stats = Counter()
    mode_by_subject = defaultdict(Counter)

    extraction_dirs = [
        ("Primary", PRIMARY_DIR),
        ("Secondary", SECONDARY_DIR),
        ("EYFS", EYFS_DIR),
    ]

    total_concepts = 0
    for label, dirpath in extraction_dirs:
        if not dirpath.exists():
            print(f"\n  WARN: {dirpath} not found — skipping")
            continue
        print(f"\nProcessing {label} extractions...")
        for filepath in sorted(dirpath.glob("*.json")):
            results = process_extraction_file(filepath, rs_data, csl_data)
            if results:
                stem = filepath.stem.replace("_extracted", "")
                all_results[stem] = results
                total_concepts += len(results)

                # Gather stats
                with open(filepath) as f:
                    meta = json.load(f)["metadata"]
                subject = meta.get("subject", "Unknown")

                for r in results:
                    mode = r["primary_mode"]
                    stats[mode] += 1
                    mode_by_subject[subject][mode] += 1
                    for tr in r["teaching_requirements"]:
                        stats[f"TR:{tr}"] += 1

                print(f"  {filepath.name}: {len(results)} concepts classified")

    # Print summary
    print("\n" + "=" * 60)
    print("CLASSIFICATION SUMMARY")
    print("=" * 60)
    print(f"\nTotal concepts classified: {total_concepts}")
    print(f"\nDelivery mode distribution:")
    for mode_name, mode_id in MODES.items():
        count = stats.get(mode_name, 0)
        pct = (count / total_concepts * 100) if total_concepts else 0
        print(f"  {mode_name:<25} {count:>5}  ({pct:.1f}%)")

    print(f"\nPlatform addressable (AI Direct + AI Facilitated):")
    ai_total = stats.get("ai_direct", 0) + stats.get("ai_facilitated", 0)
    pct = (ai_total / total_concepts * 100) if total_concepts else 0
    print(f"  {ai_total} concepts ({pct:.1f}%)")

    print(f"\nBreakdown by subject:")
    for subject in sorted(mode_by_subject.keys()):
        subject_total = sum(mode_by_subject[subject].values())
        ai_count = mode_by_subject[subject].get("ai_direct", 0) + mode_by_subject[subject].get("ai_facilitated", 0)
        print(f"  {subject:<30} Total: {subject_total:>4}  AI-reachable: {ai_count:>4} ({ai_count/subject_total*100:.0f}%)")
        for mode_name in MODES:
            count = mode_by_subject[subject].get(mode_name, 0)
            if count:
                print(f"    {mode_name:<23} {count:>4}")

    print(f"\nTeaching requirements distribution:")
    for key in sorted(stats.keys()):
        if key.startswith("TR:"):
            print(f"  {key:<10} {stats[key]:>5}")

    # Write output files
    if not args.dry_run:
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        files_written = 0
        for stem, results in sorted(all_results.items()):
            outpath = OUTPUT_DIR / f"{stem}.json"
            with open(outpath, "w") as f:
                json.dump(results, f, indent=2)
            files_written += 1

        print(f"\n  Wrote {files_written} files to {OUTPUT_DIR}")
    else:
        print("\n  [DRY RUN] No files written.")

    print("\nDone.")


if __name__ == "__main__":
    main()

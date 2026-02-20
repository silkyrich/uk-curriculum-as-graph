#!/usr/bin/env python3
"""
Import learner profile layer.

Creates:
  :InteractionType nodes  — 29 named UI/pedagogical patterns
  :ContentGuideline nodes — per year group (reading level, TTS, vocabulary)
  :PedagogyProfile nodes  — per year group (session length, hints, PF, difficulties)
  :FeedbackProfile nodes  — per year group (tone, gamification safety, metacognition)

Relationships:
  (Year)-[:SUPPORTS_INTERACTION {primary: bool}]->(InteractionType)
  (Year)-[:HAS_CONTENT_GUIDELINE]->(ContentGuideline)
  (Year)-[:HAS_PEDAGOGY_PROFILE]->(PedagogyProfile)
  (Year)-[:HAS_FEEDBACK_PROFILE]->(FeedbackProfile)

Usage:
  python3 layers/learner-profiles/scripts/import_learner_profiles.py

Requires NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD environment variables
(or the neo4j_config.py defaults).
"""

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(PROJECT_ROOT / "core" / "scripts"))

from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD
from neo4j import GraphDatabase

EXTRACTIONS = Path(__file__).resolve().parents[1] / "extractions"

DISPLAY_COLOR = "#7C3AED"   # purple — distinct from UK curriculum and CASE layers
DISPLAY_ICON = "ECB5C9"


def load_json(filename):
    with open(EXTRACTIONS / filename) as f:
        return json.load(f)


class LearnerProfileImporter:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def run(self):
        stats = {
            "interaction_types": 0,
            "content_guidelines": 0,
            "pedagogy_profiles": 0,
            "feedback_profiles": 0,
            "year_interaction_rels": 0,
            "year_profile_rels": 0,
        }

        interaction_types = load_json("interaction_types.json")
        content_guidelines = load_json("content_guidelines.json")
        pedagogy_profiles = load_json("pedagogy_profiles.json")
        feedback_profiles = load_json("feedback_profiles.json")
        year_interactions = load_json("year_interactions.json")

        with self.driver.session() as session:
            # --- InteractionType nodes ---
            for it in interaction_types:
                session.execute_write(self._merge_interaction_type, it)
                stats["interaction_types"] += 1

            # --- ContentGuideline nodes ---
            for cg in content_guidelines:
                session.execute_write(self._merge_content_guideline, cg)
                stats["content_guidelines"] += 1

            # --- PedagogyProfile nodes ---
            for pp in pedagogy_profiles:
                session.execute_write(self._merge_pedagogy_profile, pp)
                stats["pedagogy_profiles"] += 1

            # --- FeedbackProfile nodes ---
            for fp in feedback_profiles:
                session.execute_write(self._merge_feedback_profile, fp)
                stats["feedback_profiles"] += 1

            # --- Year → InteractionType relationships ---
            for mapping in year_interactions["mappings"]:
                year_code = mapping["year_code"]
                for interaction_id in mapping.get("primary", []):
                    session.execute_write(
                        self._merge_year_interaction_rel,
                        year_code, interaction_id, True
                    )
                    stats["year_interaction_rels"] += 1
                for interaction_id in mapping.get("secondary", []):
                    session.execute_write(
                        self._merge_year_interaction_rel,
                        year_code, interaction_id, False
                    )
                    stats["year_interaction_rels"] += 1

            # --- Year → ContentGuideline/PedagogyProfile/FeedbackProfile ---
            year_codes = [m["year_code"] for m in year_interactions["mappings"]]
            for year_code in year_codes:
                session.execute_write(self._merge_profile_rels, year_code)
                stats["year_profile_rels"] += 3

        return stats

    @staticmethod
    def _merge_interaction_type(tx, it):
        # Store list properties as JSON strings for portability
        subject_affinity = json.dumps(it.get("subject_affinity", []))
        tx.run(
            """
            MERGE (n:InteractionType {interaction_id: $interaction_id})
            SET n.name = $name,
                n.category = $category,
                n.description = $description,
                n.input_method = $input_method,
                n.visual_complexity = $visual_complexity,
                n.requires_literacy = $requires_literacy,
                n.requires_numeracy = $requires_numeracy,
                n.subject_affinity = $subject_affinity,
                n.ui_notes = $ui_notes,
                n.agent_prompt = $agent_prompt,
                n.display_category = 'Learner Profile',
                n.display_color = '#7C3AED',
                n.display_icon = 'lightbulb',
                n.name = $name
            """,
            interaction_id=it["interaction_id"],
            name=it["name"],
            category=it.get("category", ""),
            description=it.get("description", ""),
            input_method=it.get("input_method", ""),
            visual_complexity=it.get("visual_complexity", 1),
            requires_literacy=it.get("requires_literacy", False),
            requires_numeracy=it.get("requires_numeracy", False),
            subject_affinity=subject_affinity,
            ui_notes=it.get("ui_notes", ""),
            agent_prompt=it.get("agent_prompt", ""),
        )

    @staticmethod
    def _merge_content_guideline(tx, cg):
        tense_range = json.dumps(cg.get("tense_range", []))
        tx.run(
            """
            MERGE (n:ContentGuideline {year_code: $year_code})
            SET n.label = $label,
                n.reading_level_description = $reading_level_description,
                n.lexile_min = $lexile_min,
                n.lexile_max = $lexile_max,
                n.flesch_kincaid_grade_max = $flesch_kincaid_grade_max,
                n.max_sentence_length_words = $max_sentence_length_words,
                n.avg_sentence_length_words = $avg_sentence_length_words,
                n.vocabulary_level = $vocabulary_level,
                n.vocabulary_notes = $vocabulary_notes,
                n.academic_vocabulary_ok = $academic_vocabulary_ok,
                n.tts_required = $tts_required,
                n.tts_available = $tts_available,
                n.tts_notes = $tts_notes,
                n.complex_clauses_max = $complex_clauses_max,
                n.tense_range = $tense_range,
                n.sentence_structure = $sentence_structure,
                n.number_range = $number_range,
                n.agent_content_prompt = $agent_content_prompt,
                n.display_category = 'Learner Profile',
                n.display_color = '#7C3AED',
                n.display_icon = 'document',
                n.name = $label
            """,
            year_code=cg["year_code"],
            label=cg.get("label", cg["year_code"]),
            reading_level_description=cg.get("reading_level_description", ""),
            lexile_min=cg.get("lexile_min"),
            lexile_max=cg.get("lexile_max"),
            flesch_kincaid_grade_max=cg.get("flesch_kincaid_grade_max"),
            max_sentence_length_words=cg.get("max_sentence_length_words"),
            avg_sentence_length_words=cg.get("avg_sentence_length_words"),
            vocabulary_level=cg.get("vocabulary_level", ""),
            vocabulary_notes=cg.get("vocabulary_notes", ""),
            academic_vocabulary_ok=cg.get("academic_vocabulary_ok", False),
            tts_required=cg.get("tts_required", False),
            tts_available=cg.get("tts_available", True),
            tts_notes=cg.get("tts_notes", ""),
            complex_clauses_max=cg.get("complex_clauses_max"),
            tense_range=tense_range,
            sentence_structure=cg.get("sentence_structure", ""),
            number_range=cg.get("number_range", ""),
            agent_content_prompt=cg.get("agent_content_prompt", ""),
        )

    @staticmethod
    def _merge_pedagogy_profile(tx, pp):
        desirable_difficulties = json.dumps(pp.get("desirable_difficulties", []))
        session_sequence = json.dumps(pp.get("session_sequence", []))
        tx.run(
            """
            MERGE (n:PedagogyProfile {year_code: $year_code})
            SET n.session_length_min_minutes = $session_length_min_minutes,
                n.session_length_max_minutes = $session_length_max_minutes,
                n.activities_per_session = $activities_per_session,
                n.hint_tiers_max = $hint_tiers_max,
                n.hint_tier_notes = $hint_tier_notes,
                n.productive_failure_appropriate = $productive_failure_appropriate,
                n.productive_failure_notes = $productive_failure_notes,
                n.worked_examples_required = $worked_examples_required,
                n.worked_example_style = $worked_example_style,
                n.scaffolding_level = $scaffolding_level,
                n.prerequisite_gating_required = $prerequisite_gating_required,
                n.metacognitive_prompts = $metacognitive_prompts,
                n.desirable_difficulties = $desirable_difficulties,
                n.session_sequence = $session_sequence,
                n.mastery_threshold_correct_in_window = $mastery_threshold,
                n.mastery_window_days = $mastery_window_days,
                n.mastery_success_rate_percent = $mastery_success_rate_percent,
                n.interleaving_appropriate = $interleaving_appropriate,
                n.spacing_appropriate = $spacing_appropriate,
                n.spacing_interval_days_min = $spacing_interval_min,
                n.spacing_interval_days_max = $spacing_interval_max,
                n.agent_pedagogy_prompt = $agent_pedagogy_prompt,
                n.display_category = 'Learner Profile',
                n.display_color = '#7C3AED',
                n.display_icon = 'route',
                n.name = $year_code + ' Pedagogy'
            """,
            year_code=pp["year_code"],
            session_length_min_minutes=pp.get("session_length_min_minutes"),
            session_length_max_minutes=pp.get("session_length_max_minutes"),
            activities_per_session=pp.get("activities_per_session"),
            hint_tiers_max=pp.get("hint_tiers_max"),
            hint_tier_notes=pp.get("hint_tier_notes", ""),
            productive_failure_appropriate=pp.get("productive_failure_appropriate", False),
            productive_failure_notes=pp.get("productive_failure_notes", ""),
            worked_examples_required=pp.get("worked_examples_required", True),
            worked_example_style=pp.get("worked_example_style", ""),
            scaffolding_level=pp.get("scaffolding_level", "moderate"),
            prerequisite_gating_required=pp.get("prerequisite_gating_required", True),
            metacognitive_prompts=pp.get("metacognitive_prompts", False),
            desirable_difficulties=desirable_difficulties,
            session_sequence=session_sequence,
            mastery_threshold=pp.get("mastery_threshold_correct_in_window", 5),
            mastery_window_days=pp.get("mastery_window_days", 7),
            mastery_success_rate_percent=pp.get("mastery_success_rate_percent", 80),
            interleaving_appropriate=pp.get("interleaving_appropriate", False),
            spacing_appropriate=pp.get("spacing_appropriate", True),
            spacing_interval_min=pp.get("spacing_interval_days_min"),
            spacing_interval_max=pp.get("spacing_interval_days_max"),
            agent_pedagogy_prompt=pp.get("agent_pedagogy_prompt", ""),
        )

    @staticmethod
    def _merge_feedback_profile(tx, fp):
        metacognitive_examples = json.dumps(fp.get("metacognitive_examples", []))
        avoid_phrases = json.dumps(fp.get("avoid_phrases", []))
        tx.run(
            """
            MERGE (n:FeedbackProfile {year_code: $year_code})
            SET n.feedback_style = $feedback_style,
                n.ai_tone = $ai_tone,
                n.ai_voice_style = $ai_voice_style,
                n.gamification_safe = $gamification_safe,
                n.progress_bars_safe = $progress_bars_safe,
                n.leaderboards_safe = $leaderboards_safe,
                n.badge_systems_safe = $badge_systems_safe,
                n.visible_streaks_safe = $visible_streaks_safe,
                n.expected_reward_safe = $expected_reward_safe,
                n.unexpected_delight_safe = $unexpected_delight_safe,
                n.delight_frequency = $delight_frequency,
                n.delight_notes = $delight_notes,
                n.comparative_feedback_safe = $comparative_feedback_safe,
                n.counter_misconceptions_explicit = $counter_misconceptions_explicit,
                n.metacognitive_reflection = $metacognitive_reflection,
                n.metacognitive_examples = $metacognitive_examples,
                n.normalize_struggle = $normalize_struggle,
                n.positive_error_framing = $positive_error_framing,
                n.post_error_style = $post_error_style,
                n.immediate_feedback = $immediate_feedback,
                n.feedback_example_correct = $feedback_example_correct,
                n.feedback_example_incorrect = $feedback_example_incorrect,
                n.avoid_phrases = $avoid_phrases,
                n.agent_feedback_prompt = $agent_feedback_prompt,
                n.display_category = 'Learner Profile',
                n.display_color = '#7C3AED',
                n.display_icon = 'speech',
                n.name = $year_code + ' Feedback'
            """,
            year_code=fp["year_code"],
            feedback_style=fp.get("feedback_style", ""),
            ai_tone=fp.get("ai_tone", ""),
            ai_voice_style=fp.get("ai_voice_style", ""),
            gamification_safe=fp.get("gamification_safe", False),
            progress_bars_safe=fp.get("progress_bars_safe", False),
            leaderboards_safe=fp.get("leaderboards_safe", False),
            badge_systems_safe=fp.get("badge_systems_safe", False),
            visible_streaks_safe=fp.get("visible_streaks_safe", False),
            expected_reward_safe=fp.get("expected_reward_safe", False),
            unexpected_delight_safe=fp.get("unexpected_delight_safe", True),
            delight_frequency=fp.get("delight_frequency", "semi_random"),
            delight_notes=fp.get("delight_notes", ""),
            comparative_feedback_safe=fp.get("comparative_feedback_safe", False),
            counter_misconceptions_explicit=fp.get("counter_misconceptions_explicit", False),
            metacognitive_reflection=fp.get("metacognitive_reflection", False),
            metacognitive_examples=metacognitive_examples,
            normalize_struggle=fp.get("normalize_struggle", True),
            positive_error_framing=fp.get("positive_error_framing", True),
            post_error_style=fp.get("post_error_style", ""),
            immediate_feedback=fp.get("immediate_feedback", True),
            feedback_example_correct=fp.get("feedback_example_correct", ""),
            feedback_example_incorrect=fp.get("feedback_example_incorrect", ""),
            avoid_phrases=avoid_phrases,
            agent_feedback_prompt=fp.get("agent_feedback_prompt", ""),
        )

    @staticmethod
    def _merge_year_interaction_rel(tx, year_code, interaction_id, primary):
        tx.run(
            """
            MATCH (y:Year {year_id: $year_code})
            MATCH (i:InteractionType {interaction_id: $interaction_id})
            MERGE (y)-[r:SUPPORTS_INTERACTION]->(i)
            SET r.primary = $primary
            """,
            year_code=year_code,
            interaction_id=interaction_id,
            primary=primary,
        )

    @staticmethod
    def _merge_profile_rels(tx, year_code):
        tx.run(
            """
            MATCH (y:Year {year_id: $year_code})
            MATCH (cg:ContentGuideline {year_code: $year_code})
            MERGE (y)-[:HAS_CONTENT_GUIDELINE]->(cg)
            """,
            year_code=year_code,
        )
        tx.run(
            """
            MATCH (y:Year {year_id: $year_code})
            MATCH (pp:PedagogyProfile {year_code: $year_code})
            MERGE (y)-[:HAS_PEDAGOGY_PROFILE]->(pp)
            """,
            year_code=year_code,
        )
        tx.run(
            """
            MATCH (y:Year {year_id: $year_code})
            MATCH (fp:FeedbackProfile {year_code: $year_code})
            MERGE (y)-[:HAS_FEEDBACK_PROFILE]->(fp)
            """,
            year_code=year_code,
        )


def main():
    print("=" * 60)
    print("IMPORTING LEARNER PROFILES LAYER")
    print("=" * 60)
    print(f"  URI: {NEO4J_URI}")

    importer = LearnerProfileImporter(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD)
    try:
        stats = importer.run()
    finally:
        importer.close()

    print()
    print("Results:")
    for key, count in stats.items():
        print(f"  {key}: {count}")
    print()

    total_nodes = (
        stats["interaction_types"]
        + stats["content_guidelines"]
        + stats["pedagogy_profiles"]
        + stats["feedback_profiles"]
    )
    print(f"  Total nodes created/updated: {total_nodes}")
    print(f"  Total relationships created/updated: {stats['year_interaction_rels'] + stats['year_profile_rels']}")
    print()
    print("Done.")


if __name__ == "__main__":
    main()

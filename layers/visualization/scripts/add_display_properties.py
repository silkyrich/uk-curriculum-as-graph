#!/usr/bin/env python3
"""
Add display properties (color, icon, category, size) to all nodes for visualization.

These properties are stored IN the graph and travel with the data:
- display_color: Hex color code (e.g., '#3B82F6')
- display_icon: Material Design icon name (e.g., 'lightbulb_outline')
- display_category: High-level category (e.g., 'UK Curriculum', 'CASE Standards')
- display_size: Relative size 1-5 (5=root, 4=structural, 3=grouping, 2=content, 1=leaf)

This enables:
1. Version-controlled styling (committed to git)
2. Portable across Neo4j instances
3. Usable in Bloom, custom visualizations, exports
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent / "core" / "scripts"))
from neo4j import GraphDatabase
from neo4j_config import NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

LAYER_ROOT = Path(__file__).parent.parent

# Color scheme designed for educational graph visualization
# Blues/Purples: UK Curriculum (authority, knowledge)
# Teals/Greens: Epistemic Skills (thinking, process)
# Oranges/Browns: CASE Standards (comparison, external)
# Grays: Assessment (neutral, measurement)

NODE_STYLES = {
    # UK CURRICULUM LAYER (Blues & Purples)
    # size scale: 5=top structural, 4=mid structural, 3=grouping, 2=content, 1=detail/leaf
    'Curriculum': {
        'color': '#1F2937',  # Gray-800
        'icon': 'account_balance',
        'category': 'Structure',
        'size': 5,
    },
    'KeyStage': {
        'color': '#374151',  # Gray-700
        'icon': 'stairs',
        'category': 'Structure',
        'size': 5,
    },
    'Year': {
        'color': '#4B5563',  # Gray-600
        'icon': 'event',
        'category': 'Structure',
        'size': 4,
    },
    'Subject': {
        'color': '#DC2626',  # Red-600
        'icon': 'menu_book',
        'category': 'UK Curriculum',
        'size': 4,
    },
    'Programme': {
        'color': '#1E3A8A',  # Blue-900 (darker, foundational)
        'icon': 'assignment',
        'category': 'UK Curriculum',
        'size': 4,
    },
    'Domain': {
        'color': '#8B5CF6',  # Violet-500
        'icon': 'folder',
        'category': 'UK Curriculum',
        'size': 3,
    },
    'Topic': {
        'color': '#7C3AED',  # Violet-600
        'icon': 'history_edu',
        'category': 'UK Curriculum',
        'size': 3,
    },
    'Objective': {
        'color': '#10B981',  # Emerald-500
        'icon': 'flag',
        'category': 'UK Curriculum',
        'size': 2,
    },
    'Concept': {
        'color': '#3B82F6',  # Blue-500
        'icon': 'lightbulb_outline',
        'category': 'UK Curriculum',
        'size': 2,
    },
    'ConceptCluster': {
        'color': '#6366F1',  # Indigo-500
        'icon': 'view_module',
        'category': 'UK Curriculum',
        'size': 2,
    },
    'SourceDocument': {
        'color': '#6B7280',  # Gray-500
        'icon': 'description',
        'category': 'Structure',
        'size': 1,
    },

    # EPISTEMIC SKILLS LAYER (Teals & Greens)
    'WorkingScientifically': {
        'color': '#14B8A6',  # Teal-500
        'icon': 'science',
        'category': 'Epistemic Skills',
        'size': 2,
    },
    'ReadingSkill': {
        'color': '#EC4899',  # Pink-500
        'icon': 'menu_book',
        'category': 'Epistemic Skills',
        'size': 2,
    },
    'MathematicalReasoning': {
        'color': '#F59E0B',  # Amber-500
        'icon': 'calculate',
        'category': 'Epistemic Skills',
        'size': 2,
    },
    'GeographicalSkill': {
        'color': '#059669',  # Emerald-600
        'icon': 'public',
        'category': 'Epistemic Skills',
        'size': 2,
    },
    'HistoricalThinking': {
        'color': '#92400E',  # Amber-900
        'icon': 'history_edu',
        'category': 'Epistemic Skills',
        'size': 2,
    },
    'ComputationalThinking': {
        'color': '#4F46E5',  # Indigo-600
        'icon': 'computer',
        'category': 'Epistemic Skills',
        'size': 2,
    },

    # ASSESSMENT LAYER (Grays)
    'TestFramework': {
        'color': '#374151',  # Gray-700
        'icon': 'quiz',
        'category': 'Assessment',
        'size': 4,
    },
    'TestPaper': {
        'color': '#4B5563',  # Gray-600
        'icon': 'description',
        'category': 'Assessment',
        'size': 1,
    },
    'ContentDomainCode': {
        'color': '#6B7280',  # Gray-500
        'icon': 'bookmark',
        'category': 'Assessment',
        'size': 1,
    },

    # CASE STANDARDS LAYER (Oranges & Browns)
    'Framework': {
        'color': '#EA580C',  # Orange-600
        'icon': 'account_balance',
        'category': 'CASE Standards',
        'size': 5,
    },
    'Dimension': {
        'color': '#C2410C',  # Orange-700
        'icon': 'view_in_ar',
        'category': 'CASE Standards',
        'size': 4,
    },
    'CoreIdea': {
        'color': '#B45309',  # Amber-700
        'icon': 'school',
        'category': 'CASE Standards',
        'size': 3,
    },
    'CrosscuttingConcept': {
        'color': '#15803D',  # Green-700
        'icon': 'hub',
        'category': 'CASE Standards',
        'size': 2,
    },
    'Practice': {
        'color': '#0284C7',  # Sky-600
        'icon': 'engineering',
        'category': 'CASE Standards',
        'size': 2,
    },
    'PerformanceExpectation': {
        'color': '#6B7280',  # Gray-500
        'icon': 'assessment',
        'category': 'CASE Standards',
        'size': 1,
    },
    'GradeBand': {
        'color': '#9CA3AF',  # Gray-400
        'icon': 'grade',
        'category': 'CASE Standards',
        'size': 1,
    },
    'MathPractice': {
        'color': '#D97706',  # Amber-600
        'icon': 'functions',
        'category': 'CASE Standards',
        'size': 2,
    },

    # LEARNER PROFILE LAYER (Violets & Purples)
    'InteractionType': {
        'color': '#7C3AED',   # Violet-600 (matches import script)
        'icon': 'lightbulb',
        'category': 'Learner Profile',
        'size': 2,
    },
    'ContentGuideline': {
        'color': '#7C3AED',   # Violet-600
        'icon': 'document',
        'category': 'Learner Profile',
        'size': 3,
    },
    'PedagogyProfile': {
        'color': '#7C3AED',   # Violet-600
        'icon': 'route',
        'category': 'Learner Profile',
        'size': 3,
    },
    'FeedbackProfile': {
        'color': '#7C3AED',   # Violet-600
        'icon': 'speech',
        'category': 'Learner Profile',
        'size': 3,
    },
    'PedagogyTechnique': {
        'color': '#3B0764',   # Purple-950 (matches import script)
        'icon': 'brain',
        'category': 'Learner Profile',
        'size': 3,
    },

    # OAK CONTENT (Future layer - placeholder)
    'OakUnit': {
        'color': '#16A34A',  # Green-600
        'icon': 'collections_bookmark',
        'category': 'Oak Content',
        'size': 3,
    },
    'OakLesson': {
        'color': '#22C55E',  # Green-500
        'icon': 'play_lesson',
        'category': 'Oak Content',
        'size': 2,
    },
}


def add_display_properties(driver):
    """Add display_color, display_icon, display_category, display_size to all nodes"""

    with driver.session() as session:
        print("Adding display properties to nodes...\n")

        total_updated = 0

        for node_label, style in NODE_STYLES.items():
            try:
                result = session.run(f"""
                    MATCH (n:{node_label})
                    SET n.display_color = $color,
                        n.display_icon = $icon,
                        n.display_category = $category,
                        n.display_size = $size
                    RETURN count(n) as updated
                """, color=style['color'], icon=style['icon'],
                     category=style['category'], size=style['size'])

                updated = result.single()['updated']
                total_updated += updated

                if updated > 0:
                    color_preview = f"\033[38;2;{int(style['color'][1:3], 16)};{int(style['color'][3:5], 16)};{int(style['color'][5:7], 16)}m●\033[0m"
                    size_bar = '█' * style['size'] + '░' * (5 - style['size'])
                    print(f"  {color_preview} {node_label:28} [{size_bar}] → {updated:4} nodes ({style['icon']})")

            except Exception as e:
                print(f"  ✗ {node_label:30} → Error: {e}")

        print(f"\n✅ Total nodes styled: {total_updated:,}")

        # Summary by category
        print("\n--- SUMMARY BY CATEGORY ---")
        result = session.run("""
            MATCH (n)
            WHERE n.display_category IS NOT NULL
            RETURN n.display_category as category, count(n) as count
            ORDER BY count DESC
        """)

        for record in result:
            print(f"  {record['category']:20} {record['count']:4} nodes")


def create_cypher_backup():
    """Generate Cypher script for version control"""

    cypher_lines = [
        "// Display Properties Migration",
        "// Auto-generated styling for UK Curriculum Knowledge Graph",
        "// Color scheme: Tailwind CSS palette",
        "// Icons: Material Design icon names",
        "",
    ]

    for node_label, style in NODE_STYLES.items():
        cypher_lines.append(f"// {node_label} - {style['category']}")
        cypher_lines.append(f"MATCH (n:{node_label})")
        cypher_lines.append(f"SET n.display_color = '{style['color']}',")
        cypher_lines.append(f"    n.display_icon = '{style['icon']}',")
        cypher_lines.append(f"    n.display_category = '{style['category']}',")
        cypher_lines.append(f"    n.display_size = {style['size']};")
        cypher_lines.append("")

    return "\n".join(cypher_lines)


def main():
    print("="*70)
    print("Add Display Properties for Visualization")
    print("="*70)
    print(f"\nConnecting to {NEO4J_URI}...")

    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

    try:
        add_display_properties(driver)

        # Save Cypher backup
        cypher_script = create_cypher_backup()
        cypher_path = LAYER_ROOT / 'data' / 'cypher' / 'add_display_properties.cypher'
        cypher_path.parent.mkdir(parents=True, exist_ok=True)
        with open(cypher_path, 'w') as f:
            f.write(cypher_script)
        print(f"\n✅ Cypher backup saved to: {cypher_path}")

    finally:
        driver.close()

    print("\n" + "="*70)
    print("✅ Display properties added and version controlled!")
    print("="*70)


if __name__ == "__main__":
    main()

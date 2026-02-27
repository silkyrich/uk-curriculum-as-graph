# UK Curriculum Knowledge Graph — local dev recipes
# Install just: https://github.com/casey/just

# Default recipe: show available commands
default:
    @just --list

# ── Neo4j (local Docker) ─────────────────────────────────────────────

# Start a local Neo4j instance in Docker
neo4j-start:
    docker run -d \
        --name curriculum-neo4j \
        -p 7474:7474 -p 7687:7687 \
        -e NEO4J_AUTH=neo4j/localpassword \
        neo4j:5-community
    @echo "Neo4j starting at http://localhost:7474 (bolt: localhost:7687)"
    @echo "Credentials: neo4j / localpassword"
    @echo ""
    @echo "Set environment variables:"
    @echo "  export NEO4J_URI='neo4j://localhost:7687'"
    @echo "  export NEO4J_USERNAME='neo4j'"
    @echo "  export NEO4J_PASSWORD='localpassword'"

# Stop and remove the local Neo4j container
neo4j-stop:
    docker stop curriculum-neo4j && docker rm curriculum-neo4j

# Show Neo4j container status
neo4j-status:
    @docker inspect -f '{{`{{.State.Status}}`}}' curriculum-neo4j 2>/dev/null || echo "Not running"

# ── Full build pipeline ──────────────────────────────────────────────

# Build the full graph from scratch (schema + import + validate)
build: schema import validate
    @echo "Graph build complete"

# Create/update Neo4j schema
schema:
    python3 core/scripts/create_schema.py

# Run full import pipeline (skips Oak — not yet available)
import:
    python3 core/scripts/import_all.py --skip-oak

# Run schema validation
validate:
    python3 core/scripts/validate_schema.py

# ── Teacher planner generation ───────────────────────────────────────

# Generate all teacher planners (md + pptx + docx)
generate:
    python3 scripts/generate_all_planners.py --all

# Generate markdown planners only (fast, for development)
generate-md:
    python3 scripts/generate_all_planners.py --all --format md

# Generate binary planners only (pptx + docx)
generate-binaries:
    python3 scripts/generate_all_planners.py --all --format pptx,docx

# Generate planners for a single subject (e.g. just generate-subject history)
generate-subject subject:
    python3 scripts/generate_all_planners.py --subject {{subject}}

# Dry run — list what would be generated without creating files
generate-dry-run:
    python3 scripts/generate_all_planners.py --all --dry-run

# ── Utilities ────────────────────────────────────────────────────────

# Install Python dependencies
install:
    pip install -r requirements.txt

# Remove generated binary files (pptx + docx)
clean:
    find generated/teacher-planners -name '*.pptx' -delete 2>/dev/null || true
    find generated/teacher-planners -name '*.docx' -delete 2>/dev/null || true
    @echo "Removed generated PPTX and DOCX files"

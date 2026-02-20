#!/usr/bin/env python3
"""
Neo4j connection configuration
Supports both local and Aura instances via environment variables

IMPORTANT: Set environment variables before running:
  export NEO4J_URI="neo4j+s://your-instance.databases.neo4j.io"
  export NEO4J_USERNAME="your-username"
  export NEO4J_PASSWORD="your-password"
  export NEO4J_DATABASE="your-database-name"

For local Neo4j, defaults to localhost if no env vars set.
"""
import os
import sys
from pathlib import Path

# Auto-load .env file from project root if present (and python-dotenv not required)
_env_file = Path(__file__).parent.parent.parent / '.env'
if _env_file.exists():
    with open(_env_file) as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#') and '=' in line:
                key, _, value = line.partition('=')
                os.environ.setdefault(key.strip(), value.strip())

# Read from environment variables (required for Aura, optional for local)
NEO4J_URI = os.getenv('NEO4J_URI', 'neo4j://127.0.0.1:7687')
NEO4J_USER = os.getenv('NEO4J_USERNAME', 'neo4j')
NEO4J_PASSWORD = os.getenv('NEO4J_PASSWORD', 'password123')
NEO4J_DATABASE = os.getenv('NEO4J_DATABASE', None)

def get_connection_config():
    """Returns connection configuration for Neo4j driver"""
    config = {
        'uri': NEO4J_URI,
        'auth': (NEO4J_USER, NEO4J_PASSWORD),
    }
    # Only specify database for Aura
    if NEO4J_DATABASE and 'aura' in NEO4J_URI.lower():
        config['database'] = NEO4J_DATABASE
    return config

def validate_connection():
    """Check if connection credentials are configured"""
    if not NEO4J_PASSWORD or NEO4J_PASSWORD == 'password123':
        print("⚠️  WARNING: Using default local credentials")
        print("   For Aura, set environment variables:")
        print("   export NEO4J_URI='neo4j+s://...'")
        print("   export NEO4J_USERNAME='...'")
        print("   export NEO4J_PASSWORD='...'")
        return False
    return True

if __name__ == '__main__':
    print("Neo4j Connection Configuration:")
    print(f"  URI: {NEO4J_URI}")
    print(f"  User: {NEO4J_USER}")
    print(f"  Password: {'*' * len(NEO4J_PASSWORD) if NEO4J_PASSWORD else '[not set]'}")
    print(f"  Database: {NEO4J_DATABASE or '[default]'}")
    print()
    validate_connection()

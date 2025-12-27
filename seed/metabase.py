"""
Seed Metabase with pre-configured database connection and dashboard.
Run this after completing the Metabase setup wizard.
"""

import psycopg2
import requests
import sys
from pathlib import Path
from config import POSTGRES_CONFIG

# Override database for Metabase
POSTGRES_CONFIG = {**POSTGRES_CONFIG, 'database': 'metabase'}

def seed_metabase():
    """Seed Metabase with database connection."""
    print("\n" + "="*60)
    print("Metabase Database Seeding")
    print("="*60)

    try:
        # Read SQL seed file
        sql_file = Path(__file__).parent / 'metabase.sql'
        with open(sql_file, 'r') as f:
            sql_content = f.read()

        print("\n📊 Seeding database connection and metadata...")

        # Execute seed SQL
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cur = conn.cursor()
        cur.execute(sql_content)
        conn.commit()
        cur.close()
        conn.close()

        print("✓ Database connection and metadata configured")

        print("\n" + "="*60)
        print("METABASE READY")
        print("="*60)
        print("  URL:      http://localhost:3000")
        print("  Database: Agentic Modeling Demo (marketing schema)")
        print("="*60)

    except Exception as e:
        print(f"✗ ERROR seeding Metabase: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    seed_metabase()

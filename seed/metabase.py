"""
Pre-seed Metabase with PostgreSQL database connection.
Docker Compose ensures Metabase is running before this script executes.
"""

import psycopg2
import requests
import sys
from pathlib import Path
from config import POSTGRES_CONFIG, METABASE_URL

# Override database for Metabase
POSTGRES_CONFIG = {**POSTGRES_CONFIG, 'database': 'metabase'}

def trigger_schema_sync():
    """Trigger Metabase schema sync for database ID 2."""
    try:
        print("\n🔄 Triggering schema sync...")
        response = requests.post(
            f'{METABASE_URL}/api/database/2/sync_schema',
            timeout=30
        )

        if response.status_code == 200:
            print("✓ Schema sync triggered successfully")
        elif response.status_code == 202:
            print("✓ Schema sync accepted and will run in background")
        else:
            print(f"⚠ Schema sync returned status {response.status_code}")
            print("  Schema will sync automatically in the background")

    except Exception as e:
        print(f"⚠ Could not trigger schema sync: {str(e)}")
        print("  Schema will sync automatically in the background")

def seed_metabase():
    """Seed Metabase with PostgreSQL connection."""
    print("\n" + "="*60)
    print("Metabase Database Connection Seeding")
    print("="*60)

    # Read SQL seed file
    sql_file = Path(__file__).parent / 'metabase.sql'
    with open(sql_file, 'r') as f:
        sql_content = f.read()

    print("\n📊 Adding Agentic Modeling Demo database connection...")

    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cur = conn.cursor()

        # Execute seed SQL (idempotent with ON CONFLICT)
        cur.execute(sql_content)
        conn.commit()

        cur.close()
        conn.close()

        print("✓ Successfully configured database connection")

        # Trigger schema sync via API
        trigger_schema_sync()

        print("\n" + "="*60)
        print("METABASE READY")
        print("="*60)
        print("  URL:      http://localhost:3000")
        print("  Database: Agentic Modeling Demo (connected to marketing schema)")
        print("="*60)

    except Exception as e:
        print(f"✗ ERROR seeding Metabase: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    seed_metabase()

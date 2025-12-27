"""
Pre-seed Metabase with PostgreSQL database connection.
Users will create their account through Metabase's first-run setup.
"""

import psycopg2
import requests
import time
import sys
import os
from pathlib import Path

# PostgreSQL configuration
POSTGRES_CONFIG = {
    'host': os.environ.get('POSTGRES_HOST', 'postgresql'),
    'port': int(os.environ.get('POSTGRES_PORT', '5432')),
    'user': os.environ.get('POSTGRES_USER', 'postgres'),
    'password': os.environ.get('POSTGRES_PASSWORD', 'password'),
    'database': os.environ.get('POSTGRES_DB', 'metabase')
}

# Metabase configuration
METABASE_URL = os.environ.get('METABASE_URL', 'http://metabase:3000')

def wait_for_metabase_tables():
    """Wait for Metabase to create its database schema."""
    print("Waiting for Metabase to complete first-run setup...")
    max_attempts = 90  # 3 minutes
    attempt = 0

    while attempt < max_attempts:
        try:
            conn = psycopg2.connect(**POSTGRES_CONFIG)
            cur = conn.cursor()

            # Check if metabase_database table exists AND core_user has at least one user
            # (meaning the setup wizard was completed)
            cur.execute("""
                SELECT EXISTS (
                    SELECT FROM information_schema.tables
                    WHERE table_schema = 'public'
                    AND table_name = 'metabase_database'
                )
                AND EXISTS (
                    SELECT FROM core_user WHERE is_superuser = true LIMIT 1
                );
            """)
            ready = cur.fetchone()[0]

            cur.close()
            conn.close()

            if ready:
                print("✓ Metabase setup complete")
                return True

        except Exception as e:
            pass

        attempt += 1
        time.sleep(2)

    print("⚠ Timeout waiting for Metabase setup")
    print("  Metabase may still be initializing or setup wizard not completed")
    return False

def check_already_seeded():
    """Check if the database connection is already configured."""
    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cur = conn.cursor()

        # Check if Agentic Modeling Demo database exists
        cur.execute("SELECT COUNT(*) FROM metabase_database WHERE name = 'Agentic Modeling Demo';")
        count = cur.fetchone()[0]

        cur.close()
        conn.close()

        return count > 0
    except Exception:
        return False

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

    # Wait for Metabase setup to complete
    if not wait_for_metabase_tables():
        print("\nℹ Skipping seed - complete Metabase setup first")
        print("  Visit http://localhost:3000 to finish setup")
        return

    # Check if already seeded
    if check_already_seeded():
        print("✓ Agentic Modeling Demo database already connected")
        print("="*60)
        return

    # Read SQL seed file
    sql_file = Path(__file__).parent / 'seed_metabase.sql'
    with open(sql_file, 'r') as f:
        sql_content = f.read()

    print("\n📊 Adding Agentic Modeling Demo database connection...")

    try:
        conn = psycopg2.connect(**POSTGRES_CONFIG)
        cur = conn.cursor()

        # Execute seed SQL
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

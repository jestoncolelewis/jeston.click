"""
Database initialization script for Railway PostgreSQL

Run this once after deploying to Railway to set up the database schema
and optionally migrate data from DynamoDB.
"""
import os
import psycopg2


def init_database():
    """Initialize the PostgreSQL database schema"""
    database_url = os.getenv("DATABASE_URL")

    if not database_url:
        print("ERROR: DATABASE_URL environment variable not set")
        return

    conn = psycopg2.connect(database_url)
    cursor = conn.cursor()

    # Create table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS page_views (
            pk INTEGER PRIMARY KEY,
            view_num INTEGER NOT NULL,
            date_time TIMESTAMP NOT NULL
        )
    """)

    # Check if data exists
    cursor.execute("SELECT COUNT(*) FROM page_views WHERE pk = 0")
    count = cursor.fetchone()[0]

    if count == 0:
        # Insert initial record
        # TODO: Update this value with the current count from DynamoDB before first deployment
        initial_count = 0
        cursor.execute("""
            INSERT INTO page_views (pk, view_num, date_time)
            VALUES (0, %s, NOW())
        """, (initial_count,))
        print(f"Initialized page views with count: {initial_count}")
    else:
        print("Database already initialized")

    conn.commit()
    cursor.close()
    conn.close()
    print("Database initialization complete!")


if __name__ == "__main__":
    init_database()

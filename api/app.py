import os
from datetime import datetime
from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app, origins=["https://jeston.click", "https://www.jeston.click"])

# Railway provides DATABASE_URL automatically
DATABASE_URL = os.getenv("DATABASE_URL")


def get_db_connection():
    """Get PostgreSQL database connection"""
    conn = psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)
    return conn


def init_db():
    """Initialize database table and seed with initial value if needed"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS page_views (
            pk INTEGER PRIMARY KEY,
            view_num INTEGER NOT NULL,
            date_time TIMESTAMP NOT NULL
        )
    """)

    # Insert initial record if table is empty
    cursor.execute("SELECT COUNT(*) FROM page_views WHERE pk = 0")
    if cursor.fetchone()['count'] == 0:
        cursor.execute("""
            INSERT INTO page_views (pk, view_num, date_time)
            VALUES (0, 0, %s)
        """, (datetime.now(),))

    conn.commit()
    cursor.close()
    conn.close()


@app.route('/page-count', methods=['GET'])
def page_count():
    """Increment and return page view count"""
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get current view count
    cursor.execute("SELECT view_num FROM page_views WHERE pk = 0")
    result = cursor.fetchone()
    current_views = result['view_num']

    # Increment and update
    new_views = current_views + 1
    now = datetime.now()

    cursor.execute("""
        UPDATE page_views
        SET view_num = %s, date_time = %s
        WHERE pk = 0
    """, (new_views, now))

    conn.commit()
    cursor.close()
    conn.close()

    # Return the old count (before increment) to match Lambda behavior
    return str(current_views), 200


@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({"status": "healthy"}), 200


if __name__ == '__main__':
    # Initialize database on startup
    init_db()

    # Railway sets PORT environment variable
    port = int(os.getenv('PORT', 8000))
    app.run(host='0.0.0.0', port=port)

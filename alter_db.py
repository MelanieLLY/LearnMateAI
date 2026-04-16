import sqlite3
import os

db_path = os.path.join(os.path.dirname(__file__), 'server', 'learnmate.db')
print(f"Connecting to {db_path}")

try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("ALTER TABLE users ADD COLUMN full_name VARCHAR NOT NULL DEFAULT 'Unknown User'")
    conn.commit()
    print("Successfully added full_name to users table.")
    conn.close()
except sqlite3.OperationalError as e:
    if "duplicate column name" in str(e):
        print("Column full_name already exists in users table.")
    else:
        print(f"Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")

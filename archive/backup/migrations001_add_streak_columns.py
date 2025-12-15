# migrations/001_add_streak_columns.py
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "core4.db")
DB_PATH = os.path.abspath(DB_PATH)

def column_exists(cur, table, column):
    cur.execute(f"PRAGMA table_info({table});")
    cols = [row[1].lower() for row in cur.fetchall()]
    return column.lower() in cols

def main():
    print(f"Using DB: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    table = "users"

    if not column_exists(cur, table, "streak_count"):
        print("Adding column: streak_count")
        cur.execute(f"ALTER TABLE {table} ADD COLUMN streak_count INTEGER DEFAULT 0;")

    if not column_exists(cur, table, "last_login"):
        print("Adding column: last_login")
        cur.execute(f"ALTER TABLE {table} ADD COLUMN last_login DATE;")

    conn.commit()
    conn.close()
    print("Migration done.")

if __name__ == "__main__":
    main()

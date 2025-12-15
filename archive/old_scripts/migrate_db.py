import sqlite3

# Connect to the SQLite database
conn = sqlite3.connect("clusterverse.db")
cursor = conn.cursor()

# Create leaderboard table
cursor.execute('''
CREATE TABLE IF NOT EXISTS leaderboard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    role TEXT,
    points INTEGER DEFAULT 0,
    badge TEXT
)
''')

# Create posts table
cursor.execute('''
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    content TEXT NOT NULL,
    upvotes INTEGER DEFAULT 0,
    downvotes INTEGER DEFAULT 0,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# ✅ Create hall_of_fame table (missing before)
cursor.execute('''
CREATE TABLE IF NOT EXISTS hall_of_fame (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date DATE NOT NULL,
    username TEXT NOT NULL,
    points INTEGER NOT NULL,
    badge TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("🎉 Migration completed! Database is ready.")

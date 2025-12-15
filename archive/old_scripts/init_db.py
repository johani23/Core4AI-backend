import sqlite3

conn = sqlite3.connect("db.sqlite3")
cursor = conn.cursor()

# Users Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    role TEXT,
    score INTEGER DEFAULT 0,
    badge TEXT DEFAULT 'Newbie'
)
""")

# Posts Table (Community)
cursor.execute("""
CREATE TABLE IF NOT EXISTS posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    content TEXT,
    upvotes INTEGER DEFAULT 0,
    downvotes INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# Winners Table
cursor.execute("""
CREATE TABLE IF NOT EXISTS winners (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    date TEXT,
    FOREIGN KEY(user_id) REFERENCES users(id)
)
""")

# Segments Table (MVP3)
cursor.execute("""
CREATE TABLE IF NOT EXISTS segments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    segment TEXT,
    text TEXT,
    votes INTEGER DEFAULT 0
)
""")

# Challenges Table (MVP2 + MVP3)
cursor.execute("""
CREATE TABLE IF NOT EXISTS challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT,
    description TEXT,
    points INTEGER DEFAULT 0
)
""")

conn.commit()
conn.close()

print("✅ Database initialized with tables: users, posts, winners, segments, challenges")

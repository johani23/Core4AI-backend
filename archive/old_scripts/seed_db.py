import sqlite3
from datetime import datetime

DB_NAME = "db.sqlite3"

conn = sqlite3.connect(DB_NAME)
cur = conn.cursor()

sample_users = [
    ("User1", "Trend Setter", 37, "Explorer"),
    ("User2", "Connector", 5, "Newbie"),
    ("User3", "Connector", 125, "Leader"),
    ("User4", "Connector", 41, "Explorer"),
]

for u in sample_users:
    cur.execute("INSERT OR REPLACE INTO users (username, role, points, badge) VALUES (?, ?, ?, ?)", u)

sample_posts = [
    ("User3", "This is my first post 🚀", "2025-09-19 03:02:31", 1, 0),
    ("User3", "Clusterverse is awesome!", "2025-09-24 17:58:33", 4, 2),
    ("User4", "Working on something cool 💡", "2025-09-20 09:27:13", 2, 2),
    ("User4", "Gamification makes this fun 🎮", "2025-09-20 11:26:21", 2, 1),
]

for p in sample_posts:
    cur.execute("INSERT INTO posts (username, content, timestamp, upvotes, downvotes) VALUES (?, ?, ?, ?, ?)", p)

# Hall of Fame entry
cur.execute("INSERT INTO hall_of_fame (date, username, points, badge) VALUES (?, ?, ?, ?)",
            ("2025-09-25", "User3", 125, "Leader"))

conn.commit()
conn.close()
print("✅ Seeding complete!")

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sqlite3

router = APIRouter()
DB_NAME = "db.sqlite3"

# ==============================
# 🔹 Initialize DB (Create + Seed)
# ==============================
def init_segments_table():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS segments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        segment TEXT,
        text TEXT,
        votes INTEGER DEFAULT 0
    )
    """)

    cursor.execute("SELECT COUNT(*) FROM segments")
    count = cursor.fetchone()[0]

    if count == 0:
        segments_data = [
            ("fashion", "Best outfit of the week"),
            ("fashion", "Top 3 style tips"),
            ("humor", "Funniest meme"),
            ("humor", "Best joke of the day"),
            ("thinkers", "Deepest question"),
            ("thinkers", "Best book summary"),
            ("event-goers", "Top event highlights"),
            ("event-goers", "Best meetup idea"),
        ]
        cursor.executemany("INSERT INTO segments (segment, text) VALUES (?, ?)", segments_data)
        conn.commit()
        print("🌱 Segments table seeded!")

    conn.close()

init_segments_table()

# ==============================
# 🔹 Pydantic Model
# ==============================
class SegmentContent(BaseModel):
    id: int
    segment: str
    text: str
    votes: int

# ==============================
# 🔹 API Endpoints
# ==============================
@router.get("/api/mvp3/segments")
def get_segments():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, segment, text, votes FROM segments")
    rows = cursor.fetchall()
    conn.close()

    contents = [
        {"id": row[0], "segment": row[1], "text": row[2], "votes": row[3]}
        for row in rows
    ]
    return {"contents": contents}


@router.post("/api/mvp3/segments/{content_id}/vote")
def vote_segment(content_id: int):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("UPDATE segments SET votes = votes + 1 WHERE id = ?", (content_id,))
    conn.commit()

    cursor.execute("SELECT votes FROM segments WHERE id = ?", (content_id,))
    row = cursor.fetchone()
    conn.close()

    if row:
        return {"id": content_id, "votes": row[0]}
    else:
        raise HTTPException(status_code=404, detail="Content not found")

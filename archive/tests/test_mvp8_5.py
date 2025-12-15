from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

# ----------------- POSTS / VOTES / STATS -----------------
def test_create_post_and_vote_and_stats():
    stats_before = client.get("/stats").json()
    initial_posts = stats_before["total_posts"]
    initial_votes = stats_before["total_votes"]

    new_post = {"id": 999, "title": "Test Post", "content": "This is a test content", "votes": 0}
    res = client.post("/posts", json=new_post)
    assert res.status_code == 200
    post_data = res.json()
    assert post_data["title"] == "Test Post"

    vote_res = client.post(f"/posts/{new_post['id']}/vote", params={"vote": "up"})
    assert vote_res.status_code == 200
    vote_data = vote_res.json()
    assert vote_data["post"]["votes"] >= 1

    stats_after = client.get("/stats").json()
    assert stats_after["total_posts"] == initial_posts + 1
    assert stats_after["total_votes"] >= initial_votes + 1


# ----------------- AI DEBUG -----------------
def test_ai_debug_endpoint():
    payload = {"text": "This is a funny fashion post 😂👗"}
    res = client.post("/ai/debug", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "tokens" in data
    assert "raw_counts" in data
    assert "segment_scores" in data
    assert isinstance(data["segment_scores"], dict)


# ----------------- XP & LEVEL -----------------
def test_xp_and_level_up():
    profile_before = client.get("/users/1").json()
    level_before = profile_before["level"]

    res = client.post("/xp/1", params={"xp": 200})
    assert res.status_code == 200

    profile_after = client.get("/users/1").json()
    level_after = profile_after["level"]

    assert level_after >= level_before + 2 or level_after > level_before


# ----------------- CHALLENGES -----------------
def test_challenges_completion_and_badge():
    profile_before = client.get("/users/1").json()
    badges_before = set(profile_before["badges"])

    new_post = {"id": 12345, "title": "Challenge Test", "content": "Trigger challenge test", "votes": 0}
    client.post("/posts", json=new_post)

    challenges_after = client.get("/challenges").json()
    completed = [c for c in challenges_after if c["completed"]]
    assert len(completed) >= 1

    profile_after = client.get("/users/1").json()
    badges_after = set(profile_after["badges"])
    assert len(badges_after) >= len(badges_before)
    assert any(b not in badges_before for b in badges_after)


# ----------------- SPOTLIGHT -----------------
def test_spotlight_returns_top_post():
    low_post = {"id": 2001, "title": "Low Votes", "content": "Just a low vote post", "votes": 0}
    client.post("/posts", json=low_post)

    high_post = {"id": 2002, "title": "High Votes", "content": "This should win spotlight", "votes": 0}
    client.post("/posts", json=high_post)

    for _ in range(5):
        client.post(f"/posts/{high_post['id']}/vote", params={"vote": "up"})

    res = client.get("/spotlight")
    assert res.status_code == 200
    spotlight = res.json()

    assert spotlight["title"] == "High Votes"
    assert spotlight["votes"] >= 5


# ----------------- LEADERBOARD -----------------
def test_leaderboard_contains_user_profile():
    profile = client.get("/users/1").json()
    res = client.get("/leaderboard")
    assert res.status_code == 200
    leaderboard = res.json()

    usernames = [u["username"] for u in leaderboard]
    assert "You" in usernames

    user_entry = next((u for u in leaderboard if u["username"] == "You"), None)
    assert user_entry is not None
    assert user_entry["xp"] == profile["xp"]
    assert user_entry["level"] == profile["level"]
    assert isinstance(user_entry["badges"], list)

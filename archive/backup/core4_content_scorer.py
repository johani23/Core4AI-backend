# ============================================================
# 💎 Core4.AI – MVP-81 “Content Value Scorer”
# ------------------------------------------------------------
# Phase 1 : Offline Prototype
# • Computes Insight / Originality / Emotion / Relevance / Style
# • Returns Tribe assignment and overall Value Score
# ============================================================

from sentence_transformers import SentenceTransformer, util
import numpy as np, hashlib, json, os, re
from collections import defaultdict

# ------------------------------------------------------------
# ⚙️ Load Model
# ------------------------------------------------------------
model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

# ------------------------------------------------------------
# 📁 Load or Create Reference Profiles
# ------------------------------------------------------------
TRIBE_PROFILES_PATH = "./data/tribe_profiles.json"
if not os.path.exists("data"):
    os.makedirs("data")

default_profiles = {
    "Vibe Makers": "positivity energy motivation inspiration",
    "Deep Thinkers": "philosophy analysis depth insight reflection",
    "Humor League": "jokes sarcasm irony wit laughter clever",
    "Event Pulse": "news trends events concerts sports festivals"
}

if not os.path.exists(TRIBE_PROFILES_PATH):
    base_embeds = {k: model.encode(v, normalize_embeddings=True).tolist()
                   for k, v in default_profiles.items()}
    json.dump(base_embeds, open(TRIBE_PROFILES_PATH, "w"), indent=2)

tribe_embeddings = {k: np.array(v)
                    for k, v in json.load(open(TRIBE_PROFILES_PATH)).items()}

# ------------------------------------------------------------
# 🧩 Utility Functions
# ------------------------------------------------------------
def text_hash(txt):
    return hashlib.md5(txt.encode("utf-8")).hexdigest()

def normalize(x):
    return float(np.clip(x, 0, 1))

# ------------------------------------------------------------
# 📊 Scoring Dimensions
# ------------------------------------------------------------
def compute_dimensions(text):
    emb = model.encode(text, normalize_embeddings=True)
    dims = {}

    # Insight → novelty relative to tribe average embedding
    insight = 1 - max([float(util.cos_sim(emb, v)) for v in tribe_embeddings.values()])
    dims["Insight"] = normalize(insight)

    # Originality → penalty if text hash seen before
    penalty_path = "./data/penalty_cache.json"
    cache = json.load(open(penalty_path)) if os.path.exists(penalty_path) else {}
    h = text_hash(text)
    originality = 1.0 if h not in cache else 0.3
    cache[h] = True
    json.dump(cache, open(penalty_path, "w"))
    dims["Originality"] = normalize(originality)

    # Emotional Resonance → via heuristic sentiment intensity
    emo = len(re.findall(r"[!❤️🔥😂😭😍]", text)) / max(len(text), 1)
    dims["Emotional Resonance"] = normalize(emo * 10)

    # Relevance → max similarity with any tribe
    relevance = max([float(util.cos_sim(emb, v)) for v in tribe_embeddings.values()])
    dims["Relevance"] = normalize(relevance)

    # Style → based on length, readability, punctuation
    length = len(text.split())
    style = 1 - abs(length - 20) / 50
    style -= 0.1 * len(re.findall(r"http|www|#|@", text))
    dims["Style"] = normalize(style)

    return dims, emb

# ------------------------------------------------------------
# 🧮 Weighted Reward
# ------------------------------------------------------------
def compute_reward(dims):
    R = (
        0.3 * dims["Insight"]
        + 0.25 * dims["Originality"]
        + 0.2 * dims["Emotional Resonance"]
        + 0.15 * dims["Relevance"]
        + 0.1 * dims["Style"]
    )
    return normalize(R)

# ------------------------------------------------------------
# 🏕️ Tribe Assignment
# ------------------------------------------------------------
def assign_tribe(emb):
    sims = {t: float(util.cos_sim(emb, v)) for t, v in tribe_embeddings.items()}
    return max(sims, key=sims.get)

# ------------------------------------------------------------
# 🎯 Main Evaluation Function
# ------------------------------------------------------------
def evaluate_content(text: str):
    dims, emb = compute_dimensions(text)
    score = compute_reward(dims)
    tribe = assign_tribe(emb)
    return {
        "tribe": tribe,
        "score": round(score, 3),
        "dimensions": {k: round(v, 3) for k, v in dims.items()}
    }

# ------------------------------------------------------------
# 🧪 Quick Test
# ------------------------------------------------------------
if __name__ == "__main__":
    sample = "Life is about rhythm, not rush."
    print(evaluate_content(sample))

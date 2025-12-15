# -----------------------------------------------------------
# Core4.AI – MVP 15 Week 2: Emotional Clustering Engine
# -----------------------------------------------------------
from fastapi import APIRouter
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

router = APIRouter(prefix="/ai", tags=["AI Emotion Cluster"])

# ✅ Model (small + fast)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Define tone keywords to simulate emotional categories
TONE_KEYWORDS = {
    "inspirational": ["dream", "hope", "change", "believe", "growth"],
    "analytical": ["data", "logic", "evidence", "analysis", "reason"],
    "humorous": ["funny", "laugh", "joke", "meme", "sarcastic"],
    "emotional": ["love", "hurt", "feel", "heart", "relationship"],
    "critical": ["problem", "fail", "mistake", "issue", "concern"]
}

class EmotionRequest(BaseModel):
    text: str

def classify_tone(text: str):
    text_vec = model.encode([text])
    scores = {}
    for tone, words in TONE_KEYWORDS.items():
        tone_vec = model.encode([" ".join(words)])
        sim = cosine_similarity(text_vec, tone_vec)[0][0]
        scores[tone] = float(sim)
    return scores

def value_density(text: str):
    # Simple heuristic for now: ratio of “meaningful” words
    keywords = ["impact", "insight", "truth", "future", "create", "value"]
    words = text.lower().split()
    density = sum(1 for w in words if w in keywords) / max(len(words), 1)
    return round(density * 100, 2)

@router.post("/emotion-cluster")
def analyze_emotion(req: EmotionRequest):
    tones = classify_tone(req.text)
    best_tone = max(tones, key=tones.get)
    vds = value_density(req.text)
    return {
        "text": req.text,
        "dominant_tone": best_tone,
        "tone_scores": tones,
        "value_density": vds,
        "cluster": f"{best_tone.title()} Cluster",
        "insight": f"This content expresses a {best_tone} tone with {vds}% value density.",
    }

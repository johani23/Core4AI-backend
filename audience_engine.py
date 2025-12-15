# ============================================================================
# 💚 Core4.AI – Audience Intelligence Engine (v2.0)
# ============================================================================

from typing import List, Dict
import numpy as np
from sklearn.cluster import KMeans

# ------------------------------------------------------
# DOPAMINE WEIGHTING MAP
# ------------------------------------------------------
DOPAMINE_WEIGHTS = {
    "view": 1,
    "long_view": 4,
    "click": 6,
    "save": 8,
    "share": 12,
    "purchase": 30,
    "return_session": 20,
}

# ------------------------------------------------------
# Heatmap Score
# ------------------------------------------------------
def compute_heatmap_score(events: List[Dict]):
    score = 0
    for e in events:
        if e["event_type"] in DOPAMINE_WEIGHTS:
            score += DOPAMINE_WEIGHTS[e["event_type"]]
    return score


# ------------------------------------------------------
# AI Persona Engine
# ------------------------------------------------------
def generate_dynamic_persona(buyer_id: str, events: List[Dict]):
    score = compute_heatmap_score(events)

    if score > 150:
        level = "Power Influencer"
    elif score > 80:
        level = "Rising Micro-Influencer"
    else:
        level = "Explorer"

    top_tags = extract_top_tags(events)

    persona = {
        "buyer_id": buyer_id,
        "level": level,
        "heat_score": score,
        "tags": top_tags,
    }

    return persona


# ------------------------------------------------------
# Extract Tags from behavior
# ------------------------------------------------------
def extract_top_tags(events: List[Dict]):
    tag_map = {}

    for e in events:
        payload = e.get("payload", {})
        tag = payload.get("category") or payload.get("tribe")
        if not tag:
            continue

        tag_map[tag] = tag_map.get(tag, 0) + 1

    sorted_tags = sorted(tag_map.items(), key=lambda x: x[1], reverse=True)
    return [t[0] for t in sorted_tags[:4]]


# ------------------------------------------------------
# Lookalikes
# ------------------------------------------------------
def cluster_buyers(feature_matrix):
    kmeans = KMeans(n_clusters=5, random_state=42)
    labels = kmeans.fit_predict(feature_matrix)
    return labels, kmeans.cluster_centers_

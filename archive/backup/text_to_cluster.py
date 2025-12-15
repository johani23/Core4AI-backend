# text_to_cluster.py

from collections import defaultdict

clusters_keywords = {
    "Creative Soul": ["art", "painting", "music", "writing", "solitude"],
    "Logical Thinker": ["math", "data", "logic", "analysis", "algorithm"],
    "Empathic Leader": ["people", "empathy", "help", "guide", "care"],
    "Adventurous Mind": ["travel", "risk", "mountain", "hiking", "new"]
}

def map_text_to_cluster(text: str) -> str:
    text = text.lower()
    scores = defaultdict(int)

    for cluster, keywords in clusters_keywords.items():
        for keyword in keywords:
            if keyword in text:
                scores[cluster] += 1

    if not scores:
        return "Undefined"

    # Return the cluster with the highest score
    return max(scores, key=scores.get)

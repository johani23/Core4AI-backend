from fastapi import APIRouter

router = APIRouter()

clusters = {
    "fashion": {"shadow": "Trendy vibes 🌟"},
    "events": {"shadow": "Party mood 🎉"},
    "thinkers": {"shadow": "Deep thoughts 🤔"},
    "humor": {"shadow": "Laughs 😂"},
}

@router.get("")
def get_clusters():
    return [{"name": k, **v} for k, v in clusters.items()]

@router.get("/{cluster_name}/shadow")
def get_cluster_shadow(cluster_name: str):
    return clusters.get(cluster_name, {"shadow": "Unknown cluster"})

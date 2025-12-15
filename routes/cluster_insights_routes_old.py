from fastapi import APIRouter
from models.value_insights import ValueInsight
from db import SessionLocal
from sqlalchemy import func

router = APIRouter(prefix="/api/cluster-insights", tags=["Cluster Insights"])

@router.get("/{product_id}")
def cluster_insights(product_id: int):
    db = SessionLocal()

    # fetch all rows for this product
    insights = db.query(ValueInsight).filter(ValueInsight.product_id == product_id).all()

    # no insights yet
    if not insights:
        return {"clusters": []}

    # we assume buyer cluster is embedded in raw_answers or persona later
    # For now we simulate cluster_assignment = raw_answers.get("cluster")
    clusters = {}

    for row in insights:
        cluster = (
            row.raw_answers.get("cluster", "C1") 
        )  # fallback default

        if cluster not in clusters:
            clusters[cluster] = {
                "value_scores": [],
                "elasticities": [],
                "differentiations": [],
                "recommended_prices": [],
                "plateau_flags": [],
                "sample_size": 0,
            }

        clusters[cluster]["value_scores"].append(row.value_score)
        clusters[cluster]["elasticities"].append(row.elasticity)
        clusters[cluster]["differentiations"].append(row.differentiation)
        clusters[cluster]["recommended_prices"].append(row.recommended_price)
        clusters[cluster]["plateau_flags"].append(1 if "Plateau" in (row.plateau or "") else 0)
        clusters[cluster]["sample_size"] += 1

    # aggregate data
    results = []

    for cluster, data in clusters.items():
        sample = data["sample_size"]

        if sample == 0:
            continue

        def avg(arr): 
            return sum(arr) / len(arr)

        results.append({
            "cluster": cluster,
            "value_score_avg": avg(data["value_scores"]),
            "elasticity_avg": avg(data["elasticities"]),
            "differentiation_avg": avg(data["differentiations"]),
            "recommended_price_avg": avg(data["recommended_prices"]),
            "plateau_risk": avg(data["plateau_flags"]),
            "sample_size": sample,
        })

    return {"clusters": results}

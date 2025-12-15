# ============================================================================
# 💚 Core4.AI – RND Insights API (Value Insights + Cluster Analysis)
# ============================================================================

from fastapi import APIRouter
from db import SessionLocal
from models.value_insights import ValueInsight

router = APIRouter(tags=["RND"])

# SAVE INSIGHT
@router.post("/value-insights")
def save_value_insight(data: dict):
    db = SessionLocal()
    insight = ValueInsight(
        product_id=data["product_id"],
        buyer_id=data.get("buyer_id"),
        value_score=data["value_score"],
        plateau=data["plateau"],
        differentiation=data["differentiation"],
        elasticity=data["elasticity"],
        elasticity_label=data["elasticity_label"],
        recommended_price=data["recommended_price"],
        raw_answers=data["raw_answers"],
    )
    db.add(insight)
    db.commit()
    db.refresh(insight)
    return {"status": "saved", "id": insight.id}


# GET RAW INSIGHTS
@router.get("/value-insights/{product_id}")
def get_insights(product_id: int):
    db = SessionLocal()
    rows = db.query(ValueInsight).filter(ValueInsight.product_id == product_id).all()

    return {
        "count": len(rows),
        "insights": [
            {
                "value_score": r.value_score,
                "plateau": r.plateau,
                "differentiation": r.differentiation,
                "elasticity": r.elasticity,
                "elasticity_label": r.elasticity_label,
                "recommended_price": r.recommended_price,
                "raw_answers": r.raw_answers,
                "created_at": r.created_at.isoformat(),
            }
            for r in rows
        ],
    }


# MIT CLUSTER INSIGHTS
@router.get("/cluster-insights/{product_id}")
def get_cluster_insights(product_id: int):
    db = SessionLocal()
    rows = db.query(ValueInsight).filter(ValueInsight.product_id == product_id).all()

    if not rows:
        return {"clusters": []}

    def cluster_of(buyer_id):
        if buyer_id is None:
            return "General"
        return ["Students", "Families", "Women", "General"][buyer_id % 4]

    buckets = {}
    for r in rows:
        c = cluster_of(r.buyer_id)
        buckets.setdefault(c, []).append(r)

    clusters = []
    for cname, items in buckets.items():
        n = len(items)
        clusters.append({
            "cluster": cname,
            "value_score_avg": sum(i.value_score for i in items) / n,
            "differentiation_avg": sum(i.differentiation for i in items) / n,
            "elasticity_avg": sum(i.elasticity for i in items) / n,
            "plateau_risk": sum(1 for i in items if i.plateau != "No Plateau") / n,
            "recommended_price_avg": sum(i.recommended_price for i in items) / n,
            "sample_size": n,
        })

    return {"clusters": clusters}

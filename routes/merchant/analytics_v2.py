# ============================================================================
# 💚 Core4AI – Merchant Analytics v2 (Noor Edition)
# ============================================================================

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(
    prefix="/api/merchant/analytics-v2",
    tags=["merchant-analytics-v2"]
)

# Dummy Engines

def calculate_audience_fit(price: float, audience: str):
    return {
        "best_segment": "عوائل" if price > 100 else "شباب",
        "score": 0.82 if price > 100 else 0.74,
    }

def calculate_roi(price: float, cost: float, expected_sales: int):
    revenue = price * expected_sales
    profit = revenue - cost
    roi = profit / cost if cost > 0 else 0
    return {"roi": roi, "expected_profit": profit}

def predict_success(price: float, influencers: list, audience: str):
    base = 6
    if audience == "عوائل": base += 1
    if price < 200: base += 1
    if len(influencers) > 2: base += 1
    score = min(10, base)
    outcome = "عالية" if score >= 8 else "متوسطة" if score >= 6 else "ضعيفة"
    return {"outcome": outcome, "score": score}

def estimate_funnel(expected_sales: int, audience_strength: float):
    return {
        "estimated_sales": int(expected_sales * audience_strength),
        "conversion_rate": 0.07 * audience_strength
    }

def evaluate_influencer_quality(influencers: list, price: float):
    if len(influencers) >= 3:
        return {"rating": "ممتاز", "comment": "اختيار مؤثرين متنوعين يعزز التفاعل."}
    elif len(influencers) == 2:
        return {"rating": "جيد", "comment": "يمكنك إضافة مؤثر ثالث."}
    else:
        return {"rating": "ضعيف", "comment": "عدد المؤثرين قليل جداً."}

class AnalyticsInput(BaseModel):
    price: float
    influencers: list
    expected_sales: int
    audience: str
    cost: float

@router.post("/analyze")
async def analyze(data: AnalyticsInput):
    return {
        "audience_fit": calculate_audience_fit(data.price, data.audience),
        "roi": calculate_roi(data.price, data.cost, data.expected_sales),
        "success": predict_success(data.price, data.influencers, data.audience),
        "funnel_projection": estimate_funnel(data.expected_sales, 0.8),
        "influencer_quality": evaluate_influencer_quality(data.influencers, data.price)
    }

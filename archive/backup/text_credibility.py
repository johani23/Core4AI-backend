# ============================================================
# NLP + rule-based credibility for text
# ============================================================

from modules.utils import extract_percentages, has_location, classify_risk

def score_text(text:str):
    risk_tier = classify_risk(text)
    cred = 80
    conf = 0.7
    reasons = []

    if risk_tier == "brand_promo":
        pct = max(extract_percentages(text) or [0])
        if pct > 90: cred, reasons = 35, ["unrealistic discount"]
        elif pct > 70: cred, reasons = 55, ["high discount – no evidence"]
        if not has_location(text): cred -= 10; reasons.append("no location")
    elif risk_tier == "health": cred, reasons = 40, ["medical claim"]
    elif risk_tier == "finance": cred, reasons = 45, ["financial promise"]

    cred = max(10, min(cred, 95))
    return {
        "insight": 70, "originality": 65, "engagement": 60,
        "credibility": cred, "credibility_confidence": conf,
        "risk_tier": risk_tier, "reasons": reasons
    }

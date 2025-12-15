# ============================================================
# 💎 content_scoring.py – Unifies text + visual analysis
# ============================================================

import io, json
from modules.text_credibility import score_text
from modules.visual_credibility import score_visual
from modules.sanity_rules import apply_sanity_checks

async def evaluate_content(text, file, creator_id):
    base = {"creator_id": creator_id, "risk_tier": "general"}

    # ---------- TEXT ----------
    text_score = None
    if text:
        text_score = score_text(text)
        base.update(text_score)
        base["risk_tier"] = text_score.get("risk_tier", "general")

    # ---------- VISUAL ----------
    visual_score = None
    if file:
        content = await file.read()
        visual_score = score_visual(content, text=text)
        base.update(visual_score)
        base["risk_tier"] = visual_score.get("risk_tier", base["risk_tier"])

    # ---------- SANITY ----------
    base = apply_sanity_checks(base)

    # ---------- FUSION ----------
    cred, conf = fuse_scores(text_score, visual_score)
    base["credibility"] = round(cred * 100, 1)
    base["credibility_confidence"] = round(conf, 2)
    base["total_score"] = compute_total_score(base)
    return base


def fuse_scores(text_score, visual_score):
    if not visual_score:
        return text_score["credibility"]/100, text_score["credibility_confidence"]
    tv, vv = text_score or {}, visual_score or {}
    tcred = tv.get("credibility", 0)/100
    vcred = vv.get("credibility", 0)/100
    vconf = vv.get("credibility_confidence", 0.5)
    return (0.4*tcred + 0.6*vcred, (vconf+0.5)/2)


def compute_total_score(d):
    # base 4-axis
    weights = {"insight":0.25,"originality":0.25,"engagement":0.25,"credibility":0.25}
    score = sum(d.get(k,0)*w for k,w in weights.items() if isinstance(d.get(k,0),(int,float)))
    return round(score,1)

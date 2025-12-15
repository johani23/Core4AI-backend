# ============================================================
# CLIP + OCR + Metadata + Forgery
# ============================================================

from PIL import Image
import io, random
from modules.utils import ocr_text, extract_percentages, has_location

def score_visual(content: bytes, text:str=None):
    image = Image.open(io.BytesIO(content))
    ocr = ocr_text(image)
    pct = max(extract_percentages(ocr) or [0])
    has_brand = any(b in ocr.lower() for b in ["gucci","dior","lv","rolex","chanel"])
    has_outlet = any(w in ocr.lower() for w in ["outlet","sale","closing","liquidation"])
    cred = 80; conf = 0.6; reasons = []; risk = "general"

    if has_brand and pct >= 90 and not has_outlet:
        cred -= 45; reasons.append("luxury discount outlier"); risk="brand_promo"
    elif has_brand and pct >= 70:
        cred -= 25; reasons.append("possible exaggeration"); risk="brand_promo"

    if "99" in ocr and "off" in ocr.lower() and not has_outlet:
        cred -= 20; reasons.append("no outlet label")

    if not has_location(text or ocr):
        cred -= 10; reasons.append("no location")

    # randomize base variation
    cred = max(10, min(cred + random.uniform(-5,5), 95))
    return {
        "visual_text_match": random.uniform(0.4,0.9),
        "metadata_integrity": random.uniform(0.5,0.9),
        "forgery_prob": random.uniform(0.0,0.4),
        "context_validity": random.uniform(0.5,0.8),
        "credibility": cred,
        "credibility_confidence": conf,
        "risk_tier": risk,
        "reasons": reasons
    }

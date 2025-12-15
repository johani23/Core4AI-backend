import re, pytesseract
from PIL import Image

def extract_percentages(t:str):
    return [min(100, max(0, float(x))) for x in re.findall(r'(\d{1,3})\s*%+', t)]

def has_location(t:str):
    if not t: return False
    return any(loc in t.lower() for loc in [
        "riyadh","jeddah","dubai","ksa","mall","bicester","serravalle","outlet"
    ])

def classify_risk(text:str):
    tl = text.lower()
    if any(b in tl for b in ["gucci","louis vuitton","dior","chanel","rolex"]) and "%" in tl:
        return "brand_promo"
    if any(w in tl for w in ["cancer","cure","covid","diabetes"]): return "health"
    if any(w in tl for w in ["coin","crypto","stock","return"]): return "finance"
    return "general"

def ocr_text(image:Image.Image):
    try:
        return pytesseract.image_to_string(image)
    except Exception:
        return ""

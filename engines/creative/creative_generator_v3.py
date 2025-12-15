# ============================================================================
# Core4.AI – Creative Generator v3 (SAFE PYTHON VERSION, no emojis)
# ============================================================================

from fastapi import APIRouter
from pydantic import BaseModel
import random

router = APIRouter()

# ----------------------------------------------------------------------------
# Request Model
# ----------------------------------------------------------------------------
class CreativeRequest(BaseModel):
    product_name: str
    message: str
    tone: str = "friendly"
    target: str = "Saudi youth"


def choose(arr):
    return random.choice(arr)

# ============================================================================  
# Storyboard (7 scenes)
# ============================================================================
def generate_storyboard(product, msg):
    return [
        {"scene": 1, "shot": "Close-up", "script": f"{product} — opening line", "camera": "Slow push-in"},
        {"scene": 2, "shot": "Lifestyle Mid-shot", "script": msg, "camera": "Handheld"},
        {"scene": 3, "shot": "Feature Highlight", "script": "Key feature demo", "camera": "Macro"},
        {"scene": 4, "shot": "Transition", "script": "Fast cut movement", "camera": "Whip pan"},
        {"scene": 5, "shot": "Outdoor", "script": "Use case outdoors", "camera": "Follow shot"},
        {"scene": 6, "shot": "Hero Shot", "script": f"{product} in hero frame", "camera": "Static"},
        {"scene": 7, "shot": "Call to Action", "script": "Try it now", "camera": "Minimalistic"},
    ]

# ----------------------------------------------------------------------------
# Reels Pack
# ----------------------------------------------------------------------------
def reels_pack(product, msg):
    return [
        {"hook": "Surprising result!", "script": "Reel variant 1"},
        {"hook": "Did you know this?", "script": "Reel variant 2"},
        {"hook": "Top product this week!", "script": "Reel variant 3"},
    ]

# ----------------------------------------------------------------------------
# TikTok Pack
# ----------------------------------------------------------------------------
def tiktok_pack(product):
    return [
        {"format": "Viral Story", "script": f"{product} changed my day"},
        {"format": "Quick Demo", "script": f"{product} explained in 30 secs"},
        {"format": "Before/After", "script": "Transformation clip"},
    ]

# ----------------------------------------------------------------------------
# Carousel Pack
# ----------------------------------------------------------------------------
def carousel_pack(product):
    return [
        {"title": f"Why {product}?", "text": "3 main advantages"},
        {"title": "Advantage 1", "text": "Detail"},
        {"title": "Advantage 2", "text": "Value"},
        {"title": "Advantage 3", "text": "Better experience"},
        {"title": "Order now", "text": "CTA"},
    ]

# ----------------------------------------------------------------------------
# Voiceover Pack
# ----------------------------------------------------------------------------
def voiceover_pack(tone, product):
    return {
        "tone": tone,
        "arabic_vo": choose([
            f"{product} will upgrade your day.",
            f"{product} — highly recommended.",
            f"Try {product} and see the difference."
        ])
    }

# ----------------------------------------------------------------------------
# A/B Variations
# ----------------------------------------------------------------------------
def ab_variations(product):
    return [
        {"type": "A", "headline": f"{product} in 10 seconds", "cta": "Try now"},
        {"type": "B", "headline": "Unexpected feature!", "cta": "Order today"},
    ]

# ----------------------------------------------------------------------------
# Hooks
# ----------------------------------------------------------------------------
HOOKS = [
    "The product everyone is talking about!",
    "Unexpected results!",
    "Listen to this…",
    "This became essential!",
    "Why didn’t anyone tell me earlier?",
]

# ----------------------------------------------------------------------------
# Emotional triggers
# ----------------------------------------------------------------------------
EMO = ["Curiosity", "Desire", "Trust", "FOMO", "Logic", "Community"]

# ----------------------------------------------------------------------------
# Budget Split
# ----------------------------------------------------------------------------
def budget_ai():
    return [
        {"tier": "Mega Creators", "percentage": 15, "reason": "Awareness"},
        {"tier": "Mid Creators", "percentage": 35, "reason": "Reach"},
        {"tier": "Micro Creators", "percentage": 50, "reason": "Conversion"},
    ]

# ============================================================================
# MAIN ENDPOINT
# ============================================================================
@router.post("/api/creative/generate")
def creative_generate(req: CreativeRequest):

    return {
        "storyboard": generate_storyboard(req.product_name, req.message),
        "reels_pack": reels_pack(req.product_name, req.message),
        "tiktok_pack": tiktok_pack(req.product_name),
        "carousel_pack": carousel_pack(req.product_name),
        "voiceover": voiceover_pack(req.tone, req.product_name),
        "ab_testing": ab_variations(req.product_name),
        "hooks": HOOKS,
        "emotional_triggers": EMO,
        "budget_split": budget_ai(),
        "selling_angles": [
            "Lifestyle Upgrade",
            "Saudi Identity",
            "Minimalism",
            "Convenience",
            "Value-for-Money",
            "Trending Style"
        ],
    }

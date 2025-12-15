# ============================================================================
# 🔮 Core4AI – Pulse API (Unified System Activity Stream)
# ============================================================================

from fastapi import APIRouter

router = APIRouter(
    prefix="/api/pulse",
    tags=["pulse"]
)

@router.get("/")
async def get_pulse():
    return {
        "creator_activity": 22,       # % زيادة اليوم
        "tribe_engagement": 14,       # % ارتفاع النقاشات
        "buyer_momentum": 19,         # % نمو الطلب
        "system_score": 72.5,         # مؤشر عام
        "stream": [
            "🟣 TribeTechy ↑ ارتفاع في النقاشات",
            "⚡ FlashDeals ↑ زيادة في التصفح",
            "🎬 CreatorPosts ↑ المحتوى ارتفع 22%",
            "🛒 BuyerShift → استقرار حركة الشراء",
            "🔥 TribeWars ↑ ارتفاع التحديات بين القبائل"
        ]
    }

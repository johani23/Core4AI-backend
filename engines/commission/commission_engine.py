# ============================================================================
# 💚 Core4AI – Commission Engine (v1.0)
# Smart Earnings Engine for Creators, Merchants, and Campaign Insights
# Author: Shadow (AI Engine for Ahmad Aljohani)
# ============================================================================

from typing import Dict


def calculate_commission(
    price: float,
    commission_rate: float,
    conversions: int,
    performance_multiplier: float = 1.0,
    loyalty_tier: str = "standard",
) -> float:
    """
    Calculates the total creator earnings based on:
    - product price
    - commission rate (0.10 = 10%)
    - number of conversions
    - performance multiplier (1.0 default)
    - loyalty tier bonus
    """

    tier_bonus_map = {
        "standard": 1.0,
        "silver": 1.05,
        "gold": 1.10,
        "platinum": 1.20,
    }

    tier_bonus = tier_bonus_map.get(loyalty_tier.lower(), 1.0)

    earning_per_conversion = price * commission_rate
    raw_total = earning_per_conversion * conversions

    adjusted_total = raw_total * performance_multiplier * tier_bonus

    return round(adjusted_total, 2)



def estimate_merchant_profit(
    price: float,
    cost: float,
    conversions: int,
    commission_rate: float,
) -> Dict:
    """
    Merchant profit summary:
    - revenue = price * conversions
    - commission cost = revenue * commission rate
    - profit = revenue - cost_of_goods - commissions
    """

    revenue = price * conversions
    commission_cost = revenue * commission_rate
    cost_of_goods = cost * conversions
    profit = revenue - commission_cost - cost_of_goods

    return {
        "revenue": round(revenue, 2),
        "commission_cost": round(commission_cost, 2),
        "cost_of_goods": round(cost_of_goods, 2),
        "profit": round(profit, 2),
    }



def generate_commission_breakdown(
    price: float,
    commission_rate: float,
    conversions: int,
    creator_name: str = "Creator",
) -> Dict:
    """
    Provides a visual-friendly breakdown for dashboards.
    """

    total_earnings = price * commission_rate * conversions

    return {
        "creator": creator_name,
        "earnings": round(total_earnings, 2),
        "per_conversion": round(price * commission_rate, 2),
        "conversions": conversions,
    }



# Ready for import:
# from engines.commission.commission_engine import (
#     calculate_commission,
#     estimate_merchant_profit,
#     generate_commission_breakdown
# )

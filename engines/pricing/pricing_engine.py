# ============================================================================
# 💸 Core4.AI – Pricing Engine (Feature × Audience × Competitor Logic)
# ============================================================================

def compute_best_price(product, rnd=None, competitor_price=None):

    # If no competitor price provided → use product price
    competitor_price = competitor_price or float(product.get("price", 0))

    features = product.get("features", [])
    rnd = rnd or {
        "families": 0.8,
        "students": 0.6,
        "women": 0.7,
        "general": 0.5
    }

    MARKET_COEFFICIENT = 4
    segments = ["families", "students", "women", "general"]

    # Matrix for feature × segment impact
    matrix = []
    segment_totals = {}
    segment_prices = {}

    # Build matrix
    for feat in features:
        gap_factor = 1 if feat.get("gap") else 0.4
        seg_obj = {}

        for seg in segments:
            seg_obj[seg] = round(
                feat.get("strength", 1)
                * rnd.get(seg, 0.5)
                * gap_factor
                * MARKET_COEFFICIENT
            )

        matrix.append({
            "name": feat.get("name"),
            "segments": seg_obj
        })

    # Totals per segment
    for seg in segments:
        segment_totals[seg] = sum(f["segments"][seg] for f in matrix)

    # Compute prices per segment
    for seg in segments:
        segment_prices[seg] = competitor_price + segment_totals[seg]

    # Best segment
    best_segment = max(segment_totals, key=segment_totals.get)
    best_price = segment_prices[best_segment]

    return {
        "competitor_price": competitor_price,
        "matrix": matrix,
        "segment_totals": segment_totals,
        "segment_prices": segment_prices,
        "best_segment": best_segment,
        "best_price": best_price
    }

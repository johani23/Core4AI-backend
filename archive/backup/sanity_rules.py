def apply_sanity_checks(data):
    if data.get("credibility",100) < 40 and "engagement" in data:
        data["engagement"] = max(0, data["engagement"] - 10)
    return data

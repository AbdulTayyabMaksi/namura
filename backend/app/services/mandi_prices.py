from __future__ import annotations

MANDI_KEYWORDS = [
    "mandi", "crop", "wheat", "rice", "paddy", "cotton", "sugarcane",
    "tomato", "onion", "potato", "maize", "bajra", "jowar", "agmarknet",
    "farm price", "agricultural price", "कृषि", "ಬೆಳೆ", "मंडी",
]

# Representative mandi prices (₹/quintal) — demo data aligned with Agmarknet patterns
MANDI_PRICES: dict[str, dict] = {
    "wheat": {"price": 2275, "market": "Karnataka APMC", "trend": "+2.1%", "unit": "₹/quintal"},
    "rice": {"price": 3100, "market": "Mandya APMC", "trend": "-0.8%", "unit": "₹/quintal"},
    "paddy": {"price": 2180, "market": "Mandya APMC", "trend": "+1.2%", "unit": "₹/quintal"},
    "cotton": {"price": 6650, "market": "Gujarat APMC", "trend": "+3.4%", "unit": "₹/quintal"},
    "sugarcane": {"price": 340, "market": "Maharashtra", "trend": "MSP linked", "unit": "₹/quintal"},
    "tomato": {"price": 1850, "market": "Kolar APMC", "trend": "-12%", "unit": "₹/quintal"},
    "onion": {"price": 2200, "market": "Lasalgaon APMC", "trend": "+5.6%", "unit": "₹/quintal"},
    "maize": {"price": 1950, "market": "Karnataka APMC", "trend": "+1.8%", "unit": "₹/quintal"},
}


def is_mandi_query(message: str) -> bool:
    msg = message.lower()
    return any(k in msg for k in MANDI_KEYWORDS)


def fetch_mandi_context(message: str, location: str = "") -> str:
    if not is_mandi_query(message):
        return ""

    msg = message.lower()
    matched = [crop for crop in MANDI_PRICES if crop in msg]
    if not matched:
        matched = list(MANDI_PRICES.keys())[:4]

    lines = [f"MANDI / CROP PRICES (Agmarknet-style demo data{f' near {location}' if location else ''}):"]
    for crop in matched[:5]:
        d = MANDI_PRICES[crop]
        lines.append(
            f"\n• {crop.title()}: {d['price']:,} {d['unit']} at {d['market']} (Trend: {d['trend']})"
        )
    lines.append("\nNote: MSP for wheat (2024-25) = ₹2,275/quintal | Paddy = ₹2,300/quintal")
    return "\n".join(lines)

from __future__ import annotations

import re

DISCLAIMER = "This is educational information, not regulated financial advice."

# Only block direct buy/sell recommendations, not educational stock discussion
DIRECT_ADVICE_PATTERNS = [
    r"\byou should (definitely )?buy\b",
    r"\byou should (definitely )?sell\b",
    r"\bi recommend (you )?(buying|selling|investing in)\b",
    r"\bguaranteed returns?\b",
    r"\bwill (definitely )?go up\b",
    r"\bcan't lose\b",
]

ADVICE_REPLACEMENT = (
    "I can share educational information and help you understand the factors involved, "
    "but I cannot recommend specific buy/sell actions — that requires a SEBI-registered "
    "investment advisor. Would you like me to explain what to consider when evaluating this?"
)


def guard_response(content: str, is_crisis: bool = False) -> dict:
    warnings = []

    for pattern in DIRECT_ADVICE_PATTERNS:
        if re.search(pattern, content, re.IGNORECASE):
            content = content + f"\n\n⚠️ {ADVICE_REPLACEMENT}"
            warnings.append("Direct investment advice softened per SEBI compliance")
            break

    if is_crisis:
        warnings.append("Crisis detected — human escalation triggered")

    if DISCLAIMER not in content:
        content = f"{content}\n\n_{DISCLAIMER}_"

    return {
        "content": content,
        "disclaimer": DISCLAIMER,
        "warnings": warnings,
        "approved": True,
    }

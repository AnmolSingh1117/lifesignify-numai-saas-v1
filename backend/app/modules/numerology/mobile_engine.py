# modules/numerology/mobile_engine.py

def analyze_mobile(mobile: str) -> dict:
    if not mobile:
        return {}

    digits = [int(d) for d in mobile if d.isdigit()]
    total = sum(digits)

    while total > 9:
        total = sum(int(d) for d in str(total))

    suggestion = None
    if total in (4, 8):
        suggestion = "Consider adjusting number to reduce 4/8 dominance."

    return {
        "mobile_total": total,
        "correction_suggestion": suggestion
    }


# =====================================================
# PUBLIC WRAPPER (STANDARDIZED NAME)
# =====================================================

def analyze_mobile_number(mobile_number: str) -> dict:
    """
    Public contract wrapper used by core_engine.
    """
    return analyze_mobile(mobile_number)
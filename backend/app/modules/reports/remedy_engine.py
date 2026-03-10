from typing import Dict, Any


# =====================================================
# MANTRA LIBRARY
# =====================================================

NUMBER_MANTRAS = {

    1: {
        "deity": "Surya (Sun)",
        "mantra_sanskrit": "ॐ घृणि सूर्याय नमः",
        "mantra_english": "Om Ghrini Suryaya Namaha",
        "donation": "Donate wheat or jaggery on Sunday",
    },

    2: {
        "deity": "Chandra (Moon)",
        "mantra_sanskrit": "ॐ सोम सोमाय नमः",
        "mantra_english": "Om Som Somaya Namaha",
        "donation": "Donate rice or milk on Monday",
    },

    3: {
        "deity": "Guru (Jupiter)",
        "mantra_sanskrit": "ॐ बृहस्पतये नमः",
        "mantra_english": "Om Brihaspataye Namaha",
        "donation": "Donate yellow sweets or turmeric",
    },

    4: {
        "deity": "Rahu",
        "mantra_sanskrit": "ॐ राहवे नमः",
        "mantra_english": "Om Rahave Namaha",
        "donation": "Donate black sesame or blankets",
    },

    5: {
        "deity": "Budh (Mercury)",
        "mantra_sanskrit": "ॐ बुं बुधाय नमः",
        "mantra_english": "Om Bum Budhaya Namaha",
        "donation": "Donate green vegetables",
    },

    6: {
        "deity": "Shukra (Venus)",
        "mantra_sanskrit": "ॐ शुक्राय नमः",
        "mantra_english": "Om Shukraya Namaha",
        "donation": "Donate white clothes or rice",
    },

    7: {
        "deity": "Ketu",
        "mantra_sanskrit": "ॐ केतवे नमः",
        "mantra_english": "Om Ketave Namaha",
        "donation": "Feed stray dogs",
    },

    8: {
        "deity": "Shani",
        "mantra_sanskrit": "ॐ शं शनैश्चराय नमः",
        "mantra_english": "Om Sham Shanicharaya Namaha",
        "donation": "Donate black clothes or mustard oil",
    },

    9: {
        "deity": "Mangal (Mars)",
        "mantra_sanskrit": "ॐ क्रां क्रीं क्रौं सः भौमाय नमः",
        "mantra_english": "Om Kraam Kreem Kraum Sah Bhaumaya Namaha",
        "donation": "Donate red lentils",
    }

}


# =====================================================
# LUCKY COLORS
# =====================================================

NUMBER_COLORS = {

    1: "Gold / Orange",
    2: "White / Silver",
    3: "Yellow",
    4: "Electric Blue",
    5: "Green",
    6: "Light Blue / Pink",
    7: "Grey / Smoky White",
    8: "Dark Blue / Black",
    9: "Red"
}


# =====================================================
# MOBILE REMEDIES
# =====================================================

def generate_mobile_remedies(number: int) -> Dict[str, Any]:

    color = NUMBER_COLORS.get(number, "Neutral")

    return {

        "mobile_cover_color": color,

        "mobile_wallpaper":
            "Use a calm geometric or sacred symbol background aligned with your ruling number.",

        "charging_direction":
            "Place phone facing East or North while charging.",

        "whatsapp_dp":
            "Use a calm professional image reflecting clarity and confidence.",

        "mobile_usage_timing":
            "Avoid heavy decision making late at night. Use phone mainly during morning or early evening."
    }


# =====================================================
# LIFESTYLE REMEDIES
# =====================================================

def generate_lifestyle_remedies(number: int) -> Dict[str, Any]:

    color = NUMBER_COLORS.get(number)

    return {

        "bracelet_suggestion":
            f"Wear a bracelet using colors aligned with number {number} ({color}).",

        "daily_routine":
            "Maintain disciplined daily schedule with morning sunlight exposure.",

        "meditation":
            "Practice 10 minutes of focused breathing meditation daily.",

        "color_alignment":
            f"Use {color} tones in clothing or workspace."

    }


# =====================================================
# VEDIC REMEDIES
# =====================================================

def generate_vedic_remedies(number: int) -> Dict[str, Any]:

    mantra_data = NUMBER_MANTRAS.get(number)

    if not mantra_data:
        return {}

    return {

        "deity": mantra_data["deity"],

        "mantra_sanskrit": mantra_data["mantra_sanskrit"],

        "mantra_pronunciation": mantra_data["mantra_english"],

        "recommended_donation": mantra_data["donation"],

        "practice_guideline":
            "Chant the mantra 108 times every morning for 21 days."
    }


# =====================================================
# MASTER REMEDY GENERATOR
# =====================================================

def generate_remedy_protocol(numerology_core: Dict[str, Any]) -> Dict[str, Any]:

    pythagorean = numerology_core.get("pythagorean", {})

    mulank = pythagorean.get("life_path_number", 0)

    if not mulank:
        return {}

    return {

        "lifestyle_remedies": generate_lifestyle_remedies(mulank),

        "mobile_remedies": generate_mobile_remedies(mulank),

        "vedic_remedies": generate_vedic_remedies(mulank)

    }
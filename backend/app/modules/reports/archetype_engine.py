from typing import Dict, Any


# =====================================================
# CORE NUMEROLOGY ARCHETYPES
# =====================================================

LIFE_PATH_ARCHETYPES = {

    1: {
        "title": "Strategic Leader",
        "description":
            "Independent, pioneering, and naturally inclined toward leadership. "
            "People with this energy are driven to create their own path and influence systems around them."
    },

    2: {
        "title": "Empathic Advisor",
        "description":
            "Diplomatic, emotionally intelligent, and relationship-oriented. "
            "This archetype thrives when helping others find balance and harmony."
    },

    3: {
        "title": "Creative Communicator",
        "description":
            "Expressive, imaginative, and charismatic. "
            "These individuals influence the world through ideas, communication, and creativity."
    },

    4: {
        "title": "Strategic Builder",
        "description":
            "Disciplined, practical, and system-oriented. "
            "This archetype excels at building stable foundations and structured environments."
    },

    5: {
        "title": "Adaptive Explorer",
        "description":
            "Dynamic, curious, and freedom-seeking. "
            "These individuals evolve through new experiences and intellectual exploration."
    },

    6: {
        "title": "Responsible Guardian",
        "description":
            "Supportive, caring, and protective. "
            "This archetype often becomes the stabilizing force within family or community systems."
    },

    7: {
        "title": "Analytical Seeker",
        "description":
            "Deep thinker, researcher, and observer of patterns. "
            "People with this archetype often pursue knowledge, philosophy, or technical mastery."
    },

    8: {
        "title": "Power Architect",
        "description":
            "Strategic, ambitious, and focused on achievement. "
            "This archetype seeks influence, material growth, and large-scale impact."
    },

    9: {
        "title": "Humanitarian Visionary",
        "description":
            "Idealistic, compassionate, and globally minded. "
            "These individuals often feel drawn to contribute to society in meaningful ways."
    }

}


# =====================================================
# ARCHETYPE MODIFIERS (DESTINY NUMBER)
# =====================================================

DESTINY_MODIFIERS = {

    1: "Independent",
    2: "Diplomatic",
    3: "Creative",
    4: "Structured",
    5: "Dynamic",
    6: "Responsible",
    7: "Analytical",
    8: "Ambitious",
    9: "Visionary"

}


# =====================================================
# BEHAVIORAL STYLE MODIFIER
# =====================================================

def derive_behavior_modifier(scores: Dict[str, Any]) -> str:

    if not scores:
        return "Balanced"

    emotional = scores.get("emotional_regulation_index", 50)
    financial = scores.get("financial_discipline_index", 50)
    stability = scores.get("life_stability_index", 50)

    if emotional > 75 and stability > 70:
        return "Stable Strategist"

    if financial > 70:
        return "Resource Optimizer"

    if emotional < 40:
        return "Emotionally Reactive"

    return "Adaptive Thinker"


# =====================================================
# ARCHETYPE GENERATOR
# =====================================================

def generate_numerology_archetype(
    numerology_core: Dict[str, Any],
    scores: Dict[str, Any]
) -> Dict[str, Any]:

    pyth = numerology_core.get("pythagorean", {})

    life_path = pyth.get("life_path_number", 0)
    destiny = pyth.get("destiny_number", 0)

    base = LIFE_PATH_ARCHETYPES.get(life_path)

    if not base:
        return {}

    destiny_modifier = DESTINY_MODIFIERS.get(destiny, "Strategic")

    behavior_modifier = derive_behavior_modifier(scores)

    archetype_title = f"{destiny_modifier} {base['title']}"

    return {

        "archetype_name": archetype_title,

        "core_archetype": base["title"],

        "behavior_style": behavior_modifier,

        "description": base["description"],

        "interpretation":
            f"This profile combines the strategic traits of a {base['title']} "
            f"with a {destiny_modifier.lower()} expression style. "
            f"Behavioral indicators further suggest a '{behavior_modifier}' pattern "
            f"in decision making and life strategy."

    }
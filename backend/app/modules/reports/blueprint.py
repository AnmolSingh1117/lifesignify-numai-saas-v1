from typing import Dict, List


SECTION_TITLES: Dict[str, str] = {
    "executive_summary": "Executive Summary",
    "core_numbers_analysis": "Core Numbers Analysis",
    "mulank_description": "Mulank Description",
    "bhagyank_description": "Bhagyank Description",
    "name_number_analysis": "Name Number Analysis",
    "number_interaction_analysis": "Number Interaction Analysis",
    "loshu_grid_interpretation": "Lo Shu Grid Interpretation",
    "missing_numbers_analysis": "Missing Numbers Analysis",
    "repeating_numbers_impact": "Repeating Numbers Impact",
    "mobile_number_numerology": "Mobile Number Numerology",
    "mobile_life_number_compatibility": "Mobile + Life Number Compatibility",
    "personality_intelligence": "Personality Intelligence",
    "current_problem_analysis": "Current Problem Analysis",
    "career_wealth_strategy": "Career & Wealth Strategy",
    "relationship_patterns": "Relationship Patterns",
    "health_signals": "Health Signals",
    "personal_year_forecast": "Personal Year Forecast",
    "lucky_numbers": "Lucky Numbers",
    "color_alignment": "Color Alignment",
    "remedies_lifestyle_adjustments": "Remedies and Lifestyle Adjustments",
    "strategic_growth_blueprint": "Strategic Growth Blueprint",
}


TIER_SECTION_KEYS: Dict[str, List[str]] = {
    "basic": [
        "executive_summary",
        "core_numbers_analysis",
        "mulank_description",
        "bhagyank_description",
        "name_number_analysis",
        "loshu_grid_interpretation",
        "mobile_number_numerology",
        "personality_intelligence",
        "career_wealth_strategy",
        "remedies_lifestyle_adjustments",
    ],
    "pro": [
        "executive_summary",
        "core_numbers_analysis",
        "mulank_description",
        "bhagyank_description",
        "name_number_analysis",
        "number_interaction_analysis",
        "loshu_grid_interpretation",
        "missing_numbers_analysis",
        "repeating_numbers_impact",
        "mobile_number_numerology",
        "mobile_life_number_compatibility",
        "personality_intelligence",
        "current_problem_analysis",
        "career_wealth_strategy",
        "color_alignment",
        "remedies_lifestyle_adjustments",
        "strategic_growth_blueprint",
    ],
    "premium": [
        "executive_summary",
        "core_numbers_analysis",
        "mulank_description",
        "bhagyank_description",
        "name_number_analysis",
        "number_interaction_analysis",
        "loshu_grid_interpretation",
        "missing_numbers_analysis",
        "repeating_numbers_impact",
        "mobile_number_numerology",
        "mobile_life_number_compatibility",
        "personality_intelligence",
        "current_problem_analysis",
        "career_wealth_strategy",
        "relationship_patterns",
        "health_signals",
        "lucky_numbers",
        "color_alignment",
        "remedies_lifestyle_adjustments",
        "strategic_growth_blueprint",
    ],
    "enterprise": [
        "executive_summary",
        "core_numbers_analysis",
        "mulank_description",
        "bhagyank_description",
        "name_number_analysis",
        "number_interaction_analysis",
        "loshu_grid_interpretation",
        "missing_numbers_analysis",
        "repeating_numbers_impact",
        "mobile_number_numerology",
        "mobile_life_number_compatibility",
        "personality_intelligence",
        "current_problem_analysis",
        "career_wealth_strategy",
        "relationship_patterns",
        "health_signals",
        "personal_year_forecast",
        "lucky_numbers",
        "color_alignment",
        "remedies_lifestyle_adjustments",
        "strategic_growth_blueprint",
    ],
}


def get_tier_section_blueprint(plan_name: str) -> Dict[str, object]:
    tier = (plan_name or "basic").strip().lower()
    section_keys = TIER_SECTION_KEYS.get(tier, TIER_SECTION_KEYS["basic"])

    return {
        "plan_tier": tier,
        "section_count": len(section_keys),
        "sections": [
            {
                "order": index,
                "key": key,
                "title": SECTION_TITLES[key],
            }
            for index, key in enumerate(section_keys, start=1)
        ],
    }


def get_all_tier_section_blueprints() -> Dict[str, Dict[str, object]]:
    return {
        tier: get_tier_section_blueprint(tier)
        for tier in ("basic", "pro", "premium", "enterprise")
    }

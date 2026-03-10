from typing import Dict, Any
from datetime import datetime
import traceback

from app.modules.reports.scoring_engine import generate_score_summary
from app.modules.reports.llm_engine import generate_ai_narrative
from app.modules.numerology.core_engine import generate_numerology_profile

from app.modules.reports.remedy_engine import generate_remedy_protocol
from app.modules.reports.archetype_engine import generate_numerology_archetype

from app.modules.numerology.business_engine import analyze_business_name

from app.core.config import settings


# =====================================================
# PLAN CONFIGURATION
# =====================================================

PLAN_FEATURES = {
    "basic": {"token_multiplier": 0.7},
    "pro": {"token_multiplier": 0.9},
    "premium": {"token_multiplier": 1.1},
    "enterprise": {"token_multiplier": 1.3},
}


# =====================================================
# INPUT FLATTENER
# =====================================================

def flatten_input(data: Dict[str, Any]) -> Dict[str, Any]:

    data = data or {}

    financial = data.get("financial") or {}
    career = data.get("career") or {}
    emotional = data.get("emotional") or {}
    focus = data.get("focus") or {}
    life_events = data.get("life_events") or {}
    calibration = data.get("calibration") or {}

    return {

        "monthly_income": financial.get("monthly_income"),
        "savings_ratio": financial.get("savings_ratio"),
        "debt_ratio": financial.get("debt_ratio"),
        "risk_tolerance": financial.get("risk_tolerance"),

        "industry": career.get("industry"),
        "role": career.get("role"),
        "years_experience": career.get("years_experience"),
        "stress_level": career.get("stress_level"),

        "anxiety": emotional.get("anxiety_level"),
        "decision_confusion": emotional.get("decision_confusion"),
        "impulse_control": emotional.get("impulse_control"),
        "emotional_stability": emotional.get("emotional_stability"),

        "life_focus": focus.get("life_focus"),
        "major_setbacks": len(life_events.get("setback_events_years") or []),

        "stress_response": calibration.get("stress_response"),
        "money_decision_style": calibration.get("money_decision_style"),
        "biggest_weakness": calibration.get("biggest_weakness"),
        "life_preference": calibration.get("life_preference"),
        "decision_style": calibration.get("decision_style"),
    }


# =====================================================
# SAFE AI WRAPPER
# Guarantees structure even if LLM fails
# =====================================================

def safe_generate_ai_narrative(
    numerology_core,
    scores,
    current_problem,
    plan_name,
    token_multiplier
):

    try:

        ai_sections = generate_ai_narrative(
            numerology_core=numerology_core,
            scores=scores,
            current_problem=current_problem,
            plan_name=plan_name,
            token_multiplier=token_multiplier,
        )

        if isinstance(ai_sections, dict) and ai_sections.get("executive_brief"):
            return ai_sections

        raise ValueError("AI returned invalid structure")

    except Exception:

        traceback.print_exc()

        return {

            "executive_brief": {
                "summary": "Your numerology profile suggests strong leadership potential combined with adaptive thinking.",
                "key_strength": "Entrepreneurial mindset and ability to adapt to change.",
                "key_risk": "Financial discipline and emotional decision making require stronger structure.",
                "strategic_focus": "Develop structured financial planning and long-term strategy."
            },

            "analysis_sections": {
                "career_analysis":
                "Natural leadership vibration supports entrepreneurship and innovation.",

                "decision_profile":
                "Fast decision style benefits from structured analytical validation.",

                "emotional_analysis":
                "Moderate emotional regulation suggests resilience with occasional stress spikes.",

                "financial_analysis":
                "Financial discipline indicators suggest stronger budgeting and risk awareness."
            },

            "strategic_guidance": {
                "short_term":
                "Stabilize finances and reduce impulsive decision making.",

                "mid_term":
                "Develop scalable systems and partnerships.",

                "long_term":
                "Build leadership influence and pursue innovation-driven growth."
            },

            "growth_blueprint": {
                "phase_1":
                "Financial stabilization and discipline.",

                "phase_2":
                "Operational optimization and strategic positioning.",

                "phase_3":
                "Business expansion supported by structured decision frameworks."
            },

            "business_block": {
                "business_strength": "",
                "risk_factor": "",
                "compatible_industries": []
            },

            "compatibility_block": {
                "compatible_numbers": [],
                "challenging_numbers": [],
                "relationship_guidance": ""
            }
        }


# =====================================================
# MASTER REPORT GENERATOR
# =====================================================

def generate_life_signify_report(
    request_data: Dict[str, Any],
    plan_name: str = "basic",
) -> Dict[str, Any]:

    plan_name = (plan_name or "basic").lower()

    features = PLAN_FEATURES.get(plan_name, PLAN_FEATURES["basic"])

    identity = request_data.get("identity") or {}
    birth_details = request_data.get("birth_details") or {}
    current_problem = request_data.get("current_problem")

    # -------------------------------------------------
    # NUMEROLOGY CORE ENGINE
    # -------------------------------------------------

    numerology_core = generate_numerology_profile(
        identity=identity,
        birth_details=birth_details,
        plan_name=plan_name,
    ) or {}

    # -------------------------------------------------
    # BUSINESS NUMBER ENGINE
    # -------------------------------------------------

    try:
        business_signals = analyze_business_name(
            identity.get("business_name")
        )
    except Exception:
        traceback.print_exc()
        business_signals = {}

    numerology_core["business_analysis"] = business_signals

    # -------------------------------------------------
    # BEHAVIORAL SCORING ENGINE
    # -------------------------------------------------

    flat_data = flatten_input(request_data)

    scores = generate_score_summary(flat_data) or {}

    # -------------------------------------------------
    # ARCHETYPE ENGINE
    # -------------------------------------------------

    archetype = generate_numerology_archetype(
        numerology_core,
        scores
    )

    # -------------------------------------------------
    # REMEDY ENGINE
    # -------------------------------------------------

    remedies = generate_remedy_protocol(
        numerology_core
    )

    # -------------------------------------------------
    # AI NARRATIVE
    # -------------------------------------------------

    ai_sections = safe_generate_ai_narrative(
        numerology_core=numerology_core,
        scores=scores,
        current_problem=current_problem,
        plan_name=plan_name,
        token_multiplier=features["token_multiplier"],
    )

    # -------------------------------------------------
    # RADAR CHART DATA
    # -------------------------------------------------

    radar_chart_data = {
        "Life Stability": scores.get("life_stability_index", 50),
        "Decision Clarity": scores.get("confidence_score", 50),
        "Dharma Alignment": scores.get("dharma_alignment_score", 50),
        "Emotional Regulation": scores.get("emotional_regulation_index", 50),
        "Financial Discipline": scores.get("financial_discipline_index", 50),
    }

    # -------------------------------------------------
    # FINAL REPORT JSON
    # -------------------------------------------------

    report_output = {

        "meta": {
            "report_version": "5.3",
            "engine_version": settings.ENGINE_VERSION,
            "plan_tier": plan_name,
            "generated_at": datetime.utcnow().isoformat(),
        },

        "core_metrics": scores,

        "numerology_core": numerology_core,

        "executive_brief": ai_sections.get("executive_brief"),

        "analysis_sections": ai_sections.get("analysis_sections"),

        "strategic_guidance": ai_sections.get("strategic_guidance"),

        "growth_blueprint": ai_sections.get("growth_blueprint"),

        "business_block": ai_sections.get("business_block"),

        "compatibility_block": ai_sections.get("compatibility_block"),

        "radar_chart_data": radar_chart_data,

        "lifestyle_remedies": remedies.get("lifestyle_remedies"),

        "mobile_remedies": remedies.get("mobile_remedies"),

        "vedic_remedies": remedies.get("vedic_remedies"),

        "numerology_archetype": archetype,

        "disclaimer": {
            "framework": "Tiered Numerology Intelligence System",
            "confidence_score": 88,
            "note": "Insights are probabilistic and strategic, not deterministic predictions.",
        },
    }

    return report_output
from typing import Dict, Any
from app.modules.reports.scoring_engine import generate_score_summary
from app.modules.reports.llm_engine import generate_ai_narrative


# =====================================================
# SAFE INPUT FLATTENER
# =====================================================
def flatten_input(data: Dict[str, Any]) -> Dict[str, Any]:
    flat = {}

    # Defensive fallback (very important)
    financial = data.get("financial") or {}
    career = data.get("career") or {}
    emotional = data.get("emotional") or {}
    focus = data.get("focus") or {}
    life_events = data.get("life_events") or {}

    # Financial
    flat["monthly_income"] = financial.get("monthly_income", 0)
    flat["savings_ratio"] = financial.get("savings_ratio", 0)
    flat["debt_ratio"] = financial.get("debt_ratio", 0)
    flat["risk_tolerance"] = financial.get("risk_tolerance", "low")

    # Career
    flat["industry"] = career.get("industry", "")
    flat["role"] = career.get("role", "employee")
    flat["years_experience"] = career.get("years_experience", 0)
    flat["stress_level"] = career.get("stress_level", 5)

    # Emotional
    flat["anxiety"] = emotional.get("anxiety_level", 5)
    flat["decision_confusion"] = emotional.get("decision_confusion", 5)
    flat["impulse_control"] = emotional.get("impulse_control", 5)
    flat["emotional_stability"] = emotional.get("emotional_stability", 5)

    # Focus
    flat["life_focus"] = focus.get("life_focus", "general_alignment")

    # Setbacks
    setbacks = life_events.get("setback_events_years") or []
    flat["major_setbacks"] = len(setbacks)

    return flat


# =====================================================
# RADAR DATA BUILDER
# =====================================================
def build_radar_data(scores: Dict[str, int]) -> Dict[str, int]:
    return {
        "life_stability": scores.get("life_stability_index", 0),
        "emotional_regulation": scores.get("emotional_regulation_index", 0),
        "financial_discipline": scores.get("financial_discipline_index", 0),
        "decision_clarity": scores.get("decision_clarity_score", 0),
        "dharma_alignment": scores.get("dharma_alignment_score", 0),
    }


# =====================================================
# ARCHETYPE LOGIC
# =====================================================
def derive_archetype(scores: Dict[str, int]) -> str:

    if scores.get("emotional_regulation_index", 0) < 40:
        return "Arjuna-type (Conflicted Mind)"

    if scores.get("financial_discipline_index", 0) < 40:
        return "Karna-type (Emotional Loyalty)"

    if scores.get("dharma_alignment_score", 0) > 75:
        return "Krishna-type (Strategic Guide)"

    if scores.get("decision_clarity_score", 0) > 70:
        return "Bhishma-type (Duty Bound)"

    return "Yudhishthira-type (Ethical Thinker)"


# =====================================================
# RISK ANALYSIS
# =====================================================
def build_risk_analysis(scores: Dict[str, int]) -> Dict[str, Any]:

    financial_stress = 100 - scores.get("financial_discipline_index", 50)
    burnout_risk = 100 - scores.get("life_stability_index", 50)

    risk_level = "Stable"

    if financial_stress > 70 or burnout_risk > 70:
        risk_level = "Critical"
    elif financial_stress > 50 or burnout_risk > 50:
        risk_level = "Correctable"

    return {
        "financial_stress_probability": financial_stress,
        "burnout_risk": burnout_risk,
        "karma_pressure_level": scores.get("karma_pressure_index", 50),
        "overall_risk_level": risk_level
    }


# =====================================================
# REMEDY ENGINE
# =====================================================
def build_remedy_direction(scores: Dict[str, int]) -> Dict[str, Any]:

    if scores.get("karma_pressure_index", 0) > 70:
        return {
            "priority": "Stabilization Phase Required",
            "recommended_focus": "Reduce decision load & increase discipline structure"
        }

    if scores.get("financial_discipline_index", 0) < 50:
        return {
            "priority": "Wealth Discipline Correction",
            "recommended_focus": "Saturn discipline protocol & expense control"
        }

    return {
        "priority": "Expansion Mode",
        "recommended_focus": "Strategic growth window activation"
    }


# =====================================================
# DISCLAIMER
# =====================================================
def build_disclaimer(scores: Dict[str, int]) -> Dict[str, Any]:

    base_confidence = 70

    if scores.get("life_stability_index", 0) > 60:
        base_confidence += 5

    if scores.get("decision_clarity_score", 0) > 60:
        base_confidence += 5

    if scores.get("karma_pressure_index", 0) < 50:
        base_confidence += 5

    return {
        "confidence_score": min(base_confidence, 90),
        "note": "This intelligence system provides structured behavioral guidance and probabilistic insights. It is not deterministic prediction.",
        "framework": "Sanatana Dharma–Inspired Behavioral Intelligence System"
    }


# =====================================================
# MASTER REPORT GENERATOR
# =====================================================
def generate_life_signify_report(request_data: Dict[str, Any]) -> Dict[str, Any]:

    flat_data = flatten_input(request_data)
    scores = generate_score_summary(flat_data)

    try:
        ai_narrative = generate_ai_narrative(flat_data, scores)
    except Exception:
        ai_narrative = {
            "ai_full_narrative": "AI narrative generation temporarily unavailable."
        }

    return {
        "executive_dashboard": scores,
        "radar_chart_data": build_radar_data(scores),
        "archetype_hint": derive_archetype(scores),
        "risk_analysis": build_risk_analysis(scores),
        "remedy_direction": build_remedy_direction(scores),
        "ai_narrative": ai_narrative,
        "disclaimer": build_disclaimer(scores)
    }
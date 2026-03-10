from typing import Dict, Any
from app.core.llm_config import azure_client, DEPLOYMENT_NAME
import json
import logging

logger = logging.getLogger(__name__)

# =====================================================
# TOKEN LIMIT PER PLAN
# =====================================================

PLAN_TOKEN_BASE = {
    "basic": 1600,
    "pro": 2200,
    "premium": 3000,
    "enterprise": 3800,
}

# =====================================================
# SAFE JSON PARSER
# =====================================================

def _safe_json_parse(raw_text: str) -> Dict[str, Any]:

    if not raw_text:
        return {}

    try:
        return json.loads(raw_text)

    except Exception:

        try:

            start = raw_text.index("{")
            end = raw_text.rindex("}") + 1

            return json.loads(raw_text[start:end])

        except Exception:

            logger.error("AI JSON parsing failed")

            return {}

# =====================================================
# MAIN AI REPORT GENERATOR
# =====================================================

def generate_ai_narrative(
    numerology_core: Dict[str, Any],
    scores: Dict[str, Any],
    current_problem: str,
    plan_name: str,
    token_multiplier: float = 1.0,
) -> Dict[str, Any]:

    plan_name = (plan_name or "basic").lower()

    base_tokens = PLAN_TOKEN_BASE.get(plan_name, 1600)

    max_tokens = int(base_tokens * token_multiplier)

    business_signals = numerology_core.get("business_analysis", {})

    prompt = f"""
You are an elite numerology strategist and behavioral intelligence advisor.

Do NOT calculate numerology numbers.

All numerology calculations are already provided.

Your task is to interpret them and generate a strategic life intelligence report.

Blend:

• numerology wisdom
• behavioral psychology
• strategic advisory thinking

Write insights like a personalized consulting document rather than a mystical prediction.

--------------------------------------------------

USER CURRENT PROBLEM
{current_problem}

--------------------------------------------------

NUMEROLOGY CORE DATA
{numerology_core}

--------------------------------------------------

BUSINESS NUMEROLOGY SIGNALS
{business_signals}

--------------------------------------------------

BEHAVIORAL INTELLIGENCE SCORES
{scores}

--------------------------------------------------

PLAN TIER
{plan_name.upper()}

Depth of analysis should increase with plan tier.

--------------------------------------------------

STRICT OUTPUT RULES

Return VALID JSON ONLY.

Do NOT include markdown.

Do NOT include explanations outside JSON.

Keep responses structured and professional.

--------------------------------------------------

REQUIRED JSON STRUCTURE

{{
 "executive_brief": {{
   "summary": "",
   "key_strength": "",
   "key_risk": "",
   "strategic_focus": ""
 }},

 "analysis_sections": {{
   "career_analysis": "",
   "decision_profile": "",
   "emotional_analysis": "",
   "financial_analysis": ""
 }},

 "strategic_guidance": {{
   "short_term": "",
   "mid_term": "",
   "long_term": ""
 }},

 "growth_blueprint": {{
   "phase_1": "",
   "phase_2": "",
   "phase_3": ""
 }},

 "business_block": {{
   "business_strength": "",
   "risk_factor": "",
   "compatible_industries": []
 }},

 "compatibility_block": {{
   "compatible_numbers": [],
   "challenging_numbers": [],
   "relationship_guidance": ""
 }}
}}
"""

    try:

        response = azure_client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": """
You are an elite numerology strategist and behavioral intelligence advisor.

Do NOT calculate numerology numbers.

All numerology calculations are already provided.

Your task is to interpret them and generate a strategic life intelligence report.

Blend:

• numerology wisdom
• behavioral psychology
• strategic advisory thinking

Write insights like a personalized consulting document rather than mystical predictions.
"""
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.35,
            max_tokens=max_tokens,
        )

        raw_text = response.choices[0].message.content.strip()

        structured_output = _safe_json_parse(raw_text)

        if not structured_output:

            raise ValueError("Invalid JSON from AI")

        return structured_output

    except Exception as e:

        logger.error(f"AI generation failed: {str(e)}")

        # Safe fallback structure

        return {

            "executive_brief": {
                "summary": "",
                "key_strength": "",
                "key_risk": "",
                "strategic_focus": ""
            },

            "analysis_sections": {
                "career_analysis": "",
                "decision_profile": "",
                "emotional_analysis": "",
                "financial_analysis": ""
            },

            "strategic_guidance": {
                "short_term": "",
                "mid_term": "",
                "long_term": ""
            },

            "growth_blueprint": {
                "phase_1": "",
                "phase_2": "",
                "phase_3": ""
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
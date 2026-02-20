from typing import Dict, Any
from app.core.llm_config import azure_client, DEPLOYMENT_NAME


def generate_ai_narrative(
    flat_data: Dict[str, Any],
    scores: Dict[str, Any]
) -> Dict[str, Any]:

    prompt = f"""
You are an elite behavioral intelligence system.

User Behavioral Scores:
{scores}

User Profile Data:
{flat_data}

Generate:

1. Executive Summary (professional tone)
2. Psychological Pattern Analysis
3. Strategic Advice
4. 30-Day Action Plan
5. 90-Day Growth Plan

Be precise. Avoid fluff. Keep it structured.
"""

    try:
        response = azure_client.chat.completions.create(
            model=DEPLOYMENT_NAME,
            messages=[
                {
                    "role": "system",
                    "content": "You are a strategic behavioral intelligence analyst."
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0.7,
            max_tokens=1500,
        )

        text = response.choices[0].message.content

        return {
            "ai_full_narrative": text
        }

    except Exception as e:
        return {
            "ai_full_narrative": "AI narrative generation temporarily unavailable.",
            "error": str(e)
        }
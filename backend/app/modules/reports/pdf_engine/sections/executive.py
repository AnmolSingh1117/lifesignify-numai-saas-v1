from reportlab.platypus import PageBreak, Spacer

from ..assets import OM_SYMBOL


def build_executive(elements, renderer, styles, data):
    executive = data.get("executive_brief", {})
    summary = executive.get("summary")

    if not summary:
        return

    elements.append(renderer.section_banner("Executive Summary"))

    elements.append(
        renderer.icon_block(
            OM_SYMBOL,
            "Strategic Summary",
            summary,
        )
    )

    elements.append(Spacer(1, 10))

    strength_text = executive.get("key_strength", "No strengths provided.")
    risk_text = executive.get("key_risk", "No risks provided.")
    elements.append(renderer.two_column_cards("Strength Snapshot", strength_text, "Risk Snapshot", risk_text))

    elements.append(Spacer(1, 10))

    outlook = data.get("strategic_guidance", {}).get(
        "short_term",
        executive.get("strategic_focus", "Build disciplined systems and execute in phases."),
    )
    elements.append(renderer.insight_box("Next Phase Outlook", outlook, tone="info"))

    elements.append(PageBreak())

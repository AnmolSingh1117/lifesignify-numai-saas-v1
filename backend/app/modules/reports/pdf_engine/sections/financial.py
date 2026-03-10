from reportlab.platypus import PageBreak, Spacer


def build_financial(elements, renderer, styles, data):
    analysis = data.get("analysis_sections", {})
    text = analysis.get("financial_analysis")

    if not text or not str(text).strip():
        return

    elements.append(renderer.section_banner("Financial Intelligence"))

    elements.append(renderer.insight_box("Financial Reading", text, tone="info"))
    elements.append(Spacer(1, 8))

    actions = [
        "Set monthly budget discipline checkpoints",
        "Track cash flow weekly with variance alerts",
        "Allocate strategic capital to long-term compounding",
    ]
    elements.append(renderer.bullet_block("Actionable Financial Guidance", actions))
    elements.append(Spacer(1, 8))

    score = data.get("core_metrics", {}).get("financial_discipline_index", 0)
    explanation = (
        f"Financial Stability Score: <b>{score}</b>. "
        "Higher score indicates consistent execution in savings, controls, and investment governance."
    )
    elements.append(renderer.insight_box("Score Interpretation", explanation, tone="neutral"))

    elements.append(PageBreak())

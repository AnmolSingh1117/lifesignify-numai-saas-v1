from reportlab.platypus import PageBreak, Spacer


def build_business(elements, renderer, styles, data):
    business = data.get("business_block", {})

    if not business:
        return

    elements.append(renderer.section_banner("Business Intelligence"))

    strength = business.get("business_strength", "No business strength available.")
    risk = business.get("risk_factor", "No business risk available.")

    elements.append(renderer.two_column_cards("Business Strength", strength, "Business Risk", risk))
    elements.append(Spacer(1, 8))

    industries = business.get("compatible_industries", [])
    if industries:
        formatted = [str(item).replace("_", " ").title() for item in industries]
        elements.append(renderer.bullet_block("Recommended Business Verticals", formatted))

    elements.append(PageBreak())

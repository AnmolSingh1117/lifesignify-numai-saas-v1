from reportlab.platypus import PageBreak, Spacer


def build_lifestyle(elements, renderer, styles, data):
    life = data.get("lifestyle_remedies", {})

    if not life:
        return

    elements.append(renderer.section_banner("Lifestyle Alignment"))

    elements.append(renderer.insight_box("Color Alignment", life.get("color_alignment", "Use balancing tones in your environment."), tone="info"))
    elements.append(Spacer(1, 8))

    habits = [
        life.get("daily_routine", "Build daily consistency."),
        life.get("meditation", "Practice mindful reset each day."),
        life.get("bracelet_suggestion", "Use symbolic anchors to reinforce habit identity."),
    ]
    elements.append(renderer.bullet_block("Daily Habits", habits))
    elements.append(Spacer(1, 8))

    environment = "Align workspace, colors, and routines to reduce noise and improve strategic clarity."
    elements.append(renderer.insight_box("Environment Alignment", environment, tone="neutral"))

    elements.append(PageBreak())

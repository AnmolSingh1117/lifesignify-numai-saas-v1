from reportlab.platypus import PageBreak, Spacer


def build_mobile(elements, renderer, styles, data):
    mobile = data.get("mobile_remedies", {})

    if not mobile:
        return

    elements.append(renderer.section_banner("Digital Discipline Alignment"))

    usage = mobile.get("mobile_usage_timing", "Restrict low-value screen time in high-focus windows.")
    focus = mobile.get("whatsapp_dp", "Use digital identity cues aligned to clarity and discipline.")
    env = mobile.get("charging_direction", "Maintain a fixed charging setup to support routine discipline.")

    elements.append(renderer.insight_box("Phone Usage Timing", usage, tone="info"))
    elements.append(Spacer(1, 8))
    elements.append(renderer.insight_box("Focus Discipline", focus, tone="neutral"))
    elements.append(Spacer(1, 8))
    elements.append(renderer.insight_box("Environment Setup", env, tone="neutral"))

    elements.append(PageBreak())

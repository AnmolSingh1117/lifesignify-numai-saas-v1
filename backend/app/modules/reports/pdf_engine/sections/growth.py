from reportlab.platypus import PageBreak, Spacer, Table, TableStyle


def build_growth(elements, renderer, styles, data):
    growth = data.get("growth_blueprint", {})

    if not growth:
        return

    elements.append(renderer.section_banner("Growth Blueprint"))

    cards = [
        renderer.insight_box("Stabilization", growth.get("phase_1", "Stabilize core systems."), tone="neutral"),
        renderer.insight_box("Alignment", growth.get("phase_2", "Align execution to strategy."), tone="info"),
        renderer.insight_box("Expansion", growth.get("phase_3", "Scale with governance."), tone="success"),
    ]

    grid = Table([cards], colWidths=[156, 156, 156])
    grid.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )

    elements.append(grid)
    elements.append(Spacer(1, 8))

    elements.append(renderer.insight_box("Execution Note", "Move to the next phase only when current metrics stabilize.", tone="neutral"))

    elements.append(PageBreak())


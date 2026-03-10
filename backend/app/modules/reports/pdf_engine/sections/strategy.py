from reportlab.lib.colors import HexColor
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle


def build_strategy(elements, renderer, styles, data):
    strategy = data.get("strategic_guidance", {})

    if not strategy:
        return

    elements.append(renderer.section_banner("Strategic Guidance"))

    header = [
        Paragraph("<b>Strategic Phase</b>", styles["BodyText"]),
        Paragraph("<b>Focus</b>", styles["BodyText"]),
    ]

    rows = [
        [
            Paragraph("Phase 1: Stabilization", styles["BodyText"]),
            Paragraph(strategy.get("short_term", "Stabilize operations and priorities."), styles["BodyText"]),
        ],
        [
            Paragraph("Phase 2: Restructuring", styles["BodyText"]),
            Paragraph(strategy.get("mid_term", "Restructure systems and leverage points."), styles["BodyText"]),
        ],
        [
            Paragraph("Phase 3: Expansion", styles["BodyText"]),
            Paragraph(strategy.get("long_term", "Scale high-performing patterns."), styles["BodyText"]),
        ],
    ]

    timeline = Table([header] + rows, colWidths=[150, 320])
    timeline.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), HexColor("#1b2f4b")),
                ("TEXTCOLOR", (0, 0), (-1, 0), HexColor("#ffffff")),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("GRID", (0, 0), (-1, -1), 0.6, HexColor("#d1d8e0")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )

    elements.append(timeline)
    elements.append(Spacer(1, 8))

    elements.append(
        renderer.insight_box(
            "Strategic Interpretation",
            "Execute in phases: stabilize first, then redesign systems, then scale where metrics confirm resilience.",
            tone="neutral",
        )
    )

    elements.append(PageBreak())

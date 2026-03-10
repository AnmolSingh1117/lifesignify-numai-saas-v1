from reportlab.lib.colors import HexColor
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle


def build_decision(elements, renderer, styles, data):
    analysis = data.get("analysis_sections", {})
    text = analysis.get("decision_profile")

    if not text:
        return

    elements.append(renderer.section_banner("Decision Intelligence"))

    elements.append(renderer.insight_box("Decision Interpretation", text, tone="info"))
    elements.append(Spacer(1, 8))

    framework_rows = [
        ["Strategic Fit", "Alignment with long-term mission"],
        ["Financial Sustainability", "Resource viability and runway"],
        ["Long-term Impact", "Durability beyond short-term gains"],
        ["Emotional Alignment", "Cognitive clarity under pressure"],
    ]

    rows = [
        [
            Paragraph("<b>Decision Framework</b>", styles["BodyText"]),
            Paragraph("<b>Strategic Lens</b>", styles["BodyText"]),
        ]
    ]
    for left, right in framework_rows:
        rows.append([Paragraph(left, styles["BodyText"]), Paragraph(right, styles["BodyText"])])

    table = Table(rows, colWidths=[140, 330])
    table.setStyle(
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
    elements.append(table)

    elements.append(PageBreak())

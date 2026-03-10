from reportlab.lib.colors import HexColor
from reportlab.platypus import PageBreak, Paragraph, Spacer, Table, TableStyle


def build_numerology(elements, renderer, styles, data):
    core = data.get("numerology_core", {})

    p = core.get("pythagorean", {})
    c = core.get("chaldean", {})
    email = core.get("email_analysis", {})

    elements.append(renderer.section_banner("Core Numerology Architecture"))

    rows = [
        ["Life Path", p.get("life_path_number", "N/A"), "Strategic direction and purpose path"],
        ["Destiny", p.get("destiny_number", "N/A"), "Execution style in outer world"],
        ["Expression", p.get("expression_number", "N/A"), "Natural talent communication pattern"],
        ["Name Number", c.get("name_number", "N/A"), "Brand and social vibration"],
        ["Email Number", email.get("email_number", "N/A"), "Digital identity signal"],
    ]

    table_rows = [
        [
            Paragraph("<b>Number</b>", styles["BodyText"]),
            Paragraph("<b>Value</b>", styles["BodyText"]),
            Paragraph("<b>Interpretation</b>", styles["BodyText"]),
        ]
    ]
    for label, value, interpretation in rows:
        table_rows.append(
            [
                Paragraph(str(label), styles["BodyText"]),
                Paragraph(str(value), styles["BodyText"]),
                Paragraph(str(interpretation), styles["BodyText"]),
            ]
        )

    table = Table(table_rows, colWidths=[95, 65, 310])
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
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )

    elements.append(table)
    elements.append(Spacer(1, 8))

    summary = (
        "Your numerology stack shows how identity, execution, and communication align. "
        "Use high-signal numbers for strategic decisions and role alignment."
    )
    elements.append(renderer.insight_box("Interpretation Summary", summary, tone="neutral"))

    elements.append(PageBreak())

from reportlab.lib.colors import HexColor
from reportlab.platypus import Image, PageBreak, Spacer, Table, TableStyle

from ..assets import DEITIES


PLANETS = [
    ("surya", "Sun"),
    ("chandra", "Moon"),
    ("mangal", "Mars"),
    ("budh", "Mercury"),
    ("guru", "Jupiter"),
    ("shukra", "Venus"),
    ("shani", "Saturn"),
    ("rahu", "Rahu"),
    ("ketu", "Ketu"),
]


def _planet_cell(renderer, key, label):
    path = DEITIES / f"{key}.png"

    if path.exists():
        img = Image(str(path), width=58, height=58)
        img.hAlign = "CENTER"
        content = [[img], [renderer.paragraph(f"<b>{label}</b>")]]
    else:
        content = [
            [renderer.paragraph("<b>Image Missing</b>")],
            [renderer.paragraph(f"<b>{label}</b>")],
        ]

    card = Table(content, colWidths=[142])
    card.setStyle(
        TableStyle(
            [
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
            ]
        )
    )
    return card


def build_planetary(elements, renderer, styles, data):
    elements.append(renderer.section_banner("Planetary Influence"))

    cells = [_planet_cell(renderer, key, label) for key, label in PLANETS]

    rows = [cells[i:i + 3] for i in range(0, len(cells), 3)]
    grid = Table(rows, colWidths=[156, 156, 156])
    grid.setStyle(
        TableStyle(
            [
                ("GRID", (0, 0), (-1, -1), 0.8, HexColor("#d1d8e0")),
                ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f9fbfd")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("LEFTPADDING", (0, 0), (-1, -1), 2),
                ("RIGHTPADDING", (0, 0), (-1, -1), 2),
                ("TOPPADDING", (0, 0), (-1, -1), 2),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 2),
            ]
        )
    )

    elements.append(grid)
    elements.append(Spacer(1, 8))

    summary = (
        "Planetary energies indicate where discipline, intuition, and momentum need calibration. "
        "Use this visual map to time strategic actions and reduce reactive decisions."
    )
    elements.append(renderer.insight_box("Energy Influence Summary", summary, tone="neutral"))

    elements.append(PageBreak())

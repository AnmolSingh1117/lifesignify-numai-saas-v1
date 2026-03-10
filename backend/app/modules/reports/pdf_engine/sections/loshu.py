from reportlab.platypus import PageBreak, Spacer

from ..blocks.loshu_grid import build_loshu_grid


def build_loshu(elements, renderer, data):
    numerology = data.get("numerology_core", {})
    loshu = numerology.get("loshu_grid", {})
    grid_counts = loshu.get("grid_counts")

    if not grid_counts:
        return

    elements.append(renderer.section_banner("Lo Shu Grid"))
    elements.append(build_loshu_grid(renderer.styles, grid_counts))
    elements.append(Spacer(1, 8))

    elements.append(
        renderer.insight_box(
            "Grid Reading Legend",
            "Green cells indicate present energies. Red cells indicate missing numbers and development gaps.",
            tone="neutral",
        )
    )
    elements.append(Spacer(1, 8))

    missing = loshu.get("missing_numbers", [])
    if not missing:
        missing = [k for k, v in grid_counts.items() if int(v) == 0]

    if missing:
        gap_text = "Missing numbers: " + ", ".join([str(m) for m in missing]) + ". "
    else:
        gap_text = "No critical Lo Shu gaps detected. "

    gap_text += "Focus habits and routines around missing energies to stabilize long-term outcomes."

    elements.append(renderer.insight_box("Gap Interpretation", gap_text, tone="risk" if missing else "success"))

    elements.append(PageBreak())

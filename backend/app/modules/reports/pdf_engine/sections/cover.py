from datetime import datetime

from reportlab.lib.colors import HexColor
from reportlab.lib.units import mm
from reportlab.platypus import HRFlowable, Image, PageBreak, Paragraph, Spacer, Table, TableStyle

from ..assets import GANESHA, KRISHNA, OM_SYMBOL


def _fmt_date(raw):
    if not raw:
        return "Not Provided"
    try:
        return datetime.fromisoformat(str(raw).replace("Z", "+00:00")).strftime("%d %b %Y")
    except Exception:
        return str(raw)


def _cover_deity_image():
    if KRISHNA.exists():
        return KRISHNA
    if GANESHA.exists():
        return GANESHA
    return None


def build_cover(elements, styles, name, plan, data):
    identity = data.get("identity", {}) if isinstance(data, dict) else {}
    meta = data.get("meta", {}) if isinstance(data, dict) else {}

    full_name = name or identity.get("full_name") or "User"
    dob = identity.get("date_of_birth") or identity.get("dob") or "Not Provided"
    generated_at = _fmt_date(meta.get("generated_at"))

    elements.append(Spacer(1, 18))

    if OM_SYMBOL.exists():
        om_img = Image(str(OM_SYMBOL), width=58, height=58)
        om_img.hAlign = "CENTER"
        elements.append(om_img)
        elements.append(Spacer(1, 6))

    deity_path = _cover_deity_image()
    if deity_path is not None:
        deity_img = Image(str(deity_path), width=88, height=88)
        deity_img.hAlign = "CENTER"
        elements.append(deity_img)

    elements.append(Spacer(1, 10))

    top_hr = HRFlowable(width="68%", thickness=1.7, color=HexColor("#c6a15b"), spaceBefore=0, spaceAfter=0)
    top_hr.hAlign = "CENTER"
    elements.append(top_hr)

    elements.append(Spacer(1, 14))
    elements.append(Paragraph("Life Signify NumAI", styles["CoverTitle"]))

    elements.append(Spacer(1, 6))
    elements.append(Paragraph("Strategic Life Intelligence Report", styles["CoverSubtitle"]))

    elements.append(Spacer(1, 4))
    elements.append(Paragraph(f"{plan.upper()} Intelligence Report", styles["CoverPlan"]))

    elements.append(Spacer(1, 8))
    elements.append(Paragraph("22 Pages of Deep Intelligence", styles["CoverAccent"]))

    elements.append(Spacer(1, 14))

    bottom_hr = HRFlowable(width="68%", thickness=1.2, color=HexColor("#c6a15b"), spaceBefore=0, spaceAfter=0)
    bottom_hr.hAlign = "CENTER"
    elements.append(bottom_hr)

    elements.append(Spacer(1, 12))

    identity_table = Table(
        [
            [Paragraph("<b>User Identity</b>", styles["Heading3"])],
            [Paragraph(f"<para align='left'><b>Full Name:</b> {full_name}</para>", styles["BodyText"])],
            [Paragraph(f"<para align='left'><b>DOB:</b> {dob}</para>", styles["BodyText"])],
            [Paragraph(f"<para align='left'><b>Report Generated:</b> {generated_at}</para>", styles["BodyText"])],
        ],
        colWidths=[162 * mm],
    )
    identity_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), HexColor("#f5f7fa")),
                ("BOX", (0, 0), (-1, -1), 1, HexColor("#d9e0e8")),
                ("LEFTPADDING", (0, 0), (-1, -1), 14),
                ("RIGHTPADDING", (0, 0), (-1, -1), 14),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    elements.append(identity_table)

    elements.append(Spacer(1, 10))
    elements.append(Paragraph(full_name, styles["CoverName"]))
    elements.append(PageBreak())

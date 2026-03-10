from io import BytesIO
import logging

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY, TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import PageBreak, SimpleDocTemplate

from ..blueprint import get_tier_section_blueprint
from .decorator import PageDecorator
from .fonts import register_fonts
from .layout import *
from .renderer import Renderer

# core sections
from .sections.cover import build_cover
from .sections.executive import build_executive
from .sections.strengths_risks import build_strengths_risks
from .sections.metrics import build_metrics
from .sections.radar import build_radar
from .sections.archetype import build_archetype

# analysis sections
from .sections.career import build_career
from .sections.decision import build_decision
from .sections.emotional import build_emotional
from .sections.financial import build_financial
from .sections.business import build_business

# numerology sections
from .sections.numerology import build_numerology
from .sections.planetary import build_planetary
from .sections.loshu import build_loshu
from .sections.compatibility import build_compatibility
from .sections.personal_year import build_personal_year

# strategy sections
from .sections.strategy import build_strategy
from .sections.growth import build_growth
from .sections.lifestyle import build_lifestyle
from .sections.mobile import build_mobile

# vedic + closing
from .sections.vedic import build_vedic
from .sections.closing import build_closing

logger = logging.getLogger(__name__)


def _build_styles():
    regular_font, bold_font = register_fonts()
    styles = getSampleStyleSheet()

    deep_indigo = colors.HexColor("#0f2f59")
    royal_purple = colors.HexColor("#4a2c5f")
    slate = colors.HexColor("#4a5568")
    gold = colors.HexColor("#c6a15b")

    styles["Normal"].fontName = regular_font
    styles["Normal"].fontSize = 10
    styles["Normal"].leading = 14
    styles["Normal"].textColor = slate
    styles["Normal"].alignment = TA_CENTER

    styles["BodyText"].fontName = regular_font
    styles["BodyText"].fontSize = 10
    styles["BodyText"].leading = 14
    styles["BodyText"].textColor = slate
    styles["BodyText"].alignment = TA_JUSTIFY
    styles["BodyText"].spaceAfter = 6

    styles["Title"].fontName = bold_font
    styles["Title"].fontSize = 30
    styles["Title"].textColor = deep_indigo
    styles["Title"].alignment = TA_CENTER

    styles["Heading1"].fontName = bold_font
    styles["Heading1"].fontSize = 24
    styles["Heading1"].textColor = deep_indigo
    styles["Heading1"].alignment = TA_LEFT

    styles["Heading2"].fontName = bold_font
    styles["Heading2"].fontSize = 17
    styles["Heading2"].textColor = royal_purple
    styles["Heading2"].alignment = TA_LEFT

    styles["Heading3"].fontName = bold_font
    styles["Heading3"].fontSize = 13
    styles["Heading3"].textColor = deep_indigo
    styles["Heading3"].alignment = TA_LEFT

    styles["Heading4"].fontName = bold_font
    styles["Heading4"].fontSize = 11
    styles["Heading4"].textColor = royal_purple
    styles["Heading4"].alignment = TA_LEFT

    if "SectionBanner" not in styles:
        styles.add(
            ParagraphStyle(
                name="SectionBanner",
                parent=styles["Heading2"],
                fontName=bold_font,
                fontSize=14,
                textColor=colors.white,
                alignment=TA_LEFT,
            )
        )

    if "CoverTitle" not in styles:
        styles.add(
            ParagraphStyle(
                name="CoverTitle",
                parent=styles["Title"],
                fontName=bold_font,
                fontSize=52,
                leading=56,
                textColor=deep_indigo,
                alignment=TA_CENTER,
            )
        )

    if "CoverSubtitle" not in styles:
        styles.add(
            ParagraphStyle(
                name="CoverSubtitle",
                parent=styles["Heading2"],
                fontName=regular_font,
                fontSize=26,
                leading=30,
                textColor=deep_indigo,
                alignment=TA_CENTER,
            )
        )

    if "CoverPlan" not in styles:
        styles.add(
            ParagraphStyle(
                name="CoverPlan",
                parent=styles["Heading2"],
                fontName=regular_font,
                fontSize=23,
                leading=27,
                textColor=deep_indigo,
                alignment=TA_CENTER,
            )
        )

    if "CoverName" not in styles:
        styles.add(
            ParagraphStyle(
                name="CoverName",
                parent=styles["Heading2"],
                fontName=bold_font,
                fontSize=24,
                leading=28,
                textColor=deep_indigo,
                alignment=TA_CENTER,
            )
        )

    # Keep accent available for modules that may rely on this naming.
    if "CoverAccent" not in styles:
        styles.add(
            ParagraphStyle(
                name="CoverAccent",
                parent=styles["Normal"],
                fontName=regular_font,
                fontSize=12,
                textColor=gold,
                alignment=TA_CENTER,
            )
        )

    return styles


def safe_section(func, *args):
    try:
        func(*args)
    except Exception:
        logger.exception("Section failed: %s", func.__name__)


def _normalize_plan_tier(plan_name: str) -> str:
    plan = (plan_name or "").strip().lower()
    if plan == "professional":
        return "pro"
    if plan in {"basic", "pro", "premium", "enterprise"}:
        return plan
    return "basic"


def _resolve_active_blueprint_keys(data: dict, plan_tier: str) -> set[str]:
    blueprint = data.get("report_blueprint")
    if isinstance(blueprint, dict) and isinstance(blueprint.get("sections"), list):
        keys = {
            section.get("key")
            for section in blueprint.get("sections", [])
            if isinstance(section, dict) and section.get("key")
        }
        if keys:
            return keys

    generated = get_tier_section_blueprint(plan_tier)
    return {
        section.get("key")
        for section in generated.get("sections", [])
        if isinstance(section, dict) and section.get("key")
    }


def _is_section_enabled(active_keys: set[str], required_keys: tuple[str, ...]) -> bool:
    if not required_keys:
        return True
    return any(key in active_keys for key in required_keys)


def generate_report_pdf(data, watermark: bool = False):
    buffer = BytesIO()

    doc = SimpleDocTemplate(
        buffer,
        pagesize=(PAGE_WIDTH, PAGE_HEIGHT),
        leftMargin=LEFT_MARGIN,
        rightMargin=RIGHT_MARGIN,
        topMargin=TOP_MARGIN,
        bottomMargin=BOTTOM_MARGIN,
    )

    styles = _build_styles()
    renderer = Renderer(styles)

    elements = []

    name = data.get("identity", {}).get("full_name", "User")
    plan = _normalize_plan_tier(data.get("meta", {}).get("plan_tier", "enterprise"))
    active_blueprint_keys = _resolve_active_blueprint_keys(data, plan)

    safe_section(build_cover, elements, styles, name, plan, data)

    section_pipeline = [
        (build_executive, (elements, renderer, styles, data), ("executive_summary", "current_problem_analysis")),
        (build_strengths_risks, (elements, renderer, data), tuple()),
        (build_metrics, (elements, renderer, styles, data), ("core_numbers_analysis", "personality_intelligence")),
        (build_radar, (elements, renderer, styles, data), tuple()),
        (build_archetype, (elements, renderer, styles, data), ("personality_intelligence",)),
        (build_career, (elements, renderer, styles, data), ("career_wealth_strategy",)),
        (build_decision, (elements, renderer, styles, data), ("current_problem_analysis",)),
        (build_emotional, (elements, renderer, styles, data), ("health_signals", "current_problem_analysis")),
        (build_financial, (elements, renderer, styles, data), ("career_wealth_strategy",)),
        (build_business, (elements, renderer, styles, data), ("career_wealth_strategy",)),
        (
            build_numerology,
            (elements, renderer, styles, data),
            (
                "core_numbers_analysis",
                "mulank_description",
                "bhagyank_description",
                "name_number_analysis",
                "number_interaction_analysis",
            ),
        ),
        (build_planetary, (elements, renderer, styles, data), ("remedies_lifestyle_adjustments",)),
        (
            build_loshu,
            (elements, renderer, data),
            ("loshu_grid_interpretation", "missing_numbers_analysis", "repeating_numbers_impact"),
        ),
        (build_compatibility, (elements, renderer, styles, data), ("relationship_patterns",)),
        (build_personal_year, (elements, renderer, styles, data), ("personal_year_forecast",)),
        (build_strategy, (elements, renderer, styles, data), ("strategic_growth_blueprint",)),
        (build_growth, (elements, renderer, styles, data), ("strategic_growth_blueprint",)),
        (build_lifestyle, (elements, renderer, styles, data), ("color_alignment", "remedies_lifestyle_adjustments", "lucky_numbers")),
        (build_mobile, (elements, renderer, styles, data), ("mobile_number_numerology", "mobile_life_number_compatibility")),
        (build_vedic, (elements, renderer, styles, data), ("remedies_lifestyle_adjustments",)),
        (build_closing, (elements, renderer, styles, data), ("strategic_growth_blueprint",)),
    ]

    for func, args, required_keys in section_pipeline:
        if _is_section_enabled(active_blueprint_keys, required_keys):
            safe_section(func, *args)

    if elements and isinstance(elements[-1], PageBreak):
        elements.pop()

    decorator = PageDecorator(force_watermark=watermark)

    doc.build(
        elements,
        onFirstPage=decorator.decorate,
        onLaterPages=decorator.decorate,
    )

    buffer.seek(0)
    return buffer



# app/modules/reports/pdf_engine.py (FIXED LAYOUT VERSION)

import os
from io import BytesIO
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional, List
import traceback
import textwrap

from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    PageBreak,
    Table,
    TableStyle,
    KeepTogether
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

# Import your existing chart and table engines
from app.modules.reports.charts_engine import generate_radar_chart
from app.modules.reports.table_engine import (
    render_core_numbers_table,
    render_loshu_grid
)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

PAGE_WIDTH, PAGE_HEIGHT = A4

# =========================================================
# ASSET PATHS
# =========================================================

BASE_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../")))
ASSETS = BASE_DIR / "app" / "assets"

logger.info(f"Assets directory: {ASSETS}")

# Branding
LOGO = ASSETS / "branding" / "logo.png"

# Cover images
KRISHNA = ASSETS / "cover" / "krishna.png"
GANESHA = ASSETS / "cover" / "ganesha.png"
OM_SYMBOL = ASSETS / "cover" / "om_symbol.png"

# Backgrounds
MANDALA = ASSETS / "background" / "mandala_bg.png"
LOTUS = ASSETS / "background" / "lotus.png"

# Icons
CHAKRA = ASSETS / "icons" / "chakra.png"

# Deities - ALL 9 PLANETS
DEITIES = {
    "surya": ASSETS / "deities" / "surya.png",
    "chandra": ASSETS / "deities" / "chandra.png",
    "mangal": ASSETS / "deities" / "mangal.png",
    "budh": ASSETS / "deities" / "budh.png",
    "guru": ASSETS / "deities" / "guru.png",
    "shukra": ASSETS / "deities" / "shukra.png",
    "shani": ASSETS / "deities" / "shani.png",
    "rahu": ASSETS / "deities" / "rahu.png",
    "ketu": ASSETS / "deities" / "ketu.png",
}

# Fonts
FONT_REGULAR = ASSETS / "fonts" / "NotoSans-Regular.ttf"
FONT_BOLD = ASSETS / "fonts" / "NotoSans-Bold.ttf"

# =========================================================
# FONT REGISTRATION
# =========================================================

try:
    if os.path.exists(FONT_REGULAR):
        pdfmetrics.registerFont(TTFont("NotoSans", str(FONT_REGULAR)))
        BASE_FONT = "NotoSans"
        logger.info(f"Registered NotoSans font")
    else:
        BASE_FONT = "Helvetica"
        logger.warning(f"NotoSans font not found, using Helvetica")

    if os.path.exists(FONT_BOLD):
        pdfmetrics.registerFont(TTFont("NotoSans-Bold", str(FONT_BOLD)))
        BOLD_FONT = "NotoSans-Bold"
        logger.info(f"Registered NotoSans-Bold font")
    else:
        BOLD_FONT = "Helvetica-Bold"
        logger.warning(f"NotoSans-Bold font not found, using Helvetica-Bold")
except Exception as e:
    logger.error(f"Font registration error: {e}")
    BASE_FONT = "Helvetica"
    BOLD_FONT = "Helvetica-Bold"

# =========================================================
# PREMIUM COLOR PALETTE
# =========================================================

class PremiumColors:
    DEEP_INDIGO = colors.HexColor("#1a2b4c")
    ROYAL_PURPLE = colors.HexColor("#4a2c5f")
    GOLD = colors.HexColor("#c6a15b")
    SOFT_GOLD = colors.HexColor("#e5d5b3")
    MIST_GREY = colors.HexColor("#f5f7fa")
    SLATE_GREY = colors.HexColor("#4a5568")
    LIGHT_LAVENDER = colors.HexColor("#f0f0fa")
    BORDER_GREY = colors.HexColor("#e2e8f0")
    SUCCESS = colors.HexColor("#48bb78")
    WARNING = colors.HexColor("#ecc94b")
    DANGER = colors.HexColor("#f56565")
    INFO = colors.HexColor("#4299e1")

# =========================================================
# PREMIUM STYLES
# =========================================================

def get_premium_styles():
    styles = getSampleStyleSheet()
    
    # Base text style
    styles["Normal"].fontName = BASE_FONT
    styles["Normal"].fontSize = 10
    styles["Normal"].leading = 14
    styles["Normal"].textColor = PremiumColors.SLATE_GREY
    
    # Body text
    styles["BodyText"].fontName = BASE_FONT
    styles["BodyText"].fontSize = 10
    styles["BodyText"].leading = 14
    styles["BodyText"].textColor = PremiumColors.SLATE_GREY
    styles["BodyText"].alignment = TA_JUSTIFY
    styles["BodyText"].spaceAfter = 6
    
    # Title styles
    styles["Title"].fontName = BOLD_FONT
    styles["Title"].fontSize = 32
    styles["Title"].textColor = PremiumColors.DEEP_INDIGO
    styles["Title"].alignment = TA_CENTER
    
    # Heading styles
    styles["Heading1"].fontName = BOLD_FONT
    styles["Heading1"].fontSize = 24
    styles["Heading1"].textColor = PremiumColors.DEEP_INDIGO
    styles["Heading1"].alignment = TA_LEFT
    styles["Heading1"].spaceAfter = 15
    
    styles["Heading2"].fontName = BOLD_FONT
    styles["Heading2"].fontSize = 18
    styles["Heading2"].textColor = PremiumColors.ROYAL_PURPLE
    styles["Heading2"].alignment = TA_LEFT
    styles["Heading2"].spaceAfter = 12
    
    styles["Heading3"].fontName = BOLD_FONT
    styles["Heading3"].fontSize = 14
    styles["Heading3"].textColor = PremiumColors.DEEP_INDIGO
    styles["Heading3"].alignment = TA_LEFT
    styles["Heading3"].spaceAfter = 8
    
    styles["Heading4"].fontName = BOLD_FONT
    styles["Heading4"].fontSize = 12
    styles["Heading4"].textColor = PremiumColors.ROYAL_PURPLE
    styles["Heading4"].alignment = TA_LEFT
    styles["Heading4"].spaceAfter = 6
    
    # Custom premium styles
    styles.add(ParagraphStyle(
        name='CoverSubtitle',
        parent=styles["Heading2"],
        fontSize=20,
        textColor=PremiumColors.GOLD,
        alignment=TA_CENTER
    ))
    
    styles.add(ParagraphStyle(
        name='SectionBanner',
        parent=styles["Heading1"],
        fontSize=22,
        textColor=colors.white,
        alignment=TA_LEFT
    ))
    
    styles.add(ParagraphStyle(
        name='CardTitle',
        parent=styles["Heading4"],
        fontSize=13,
        textColor=PremiumColors.DEEP_INDIGO,
        alignment=TA_LEFT,
        spaceAfter=4
    ))
    
    styles.add(ParagraphStyle(
        name='KPIValue',
        parent=styles["Title"],
        fontSize=24,
        textColor=PremiumColors.ROYAL_PURPLE,
        alignment=TA_CENTER
    ))
    
    styles.add(ParagraphStyle(
        name='Caption',
        parent=styles["Normal"],
        fontSize=8,
        textColor=colors.grey,
        alignment=TA_CENTER,
        italic=True
    ))
    
    styles.add(ParagraphStyle(
        name='Quote',
        parent=styles["Normal"],
        fontSize=11,
        textColor=PremiumColors.DEEP_INDIGO,
        alignment=TA_CENTER,
        italic=True
    ))
    
    return styles

# =========================================================
# TEXT HELPER
# =========================================================

def safe_text(value: Any) -> str:
    """Safely convert any value to string"""
    if value is None:
        return ""
    if isinstance(value, list):
        return "<br/>".join([f"• {v}" for v in value if v])
    if isinstance(value, dict):
        lines = []
        for k, v in value.items():
            if v:
                lines.append(f"<b>{k.replace('_', ' ').title()}:</b> {v}")
        return "<br/>".join(lines)
    return str(value)

def wrap_text(text: str, width: int = 80) -> str:
    """Wrap long text to prevent overflow"""
    if not text or len(text) < width:
        return text
    return "<br/>".join(textwrap.wrap(text, width=width))

# =========================================================
# PAGE DECORATORS
# =========================================================

class PremiumPageDecorator:
    """Handles all page decorations - backgrounds, headers, footers"""
    
    def __init__(self):
        self.styles = get_premium_styles()
    
    def draw_background(self, canvas, doc):
        """Draw premium background with mandala on ALL pages"""
        canvas.saveState()
        
        # White background
        canvas.setFillColor(colors.white)
        canvas.rect(0, 0, PAGE_WIDTH, PAGE_HEIGHT, fill=1)
        
        # Subtle mandala watermark
        if os.path.exists(MANDALA):
            try:
                canvas.saveState()
                canvas.setFillAlpha(0.03)
                canvas.drawImage(
                    str(MANDALA), 
                    0, 0, 
                    width=PAGE_WIDTH, 
                    height=PAGE_HEIGHT,
                    preserveAspectRatio=False, 
                    mask="auto"
                )
                canvas.restoreState()
            except Exception as e:
                logger.error(f"Error drawing mandala: {e}")
        
        # Decorative top border
        canvas.setStrokeColor(PremiumColors.GOLD)
        canvas.setLineWidth(2)
        canvas.line(20 * mm, PAGE_HEIGHT - 15 * mm, 
                   PAGE_WIDTH - 20 * mm, PAGE_HEIGHT - 15 * mm)
        
        # Decorative bottom border
        canvas.setStrokeColor(PremiumColors.GOLD)
        canvas.setLineWidth(1)
        canvas.line(20 * mm, 15 * mm, PAGE_WIDTH - 20 * mm, 15 * mm)
        
        canvas.restoreState()
    
    def draw_header(self, canvas, doc):
        """Draw premium header on pages > 1"""
        canvas.saveState()
        page = canvas.getPageNumber()
        
        if page > 1:
            # Logo on left
            if os.path.exists(LOGO):
                try:
                    canvas.drawImage(
                        str(LOGO), 
                        20 * mm, 
                        PAGE_HEIGHT - 25 * mm,
                        width=100, 
                        height=25, 
                        mask="auto"
                    )
                except Exception as e:
                    logger.error(f"Error drawing logo: {e}")
            
            # Title in center
            canvas.setFont(BOLD_FONT, 10)
            canvas.setFillColor(PremiumColors.DEEP_INDIGO)
            canvas.drawCentredString(
                PAGE_WIDTH/2, 
                PAGE_HEIGHT - 20 * mm,
                "NumAI Strategic Intelligence Brief"
            )
            
            # Date on right
            canvas.setFont(BASE_FONT, 9)
            canvas.setFillColor(colors.grey)
            canvas.drawRightString(
                PAGE_WIDTH - 20 * mm, 
                PAGE_HEIGHT - 20 * mm,
                datetime.now().strftime("%B %Y")
            )
        
        canvas.restoreState()
    
    def draw_footer(self, canvas, doc):
        """Draw premium footer on all pages"""
        canvas.saveState()
        page = canvas.getPageNumber()
        
        # Page number
        canvas.setFont(BASE_FONT, 9)
        canvas.setFillColor(colors.grey)
        canvas.drawRightString(PAGE_WIDTH - 20 * mm, 10 * mm, f"• {page} •")
        
        # Confidential text
        canvas.setFont(BASE_FONT, 8)
        canvas.setFillColor(colors.lightgrey)
        canvas.drawString(20 * mm, 10 * mm, "CONFIDENTIAL • STRATEGIC INTELLIGENCE")
        
        canvas.restoreState()
    
    def add_watermark(self, canvas):
        """Add premium watermark for basic version"""
        canvas.saveState()
        canvas.setFont(BOLD_FONT, 50)
        canvas.setFillColor(colors.Color(0.9, 0.9, 0.9, alpha=0.15))
        canvas.rotate(45)
        canvas.drawCentredString(300, 100, "BASIC VERSION")
        canvas.restoreState()

# =========================================================
# PREMIUM COMPONENT RENDERERS
# =========================================================

class PremiumRenderer:
    """Renders all premium components"""
    
    def __init__(self, styles):
        self.styles = styles
    
    def section_banner(self, title, subtitle=None):
        """Create a premium section banner"""
        content = [Paragraph(title.upper(), self.styles["SectionBanner"])]
        if subtitle:
            content.append(Spacer(1, 5))
            content.append(Paragraph(subtitle, self.styles["Caption"]))
        
        banner = Table([content], colWidths=[460])
        banner.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), PremiumColors.DEEP_INDIGO),
            ("TEXTCOLOR", (0, 0), (-1, -1), colors.white),
            ("ALIGN", (0, 0), (-1, -1), "LEFT"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 15),
            ("RIGHTPADDING", (0, 0), (-1, -1), 15),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ]))
        return banner
    
    def insight_card(self, title, content_text, color=PremiumColors.LIGHT_LAVENDER):
        """Create a premium insight card"""
        if not content_text:
            return None
        
        text = wrap_text(safe_text(content_text), 100)
        
        card = Table([
            [Paragraph(f"<b>{title}</b>", self.styles["CardTitle"])],
            [Paragraph(text, self.styles["BodyText"])]
        ], colWidths=[440])
        
        card.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), color),
            ("BOX", (0, 0), (-1, -1), 1, PremiumColors.BORDER_GREY),
            ("LEFTPADDING", (0, 0), (-1, -1), 15),
            ("RIGHTPADDING", (0, 0), (-1, -1), 15),
            ("TOPPADDING", (0, 0), (-1, -1), 12),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 12),
        ]))
        return card
    
    def kpi_card(self, title, value):
        """Create a premium KPI card with color coding"""
        # Determine color based on value
        try:
            val = float(value) if value else 0
            if val >= 70:
                bg_color = PremiumColors.SUCCESS
            elif val >= 50:
                bg_color = PremiumColors.WARNING
            elif val < 50 and val > 0:
                bg_color = PremiumColors.DANGER
            else:
                bg_color = PremiumColors.LIGHT_LAVENDER
        except:
            bg_color = PremiumColors.LIGHT_LAVENDER
        
        card = Table([
            [Paragraph(title, self.styles["CardTitle"])],
            [Paragraph(str(value), self.styles["KPIValue"])]
        ], colWidths=[140])
        
        card.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), bg_color),
            ("BOX", (0, 0), (-1, -1), 1, PremiumColors.BORDER_GREY),
            ("ALIGN", (0, 0), (-1, -1), "CENTER"),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("TOPPADDING", (0, 0), (-1, -1), 10),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 10),
        ]))
        return card
    
    def planetary_grid(self):
        """Create a premium planetary grid with all 9 deities"""
        planets = [
            ("surya", "Sun", "Leadership"),
            ("chandra", "Moon", "Emotions"),
            ("mangal", "Mars", "Energy"),
            ("budh", "Mercury", "Communication"),
            ("guru", "Jupiter", "Wisdom"),
            ("shukra", "Venus", "Harmony"),
            ("shani", "Saturn", "Discipline"),
            ("rahu", "Rahu", "Ambition"),
            ("ketu", "Ketu", "Spirituality")
        ]
        
        cells = []
        for key, name, quality in planets:
            path = DEITIES.get(key)
            if path and os.path.exists(path):
                try:
                    img = Image(str(path), width=45, height=45)
                    content = [
                        [img],
                        [Paragraph(f"<b>{name}</b>", self.styles["Caption"])],
                        [Paragraph(quality, self.styles["Caption"])]
                    ]
                    cell = Table(content, colWidths=[75])
                    cell.setStyle(TableStyle([
                        ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                    ]))
                    cells.append(cell)
                except:
                    cells.append(Paragraph(name, self.styles["BodyText"]))
            else:
                cells.append(Paragraph(name, self.styles["BodyText"]))
        
        if cells:
            rows = [cells[i:i+3] for i in range(0, len(cells), 3)]
            grid = Table(rows, colWidths=[130, 130, 130])
            grid.setStyle(TableStyle([
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("GRID", (0, 0), (-1, -1), 1, PremiumColors.BORDER_GREY),
            ]))
            return grid
        return None

# =========================================================
# MAIN REPORT GENERATOR
# =========================================================

class PremiumReportGenerator:
    """Generates premium 15-21 page reports"""
    
    def __init__(self, data):
        self.content = data if isinstance(data, dict) else {}
        self.meta = self.content.get("meta", {})
        self.plan = self.meta.get("plan_tier", "professional")
        
        self.styles = get_premium_styles()
        self.renderer = PremiumRenderer(self.styles)
        
        self.elements = []
        self.section_count = 0
        
        logger.info(f"Initialized report generator for plan: {self.plan}")
    
    def generate(self):
        """Generate the complete report"""
        logger.info("Starting premium report generation")
        
        try:
            # Build all sections
            self._build_cover()
            self._build_executive_summary()
            self._build_archetype()
            self._build_metrics()
            self._build_analysis()
            self._build_business()
            self._build_numerology()
            self._build_planetary()
            self._build_loshu()
            self._build_compatibility()
            self._build_strategy()
            self._build_growth()
            self._build_lifestyle()
            self._build_mobile()
            self._build_vedic()
            self._build_closing()
            
            logger.info(f"Built {len(self.elements)} elements")
            
        except Exception as e:
            logger.error(f"Error during report generation: {e}")
            logger.error(traceback.format_exc())
        
        return self.elements
    
    def _add_banner(self, title, subtitle=None):
        """Add a section banner"""
        self.elements.append(self.renderer.section_banner(title, subtitle))
        self.elements.append(Spacer(1, 12))
        self.section_count += 1
    
    def _build_cover(self):
        """Build premium cover page"""
        self.elements.append(Spacer(1, 60))
        
        # OM Symbol
        if os.path.exists(OM_SYMBOL):
            try:
                img = Image(str(OM_SYMBOL), width=70, height=70)
                img.hAlign = "CENTER"
                self.elements.append(img)
                self.elements.append(Spacer(1, 15))
            except:
                pass
        
        # Title
        self.elements.append(Paragraph("NumAI", self.styles["Title"]))
        self.elements.append(Spacer(1, 5))
        self.elements.append(Paragraph("Strategic Intelligence Brief", self.styles["CoverSubtitle"]))
        self.elements.append(Spacer(1, 5))
        
        # Subtitle
        subtitle = f"{self.plan.title()} Edition • {datetime.now().strftime('%B %Y')}"
        self.elements.append(Paragraph(subtitle, self.styles["Caption"]))
        self.elements.append(Spacer(1, 30))
        
        # Cover image
        cover_img = KRISHNA if self.plan == "enterprise" else GANESHA
        if os.path.exists(cover_img):
            try:
                img = Image(str(cover_img), width=160, height=160)
                img.hAlign = "CENTER"
                self.elements.append(img)
            except:
                pass
        
        self.elements.append(PageBreak())
    
    def _build_executive_summary(self):
        """Build executive summary - SIMPLIFIED to avoid overflow"""
        exec_sum = self.content.get("executive_brief", {})
        if not exec_sum:
            return
        
        self._add_banner("Executive Summary")
        
        # Summary
        if exec_sum.get("summary"):
            self.elements.append(Paragraph("<b>Overview</b>", self.styles["Heading4"]))
            self.elements.append(Paragraph(exec_sum["summary"], self.styles["BodyText"]))
            self.elements.append(Spacer(1, 10))
        
        # Strength and Risk - SIMPLE VERTICAL LAYOUT (no two-column)
        if exec_sum.get("key_strength"):
            self.elements.append(Paragraph("<b>Key Strength</b>", self.styles["Heading4"]))
            self.elements.append(Paragraph(exec_sum["key_strength"], self.styles["BodyText"]))
            self.elements.append(Spacer(1, 10))
        
        if exec_sum.get("key_risk"):
            self.elements.append(Paragraph("<b>Key Risk</b>", self.styles["Heading4"]))
            self.elements.append(Paragraph(exec_sum["key_risk"], self.styles["BodyText"]))
            self.elements.append(Spacer(1, 10))
        
        # Strategic Focus
        if exec_sum.get("strategic_focus"):
            card = self.renderer.insight_card("Strategic Focus", exec_sum["strategic_focus"])
            if card:
                self.elements.append(card)
        
        self.elements.append(PageBreak())
    
    def _build_archetype(self):
        """Build archetype section"""
        arch = self.content.get("numerology_archetype", {})
        if not arch:
            return
        
        self._add_banner("Your Archetype")
        
        if arch.get("archetype_name"):
            self.elements.append(Paragraph(arch["archetype_name"], self.styles["Heading2"]))
            self.elements.append(Spacer(1, 5))
        
        if arch.get("core_archetype"):
            self.elements.append(Paragraph(f"<b>Core:</b> {arch['core_archetype']}", self.styles["BodyText"]))
        if arch.get("behavior_style"):
            self.elements.append(Paragraph(f"<b>Style:</b> {arch['behavior_style']}", self.styles["BodyText"]))
        
        self.elements.append(Spacer(1, 10))
        
        if arch.get("description"):
            self.elements.append(Paragraph("Description", self.styles["Heading3"]))
            self.elements.append(Paragraph(arch["description"], self.styles["BodyText"]))
            self.elements.append(Spacer(1, 10))
        
        if arch.get("interpretation"):
            self.elements.append(Paragraph("Interpretation", self.styles["Heading3"]))
            self.elements.append(Paragraph(arch["interpretation"], self.styles["BodyText"]))
        
        self.elements.append(PageBreak())
    
    def _build_metrics(self):
        """Build metrics dashboard"""
        metrics = self.content.get("core_metrics", {})
        if not metrics:
            return
        
        self._add_banner("Key Metrics")
        
        # KPI Cards
        cards = []
        for key, title in [
            ("confidence_score", "Confidence"),
            ("karma_pressure_index", "Karma"),
            ("life_stability_index", "Stability"),
            ("dharma_alignment_score", "Dharma"),
            ("emotional_regulation_index", "Emotional"),
            ("financial_discipline_index", "Financial")
        ]:
            if key in metrics:
                cards.append(self.renderer.kpi_card(title, metrics[key]))
        
        if cards:
            rows = [cards[i:i+3] for i in range(0, len(cards), 3)]
            grid = Table(rows, colWidths=[150, 150, 150])
            self.elements.append(grid)
            self.elements.append(Spacer(1, 10))
        
        # Risk band
        if metrics.get("risk_band"):
            self.elements.append(Paragraph(f"<b>Risk Band:</b> {metrics['risk_band']}", self.styles["BodyText"]))
        
        self.elements.append(PageBreak())
    
    def _build_analysis(self):
        """Build analysis sections"""
        analysis = self.content.get("analysis_sections", {})
        if not analysis:
            return
        
        self._add_banner("Analysis")
        
        for key, title in [
            ("career_analysis", "Career"),
            ("decision_profile", "Decision"),
            ("emotional_analysis", "Emotional"),
            ("financial_analysis", "Financial")
        ]:
            if key in analysis and analysis[key]:
                card = self.renderer.insight_card(title, analysis[key])
                if card:
                    self.elements.append(card)
                    self.elements.append(Spacer(1, 8))
        
        self.elements.append(PageBreak())
    
    def _build_business(self):
        """Build business intelligence"""
        business = self.content.get("business_block", {})
        if not business:
            return
        
        self._add_banner("Business")
        
        if business.get("business_strength"):
            card = self.renderer.insight_card("Strength", business["business_strength"])
            if card:
                self.elements.append(card)
                self.elements.append(Spacer(1, 8))
        
        if business.get("risk_factor"):
            card = self.renderer.insight_card("Risk", business["risk_factor"])
            if card:
                self.elements.append(card)
                self.elements.append(Spacer(1, 8))
        
        if business.get("compatible_industries"):
            industries = "<br/>".join([f"• {i}" for i in business["compatible_industries"]])
            card = self.renderer.insight_card("Compatible Industries", industries)
            if card:
                self.elements.append(card)
        
        self.elements.append(PageBreak())
    
    def _build_numerology(self):
        """Build numerology core"""
        core = self.content.get("numerology_core", {})
        if not core:
            return
        
        self._add_banner("Numerology")
        
        p = core.get("pythagorean", {})
        c = core.get("chaldean", {})
        
        data = [
            ["Life Path", p.get("life_path_number", "N/A")],
            ["Destiny", p.get("destiny_number", "N/A")],
            ["Expression", p.get("expression_number", "N/A")],
            ["Name", c.get("name_number", "N/A")],
            ["Email", core.get("email_analysis", {}).get("email_number", "N/A")],
        ]
        
        table = Table(data, colWidths=[200, 200])
        table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (0, -1), PremiumColors.LIGHT_LAVENDER),
            ("GRID", (0, 0), (-1, -1), 1, PremiumColors.BORDER_GREY),
            ("PADDING", (0, 0), (-1, -1), 6),
        ]))
        self.elements.append(table)
        self.elements.append(Spacer(1, 10))
        
        # Name correction
        name = core.get("name_correction", {})
        if name and name.get("suggestion"):
            self.elements.append(Paragraph(f"<b>Name:</b> {name['suggestion']}", self.styles["BodyText"]))
            self.elements.append(Spacer(1, 5))
        
        # Forecast
        forecast = core.get("strategic_forecast", {})
        if forecast:
            text = []
            if forecast.get("risk_window"):
                text.append(f"<b>Risk:</b> {forecast['risk_window']}")
            if forecast.get("growth_window"):
                text.append(f"<b>Growth:</b> {forecast['growth_window']}")
            if forecast.get("next_3_year_theme"):
                text.append(f"<b>3 Year:</b> {forecast['next_3_year_theme']}")
            
            if text:
                self.elements.append(Paragraph("<br/>".join(text), self.styles["BodyText"]))
        
        self.elements.append(PageBreak())
    
    def _build_planetary(self):
        """Build planetary alignment"""
        self._add_banner("Planetary Alignment")
        
        grid = self.renderer.planetary_grid()
        if grid:
            self.elements.append(grid)
            self.elements.append(Spacer(1, 10))
            self.elements.append(Paragraph(
                "Nine planetary energies influence your life path.",
                self.styles["Caption"]
            ))
        
        self.elements.append(PageBreak())
    
    def _build_loshu(self):
        """Build Lo Shu grid"""
        core = self.content.get("numerology_core", {})
        loshu = core.get("loshu_grid", {})
        if not loshu:
            return
        
        self._add_banner("Lo Shu Grid")
        
        try:
            self.elements.append(render_loshu_grid(loshu))
        except:
            if loshu.get("grid_counts"):
                counts = loshu["grid_counts"]
                data = [[str(i), str(counts.get(str(i), 0))] for i in range(1, 10)]
                table = Table(data, colWidths=[50, 50])
                table.setStyle(TableStyle([
                    ("GRID", (0, 0), (-1, -1), 1, PremiumColors.BORDER_GREY),
                    ("BACKGROUND", (0, 0), (-1, -1), PremiumColors.LIGHT_LAVENDER),
                ]))
                self.elements.append(table)
        
        if loshu.get("missing_numbers"):
            missing = ", ".join(loshu["missing_numbers"])
            self.elements.append(Spacer(1, 8))
            self.elements.append(Paragraph(f"Missing: {missing}", self.styles["BodyText"]))
        
        self.elements.append(PageBreak())
    
    def _build_compatibility(self):
        """Build compatibility section"""
        comp = self.content.get("compatibility_block", {})
        if not comp:
            return
        
        self._add_banner("Compatibility")
        
        if comp.get("compatible_numbers"):
            nums = ", ".join([str(n) for n in comp["compatible_numbers"]])
            self.elements.append(Paragraph(f"<b>Compatible:</b> {nums}", self.styles["BodyText"]))
            self.elements.append(Spacer(1, 5))
        
        if comp.get("challenging_numbers"):
            nums = ", ".join([str(n) for n in comp["challenging_numbers"]])
            self.elements.append(Paragraph(f"<b>Challenging:</b> {nums}", self.styles["BodyText"]))
            self.elements.append(Spacer(1, 8))
        
        if comp.get("relationship_guidance"):
            card = self.renderer.insight_card("Guidance", comp["relationship_guidance"])
            if card:
                self.elements.append(card)
        
        self.elements.append(PageBreak())
    
    def _build_strategy(self):
        """Build strategic guidance"""
        strategy = self.content.get("strategic_guidance", {})
        if not strategy:
            return
        
        self._add_banner("Strategic Guidance")
        
        for key, title in [
            ("short_term", "Short Term"),
            ("mid_term", "Mid Term"),
            ("long_term", "Long Term")
        ]:
            if key in strategy and strategy[key]:
                card = self.renderer.insight_card(title, strategy[key])
                if card:
                    self.elements.append(card)
                    self.elements.append(Spacer(1, 8))
        
        self.elements.append(PageBreak())
    
    def _build_growth(self):
        """Build growth blueprint"""
        growth = self.content.get("growth_blueprint", {})
        if not growth:
            return
        
        self._add_banner("Growth Blueprint")
        
        for key, title in [
            ("phase_1", "Phase 1"),
            ("phase_2", "Phase 2"),
            ("phase_3", "Phase 3")
        ]:
            if key in growth and growth[key]:
                card = self.renderer.insight_card(title, growth[key])
                if card:
                    self.elements.append(card)
                    self.elements.append(Spacer(1, 8))
        
        self.elements.append(PageBreak())
    
    def _build_lifestyle(self):
        """Build lifestyle remedies"""
        life = self.content.get("lifestyle_remedies", {})
        if not life:
            return
        
        self._add_banner("Lifestyle")
        
        for key, title in [
            ("meditation", "Meditation"),
            ("daily_routine", "Daily Routine"),
            ("color_alignment", "Color"),
            ("bracelet_suggestion", "Bracelet")
        ]:
            if key in life and life[key]:
                card = self.renderer.insight_card(title, life[key])
                if card:
                    self.elements.append(card)
                    self.elements.append(Spacer(1, 5))
        
        self.elements.append(PageBreak())
    
    def _build_mobile(self):
        """Build mobile remedies"""
        mobile = self.content.get("mobile_remedies", {})
        if not mobile:
            return
        
        self._add_banner("Mobile")
        
        for key, title in [
            ("whatsapp_dp", "WhatsApp"),
            ("mobile_wallpaper", "Wallpaper"),
            ("charging_direction", "Charging"),
            ("mobile_cover_color", "Cover"),
            ("mobile_usage_timing", "Usage")
        ]:
            if key in mobile and mobile[key]:
                card = self.renderer.insight_card(title, mobile[key])
                if card:
                    self.elements.append(card)
                    self.elements.append(Spacer(1, 5))
        
        self.elements.append(PageBreak())
    
    def _build_vedic(self):
        """Build vedic remedies"""
        vedic = self.content.get("vedic_remedies", {})
        if not vedic:
            return
        
        self._add_banner("Vedic")
        
        # Deity image
        deity = vedic.get("deity")
        if deity:
            key = deity.lower().split()[0].replace("(", "").replace(")", "")
            path = DEITIES.get(key)
            if path and os.path.exists(path):
                try:
                    img = Image(str(path), width=80, height=80)
                    img.hAlign = "CENTER"
                    self.elements.append(img)
                    self.elements.append(Spacer(1, 8))
                except:
                    pass
        
        # Mantra
        if vedic.get("mantra_sanskrit"):
            text = f"<b>Mantra:</b> {vedic['mantra_sanskrit']}"
            if vedic.get("mantra_pronunciation"):
                text += f"<br/><b>Pronounced:</b> {vedic['mantra_pronunciation']}"
            card = self.renderer.insight_card("Mantra", text)
            if card:
                self.elements.append(card)
                self.elements.append(Spacer(1, 8))
        
        # Practice
        if vedic.get("practice_guideline"):
            card = self.renderer.insight_card("Practice", vedic["practice_guideline"])
            if card:
                self.elements.append(card)
                self.elements.append(Spacer(1, 8))
        
        # Donation
        if vedic.get("recommended_donation"):
            card = self.renderer.insight_card("Donation", vedic["recommended_donation"])
            if card:
                self.elements.append(card)
        
        self.elements.append(PageBreak())
    
    def _build_closing(self):
        """Build closing synthesis"""
        self._add_banner("Closing")
        
        arch = self.content.get("numerology_archetype", {})
        name = arch.get("archetype_name", "Strategic Adaptive Explorer")
        
        text = [
            f"By addressing risk bands through financial discipline,",
            f"the {name} stabilizes their foundation.",
            "",
            f"This unlocks your visionary leadership potential."
        ]
        
        self.elements.append(Paragraph("<br/>".join(text), self.styles["Quote"]))
        self.elements.append(Spacer(1, 15))
        self.elements.append(Paragraph("NumAI v1.0", self.styles["Caption"]))


# =========================================================
# MAIN EXPORT FUNCTION
# =========================================================

def generate_report_pdf(data: Dict[str, Any]) -> BytesIO:
    """Generate a premium PDF report"""
    buffer = BytesIO()
    
    try:
        doc = SimpleDocTemplate(
            buffer,
            pagesize=A4,
            rightMargin=50,
            leftMargin=50,
            topMargin=70,
            bottomMargin=50
        )
        
        generator = PremiumReportGenerator(data)
        elements = generator.generate()
        
        if elements and isinstance(elements[-1], PageBreak):
            elements.pop()
        
        decorator = PremiumPageDecorator()
        plan = generator.plan
        
        logger.info(f"Building PDF with {len(elements)} elements")
        logger.info(f"Mandala exists: {os.path.exists(MANDALA)}")
        
        if plan == "basic":
            doc.build(
                elements,
                onFirstPage=lambda c,d: (
                    decorator.draw_background(c,d),
                    decorator.draw_header(c,d),
                    decorator.draw_footer(c,d),
                    decorator.add_watermark(c)
                ),
                onLaterPages=lambda c,d: (
                    decorator.draw_background(c,d),
                    decorator.draw_header(c,d),
                    decorator.draw_footer(c,d),
                    decorator.add_watermark(c)
                )
            )
        else:
            doc.build(
                elements,
                onFirstPage=lambda c,d: (
                    decorator.draw_background(c,d),
                    decorator.draw_header(c,d),
                    decorator.draw_footer(c,d)
                ),
                onLaterPages=lambda c,d: (
                    decorator.draw_background(c,d),
                    decorator.draw_header(c,d),
                    decorator.draw_footer(c,d)
                )
            )
        
        logger.info("PDF built successfully")
        
    except Exception as e:
        logger.error(f"PDF generation failed: {e}")
        logger.error(traceback.format_exc())
        raise
    
    buffer.seek(0)
    return buffer
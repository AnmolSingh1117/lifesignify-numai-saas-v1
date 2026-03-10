from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from .assets import FONTS

FONT_REGULAR_PATH = FONTS / "NotoSans-Regular.ttf"
FONT_BOLD_PATH = FONTS / "NotoSans-Bold.ttf"


# Returns a tuple: (regular_font_name, bold_font_name)
def register_fonts():
    regular = "Helvetica"
    bold = "Helvetica-Bold"

    try:
        if FONT_REGULAR_PATH.exists():
            pdfmetrics.registerFont(TTFont("NotoSans", str(FONT_REGULAR_PATH)))
            regular = "NotoSans"
    except Exception:
        pass

    try:
        if FONT_BOLD_PATH.exists():
            pdfmetrics.registerFont(TTFont("NotoSans-Bold", str(FONT_BOLD_PATH)))
            bold = "NotoSans-Bold"
    except Exception:
        pass

    return regular, bold

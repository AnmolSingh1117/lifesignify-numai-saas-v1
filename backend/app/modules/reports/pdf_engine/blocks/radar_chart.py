from reportlab.graphics.charts.lineplots import LinePlot
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.widgets.markers import makeMarker
from reportlab.lib.colors import HexColor


LABELS = [
    "Life Stability",
    "Decision Clarity",
    "Dharma Alignment",
    "Emotional Regulation",
    "Financial Discipline",
]


def _score(metrics, key, default=0):
    value = metrics.get(key, default)
    try:
        return max(0, min(100, int(value)))
    except Exception:
        return default


def radar_chart(metrics):
    values = [
        _score(metrics, "Life Stability"),
        _score(metrics, "Decision Clarity"),
        _score(metrics, "Dharma Alignment"),
        _score(metrics, "Emotional Regulation"),
        _score(metrics, "Financial Discipline"),
    ]

    drawing = Drawing(470, 230)

    chart = LinePlot()
    chart.x = 40
    chart.y = 34
    chart.height = 145
    chart.width = 270
    chart.data = [[(1, values[0]), (2, values[1]), (3, values[2]), (4, values[3]), (5, values[4])]]
    chart.lines[0].strokeColor = HexColor("#1b2f4b")
    chart.lines[0].strokeWidth = 2
    chart.lines[0].symbol = makeMarker("Circle")
    chart.lines[0].symbol.size = 5

    chart.yValueAxis.valueMin = 0
    chart.yValueAxis.valueMax = 100
    chart.yValueAxis.valueStep = 20
    chart.xValueAxis.valueMin = 1
    chart.xValueAxis.valueMax = 5
    chart.xValueAxis.valueStep = 1

    drawing.add(chart)

    drawing.add(String(340, 200, "Metric Scores", fontName="Helvetica-Bold", fontSize=10, fillColor=HexColor("#1b2f4b")))
    y = 184
    for label, value in zip(LABELS, values):
        drawing.add(String(340, y, f"{label}: {value}", fontName="Helvetica", fontSize=8, fillColor=HexColor("#4a5568")))
        y -= 15

    return drawing

from reportlab.platypus import PageBreak, Spacer

from ..blocks.radar_chart import radar_chart


def _pick(metrics, key, default=0):
    value = metrics.get(key, default)
    try:
        return int(value)
    except Exception:
        return default


def build_metrics(elements, renderer, styles, data):
    metrics = data.get("core_metrics", {})

    if not metrics:
        return

    elements.append(renderer.section_banner("Intelligence Metrics"))

    confidence = _pick(metrics, "confidence_score")
    karma_pressure = _pick(metrics, "karma_pressure_index")
    life_stability = _pick(metrics, "life_stability_index")
    dharma_alignment = _pick(metrics, "dharma_alignment_score")
    emotional_regulation = _pick(metrics, "emotional_regulation_index")
    financial_discipline = _pick(metrics, "financial_discipline_index")

    metric_pairs = [
        ("Confidence Score", confidence),
        ("Karma Pressure Index", karma_pressure),
        ("Life Stability Index", life_stability),
        ("Dharma Alignment", dharma_alignment),
        ("Emotional Regulation", emotional_regulation),
        ("Financial Discipline", financial_discipline),
    ]

    elements.append(renderer.metric_grid(metric_pairs))
    elements.append(Spacer(1, 8))

    radar_data = data.get("radar_chart_data") or {
        "Life Stability": life_stability,
        "Decision Clarity": confidence,
        "Dharma Alignment": dharma_alignment,
        "Emotional Regulation": emotional_regulation,
        "Financial Discipline": financial_discipline,
    }
    elements.append(radar_chart(radar_data))
    elements.append(Spacer(1, 8))

    risk_band = metrics.get("risk_band", "Not classified")
    explanation = (
        f"Risk Band: <b>{risk_band}</b><br/>"
        f"Confidence {confidence}, Karma Pressure {karma_pressure}, Life Stability {life_stability}, "
        f"Dharma Alignment {dharma_alignment}, Emotional Regulation {emotional_regulation}, "
        f"Financial Discipline {financial_discipline}."
    )
    elements.append(renderer.insight_box("Metric Interpretation", explanation, tone="neutral"))

    elements.append(PageBreak())

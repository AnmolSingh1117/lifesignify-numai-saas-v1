from reportlab.platypus import PageBreak, Spacer, Table, TableStyle

from ..assets import CHAKRA_ICON


def _shadow_traits(arch, metrics):
    stated_shadow = arch.get("shadow_traits") or arch.get("shadow")
    if stated_shadow:
        return stated_shadow

    behavior = arch.get("behavior_style", "adaptive")
    emotional = int(metrics.get("emotional_regulation_index", 50) or 50)
    finance = int(metrics.get("financial_discipline_index", 50) or 50)

    pressure_note = ""
    if emotional < 55:
        pressure_note += " Under stress, emotional reactivity can compress decision quality."
    if finance < 55:
        pressure_note += " Financial execution can drift without an explicit control rhythm."

    return (
        f"The {behavior.lower()} pattern can over-index on possibility and under-index on operating discipline."
        f"{pressure_note}"
    )


def _growth_path(arch, strategy):
    anchor = arch.get("core_archetype", "Adaptive Explorer")
    mid_term = strategy.get("mid_term", "Install structure before expansion.")
    return (
        f"Growth path for {anchor}: codify repeatable systems, then scale creative bets in phases. "
        f"Execution focus: {mid_term}"
    )


def build_archetype(elements, renderer, styles, data):
    arch = data.get("numerology_archetype", {})

    if not arch:
        return

    elements.append(renderer.section_banner("Archetype Intelligence"))

    title = arch.get("archetype_name", "Strategic Archetype")
    description = arch.get("description", "")
    elements.append(
        renderer.icon_block(
            CHAKRA_ICON,
            "Archetype Signature",
            f"<b>{title}</b><br/>{description}",
        )
    )
    elements.append(Spacer(1, 8))

    leadership_traits = "<br/>".join(
        [
            f"- Core Archetype: {arch.get('core_archetype', 'Adaptive')}",
            f"- Leadership Traits: {arch.get('behavior_style', 'Strategic and adaptive')}",
            "- Strength Pattern: Strategic direction under uncertainty",
        ]
    )

    shadow_traits = _shadow_traits(arch, data.get("core_metrics", {}))
    growth_path = _growth_path(arch, data.get("strategic_guidance", {}))

    cards = Table(
        [
            [renderer.insight_box("Leadership Traits", leadership_traits, tone="success")],
            [renderer.insight_box("Shadow Traits", shadow_traits, tone="risk")],
            [renderer.insight_box("Archetype Growth Path", growth_path, tone="neutral")],
        ],
        colWidths=[renderer.full_width],
    )
    cards.setStyle(
        TableStyle(
            [
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 4),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
            ]
        )
    )

    elements.append(cards)
    elements.append(PageBreak())

import json


def _safe_int(value, default=0):
    try:
        return int(value)
    except (TypeError, ValueError):
        return default


def parse_audit_response(raw_response: str) -> dict:
    data = json.loads(raw_response)

    scores = data.get("scores", {})
    impact = data.get("impact", {})
    roadmap = data.get("roadmap_30_60_90", {})

    parsed = {
        "scores": {
            "ux": _safe_int(scores.get("ux", 0)),
            "speed": _safe_int(scores.get("speed", 0)),
            "trust": _safe_int(scores.get("trust", 0)),
            "overall": _safe_int(scores.get("overall", 0)),
        },
        "impact": {
            "improvement_range": impact.get("improvement_range", "-"),
            "priority_focus": impact.get("priority_focus", "-"),
        },
        "summary": data.get("summary", ""),
        "executive_hook": data.get("executive_hook", ""),
        "critical_issues": [],
        "quick_wins": [],
        "growth_strategy": [],
        "psychology_triggers": data.get("psychology_triggers", []),
        "experiment_backlog": data.get("experiment_backlog", []),
        "roadmap_30_60_90": {
            "day_30": roadmap.get("day_30", []),
            "day_60": roadmap.get("day_60", []),
            "day_90": roadmap.get("day_90", []),
        },
        "revenue_note": data.get("revenue_note", ""),
    }

    for item in data.get("critical_issues", []):
        parsed["critical_issues"].append(
            {
                "problem": item.get("problem", "-"),
                "why_it_matters": item.get("why_it_matters", "-"),
                "impact": item.get("impact", "-"),
                "solution": item.get("solution", "-"),
                "example": item.get("example", "-"),
            }
        )

    for item in data.get("quick_wins", []):
        parsed["quick_wins"].append(
            {
                "action": item.get("action", "-"),
                "expected_result": item.get("expected_result", "-"),
            }
        )

    for item in data.get("growth_strategy", []):
        parsed["growth_strategy"].append(
            {
                "idea": item.get("idea", "-"),
                "reason": item.get("reason", "-"),
                "expected_impact": item.get("expected_impact", "-"),
            }
        )

    return parsed


def audit_data_to_text(audit_data: dict, lang: str) -> str:
    lines = []

    scores = audit_data.get("scores", {})
    impact = audit_data.get("impact", {})
    roadmap = audit_data.get("roadmap_30_60_90", {})

    lines.append(f'UX_SCORE: {scores.get("ux", 0)}')
    lines.append(f'SPEED_SCORE: {scores.get("speed", 0)}')
    lines.append(f'TRUST_SCORE: {scores.get("trust", 0)}')
    lines.append(f'OVERALL_SCORE: {scores.get("overall", 0)}')
    lines.append("")

    lines.append("EXECUTIVE HOOK" if lang == "EN" else "YONETICI HOOK")
    lines.append(audit_data.get("executive_hook", "-"))
    lines.append("")

    lines.append("SUMMARY" if lang == "EN" else "OZET")
    lines.append(audit_data.get("summary", "-"))
    lines.append("")

    lines.append("IMPACT OVERVIEW" if lang == "EN" else "ETKI OZETI")
    lines.append(
        f'Improvement Range: {impact.get("improvement_range", "-")}'
        if lang == "EN"
        else f'Iyilestirme Araligi: {impact.get("improvement_range", "-")}'
    )
    lines.append(
        f'Priority Focus: {impact.get("priority_focus", "-")}'
        if lang == "EN"
        else f'Oncelikli Odak: {impact.get("priority_focus", "-")}'
    )
    lines.append("")

    lines.append("CRITICAL ISSUES" if lang == "EN" else "KRITIK SORUNLAR")
    for idx, item in enumerate(audit_data.get("critical_issues", []), start=1):
        lines.append(f"{idx}. Problem: {item.get('problem', '-')}")
        lines.append(
            f"   Why It Matters: {item.get('why_it_matters', '-')}"
            if lang == "EN"
            else f"   Neden Onemli: {item.get('why_it_matters', '-')}"
        )
        lines.append(
            f"   Impact: {item.get('impact', '-')}"
            if lang == "EN"
            else f"   Etki: {item.get('impact', '-')}"
        )
        lines.append(
            f"   Solution: {item.get('solution', '-')}"
            if lang == "EN"
            else f"   Cozum: {item.get('solution', '-')}"
        )
        lines.append(
            f"   Example: {item.get('example', '-')}"
            if lang == "EN"
            else f"   Ornek: {item.get('example', '-')}"
        )
        lines.append("")

    lines.append("PSYCHOLOGY TRIGGERS" if lang == "EN" else "PSIKOLOJIK TETIKLEYICILER")
    for item in audit_data.get("psychology_triggers", []):
        lines.append(f"- {item}")
    lines.append("")

    lines.append("EXPERIMENT BACKLOG" if lang == "EN" else "DENEY BACKLOG")
    for idx, item in enumerate(audit_data.get("experiment_backlog", []), start=1):
        lines.append(f"{idx}. Test: {item.get('test', '-')}")
        lines.append(f"   Hypothesis: {item.get('hypothesis', '-')}")
        lines.append(f"   Metric: {item.get('metric', '-')}")
        lines.append(f"   Expected Lift: {item.get('expected_lift', '-')}")
        lines.append("")

    lines.append("30-60-90 ROADMAP")
    lines.append("Day 30:")
    for item in roadmap.get("day_30", []):
        lines.append(f"- {item}")
    lines.append("Day 60:")
    for item in roadmap.get("day_60", []):
        lines.append(f"- {item}")
    lines.append("Day 90:")
    for item in roadmap.get("day_90", []):
        lines.append(f"- {item}")
    lines.append("")

    lines.append("QUICK WINS" if lang == "EN" else "HIZLI KAZANIMLAR")
    for idx, item in enumerate(audit_data.get("quick_wins", []), start=1):
        lines.append(
            f"{idx}. {item.get('action', '-')} -> {item.get('expected_result', '-')}"
        )
    lines.append("")

    lines.append("GROWTH STRATEGY" if lang == "EN" else "BUYUME STRATEJISI")
    for idx, item in enumerate(audit_data.get("growth_strategy", []), start=1):
        lines.append(f"{idx}. {item.get('idea', '-')}")
        lines.append(
            f"   Reason: {item.get('reason', '-')}"
            if lang == "EN"
            else f"   Sebep: {item.get('reason', '-')}"
        )
        lines.append(
            f"   Expected Impact: {item.get('expected_impact', '-')}"
            if lang == "EN"
            else f"   Beklenen Etki: {item.get('expected_impact', '-')}"
        )
        lines.append("")

    lines.append("OPTIMIZATION NOTE" if lang == "EN" else "OPTIMIZASYON NOTU")
    lines.append(audit_data.get("revenue_note", "-"))

    return "\n".join(lines)

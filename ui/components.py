import streamlit as st


def _item_to_text(item):
    if item is None:
        return "-"
    if isinstance(item, str):
        return item
    if isinstance(item, dict):
        # Common audit object shapes
        if "problem" in item:
            impact = item.get("impact", "-")
            solution = item.get("solution", "-")
            return f"{item.get('problem', '-')} | Etki: {impact} | Cozum: {solution}"
        if "action" in item and "expected_result" in item:
            return f"{item.get('action', '-')} -> {item.get('expected_result', '-')}"
        if "idea" in item and "reason" in item:
            return f"{item.get('idea', '-')} - {item.get('reason', '-')}"
        parts = []
        for k, v in item.items():
            if v in [None, "", []]:
                continue
            parts.append(f"{k}: {v}")
        return " | ".join(parts) if parts else "-"
    if isinstance(item, (list, tuple, set)):
        sub = [str(x) for x in item if x not in [None, ""]]
        return ", ".join(sub) if sub else "-"
    return str(item)


def render_hero(l, audit_type):
    title = "Web Site Analizi" if audit_type == "website" else "Instagram Analizi"

    subtitle = (
        "Web sitenizin performansını, güven algısını ve dönüşüm potansiyelini analiz edin."
        if audit_type == "website" and l.get("currency") == "TL"
        else (
            "Instagram profilinizin içerik gücünü, güven algısını ve büyüme potansiyelini analiz edin."
            if l.get("currency") == "TL"
            else (
                "Analyze your website's performance, trust perception and conversion potential."
                if audit_type == "website"
                else "Analyze your Instagram profile's content strength, trust perception and growth potential."
            )
        )
    )

    badge = "AI Destekli Denetim" if l.get("currency") == "TL" else "AI Powered Audit"

    st.markdown(
        f"""
        <div class="hero-shell">
            <div class="hero-badge">{badge}</div>
            <div class="hero-title">{title}</div>
            <div class="hero-subtitle">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_intro_panels(
    l,
    input_label=None,
    placeholder="",
    button_text=None,
    input_key=None,
    default_value="",
):
    st.markdown(
        f'<div class="form-label">{input_label or l["url_label"]}</div>',
        unsafe_allow_html=True,
    )

    url_input = st.text_input(
        "",
        placeholder=placeholder,
        label_visibility="collapsed",
        key=input_key,
        value=default_value,
    )

    start = st.button(
        button_text or l["analyze_btn"],
        use_container_width=True,
    )

    return url_input, start


def render_metric_card(title, value, subtitle=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-title">{title}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_text_section(title, text):
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-card-title">{title}</div>
            <div class="section-card-text">{text}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_list_section(title, items):
    safe_items = [_item_to_text(item) for item in (items or [])]
    list_html = "".join([f"<li>{item}</li>" for item in safe_items]) if safe_items else "<li>-</li>"
    st.markdown(
        f"""
        <div class="section-card">
            <div class="section-card-title">{title}</div>
            <div class="section-card-text">
                <ul>{list_html}</ul>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_spotlight_card(title, text):
    st.markdown(
        f"""
        <div class="spotlight-card">
            <div class="spotlight-title">{title}</div>
            <div class="spotlight-text">{text or "-"}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_issue_card(issue, lang, index):
    impact = (issue.get("impact", "-") or "-").strip().lower()
    badge_class = "impact-low"
    if impact == "high":
        badge_class = "impact-high"
    elif impact == "medium":
        badge_class = "impact-medium"

    why_label = "Neden Onemli" if lang == "TR" else "Why It Matters"
    solution_label = "Cozum" if lang == "TR" else "Solution"
    example_label = "Ornek" if lang == "TR" else "Example"
    issue_label = f"Sorun {index}" if lang == "TR" else f"Issue {index}"

    st.markdown(
        f"""
        <div class="issue-card">
            <div class="issue-head">
                <div class="issue-name">{issue_label}</div>
                <div class="impact-badge {badge_class}">{issue.get("impact", "-")}</div>
            </div>
            <div class="issue-block"><strong>Problem:</strong> {issue.get("problem", "-")}</div>
            <div class="issue-block"><strong>{why_label}:</strong> {issue.get("why_it_matters", "-")}</div>
            <div class="issue-block"><strong>{solution_label}:</strong> {issue.get("solution", "-")}</div>
            <div class="issue-block"><strong>{example_label}:</strong> {issue.get("example", "-")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

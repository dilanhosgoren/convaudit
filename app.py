import os
import asyncio
import hashlib
import hmac
import base64
import json
import time
import re
from html import escape
from textwrap import dedent
from urllib.parse import quote_plus, urlparse
import streamlit as st
import streamlit.components.v1 as components

if os.name == "nt":
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


from config.languages import LANGS
from ui.styles import load_global_styles
from ui.components import (
    render_hero,
    render_intro_panels,
    render_metric_card,
    render_text_section,
    render_list_section,
    render_spotlight_card,
    render_issue_card,
)
from services.ai_service import analyze_site
from services.pdf_service import create_pdf
from services.auth_service import (
    init_auth_tables,
    register_user,
    login_user,
    get_user_by_email,
    get_user_account_info,
    consume_bridge_nonce,
    bump_user_token_version,
    upgrade_user_plan,
    update_user_avatar,
)
from services.history_service import (
    init_history_tables,
    save_analysis,
    get_user_history,
    get_history_detail,
    get_latest_analysis_for_target,
    get_previous_analysis_for_target,
    get_target_full_history,
)
from services.telemetry_service import (
    init_telemetry_tables,
    log_event as db_log_event,
    log_error as db_log_error,
    increment_metric as db_increment_metric,
    get_metrics_map,
    get_error_context_counts,
    get_recent_errors,
    clear_telemetry,
)
from utils.parser import parse_audit_response, audit_data_to_text

st.set_page_config(page_title="ConvAudit AI PRO", layout="wide")
load_global_styles()
init_auth_tables()
init_history_tables()
init_telemetry_tables()


if "user" not in st.session_state:
    st.session_state["user"] = None
if "selected_history_id" not in st.session_state:
    st.session_state["selected_history_id"] = None
if "auth_view" not in st.session_state:
    st.session_state["auth_view"] = None
if "teaser_preview" not in st.session_state:
    st.session_state["teaser_preview"] = None
if "post_login_prefill_url" not in st.session_state:
    st.session_state["post_login_prefill_url"] = ""
if "profile_edit_open" not in st.session_state:
    st.session_state["profile_edit_open"] = False
if "account_info_open" not in st.session_state:
    st.session_state["account_info_open"] = False
if "history_flash" not in st.session_state:
    st.session_state["history_flash"] = ""
if "website_form_open" not in st.session_state:
    st.session_state["website_form_open"] = False
if "instagram_form_open" not in st.session_state:
    st.session_state["instagram_form_open"] = False
if "sidebar_view" not in st.session_state:
    st.session_state["sidebar_view"] = "home"
if "runtime_error_log" not in st.session_state:
    st.session_state["runtime_error_log"] = []
if "rate_limit_events" not in st.session_state:
    st.session_state["rate_limit_events"] = {}
if "runtime_metrics" not in st.session_state:
    st.session_state["runtime_metrics"] = {}
if "event_flags" not in st.session_state:
    st.session_state["event_flags"] = {}


def _t(lang, tr_text, en_text):
    return tr_text if lang == "TR" else en_text


def _admin_emails() -> set[str]:
    raw = os.getenv("ADMIN_EMAILS", "")
    return {x.strip().lower() for x in raw.split(",") if x.strip()}


def _is_admin_user() -> bool:
    user = st.session_state.get("user") or {}
    email = str(user.get("email", "")).strip().lower()
    return bool(email and email in _admin_emails())


def _log_runtime_error(context: str, err: Exception) -> None:
    entry = {
        "ts": int(time.time()),
        "context": context,
        "error": str(err),
    }
    logs = st.session_state.get("runtime_error_log", [])
    logs.insert(0, entry)
    st.session_state["runtime_error_log"] = logs[:60]
    try:
        db_log_error(context=context, error_text=str(err))
    except Exception:
        pass


def _inc_runtime_metric(key: str, amount: int = 1) -> None:
    metrics = st.session_state.get("runtime_metrics", {})
    metrics[key] = int(metrics.get(key, 0) or 0) + amount
    st.session_state["runtime_metrics"] = metrics
    try:
        db_increment_metric(metric_key=key, amount=amount)
    except Exception:
        pass


def _track_event(name: str, meta: dict | None = None) -> None:
    _inc_runtime_metric(f"event:{name}")
    try:
        user = st.session_state.get("user") or {}
        payload = {
            "ts": int(time.time()),
            "event": name,
            "user_id": user.get("id"),
            "email": user.get("email"),
            "meta": meta or {},
        }
        db_log_event(
            event_name=name,
            user_id=int(user.get("id")) if user.get("id") is not None else None,
            email=str(user.get("email")) if user.get("email") else None,
            meta_json=json.dumps(payload.get("meta", {}), ensure_ascii=False),
        )
    except Exception:
        pass


def _track_once(flag: str, event_name: str, meta: dict | None = None) -> None:
    flags = st.session_state.get("event_flags", {})
    if flags.get(flag):
        return
    flags[flag] = True
    st.session_state["event_flags"] = flags
    _track_event(event_name, meta=meta)


def _show_handled_error(
    lang: str,
    err: Exception,
    *,
    context: str,
    tr_generic: str,
    en_generic: str,
) -> None:
    _log_runtime_error(context, err)
    err_text = str(err or "").strip()
    lowered = err_text.lower()
    is_admin = _is_admin_user()
    if "api_key" in lowered or "openai_api_key" in lowered:
        st.error(
            _t(
                lang,
                "API baglantisi ayarlanamadi. OPENAI_API_KEY kontrol edin.",
                "API connection is not configured. Please check OPENAI_API_KEY.",
            )
        )
        return
    if "rate limit" in lowered or "429" in lowered:
        st.error(
            _t(
                lang,
                "Servis gecici olarak yogun. Lutfen 20-30 saniye sonra tekrar deneyin.",
                "Service is temporarily busy. Please try again in 20-30 seconds.",
            )
        )
        return
    if is_admin:
        st.error(f"{_t(lang, tr_generic, en_generic)}: {err_text}")
    else:
        st.error(
            _t(
                lang,
                "Bir sorun olustu. Lutfen tekrar deneyin.",
                "Something went wrong. Please try again.",
            )
        )


def render_admin_health_panel(lang: str) -> None:
    if not _is_admin_user():
        return

    metrics = get_metrics_map()
    logs = get_recent_errors(limit=8)

    def _tr(k: str) -> int:
        return int(metrics.get(k, 0) or 0)

    web_attempt = _tr("website_attempt")
    web_success = _tr("website_success")
    web_fail = _tr("website_fail")

    ig_attempt = _tr("instagram_attempt")
    ig_success = _tr("instagram_success")
    ig_fail = _tr("instagram_fail")

    total_attempt = web_attempt + ig_attempt
    total_success = web_success + ig_success
    success_rate = (
        round((total_success / total_attempt) * 100.0, 1) if total_attempt else 0.0
    )
    landing_views = _tr("event:landing_view")
    landing_cta = _tr("event:landing_cta_website") + _tr("event:landing_cta_instagram")
    login_success = _tr("event:auth_login_success")
    analysis_success = _tr("website_success") + _tr("instagram_success")

    top_context = get_error_context_counts(limit=5)

    st.markdown(
        f'<div class="section-title">{_t(lang, "Admin Sistem Sagligi", "Admin System Health")}</div>',
        unsafe_allow_html=True,
    )
    user = st.session_state.get("user") or {}
    st.caption(
        _t(
            lang,
            f"Admin oturumu: {user.get('email', '-')}",
            f"Admin session: {user.get('email', '-')}",
        )
    )
    with st.expander(
        _t(lang, "Canli Durum Paneli", "Live Health Panel"), expanded=True
    ):
        m1, m2, m3, m4 = st.columns(4)
        with m1:
            render_metric_card(
                _t(lang, "Toplam Istek", "Total Attempts"), str(total_attempt)
            )
        with m2:
            render_metric_card(
                _t(lang, "Basari Orani", "Success Rate"), f"{success_rate}%"
            )
        with m3:
            render_metric_card(_t(lang, "Website Hata", "Website Fail"), str(web_fail))
        with m4:
            render_metric_card(
                _t(lang, "Instagram Hata", "Instagram Fail"), str(ig_fail)
            )

        f1, f2, f3, f4 = st.columns(4)
        with f1:
            render_metric_card(_t(lang, "Landing", "Landing"), str(landing_views))
        with f2:
            render_metric_card(_t(lang, "CTA Tiklama", "CTA Click"), str(landing_cta))
        with f3:
            render_metric_card(
                _t(lang, "Basarili Giris", "Login Success"), str(login_success)
            )
        with f4:
            render_metric_card(
                _t(lang, "Tamamlanan Analiz", "Completed Analysis"),
                str(analysis_success),
            )

        cta_rate = (
            round((landing_cta / landing_views) * 100.0, 1) if landing_views else 0.0
        )
        login_rate = (
            round((login_success / landing_cta) * 100.0, 1) if landing_cta else 0.0
        )
        analysis_rate = (
            round((analysis_success / login_success) * 100.0, 1)
            if login_success
            else 0.0
        )
        st.caption(
            _t(
                lang,
                f"Funnel Oranlari -> Landing→CTA: %{cta_rate} | CTA→Giris: %{login_rate} | Giris→Analiz: %{analysis_rate}",
                f"Funnel Rates -> Landing→CTA: {cta_rate}% | CTA→Login: {login_rate}% | Login→Analysis: {analysis_rate}%",
            )
        )

        st.caption(
            _t(lang, "En cok hata veren contextler", "Most frequent error contexts")
        )
        if top_context:
            for row in top_context:
                st.write(
                    f"- `{row.get('context','unknown')}`: {int(row.get('cnt', 0) or 0)}"
                )
        else:
            st.write(_t(lang, "Kayitli hata yok.", "No logged errors."))

        st.caption(_t(lang, "Son hata kayitlari", "Latest error logs"))
        if logs:
            for row in logs[:8]:
                time_str = str(row.get("created_at", "-"))
                st.code(
                    f"[{time_str}] {row.get('context','-')} -> {row.get('error_text','-')}"
                )
        else:
            st.write(_t(lang, "Hata kaydi bulunmuyor.", "No error records found."))

        if st.button(
            _t(lang, "Loglari Temizle", "Clear Logs"),
            key="clear_admin_runtime_logs_btn",
        ):
            st.session_state["runtime_error_log"] = []
            st.session_state["runtime_metrics"] = {}
            clear_telemetry()
            st.rerun()


def _normalize_url_input(raw: str) -> str:
    value = (raw or "").strip()
    if not value:
        return ""
    if "://" not in value:
        value = f"https://{value}"
    return value


def _validate_website_url(raw: str) -> tuple[bool, str]:
    normalized = _normalize_url_input(raw)
    if not normalized:
        return False, ""
    try:
        parsed = urlparse(normalized)
    except Exception:
        return False, ""
    host = (parsed.netloc or "").lower().strip()
    if host.startswith("www."):
        host = host[4:]
    if not host or "." not in host or " " in host:
        return False, ""
    return True, normalized


def _validate_instagram_target(raw: str) -> tuple[bool, str]:
    normalized = _normalize_url_input(raw)
    if not normalized:
        return False, ""
    try:
        parsed = urlparse(normalized)
    except Exception:
        return False, ""
    host = (parsed.netloc or "").lower()
    if "instagram.com" not in host:
        return False, ""
    path = (parsed.path or "").strip("/")
    handle = path.split("/")[0] if path else ""
    if not handle:
        return False, ""
    if not re.fullmatch(r"[A-Za-z0-9._]{1,30}", handle):
        return False, ""
    return True, f"https://www.instagram.com/{handle}/"


def _check_rate_limit(
    action_key: str, limit: int = 5, window_seconds: int = 60
) -> tuple[bool, int]:
    now = int(time.time())
    event_map = st.session_state.get("rate_limit_events", {})
    events = [
        int(ts)
        for ts in event_map.get(action_key, [])
        if now - int(ts) <= window_seconds
    ]
    if len(events) >= limit:
        wait_sec = max(1, window_seconds - (now - events[0]))
        event_map[action_key] = events
        st.session_state["rate_limit_events"] = event_map
        return False, wait_sec
    events.append(now)
    event_map[action_key] = events
    st.session_state["rate_limit_events"] = event_map
    return True, 0


def _b64url_decode(data: str) -> bytes:
    padding = "=" * ((4 - len(data) % 4) % 4)
    return base64.urlsafe_b64decode((data + padding).encode("utf-8"))


def _verify_bridge_token(token: str) -> tuple[bool, dict]:
    secret = (
        os.getenv("AUTH_BRIDGE_SECRET", "").strip()
    )
    if not secret:
        return False, {}
    parts = (token or "").split(".")
    if len(parts) != 2:
        return False, {}
    payload_b64, signature_b64 = parts
    expected_sig = hmac.new(
        secret.encode("utf-8"),
        payload_b64.encode("utf-8"),
        hashlib.sha256,
    ).digest()
    expected_b64 = base64.urlsafe_b64encode(expected_sig).decode("utf-8").rstrip("=")
    if not hmac.compare_digest(expected_b64, signature_b64):
        return False, {}
    try:
        payload = json.loads(_b64url_decode(payload_b64).decode("utf-8"))
    except Exception:
        return False, {}

    expected_iss = os.getenv("AUTH_BRIDGE_ISSUER", "convaudit-frontend")
    expected_aud = os.getenv("AUTH_BRIDGE_AUDIENCE", "convaudit-streamlit")

    email = str(payload.get("sub", "")).strip().lower()
    exp = int(payload.get("exp", 0) or 0)
    iat = int(payload.get("iat", 0) or 0)
    nonce = str(payload.get("nonce", "")).strip()
    iss = str(payload.get("iss", "")).strip()
    aud = str(payload.get("aud", "")).strip()
    token_version = int(payload.get("tver", 0) or 0)
    now = int(time.time())
    if (
        not email
        or not nonce
        or exp < now
        or iat > now + 30
        or iss != expected_iss
        or aud != expected_aud
    ):
        return False, {}
    if not consume_bridge_nonce(nonce, exp):
        return False, {}

    return True, {
        "email": email,
        "token_version": token_version,
    }


def perform_logout():
    user = st.session_state.get("user") or {}
    user_id = user.get("id")
    if user_id:
        bump_user_token_version(int(user_id))
    st.session_state["user"] = None
    st.session_state["selected_history_id"] = None
    st.session_state["auth_view"] = None
    st.session_state["profile_edit_open"] = False
    st.session_state["account_info_open"] = False
    st.rerun()


def _legal_links():
    base = os.getenv("LEGAL_SITE_BASE_URL", "http://localhost:3000").rstrip("/")
    return {
        "kvkk": f"{base}/kvkk",
        "privacy": f"{base}/privacy",
        "terms": f"{base}/terms",
    }


def _safe_pct_delta(current, previous):
    if previous in [None, 0]:
        return None
    try:
        return round(((current - previous) / previous) * 100.0, 1)
    except ZeroDivisionError:
        return None


def _delta_status(delta_value: int, lang: str) -> str:
    if delta_value > 0:
        return _t(lang, "Ilerleme", "Improvement")
    if delta_value < 0:
        return _t(lang, "Gerileme", "Regression")
    return _t(lang, "Degisim Yok", "No Change")


def _score_cards_for_audit(audit_type: str, lang: str):
    if audit_type == "instagram":
        return [
            ("overall", _t(lang, "Genel Skor", "Overall Score")),
            ("profile_clarity", _t(lang, "Profil Netligi", "Profile Clarity")),
            ("content_quality", _t(lang, "Icerik Kalitesi", "Content Quality")),
            (
                "conversion_readiness",
                _t(lang, "Donusum Hazirligi", "Conversion Readiness"),
            ),
        ]
    return [
        ("overall", _t(lang, "Genel Skor", "Overall Score")),
        ("ux", "UX"),
        ("speed", _t(lang, "Hiz", "Speed")),
        ("trust", _t(lang, "Guven", "Trust")),
    ]


def render_progress_comparison_panel(
    current_scores: dict,
    previous_scores: dict | None,
    lang: str,
    audit_type: str,
    trend_points: list[dict] | None = None,
):
    if not previous_scores:
        return

    current_overall = int(current_scores.get("overall", 0) or 0)
    prev_overall = int(previous_scores.get("overall", 0) or 0)
    delta_abs = current_overall - prev_overall
    delta_pct = _safe_pct_delta(current_overall, prev_overall)
    status = _delta_status(delta_abs, lang)

    st.markdown(
        f'<div class="section-title">{_t(lang, "Onceki Analize Gore Performans", "Performance vs Previous Audit")}</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns([3, 2])
    with left:
        pct_part = ""
        if delta_pct is not None:
            pct_part = f" | {'+' if delta_pct >= 0 else ''}{delta_pct}%"
        st.markdown(
            f'<div class="cmp-main">{current_overall}/100 • {status} • Δ {"+" if delta_abs >= 0 else ""}{delta_abs}{pct_part}</div>',
            unsafe_allow_html=True,
        )
    with right:
        st.markdown(
            f'<div class="cmp-hint">{_t(lang, "Son analiz baz alindi", "Last audit baseline used")}</div>',
            unsafe_allow_html=True,
        )

    card_map = _score_cards_for_audit(audit_type, lang)
    cols = st.columns(len(card_map))
    for col, (key, label) in zip(cols, card_map):
        with col:
            current = int(current_scores.get(key, 0) or 0)
            previous = int(previous_scores.get(key, 0) or 0)
            delta_value = current - previous
            delta_pct_val = _safe_pct_delta(current, previous)
            delta_text = (
                _t(lang, "Baz veri yok", "No baseline")
                if delta_pct_val is None
                else f"{_delta_status(delta_value, lang)} • Δ {'+' if delta_value >= 0 else ''}{delta_value} ({'+' if delta_pct_val >= 0 else ''}{delta_pct_val}%)"
            )
            render_metric_card(
                label,
                f"{current}",
                f"{_t(lang, 'Onceki', 'Prev')}: {previous} | {delta_text}",
            )

    if trend_points:
        normalized = list(reversed(trend_points[:8]))
        bars = []
        for p in normalized:
            s = int(p.get("overall_score", 0) or 0)
            t = str(p.get("created_at", "-"))[:16]
            bars.append(
                f'<div class="cmp-row"><div class="cmp-row-meta"><span>{t}</span><span>{s}/100</span></div><div class="cmp-track"><div class="cmp-fill" style="width:{max(6, min(100, s))}%;"></div></div></div>'
            )
        st.markdown(
            f'<div class="cmp-wrap"><div class="cmp-title">{_t(lang, "Ayni Hedef Trend", "Same Target Trend")}</div>{"".join(bars)}</div>',
            unsafe_allow_html=True,
        )


def _compact_target(target: str) -> str:
    raw = (target or "").strip()
    if not raw:
        return "-"
    try:
        parsed = urlparse(raw if "://" in raw else f"https://{raw}")
        host = (parsed.netloc or "").replace("www.", "")
        path = (parsed.path or "").strip("/")
        if "instagram.com" in host and path:
            handle = path.split("/")[0]
            compact = f"instagram.com/{handle}"
        else:
            compact = f"{host}/{path}".rstrip("/") if host else raw
    except Exception:
        compact = raw
    if len(compact) > 52:
        return compact[:49] + "..."
    return compact


def _normalize_text_blob(value) -> str:
    if value is None:
        return ""
    if isinstance(value, str):
        return value
    if isinstance(value, dict):
        parts = []
        for v in value.values():
            txt = _normalize_text_blob(v)
            if txt:
                parts.append(txt)
        return " ".join(parts)
    if isinstance(value, (list, tuple, set)):
        parts = []
        for item in value:
            txt = _normalize_text_blob(item)
            if txt:
                parts.append(txt)
        return " ".join(parts)
    return str(value)


def _build_teaser_preview(target: str, audit_kind: str, lang: str) -> dict:
    seed_src = f"{target}|{audit_kind}"
    seed = int(hashlib.md5(seed_src.encode("utf-8")).hexdigest()[:6], 16)
    ux = 5 + (seed % 4)
    speed = 4 + ((seed // 3) % 4)
    trust = 5 + ((seed // 7) % 4)
    overall = int(((ux + speed + trust) / 30) * 100)

    if audit_kind == "website":
        visible = [
            _t(
                lang,
                "İlk ekranda değer önerisi zayıf: ziyaretçi neden satın alması gerektiğini ilk 3 saniyede anlamıyor.",
                "Weak above-the-fold value proposition: visitors don't understand why to buy in the first 3 seconds.",
            ),
            _t(
                lang,
                "Ana CTA kontrastı ve konumu karar akışını yavaşlatıyor; tıklama niyeti düşüyor.",
                "Main CTA contrast and placement slows decision flow; click intent drops.",
            ),
            _t(
                lang,
                "Güven sinyalleri (iade, teslimat, ödeme güveni) yukarı akışta yeterince görünmüyor.",
                "Trust signals (return, shipping, payment security) are not visible enough in upper flow.",
            ),
        ]
        locked = [
            _t(
                lang,
                "Kritik gelir kaybı haritası + sayfa bazlı etki puanı",
                "Critical revenue leakage map + page-level impact score",
            ),
            _t(
                lang,
                "Checkout güven katmanı için adım adım UX planı",
                "Step-by-step UX plan for checkout trust layer",
            ),
            _t(
                lang,
                "A/B test backlog + KPI önceliklendirmesi + 30/60/90 yol haritası",
                "A/B backlog + KPI prioritization + 30/60/90 execution roadmap",
            ),
        ]
    else:
        visible = [
            _t(
                lang,
                "Profil konumlandirma mesaji net degil; ilk 5 saniyede deger algisi dusuk.",
                "Profile positioning is unclear; value perception is weak in the first 5 seconds.",
            ),
            _t(
                lang,
                "Reels ve CTA baglantisi donusume yeterince hizmet etmiyor.",
                "Reels-to-CTA flow is not strong enough for conversion.",
            ),
        ]
        locked = [
            _t(lang, "Bio + CTA copy revizyonu", "Bio + CTA copy redesign"),
            _t(
                lang,
                "Icerik serisi ve reels akisi plani",
                "Content series and reels flow plan",
            ),
            _t(
                lang,
                "Buyume deneyleri ve uygulama yol haritasi",
                "Growth experiments and implementation roadmap",
            ),
        ]

    monthly_loss = 32000 + (seed % 26) * 1400
    bounce_gain = 12 + (seed % 9)
    conv_gain = 18 + ((seed // 5) % 14)
    aov_gain = 9 + ((seed // 9) % 11)

    return {
        "audit_kind": audit_kind,
        "target": target or "-",
        "scores": {"ux": ux, "speed": speed, "trust": trust, "overall": overall},
        "visible_findings": visible,
        "locked_items": locked,
        "monthly_loss_estimate": monthly_loss,
        "premium_benchmarks": {
            "conversion": conv_gain,
            "bounce": bounce_gain,
            "aov": aov_gain,
        },
    }


def render_teaser_preview(lang):
    teaser = st.session_state.get("teaser_preview")
    if not teaser:
        return

    st.markdown('<div id="teaser-preview-anchor"></div>', unsafe_allow_html=True)
    if st.session_state.get("scroll_to_teaser"):
        components.html(
            """
            <script>
            const el = window.parent.document.getElementById("teaser-preview-anchor");
            if (el) { el.scrollIntoView({ behavior: "smooth", block: "start" }); }
            </script>
            """,
            height=0,
        )
        st.session_state["scroll_to_teaser"] = False

    scores = teaser.get("scores", {})
    locks = teaser.get("locked_items", [])
    visible = teaser.get("visible_findings", [])
    bench = teaser.get("premium_benchmarks", {})
    target = escape(str(teaser.get("target", "-")))

    finding_list = "".join([f"<li>{escape(str(item))}</li>" for item in visible])
    lock_cards = "".join(
        [
            (
                f'<div class="teaser-lock-card">'
                f'<div class="teaser-lock-mock">'
                f'<div class="teaser-lock-line w1"></div>'
                f'<div class="teaser-lock-line w2"></div>'
                f'<div class="teaser-lock-line w3"></div>'
                f'<div class="teaser-lock-bars"><span></span><span></span><span></span><span></span></div>'
                f"</div>"
                f'<div class="teaser-lock-badge">🔒</div>'
                f'<div class="teaser-lock-title">{escape(str(item))}</div>'
                f'<div class="teaser-lock-sub">{_t(lang, "Premiumda açılır", "Unlocks in Premium")}</div>'
                f"</div>"
            )
            for item in locks[:3]
        ]
    )

    teaser_html = dedent(
        f"""
        <section class="teaser-premium-wrap">
            <div class="teaser-head">
                <div>
                    <h3>{_t(lang, "Ücretsiz Ön İnceleme", "Free Initial Audit")}</h3>
                    <p>{_t(lang, "Hedef", "Target")}: {target} | {_t(lang, "Tür", "Type")}: {escape(str(teaser.get("audit_kind", "website")))}</p>
                </div>
                <div class="teaser-score-grid">
                    <div class="teaser-score-item"><span>UX</span><b>{int(scores.get("ux", 0))}/10</b></div>
                    <div class="teaser-score-item"><span>{_t(lang, "Hız", "Speed")}</span><b>{int(scores.get("speed", 0))}/10</b></div>
                    <div class="teaser-score-item"><span>{_t(lang, "Güven", "Trust")}</span><b>{int(scores.get("trust", 0))}/10</b></div>
                    <div class="teaser-score-item teaser-score-main"><span>{_t(lang, "Genel", "Overall")}</span><b>{int(scores.get("overall", 0))}/100</b></div>
                </div>
            </div>

            <div class="teaser-finding-box">
                <div class="teaser-finding-title">{_t(lang, "Görünen Bulgular", "Visible Findings")}</div>
                <ul>{finding_list}</ul>
                <div class="teaser-warning">{_t(lang, "Detaylı bulgular ve çözüm öncelikleri premium raporda açılır.", "Detailed findings and solution priorities unlock in premium report.")}</div>
            </div>

            <div class="teaser-lock-zone">
                <div class="teaser-lock-zone-title">🔒 {_t(lang, "AI Analizinin Tam Sonuçları Kilitli", "Full AI Analysis Is Locked")}</div>
                <div class="teaser-lock-zone-sub">{_t(lang, "Satış kaybını azaltacak net aksiyon planı, gelir etkisi ve deney backlogu premium raporda açılır.", "Action plan, revenue impact, and experiment backlog to reduce sales leakage unlock in the premium report.")}</div>
                <div class="teaser-lock-grid">{lock_cards}</div>
            </div>

            <div class="teaser-bench-grid">
                <div class="teaser-bench-item"><span>↗</span><b>%{int(bench.get("conversion", 0))}</b><small>{_t(lang, "Potansiyel dönüşüm artışı", "Potential conversion lift")}</small></div>
                <div class="teaser-bench-item"><span>◎</span><b>%{int(bench.get("bounce", 0))}</b><small>{_t(lang, "Bounce iyileşmesi", "Bounce improvement")}</small></div>
                <div class="teaser-bench-item"><span>₺</span><b>%{int(bench.get("aov", 0))}</b><small>{_t(lang, "Sepet değeri etkisi", "Basket value effect")}</small></div>
            </div>
        </section>
        """
    )
    teaser_html_clean = "\n".join(
        line.lstrip() for line in teaser_html.splitlines() if line.strip() != ""
    )
    st.markdown(teaser_html_clean, unsafe_allow_html=True)

    # ── Premium e-posta bırakma formu ──────────────────────────────────
    if st.session_state.get("teaser_waitlist_done"):
        st.markdown(
            f"""
            <div style="margin-top:14px;background:rgba(34,211,238,0.07);border:1px solid rgba(34,211,238,0.25);
                        border-radius:16px;padding:18px 20px;text-align:center;">
                <div style="font-size:20px;margin-bottom:6px;">✅</div>
                <div style="font-size:15px;font-weight:800;color:#67e8f9;margin-bottom:4px;">
                    {_t(lang, "Kaydedildiniz!", "You're on the list!")}
                </div>
                <div style="font-size:13px;color:#94a3b8;">
                    {_t(lang, "Premium erken erişim hazır olduğunda size haber vereceğiz.", "We'll notify you when premium early access is ready.")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
    elif st.session_state.get("teaser_waitlist_open"):
        st.markdown(
            f"""
            <div style="margin-top:14px;background:rgba(34,211,238,0.05);border:1px solid rgba(34,211,238,0.2);
                        border-radius:16px;padding:18px 20px;">
                <div style="font-size:14px;font-weight:700;color:#e2e8f0;margin-bottom:4px;">
                    {_t(lang, "Full AI Raporu için e-postanızı bırakın", "Leave your email for the full AI report")}
                </div>
                <div style="font-size:12px;color:#64748b;margin-bottom:12px;">
                    {_t(lang, "Premium erken erişim açıldığında ilk sizi haberdar ederiz. Spam yok.", "You'll be first to know when premium opens. No spam.")}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        col_email, col_btn = st.columns([3, 1])
        with col_email:
            waitlist_email = st.text_input(
                _t(lang, "E-posta", "Email"),
                placeholder="ornek@email.com",
                label_visibility="collapsed",
                key="teaser_waitlist_email_input",
            )
        with col_btn:
            if st.button(
                _t(lang, "Listeye Katıl", "Join List"),
                use_container_width=True,
                key="teaser_waitlist_submit",
            ):
                if waitlist_email and "@" in waitlist_email:
                    _track_event("waitlist_signup", {"email": waitlist_email, "source": "teaser"})
                    st.session_state["teaser_waitlist_done"] = True
                    st.rerun()
                else:
                    st.warning(_t(lang, "Geçerli bir e-posta girin.", "Please enter a valid email."))
    else:
        if st.button(
            _t(lang, "Full AI Raporunu Al →", "Get Full AI Report →"),
            use_container_width=True,
            key="teaser_continue_login",
        ):
            st.session_state["teaser_waitlist_open"] = True
            st.rerun()


def persist_preview_to_history_if_available(lang):
    user = st.session_state.get("user")
    teaser = st.session_state.get("teaser_preview")
    if not user or not teaser:
        return

    preview_payload = {
        "scores": teaser.get("scores", {}),
        "impact": {"improvement_range": "-", "priority_focus": "-"},
        "summary": " | ".join(teaser.get("visible_findings", [])),
        "visible_findings": teaser.get("visible_findings", []),
        "locked_items": teaser.get("locked_items", []),
        "source": "preview",
    }

    save_analysis(
        user_id=user["id"],
        audit_type=teaser.get("audit_kind", "website"),
        target=teaser.get("target", "-"),
        lang=lang,
        audit_data=preview_payload,
        analysis_level="preview",
    )
    st.session_state["teaser_preview"] = None
    st.session_state["history_flash"] = _t(
        lang,
        "Ucretsiz on analiz gecmise Preview olarak eklendi.",
        "Free preview has been saved to history as Preview.",
    )


def render_delta_overview(
    current_scores, previous_scores, lang, audit_type="website", trend_points=None
):
    render_progress_comparison_panel(
        current_scores,
        previous_scores,
        lang,
        audit_type,
        trend_points=trend_points,
    )


def is_premium_user() -> bool:
    # Demo / review mode: unlock all premium blocks before payment integration is finalized.
    if str(os.getenv("UNLOCK_ALL_PREMIUM_PREVIEW", "0")).strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }:
        return True
    user = st.session_state.get("user") or {}
    return user.get("plan", "free") == "premium"


def save_avatar_file(uploaded_file, user_id: int) -> str:
    if not uploaded_file:
        return ""
    os.makedirs(os.path.join("data", "avatars"), exist_ok=True)
    ext = "png"
    if "." in uploaded_file.name:
        ext = uploaded_file.name.rsplit(".", 1)[-1].lower()
        if ext not in ["png", "jpg", "jpeg", "webp"]:
            ext = "png"
    avatar_path = os.path.join("data", "avatars", f"user_{user_id}.{ext}")
    with open(avatar_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    return avatar_path


def render_profile_edit_popup(lang):
    if not st.session_state.get("profile_edit_open"):
        return

    @st.dialog(_t(lang, "Profil Düzenle", "Edit Profile"), width="small")
    def _profile_dialog():
        user = st.session_state.get("user") or {}
        avatar_path = user.get("avatar_path", "")

        if avatar_path and os.path.exists(avatar_path):
            st.image(avatar_path, width=120)
        else:
            st.markdown('<div class="avatar-default">👤</div>', unsafe_allow_html=True)

        avatar_file = st.file_uploader(
            _t(lang, "Profil Fotoğrafı Yükle", "Upload Profile Photo"),
            type=["png", "jpg", "jpeg", "webp"],
            key="profile_avatar_upload_dialog",
        )

        c1, c2 = st.columns(2)
        with c1:
            if st.button(
                _t(lang, "Kaydet", "Save"),
                key="profile_edit_save_btn",
                use_container_width=True,
            ):
                if avatar_file is None:
                    st.warning(
                        _t(lang, "Lütfen bir görsel seç.", "Please select an image.")
                    )
                else:
                    saved_path = save_avatar_file(avatar_file, user.get("id", 0))
                    if saved_path:
                        update_user_avatar(user.get("id", 0), saved_path)
                        st.session_state["user"]["avatar_path"] = saved_path
                        st.session_state["profile_edit_open"] = False
                        st.success(_t(lang, "Profil güncellendi.", "Profile updated."))
                        st.rerun()
        with c2:
            if st.button(
                _t(lang, "Vazgeç", "Cancel"),
                key="profile_edit_cancel_btn",
                use_container_width=True,
            ):
                st.session_state["profile_edit_open"] = False
                st.rerun()

    _profile_dialog()


def render_account_info_popup(lang):
    if not st.session_state.get("account_info_open"):
        return

    user = st.session_state.get("user") or {}
    user_id = user.get("id")
    info = get_user_account_info(int(user_id)) if user_id else None

    if not hasattr(st, "dialog"):
        if info:
            st.info(
                _t(
                    lang,
                    f"Hesap: {info.get('email', '-')} | Plan: {str(info.get('plan', 'free')).upper()} | Acilis: {info.get('created_at', '-')}",
                    f"Account: {info.get('email', '-')} | Plan: {str(info.get('plan', 'free')).upper()} | Created: {info.get('created_at', '-')}",
                )
            )
        return

    @st.dialog(_t(lang, "Hesap Bilgileri", "Account Details"), width="small")
    def _account_dialog():
        if not info:
            st.warning(
                _t(lang, "Hesap bilgisi bulunamadi.", "Account information not found.")
            )
        else:
            st.markdown(
                f"""
                <div class="account-info-line"><span class="account-info-label">{_t(lang, 'E-posta', 'Email')}:</span> <span class="account-info-value">{info.get('email', '-')}</span></div>
                <div class="account-info-line"><span class="account-info-label">{_t(lang, 'Plan', 'Plan')}:</span> <span class="account-info-value">{str(info.get('plan', 'free')).upper()}</span></div>
                <div class="account-info-line"><span class="account-info-label">{_t(lang, 'Hesap Acilis Tarihi', 'Account Created At')}:</span> <span class="account-info-value">{info.get('created_at', '-')}</span></div>
                """,
                unsafe_allow_html=True,
            )

        if st.button(
            _t(lang, "Kapat", "Close"),
            use_container_width=True,
            key="account_info_close_btn",
        ):
            st.session_state["account_info_open"] = False
            st.rerun()

    _account_dialog()


def render_left_sidebar(lang, active_mode):
    st.markdown(
        f"""
        <div class="dash-side-shell">
            <div class="dash-brand">ConvAudit <span class="brand-green">AI PRO</span></div>
            <div class="dash-menu-title">{_t(lang, "Menü", "Menu")}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button(
        _t(lang, "Web Site Analizi", "Website Analysis"),
        key="side_website_btn",
        use_container_width=True,
    ):
        st.query_params["audit"] = "website"
        st.rerun()

    with st.expander(_t(lang, "Destek Al", "Get Support"), expanded=False):
        st.markdown(
            f"""
            <div class="support-box">
                <div class="support-title">{_t(lang, "Yardıma mı ihtiyacın var?", "Need help?")}</div>
                <div class="support-sub">{_t(lang, "Aşağıdaki bağlantıdan bize ulaşabilirsin.", "You can reach us through the link below.")}</div>
                <div class="support-meta">• {_t(lang, "Hata ve önerileri GitHub üzerinden iletebilirsin.", "Report bugs and suggestions on GitHub.")}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        st.link_button(
            _t(lang, "Sorun Bildir", "Report an Issue"),
            "https://github.com/dilanhosgoren/convaudit/issues",
            use_container_width=True,
        )


def render_right_profile_panel(lang):
    user = st.session_state.get("user") or {}
    first = str(user.get("first_name", "") or "").strip()
    last = str(user.get("last_name", "") or "").strip()
    full_name = f"{first} {last}".strip() or user.get("email", "-")
    plan = user.get("plan", "free").upper()
    avatar_path = user.get("avatar_path", "")
    icon_col, plan_col = st.columns([1, 4], gap="medium")

    with icon_col:
        if hasattr(st, "popover"):
            with st.popover("👤", use_container_width=False):
                st.markdown(
                    f"""
                    <div class="account-menu-head">
                        <div class="account-name">{full_name}</div>
                        <div class="account-sub">{user.get('email', '-')}</div>
                        <div class="account-sub">PLAN: {plan}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                if avatar_path and os.path.exists(avatar_path):
                    st.image(avatar_path, width=88)
                else:
                    st.markdown(
                        '<div class="avatar-default avatar-small">👤</div>',
                        unsafe_allow_html=True,
                    )

                if st.button(
                    _t(lang, "Profilini Düzenle", "Edit Profile"),
                    key="right_edit_profile_btn",
                    use_container_width=True,
                ):
                    st.session_state["account_info_open"] = False
                    st.session_state["profile_edit_open"] = True
                    st.rerun()
                if st.button(
                    _t(lang, "Hesap Bilgileri", "Account Info"),
                    key="right_account_info_btn",
                    use_container_width=True,
                ):
                    st.session_state["profile_edit_open"] = False
                    st.session_state["account_info_open"] = True
                    st.rerun()
                if st.button(
                    _t(lang, "Çıkış", "Log out"),
                    key="right_logout_btn",
                    use_container_width=True,
                ):
                    perform_logout()
        else:
            if st.button(
                _t(lang, "Profil", "Profile"),
                key="right_profile_menu_btn",
                use_container_width=False,
            ):
                st.session_state["profile_edit_open"] = True
                st.rerun()

    with plan_col:
        st.markdown(
            f'<div class="right-topline"><span class="right-plan-pill">PLAN: {plan}</span></div>',
            unsafe_allow_html=True,
        )


def render_main_dashboard_header(lang, active_mode):
    user = st.session_state.get("user") or {}
    first = str(user.get("first_name", "") or "").strip()
    last = str(user.get("last_name", "") or "").strip()
    full_name = f"{first} {last}".strip() or user.get("email", "Kullanıcı").split("@")[0]

    elite_html = dedent(
        f"""
        <section class="elite-wrap">
            <div class="elite-top">
                <div>
                    <div class="elite-welcome">{_t(lang, "Hoş geldiniz", "Welcome")}, {full_name}! 👋</div>
                    <div class="elite-sub">{_t(lang, "Sitenizin performansını artırmak için yapay zeka destekli içgörüler.", "AI-powered insights to increase your site's performance.")}</div>
                </div>
                <div class="elite-date">📅 12 Mayıs - 18 Mayıs 2024</div>
            </div>

            <div class="elite-metrics">
                <div class="elite-card"><span>{_t(lang, "Genel Performans Skoru", "Overall Performance Score")}</span><b>47</b><small>/100</small></div>
                <div class="elite-card"><span>{_t(lang, "Dönüşüm Potansiyeli", "Conversion Potential")}</span><b>79%</b><small>/{_t(lang, "ay", "mo")}</small></div>
                <div class="elite-card"><span>{_t(lang, "Tahmini Gelir Kaybı", "Estimated Revenue Loss")}</span><b>₺42.500</b><small>/{_t(lang, "ay", "mo")}</small></div>
                <div class="elite-card"><span>{_t(lang, "Son Tarama", "Last Scan")}</span><b>2 {_t(lang, "saat önce", "hours ago")}</b><small>18 May 14:25</small></div>
            </div>

            <div class="elite-main-grid">
                <div class="elite-hero-card">
                    <div class="elite-pill">{_t(lang, "AI Destekli Denetim Tamamlandı", "AI-powered audit completed")}</div>
                    <h2>{_t(lang, "E-Ticaret Siteniz Neden Satış Yapmıyor?", "Why is your e-commerce site not selling?")}</h2>
                    <p>{_t(lang, "Yapay zeka analizimiz tamamlandı. Dönüşümü artırmak için 18 kritik sorun tespit edildi.", "AI analysis completed. 18 critical issues were detected to increase conversion.")}</p>
                    <div class="elite-hero-cta">{_t(lang, "Detaylı Raporu Görüntüle", "View Detailed Report")} →</div>
                </div>
                <div class="elite-issues">
                    <div class="elite-issues-head">{_t(lang, "Öncelikli Sorunlar", "Priority Issues")}</div>
                    <div class="elite-issue-item"><span>⚠ Checkout güven adımı eksik</span><b>{_t(lang, "Çok Önemli", "High")}</b></div>
                    <div class="elite-issue-item"><span>⚠ Sepete ekleme oranı düşük</span><b>{_t(lang, "Yüksek", "High")}</b></div>
                    <div class="elite-issue-item"><span>⚠ Ürün sayfası CTA zayıf</span><b>{_t(lang, "Yüksek", "High")}</b></div>
                    <div class="elite-issue-item"><span>⚠ Mobil yükleme süresi yavaş</span><b>{_t(lang, "Orta", "Medium")}</b></div>
                </div>
            </div>

            <div class="elite-bottom-grid">
                <div class="elite-mini-card">
                    <div class="elite-mini-title">{_t(lang, "Dönüşüm Hunisi Analizi", "Conversion Funnel Analysis")}</div>
                    <div class="elite-funnel-row"><span>Ziyaret</span><b>10.450</b></div>
                    <div class="elite-funnel-row"><span>Ürün Görüntüleme</span><b>3.820</b></div>
                    <div class="elite-funnel-row"><span>Sepete Ekleme</span><b>1.250</b></div>
                    <div class="elite-funnel-row"><span>Checkout</span><b>420</b></div>
                </div>
                <div class="elite-mini-card">
                    <div class="elite-mini-title">{_t(lang, "Performans Trendi", "Performance Trend")}</div>
                    <div class="elite-trend-mock"></div>
                </div>
                <div class="elite-mini-card">
                    <div class="elite-mini-title">{_t(lang, "AI Önerileri", "AI Recommendations")}</div>
                    <div class="elite-reco-item">• Checkout sayfasına güven rozetleri ekleyin</div>
                    <div class="elite-reco-item">• Ürün görsellerini optimize edin</div>
                    <div class="elite-reco-item">• Mobil yükleme hızını iyileştirin</div>
                </div>
            </div>
        </section>
        """
    )
    elite_html_clean = "\n".join(
        line.lstrip() for line in elite_html.splitlines() if line.strip()
    )
    st.markdown(elite_html_clean, unsafe_allow_html=True)


def render_premium_sidebar(lang: str):
    user = st.session_state.get("user") or {}
    first = str(user.get("first_name", "") or "").strip()
    last = str(user.get("last_name", "") or "").strip()
    full_name = f"{first} {last}".strip() or user.get("email", "Kullanıcı").split("@")[0]
    email = str(user.get("email", "") or "")
    plan = str(user.get("plan", "free")).upper()

    with st.sidebar:
        st.markdown(
            '<div class="sb-logo">ConvAudit <span>AI</span></div>',
            unsafe_allow_html=True,
        )
        st.markdown('<div class="sb-nav-label">Menü</div>', unsafe_allow_html=True)

        view = st.session_state.get("sidebar_view", "home")

        if st.button(
            ("▶  " if view == "home" else "    ") + _t(lang, "Ana Sayfa", "Home"),
            key="sb_btn_home",
            use_container_width=True,
        ):
            st.session_state["sidebar_view"] = "home"
            st.session_state["selected_history_id"] = None
            st.rerun()

        if st.button(
            ("▶  " if view == "history" else "    ") + _t(lang, "Analiz Geçmişi", "Analysis History"),
            key="sb_btn_history",
            use_container_width=True,
        ):
            st.session_state["sidebar_view"] = "history"
            st.rerun()

        st.markdown("<hr class='sb-divider'>", unsafe_allow_html=True)

        if plan == "FREE":
            plan_extra = f'<a class="sb-upgrade-link" href="http://localhost:3000#fiyatlar" target="_blank">{_t(lang, "Premium\'a Geç →", "Upgrade to Premium →")}</a>'
        else:
            plan_extra = ""
        st.markdown(
            f"""<div class="sb-plan">
                <b>Plan: {plan}</b>
                <small>{"Premium aktif ✓" if plan != "FREE" else _t(lang, "Tüm analizleri açmak için premium\'a geç.", "Upgrade to unlock all analyses.")}</small>
                {plan_extra}
            </div>
            <div class="sb-user"><b>{full_name}</b>{email}</div>""",
            unsafe_allow_html=True,
        )

        st.markdown("<hr class='sb-divider'>", unsafe_allow_html=True)
        if st.button(_t(lang, "Çıkış Yap", "Log out"), key="sb_logout_btn", use_container_width=True):
            perform_logout()


def render_client_premium_dashboard(lang: str):
    user = st.session_state.get("user") or {}
    user_id = int(user.get("id", 0) or 0)
    first = str(user.get("first_name", "") or "").strip()
    last = str(user.get("last_name", "") or "").strip()
    full_name = f"{first} {last}".strip() or user.get("email", "Kullanıcı").split("@")[0]

    history_rows = get_user_history(user_id, limit=10) if user_id else []
    full_rows = [r for r in history_rows if str(r.get("analysis_level", "")).lower() == "full"]
    latest = full_rows[0] if full_rows else (history_rows[0] if history_rows else None)
    latest_target = str((latest or {}).get("target", "") or "")
    latest_score = int((latest or {}).get("overall_score", 0) or 0)

    # Action banner: shown when user logged in from Next.js with a pre-filled URL
    prefill_url = str(st.session_state.get("post_login_prefill_url", "") or "")
    if prefill_url:
        action_banner = f"""
        <div class="cp-action-banner">
            <div class="cp-action-icon">🔍</div>
            <div class="cp-action-body">
                <div class="cp-action-title">{_t(lang, "Analize hazır", "Ready to analyze")}: <b>{prefill_url[:60]}</b></div>
                <div class="cp-action-sub">{_t(lang, "Aşağıdaki Web Site Analizi formunu kullanarak 120+ metrikli tam AI analizini başlatın.", "Use the Website Analysis form below to start the full 120+ metric AI analysis.")}</div>
            </div>
        </div>"""
    elif latest_score > 0:
        score_color = "#4ade80" if latest_score >= 75 else ("#fbbf24" if latest_score >= 50 else "#f87171")
        action_banner = f"""
        <div class="cp-last-score-banner">
            <div>
                <div class="cp-last-score-label">{_t(lang, "Son Analiz", "Latest Analysis")}</div>
                <div class="cp-last-score-target">{latest_target[:50] if latest_target else "-"}</div>
            </div>
            <div class="cp-last-score-num" style="color:{score_color}">{latest_score}<span>/100</span></div>
        </div>"""
    else:
        action_banner = f"""
        <div class="cp-welcome-banner">
            <div class="cp-welcome-icon">⚡</div>
            <div>
                <div class="cp-welcome-title">{_t(lang, "İlk analizinizi başlatın", "Start your first analysis")}</div>
                <div class="cp-welcome-sub">{_t(lang, "URL'nizi aşağıdaki forma girin ve 120+ metrik ile tam AI analizini çalıştırın.", "Enter your URL in the form below to run a full AI analysis with 120+ metrics.")}</div>
            </div>
        </div>"""

    dashboard_html = dedent(
        f"""
            <div class="cp-main" style="border-radius:16px; padding:20px;">
                <div class="cp-head">
                    <div>
                        <h2>{_t(lang, f"Merhaba {full_name}", f"Hello {full_name}")} 👋</h2>
                        <p>{_t(lang, "Sitenizi analiz edin ve dönüşüm kayıplarını tespit edin.", "Analyze your site and find conversion leaks.")}</p>
                    </div>
                </div>
                {action_banner}
            </div>
        """
    )
    dashboard_html_clean = "\n".join(
        line.lstrip() for line in dashboard_html.splitlines() if line.strip()
    )
    st.markdown(dashboard_html_clean, unsafe_allow_html=True)


def render_landing(lang):
    _track_once("landing_view", "landing_view", {"lang": lang})
    login_href = f"?lang={lang}&auth_view=login"
    register_href = f"?lang={lang}&auth_view=register"

    # Fast path: user arrived from Next.js with a pre-filled URL — skip marketing
    # content and show the teaser result directly with a minimal bridge header.
    if st.session_state.get("_from_next_landing") and st.session_state.get("teaser_preview"):
        back_url = os.environ.get("NEXTJS_URL", "http://localhost:3000")
        st.markdown(
            f"""
            <div class="ca-bridge-header">
                <a class="ca-bridge-back" href="{back_url}">← {_t(lang, "Ana Sayfaya Dön", "Back to Home")}</a>
                <div class="ca-brand-wrap" style="gap:10px">
                    <div class="ca-logo-mark">C</div>
                    <div class="ca-brand-text">ConvAudit <span>AI</span></div>
                </div>
                <div class="ca-bridge-result-title">✓ {_t(lang, "Ücretsiz Ön Analiz Hazır", "Free Preview Ready")}</div>
                <a class="ca-nav-btn ca-nav-btn-ghost" href="{login_href}">{_t(lang, "Giriş Yap", "Sign In")}</a>
                <a class="ca-nav-btn ca-nav-btn-solid" href="{register_href}">{_t(lang, "Kayıt Ol", "Sign Up")}</a>
            </div>
            """,
            unsafe_allow_html=True,
        )
        render_teaser_preview(lang)
        return

    st.markdown(
        f"""
        <div class="ca-landing-shell">
            <div class="ca-nav">
                <div class="ca-brand-wrap">
                    <div class="ca-logo-mark">C</div>
                    <div class="ca-brand-text">ConvAudit <span>AI</span></div>
                </div>
                <div class="ca-nav-links">
                    <div class="ca-nav-item">
                        <a href="#how">{_t(lang, "Nasıl Çalışır?", "How It Works")}</a>
                        <div class="ca-nav-popover">
                            <h4>{_t(lang, "İşleyiş", "Workflow")}</h4>
                            <ul>
                                <li>{_t(lang, "Mağaza URL’ni girersin.", "Enter your store URL.")}</li>
                                <li>{_t(lang, "Sistem 30 saniyede kritik kayıp noktalarını çıkarır.", "The system identifies critical leakage points in 30 seconds.")}</li>
                                <li>{_t(lang, "Güven, hız, UX ve dönüşüm için öncelikli aksiyon planı verir.", "It gives prioritized actions for trust, speed, UX, and conversion.")}</li>
                                <li>{_t(lang, "Yeni analizlerde önceki raporla kıyaslayıp ilerleme/gerilemeyi gösterir.", "In new audits, it compares with previous reports and shows progress/regression.")}</li>
                            </ul>
                        </div>
                    </div>
                    <div class="ca-nav-item">
                        <a href="#features">{_t(lang, "Özellikler", "Features")}</a>
                        <div class="ca-nav-popover">
                            <h4>{_t(lang, "Öne Çıkanlar", "Highlights")}</h4>
                            <ul>
                                <li>{_t(lang, "120+ metrikle çok katmanlı denetim", "Multi-layer audit with 120+ metrics")}</li>
                                <li>{_t(lang, "Yönetici özeti + teknik kırılım", "Executive summary + technical breakdown")}</li>
                                <li>{_t(lang, "Önceliklendirilmiş backlog (hemen / bu hafta / bu ay)", "Prioritized backlog (now / this week / this month)")}</li>
                                <li>{_t(lang, "Geçmiş analiz trendi ve skor değişim takibi", "Historical trend and score change tracking")}</li>
                                <li>{_t(lang, "Müşteriye sunulabilir premium rapor formatı", "Premium report format ready for client presentation")}</li>
                            </ul>
                        </div>
                    </div>
                    <div class="ca-nav-item">
                        <a href="#pricing">{_t(lang, "Fiyatlar", "Pricing")}</a>
                        <div class="ca-nav-popover">
                            <h4>{_t(lang, "Paketler", "Plans")}</h4>
                            <ul>
                                <li>{_t(lang, "Preview: Ücretsiz ön analiz", "Preview: Free audit preview")}</li>
                                <li>{_t(lang, "Premium: ₺699/ay — detaylı denetim + aksiyon planı", "Premium: ₺699/mo — detailed audit + action roadmap")}</li>
                                <li>{_t(lang, "Kurumsal: Özel ihtiyaçlara göre teklif", "Enterprise: custom quote for advanced needs")}</li>
                                <li>{_t(lang, "Riski düşük başla, sonuç aldıkça premium’a geç.", "Start low-risk, upgrade as results become clear.")}</li>
                            </ul>
                        </div>
                    </div>
                </div>
                <div class="ca-nav-actions">
                    <a class="ca-nav-btn ca-nav-btn-ghost" href="{login_href}">{_t(lang, "Giriş Yap", "Sign In")}</a>
                    <a class="ca-nav-btn ca-nav-btn-solid" href="{register_href}">{_t(lang, "Kayıt Ol", "Sign Up")}</a>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    hero_left, hero_right = st.columns([1.02, 1], gap="large")

    with hero_left:
        st.markdown(
            f"""
            <section class="ca-hero-copy">
                <div class="ca-eyebrow">✦ {_t(lang, "AI destekli dönüşüm denetimi", "AI-powered conversion audit")}</div>
                <h1>{_t(lang, "E-Ticaret Siteniz Neden", "Why Is Your E-Commerce Site")} <span>{_t(lang, "Satış Yapmıyor?", "Not Selling?")}</span></h1>
                <p>{_t(lang, "Satış kaybını saniyeler içinde görün. Ziyaretçilerin neden müşteriye dönüşmediğini keşfedin; sitenizdeki güven, hız ve UX problemlerini net şekilde tespit edin.", "See conversion leaks in seconds. Discover why visitors do not become customers and identify trust, speed, and UX problems clearly.")}</p>
            </section>
            """,
            unsafe_allow_html=True,
        )

        landing_url = st.text_input(
            _t(lang, "Mağaza URL", "Store URL"),
            placeholder=_t(
                lang,
                "Mağaza adresinizi yapıştırın — örnek: apple.com",
                "Paste your store domain — example: apple.com",
            ),
            key="landing_url_input",
        )

        if st.button(
            _t(lang, "Ücretsiz Web Site Ön Analizi", "Start Free Website Audit"),
            key="landing_website_cta",
            use_container_width=True,
        ):
            _track_event(
                "landing_cta_website", {"has_input": bool(landing_url.strip())}
            )
            target = landing_url.strip()
            if not target:
                st.session_state["teaser_preview"] = None
                st.warning(
                    _t(
                        lang,
                        "Ücretsiz ön analiz için önce URL girmen gerekiyor.",
                        "Please enter a URL before starting the free preview.",
                    )
                )
            else:
                st.session_state["post_login_prefill_url"] = target
                st.session_state["teaser_preview"] = _build_teaser_preview(
                    target=target,
                    audit_kind="website",
                    lang=lang,
                )
                st.session_state["scroll_to_teaser"] = True

        st.markdown(
            f"""
            <div class="ca-trust-row">
                <span>✓ {_t(lang, "Kredi kartı gerekmez", "No credit card required")}</span>
                <span>✓ {_t(lang, "30 saniyede sonuç", "Results in 30 seconds")}</span>
                <span>✓ {_t(lang, "Aksiyon odaklı rapor", "Action-focused report")}</span>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with hero_right:
        st.markdown(
            f"""<div class="ca-demo-card">
<div class="ca-demo-orb"></div>
<div class="ca-demo-head">
<div>
<div class="ca-demo-kicker">ConvAudit Dashboard</div>
<div class="ca-demo-sub">{_t(lang, "Canlı denetim özeti", "Live audit summary")}</div>
</div>
<div class="ca-score-ring">
<div class="ca-ring-number">47</div>
<div class="ca-ring-label">/100</div>
</div>
</div>
<div class="ca-alert-box">
<span>⚠</span>
<div>
<strong>{_t(lang, "Checkout güven adımı eksik", "Checkout trust step missing")}</strong>
<small>{_t(lang, "Çok önemli kırılım noktası", "High priority friction point")}</small>
</div>
</div>
<div class="ca-loss-line">
<div class="ca-loss-icon">₺</div>
<div><strong>79₺</strong> / {_t(lang, "ay potansiyel kayıp", "mo potential loss")}</div>
</div>
<div class="ca-metric-line"><span>{_t(lang, "Sepete ekleme oranı düşük", "Low add-to-cart rate")}</span><b>8%</b></div>
<div class="ca-track"><div class="ca-fill ca-fill-warm"></div></div>
<div class="ca-metric-line"><span>{_t(lang, "Müşteri güveni artırıcı eksikler", "Trust-building gaps")}</span><b>45%</b></div>
<div class="ca-track"><div class="ca-fill ca-fill-cyan"></div></div>
<div class="ca-chip-row"><span>UX</span><span>{_t(lang, "Hız", "Speed")}</span><span>{_t(lang, "Güven", "Trust")}</span></div>
<div class="ca-demo-btn">{_t(lang, "Detaylı Raporu Al", "Get Detailed Report")} →</div>
</div>""",
            unsafe_allow_html=True,
        )

    st.markdown(
        f"""
        <section id="how" class="ca-anchor-section">
            <div class="ca-anchor-title">{_t(lang, "Nasıl Çalışır?", "How It Works")}</div>
            <div class="ca-anchor-grid">
                <div class="ca-anchor-card">1) {_t(lang, "URL girilir ve denetim başlatılır", "Enter URL and start audit")}</div>
                <div class="ca-anchor-card">2) {_t(lang, "Yapay zeka kritik kırılımları tespit eder", "AI detects critical friction points")}</div>
                <div class="ca-anchor-card">3) {_t(lang, "Önceliklendirilmiş aksiyon planı sunulur", "A prioritized action plan is delivered")}</div>
            </div>
        </section>

        <section id="features" class="ca-feature-grid">
            <div class="ca-feature-card">
                <div class="ca-feature-icon">↗</div>
                <div><span>{_t(lang, "Canlı Öncelikleme", "Live Prioritization")}</span><h3>120+ {_t(lang, "Farklı Metrik", "Metrics")}</h3><p>{_t(lang, "Güven, hız, UX ve dönüşüm psikolojisini birlikte okuyarak satışa etki eden kırılma noktalarını gösterir.", "Reads trust, speed, UX and conversion psychology together to reveal revenue-impacting friction.")}</p></div>
            </div>
            <div class="ca-feature-card">
                <div class="ca-feature-icon">◎</div>
                <div><span>{_t(lang, "Kıyaslamalı İçgörü", "Benchmark Insight")}</span><h3>{_t(lang, "Rakip Analizi", "Competitor Analysis")}</h3><p>{_t(lang, "Kategori standartlarını ve rakip sinyallerini karşılaştırır; hangi alanda geride kaldığınızı netleştirir.", "Compares category standards and competitor signals to clarify where you are behind.")}</p></div>
            </div>
            <div class="ca-feature-card">
                <div class="ca-feature-icon">⚡</div>
                <div><span>{_t(lang, "Aksiyon Odaklı", "Action Focused")}</span><h3>{_t(lang, "Kişiye Özel Çözümler", "Tailored Solutions")}</h3><p>{_t(lang, "Sitenizin yapısına göre uygulanabilir aksiyonlar sunar; sadece sorun değil, çözüm yolu da verir.", "Provides practical actions for your site structure, not just problems but the path to fix them.")}</p></div>
            </div>
        </section>

        <section class="ca-insight-grid">
            <div class="ca-ai-card">
                <div class="ca-card-badge">{_t(lang, "AI Önerisi", "AI Recommendation")}</div>
                <h3>{_t(lang, "Checkout sayfasına güven rozetleri ekleyin", "Add trust badges to checkout")}</h3>
                <p>{_t(lang, "Güven rozetleri, kullanıcıların satın alma kararını olumlu etkiler ve terk oranını azaltır.", "Trust badges positively influence purchase decisions and reduce abandonment.")}</p>
                <div class="ca-impact">+%8 {_t(lang, "Dönüşüm Artışı", "Conversion Lift")}</div>
            </div>
            <div class="ca-trend-card">
                <div class="ca-card-badge">{_t(lang, "Performans Trendi", "Performance Trend")}</div>
                <div class="ca-chart-line"></div>
                <div class="ca-chart-points"><span>35</span><span>41</span><span>45</span><span>47</span><b>+12</b></div>
                <p>{_t(lang, "Son 30 günde ölçülen potansiyel iyileşme", "Potential improvement measured over the last 30 days")}</p>
            </div>
        </section>

        <div id="pricing"></div>

        <div class="ca-proof-strip">
            <div>🏆 {_t(lang, "Şimdiye kadar", "More than")} <b>7,000+</b> {_t(lang, "e-ticaret sitesi ConvAudit AI ile analiz edildi", "e-commerce stores analyzed with ConvAudit AI")}</div>
            <div class="ca-logo-row"><span>nike</span><span>airbnb</span><span>shopify</span><span>hepsiburada</span><span>n11</span></div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    render_teaser_preview(lang)


def render_legal_footer(lang):
    links = _legal_links()
    st.markdown(
        f"""
        <div class="footer-site">
            <div class="footer-brand">© 2026 ConvAudit AI PRO</div>
            <div class="footer-links">
                <a href="{links['kvkk']}" target="_blank">{_t(lang, "KVKK", "Data Protection")}</a>
                <a href="{links['privacy']}" target="_blank">{_t(lang, "Gizlilik Politikasi", "Privacy Policy")}</a>
                <a href="{links['terms']}" target="_blank">{_t(lang, "Kullanim Kosullari", "Terms")}</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_paywall_preview(lang):
    st.markdown(
        f"""
        <div class="premium-lock-shell">
            <div class="premium-lock-blur">
                <div style="color:#d6e2ef; line-height:1.8;">
                    1) { _t(lang, "Urun sayfasi ust alan mesaj hiyerarsisi yeniden yazilacak.", "Rewrite above-the-fold value hierarchy on product pages.") }<br>
                    2) { _t(lang, "Checkout guven katmanlari 3 adimda kurgulanacak.", "Design a 3-layer checkout trust architecture.") }<br>
                    3) { _t(lang, "A/B test backlog KPI agaci ile siralanacak.", "Prioritize A/B backlog with a KPI tree.") }
                </div>
            </div>
            <div class="premium-lock-overlay">
                <div>
                    <div class="premium-lock-title">{_t(lang, "Premium Kilitli Bolum", "Premium Locked Section")}</div>
                    <div class="premium-lock-sub">{_t(lang, "Detayli deney plani, psikolojik tetikleyiciler ve 30/60/90 yol haritasi premium ile acilir.", "Detailed experiment plans, psychology triggers, and 30/60/90 roadmap are unlocked with premium.")}</div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_upgrade_panel(lang):
    user = st.session_state.get("user")
    if not user:
        return
    if str(os.getenv("UNLOCK_ALL_PREMIUM_PREVIEW", "0")).strip().lower() in {
        "1",
        "true",
        "yes",
        "on",
    }:
        st.info(
            _t(
                lang,
                "Inceleme modu acik: premium kilitleri gecici olarak kaldirildi.",
                "Review mode is on: premium locks are temporarily disabled.",
            )
        )
        return
    if is_premium_user():
        st.success(_t(lang, "Premium plan aktif.", "Premium plan is active."))
        return

    st.markdown(
        f'<div class="section-title">{_t(lang, "Premiuma Yukselt", "Upgrade to Premium")}</div>',
        unsafe_allow_html=True,
    )
    st.caption(
        _t(
            lang,
            "Odeme entegrasyonu icin Iyzico veya Stripe checkout linki baglayabilirsin. Simdilik butonlar dis checkouta gider.",
            "You can wire this to Iyzico or Stripe checkout links. Buttons currently route to external checkout.",
        )
    )

    iyzico_url = os.getenv("IYZICO_CHECKOUT_URL", "").strip()
    stripe_url = os.getenv("STRIPE_CHECKOUT_URL", "").strip()
    frontend_base = os.getenv("FRONTEND_BASE_URL", "http://localhost:3000").rstrip("/")
    if not stripe_url and user and user.get("email"):
        stripe_url = f"{frontend_base}/api/billing/checkout?email={quote_plus(user.get('email', ''))}&plan=premium"
    c1, c2 = st.columns(2)
    with c1:
        if iyzico_url:
            st.link_button("Iyzico ile Ode", iyzico_url, use_container_width=True)
        else:
            st.button(
                "Iyzico ile Ode (URL tanimla)",
                use_container_width=True,
                disabled=True,
                key="iyzico_disabled",
            )
    with c2:
        if stripe_url:
            st.link_button("Stripe ile Ode", stripe_url, use_container_width=True)
        else:
            st.button(
                "Stripe ile Ode (URL tanimla)",
                use_container_width=True,
                disabled=True,
                key="stripe_disabled",
            )

    if st.button(
        _t(
            lang, "Odeme Tamamlandi, Premiumu Ac", "I Completed Payment, Unlock Premium"
        ),
        use_container_width=True,
        key="unlock_premium_btn",
    ):
        upgrade_user_plan(user["id"], "premium")
        st.session_state["user"]["plan"] = "premium"
        st.success(_t(lang, "Premium aktif edildi.", "Premium activated."))
        st.rerun()


def render_auth_section(lang, show_title=True):
    user = st.session_state.get("user")

    if show_title:
        st.markdown(
            f'<div class="section-title">{_t(lang, "Hesap", "Account")}</div>',
            unsafe_allow_html=True,
        )

    if user:
        c1, c2 = st.columns([4, 1])
        with c1:
            st.success(
                _t(
                    lang,
                    f"Giris yapildi: {user['email']} ({user.get('plan', 'free').upper()})",
                    f"Signed in: {user['email']} ({user.get('plan', 'free').upper()})",
                )
            )
        with c2:
            if st.button(_t(lang, "Cikis", "Log out"), use_container_width=True):
                perform_logout()
        return True

    default_mode = st.session_state.get("auth_view") or "login"
    tabs = st.tabs([_t(lang, "Giris Yap", "Sign In"), _t(lang, "Kayit Ol", "Sign Up")])
    tab_login, tab_register = tabs

    with tab_login:
        if default_mode == "register":
            st.caption(
                _t(
                    lang,
                    "Kayit sekmesi secildi. Giris icin bu sekmeyi kullan.",
                    "Sign-up tab selected. Use this tab to sign in.",
                )
            )
        email = st.text_input(
            _t(lang, "E-posta", "Email"),
            key="auth_login_email",
        )
        password = st.text_input(
            _t(lang, "Sifre", "Password"),
            type="password",
            key="auth_login_password",
        )
        if st.button(_t(lang, "Giris Yap", "Sign In"), key="auth_login_btn"):
            ok, user_data, msg = login_user(email, password)
            if ok:
                st.session_state["user"] = user_data
                st.session_state["auth_view"] = None
                _track_event("auth_login_success", {"source": "section"})
                persist_preview_to_history_if_available(lang)
                st.success(_t(lang, "Giris basarili.", "Signed in successfully."))
                st.rerun()
            else:
                _track_event("auth_login_fail", {"source": "section"})
                st.error(msg if lang == "TR" else "Email or password is incorrect.")

    with tab_register:
        if default_mode == "login":
            st.caption(
                _t(
                    lang,
                    "Giris sekmesi secildi. Kayit icin bu sekmeyi kullan.",
                    "Sign-in tab selected. Use this tab to create account.",
                )
            )
        reg_email = st.text_input(
            _t(lang, "E-posta", "Email"),
            key="auth_register_email",
        )
        reg_first_name = st.text_input(
            _t(lang, "Ad", "First Name"),
            key="auth_register_first_name",
        )
        reg_last_name = st.text_input(
            _t(lang, "Soyad", "Last Name"),
            key="auth_register_last_name",
        )
        reg_password = st.text_input(
            _t(lang, "Sifre", "Password"),
            type="password",
            key="auth_register_password",
        )
        if st.button(_t(lang, "Kayit Ol", "Sign Up"), key="auth_register_btn"):
            ok, msg = register_user(
                reg_email, reg_password, reg_first_name, reg_last_name
            )
            if ok:
                _track_event("auth_register_success", {"source": "section"})
                st.success(
                    _t(
                        lang,
                        "Kayit tamamlandi. Simdi giris yapin.",
                        "Account created. Please sign in.",
                    )
                )
            else:
                _track_event("auth_register_fail", {"source": "section"})
                st.error(msg if lang == "TR" else "Could not create account.")

    return False


def render_auth_popup(lang):
    if not st.session_state.get("auth_view"):
        return

    if not hasattr(st, "dialog"):
        render_auth_section(lang, show_title=True)
        return

    @st.dialog(_t(lang, "Giris", "Sign In"), width="small")
    def _auth_dialog():
        st.caption(
            _t(
                lang,
                "Devam etmek icin giris yapiniz veya yeni hesap olusturunuz.",
                "Please sign in or create a new account to continue.",
            )
        )
        tab_login, tab_register = st.tabs(
            [_t(lang, "Giris Yap", "Sign In"), _t(lang, "Kayit Ol", "Sign Up")]
        )

        with tab_login:
            email = st.text_input(
                _t(lang, "E-posta", "Email"),
                key="popup_auth_login_email",
            )
            password = st.text_input(
                _t(lang, "Sifre", "Password"),
                type="password",
                key="popup_auth_login_password",
            )
            if st.button(_t(lang, "Giris Yap", "Sign In"), key="popup_auth_login_btn"):
                ok, user_data, msg = login_user(email, password)
                if ok:
                    st.session_state["user"] = user_data
                    st.session_state["auth_view"] = None
                    _track_event("auth_login_success", {"source": "popup"})
                    persist_preview_to_history_if_available(lang)
                    st.success(_t(lang, "Giris basarili.", "Signed in successfully."))
                    st.rerun()
                else:
                    _track_event("auth_login_fail", {"source": "popup"})
                    st.error(msg if lang == "TR" else "Email or password is incorrect.")

        with tab_register:
            reg_email = st.text_input(
                _t(lang, "E-posta", "Email"),
                key="popup_auth_register_email",
            )
            reg_first_name = st.text_input(
                _t(lang, "Ad", "First Name"),
                key="popup_auth_register_first_name",
            )
            reg_last_name = st.text_input(
                _t(lang, "Soyad", "Last Name"),
                key="popup_auth_register_last_name",
            )
            reg_password = st.text_input(
                _t(lang, "Sifre", "Password"),
                type="password",
                key="popup_auth_register_password",
            )
            if st.button(
                _t(lang, "Kayit Ol", "Sign Up"), key="popup_auth_register_btn"
            ):
                ok, msg = register_user(
                    reg_email, reg_password, reg_first_name, reg_last_name
                )
                if ok:
                    _track_event("auth_register_success", {"source": "popup"})
                    st.success(
                        _t(
                            lang,
                            "Kayit tamamlandi. Simdi giris yapin.",
                            "Account created. Please sign in.",
                        )
                    )
                else:
                    _track_event("auth_register_fail", {"source": "popup"})
                    st.error(msg if lang == "TR" else "Could not create account.")

    _auth_dialog()


def render_impact_overview(overall, improvement_range, priority_focus, lang):
    st.markdown(
        f'<div class="section-title">{_t(lang, "Etki Ozeti", "Impact Overview")}</div>',
        unsafe_allow_html=True,
    )

    r1, r2, r3 = st.columns(3)
    with r1:
        render_metric_card(_t(lang, "Genel Skor", "Overall Score"), f"{overall}/100")
    with r2:
        render_metric_card(
            _t(lang, "Iyilestirme Araligi", "Improvement Range"), improvement_range
        )
    with r3:
        render_metric_card(_t(lang, "Oncelikli Odak", "Priority Focus"), priority_focus)


def _extract_issue_text(issue) -> str:
    if isinstance(issue, str):
        return issue
    if isinstance(issue, dict):
        p = str(issue.get("problem", "")).strip()
        w = str(issue.get("why_it_matters", "")).strip()
        if p and w:
            return f"{p} — {w}"
        if p:
            return p
        if w:
            return w
    return str(issue) if issue is not None else "-"


def render_decision_panel(
    audit_data: dict, lang: str, audit_type: str, is_premium: bool = True
):
    scores = audit_data.get("scores", {}) or {}
    overall = int(scores.get("overall", 0) or 0)
    impact = audit_data.get("impact", {}) or {}
    priority = str(impact.get("priority_focus", "-") or "-")
    improvement = str(impact.get("improvement_range", "-") or "-")

    if audit_type == "website":
        raw_issues = audit_data.get("critical_issues", []) or []
    else:
        raw_issues = (
            (audit_data.get("critical_issues", []) or [])
            + (audit_data.get("profile_issues", []) or [])
            + (audit_data.get("content_issues", []) or [])
        )

    issues = [
        _extract_issue_text(x)
        for x in raw_issues
        if _extract_issue_text(x) and _extract_issue_text(x) != "-"
    ]
    top_issue = (
        issues[0]
        if issues
        else _t(lang, "Kritik sorun tespit edilmedi", "No critical issue detected")
    )

    quick_wins = audit_data.get("quick_wins", []) or []
    first_win = "-"
    if quick_wins:
        q0 = quick_wins[0]
        if isinstance(q0, dict):
            first_win = f"{q0.get('action', '-')} -> {q0.get('expected_result', '-')}"
        else:
            first_win = str(q0)

    st.markdown(
        f'<div class="section-title">{_t(lang, "Karar Paneli", "Decision Panel")}</div>',
        unsafe_allow_html=True,
    )
    c1, c2, c3, c4 = st.columns(4)
    with c1:
        render_metric_card(_t(lang, "Genel Etki", "Overall Impact"), f"{overall}/100")
    with c2:
        render_metric_card(_t(lang, "Oncelikli Odak", "Priority Focus"), priority)
    with c3:
        render_metric_card(_t(lang, "Potansiyel Artis", "Potential Lift"), improvement)
    with c4:
        render_metric_card(
            _t(lang, "Kritik Bulgu", "Critical Finding"),
            "1",
            top_issue[:58] + ("..." if len(top_issue) > 58 else ""),
        )

    render_text_section(
        _t(lang, "En Kritik Problem", "Most Critical Problem"), top_issue
    )
    render_text_section(_t(lang, "En Hizli Kazanim", "Fastest Win"), first_win)

    actions = []
    if audit_type == "website":
        for item in (audit_data.get("quick_wins", []) or [])[:3]:
            if isinstance(item, dict):
                actions.append(
                    f"{item.get('action', '-')} -> {item.get('expected_result', '-')}"
                )
            else:
                actions.append(str(item))
    else:
        for item in (audit_data.get("recommended_solutions", []) or [])[:3]:
            actions.append(str(item))

    if not actions:
        actions = [
            _t(lang, "Aksiyon listesi olusturulamadi", "Could not build action list")
        ]
    render_list_section(
        _t(lang, "Ilk 3 Aksiyon", "Top 3 Actions"),
        actions if is_premium else actions[:1],
    )


def render_ultra_sections(audit_data, lang, growth_note_key="revenue_note"):
    hook = audit_data.get("executive_hook", "")
    if hook:
        render_text_section(_t(lang, "Dikkat Ceken Ozet", "Executive Hook"), hook)

    render_list_section(
        _t(lang, "Psikolojik Tetikleyiciler", "Psychology Triggers"),
        audit_data.get("psychology_triggers", []),
    )

    experiment_items = []
    for item in audit_data.get("experiment_backlog", []):
        experiment_items.append(
            f"{item.get('test', '-')} | H: {item.get('hypothesis', '-')} | KPI: {item.get('metric', '-')} | Lift: {item.get('expected_lift', '-')}"
        )
    render_list_section(
        _t(lang, "Deney Backlog", "Experiment Backlog"), experiment_items
    )

    roadmap = audit_data.get("roadmap_30_60_90", {})
    render_list_section(_t(lang, "30 Gun", "30 Days"), roadmap.get("day_30", []))
    render_list_section(_t(lang, "60 Gun", "60 Days"), roadmap.get("day_60", []))
    render_list_section(_t(lang, "90 Gun", "90 Days"), roadmap.get("day_90", []))

    render_text_section(
        (
            _t(lang, "Optimizasyon Notu", "Optimization Note")
            if growth_note_key == "revenue_note"
            else _t(lang, "Buyume Notu", "Growth Note")
        ),
        audit_data.get(growth_note_key, "-"),
    )


def render_website_results(audit_data, lang, is_premium=False):
    st.markdown(
        f'<div class="section-title">{_t(lang, "Analiz Sonuclari", "Audit Results")}</div>',
        unsafe_allow_html=True,
    )
    tab_exec, tab_issues, tab_experiments, tab_roadmap = st.tabs(
        [
            _t(lang, "Yonetici Gorunumu", "Executive View"),
            _t(lang, "Kritik Sorunlar", "Critical Issues"),
            _t(lang, "Deneyler", "Experiments"),
            _t(lang, "Aksiyon Roadmap", "Action Roadmap"),
        ]
    )

    with tab_exec:
        render_decision_panel(audit_data, lang, "website", is_premium=is_premium)
        render_spotlight_card(
            _t(lang, "Dikkat Ceken Ozet", "Executive Hook"),
            audit_data.get("executive_hook", "-"),
        )
        render_text_section(
            _t(lang, "Yonetici Ozeti", "Executive Summary"),
            audit_data.get("summary", "-"),
        )
        quick_wins = [
            f"{item.get('action', '-')} -> {item.get('expected_result', '-')}"
            for item in audit_data.get("quick_wins", [])
        ]
        render_list_section(_t(lang, "Hizli Kazanimlar", "Quick Wins"), quick_wins)

    with tab_issues:
        critical_issues = audit_data.get("critical_issues", [])
        if not critical_issues:
            st.info(_t(lang, "Kritik sorun bulunamadi.", "No critical issues found."))
        visible_issues = critical_issues if is_premium else critical_issues[:1]
        for idx, issue in enumerate(visible_issues, start=1):
            render_issue_card(issue, lang, idx)
        if not is_premium and len(critical_issues) > 1:
            render_paywall_preview(lang)
            render_upgrade_panel(lang)

    with tab_experiments:
        if not is_premium:
            render_paywall_preview(lang)
            render_upgrade_panel(lang)
        else:
            render_list_section(
                _t(lang, "Psikolojik Tetikleyiciler", "Psychology Triggers"),
                audit_data.get("psychology_triggers", []),
            )
            experiment_items = []
            for item in audit_data.get("experiment_backlog", []):
                experiment_items.append(
                    f"{item.get('test', '-')} | H: {item.get('hypothesis', '-')} | KPI: {item.get('metric', '-')} | Lift: {item.get('expected_lift', '-')}"
                )
            render_list_section(
                _t(lang, "Deney Backlog", "Experiment Backlog"), experiment_items
            )

    with tab_roadmap:
        if not is_premium:
            render_paywall_preview(lang)
            render_upgrade_panel(lang)
        else:
            roadmap = audit_data.get("roadmap_30_60_90", {})
            c1, c2, c3 = st.columns(3)
            with c1:
                render_list_section(
                    _t(lang, "30 Gun", "30 Days"), roadmap.get("day_30", [])
                )
            with c2:
                render_list_section(
                    _t(lang, "60 Gun", "60 Days"), roadmap.get("day_60", [])
                )
            with c3:
                render_list_section(
                    _t(lang, "90 Gun", "90 Days"), roadmap.get("day_90", [])
                )

            growth_strategy = [
                f"{item.get('idea', '-')} - {item.get('reason', '-')} ({item.get('expected_impact', '-')})"
                for item in audit_data.get("growth_strategy", [])
            ]
            render_list_section(
                _t(lang, "Buyume Stratejisi", "Growth Strategy"), growth_strategy
            )
            render_text_section(
                _t(lang, "Optimizasyon Notu", "Optimization Note"),
                audit_data.get("revenue_note", "-"),
            )


def render_history_section(lang):
    user = st.session_state.get("user")
    if not user:
        return

    st.markdown(
        f'<div class="section-title">{_t(lang, "Gecmis Analizlerim", "My Analysis History")}</div>',
        unsafe_allow_html=True,
    )

    all_rows_raw = get_user_history(user["id"], limit=100, analysis_level=None)
    all_rows = [
        r
        for r in all_rows_raw
        if str(r.get("audit_type", "website")).lower() == "website"
    ]
    level_options = [
        ("all", _t(lang, "Tumu", "All")),
        ("preview", _t(lang, "Preview", "Preview")),
        ("full", _t(lang, "Full", "Full")),
    ]
    level_choice = st.radio(
        _t(lang, "Kayit Turu", "Record Type"),
        options=[opt[0] for opt in level_options],
        horizontal=True,
        key="history_level_filter_radio",
        format_func=lambda x: dict(level_options).get(x, x),
    )
    level_filter = None if level_choice == "all" else level_choice

    rows_raw = get_user_history(user["id"], limit=30, analysis_level=level_filter)
    rows = [
        r for r in rows_raw if str(r.get("audit_type", "website")).lower() == "website"
    ]

    if not rows:
        st.info(_t(lang, "Henuz kayitli analiz yok.", "No saved analyses yet."))
        return

    st.markdown(
        f'<div class="section-title">{_t(lang, "Kayit Listesi", "Record List")}</div>',
        unsafe_allow_html=True,
    )
    selected_id = None
    for r in rows:
        row_id = int(r["id"])
        level = str(r.get("analysis_level", "full")).upper()
        target_short = _compact_target(str(r.get("target", "")))
        score = int(r.get("overall_score", 0) or 0)
        col1, col2 = st.columns([5, 1])
        with col1:
            st.markdown(
                f"""
                <div class="history-row-card">
                    <div class="history-row-top">#{row_id} • {level} • {str(r.get('audit_type','-')).upper()}</div>
                    <div class="history-row-main">{target_short}</div>
                    <div class="history-row-sub">{r.get('created_at','-')} • {score}/100</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            if st.button(
                _t(lang, "Ac", "Open"),
                key=f"history_open_{row_id}",
                use_container_width=True,
            ):
                selected_id = row_id

    if selected_id:
        st.session_state["selected_history_id"] = selected_id

    selected_id = st.session_state.get("selected_history_id")

    if not selected_id:
        return

    detail = get_history_detail(selected_id, user["id"])
    if not detail:
        st.warning(_t(lang, "Secilen kayit bulunamadi.", "Selected record not found."))
        return

    payload = detail["payload"]
    st.caption(
        _t(
            lang,
            f"Kayit: {detail['created_at']} | Tur: {str(detail.get('analysis_level', 'full')).upper()} | Hedef: {_compact_target(str(detail.get('target', '')))}",
            f"Record: {detail['created_at']} | Type: {str(detail.get('analysis_level', 'full')).upper()} | Target: {_compact_target(str(detail.get('target', '')))}",
        )
    )

    if str(detail.get("analysis_level", "full")).lower() == "preview":
        scores = payload.get("scores", {})
        visible = payload.get("visible_findings", [])
        locked = payload.get("locked_items", [])
        target_str = escape(str(detail.get("target", "-")))
        created_at = str(detail.get("created_at", "-"))[:16]
        overall = int(scores.get("overall", 0) or 0)

        risk = _t(lang, "Kritik", "Critical") if overall < 50 else (_t(lang, "Yuksek", "High") if overall < 65 else _t(lang, "Orta", "Medium"))
        risk_color = "#f87171" if overall < 50 else ("#fbbf24" if overall < 65 else "#4ade80")
        bar_color = "#ef4444" if overall < 50 else ("#f59e0b" if overall < 65 else "#10b981")

        findings_html = "".join([
            f'<li class="pd-finding-item"><span class="pd-finding-icon">⚠</span><span>{escape(str(f))}</span></li>'
            for f in visible
        ])
        locked_html = "".join([
            f'<div class="pd-lock-card"><span class="pd-lock-icon">🔒</span><span class="pd-lock-text">{escape(str(item))}</span></div>'
            for item in locked
        ])

        nextjs_url = os.environ.get("NEXTJS_URL", "http://localhost:3000")

        st.markdown(dedent(f"""
        <div class="pd-shell">

            <div class="pd-header">
                <div class="pd-header-left">
                    <div class="pd-badge">{_t(lang, "Ucretsiz On Analiz", "Free Preview")}</div>
                    <div class="pd-target">{target_str}</div>
                    <div class="pd-date">{created_at}</div>
                </div>
                <div class="pd-score-block">
                    <div class="pd-score-label">{_t(lang, "Donusum Skoru", "Conversion Score")}</div>
                    <div class="pd-score-num" style="color:{risk_color}">{overall}<span>/100</span></div>
                    <div class="pd-risk-pill" style="border-color:{risk_color}44;color:{risk_color};background:{risk_color}14">{risk}</div>
                </div>
            </div>

            <div class="pd-bar-track"><div class="pd-bar-fill" style="width:{overall}%;background:{bar_color}"></div></div>

            <div class="pd-sub-grid">
                <div class="pd-sub-item"><span>{_t(lang, "UX", "UX")}</span><b>{int(scores.get("ux",0))}/10</b></div>
                <div class="pd-sub-item"><span>{_t(lang, "Hiz", "Speed")}</span><b>{int(scores.get("speed",0))}/10</b></div>
                <div class="pd-sub-item"><span>{_t(lang, "Guven", "Trust")}</span><b>{int(scores.get("trust",0))}/10</b></div>
            </div>

            <div class="pd-section-title">⚠ {_t(lang, "Tespit Edilen Sorunlar", "Issues Found")}</div>
            <ul class="pd-findings-list">{findings_html}</ul>

            <div class="pd-lock-zone">
                <div class="pd-lock-zone-head">
                    <div class="pd-lock-zone-title">🔒 {_t(lang, "Premium Raporda Acilan Analizler", "Unlocked in Premium Report")}</div>
                    <div class="pd-lock-zone-sub">{_t(lang, "120+ metrik, rakip karsilastirmasi ve aksiyonlar gizlendi. Premium'a gec, tum detaylari gor.", "120+ metrics, competitor comparison and actions are hidden. Upgrade to see everything.")}</div>
                </div>
                <div class="pd-lock-cards">{locked_html}</div>
            </div>

            <div class="pd-upgrade-shell">
                <div class="pd-upgrade-top">
                    <div class="pd-upgrade-title">{_t(lang, "Tam AI Raporunu Al", "Get the Full AI Report")}</div>
                    <div class="pd-upgrade-sub">{_t(lang, "120+ metrik · Rakip karsilastirmasi · 30/60/90 gun aksiyon plani · Sinırsiz analiz", "120+ metrics · Competitor comparison · 30/60/90 day action plan · Unlimited analyses")}</div>
                </div>
                <div class="pd-upgrade-features">
                    <div class="pd-upgrade-feat">✓ {_t(lang, "Kritik gelir kaybi haritasi", "Critical revenue leakage map")}</div>
                    <div class="pd-upgrade-feat">✓ {_t(lang, "Checkout guveni icin adim adim UX plani", "Step-by-step UX plan for checkout trust")}</div>
                    <div class="pd-upgrade-feat">✓ {_t(lang, "A/B test backlog + KPI onceliklendirmesi", "A/B test backlog + KPI prioritization")}</div>
                    <div class="pd-upgrade-feat">✓ {_t(lang, "Rakibinizle kiyaslama", "Benchmark vs. competitors")}</div>
                </div>
                <a class="pd-upgrade-btn" href="{nextjs_url}#fiyatlar" target="_blank">{_t(lang, "Premium Erken Erisime Katil →", "Join Premium Early Access →")}</a>
                <div class="pd-upgrade-note">{_t(lang, "Ucretsiz hesabiniz var. Premium erken erisim icin bekleme listesine katilabilirsiniz.", "You have a free account. Join the waitlist for premium early access.")}</div>
            </div>

        </div>
        """), unsafe_allow_html=True)
        return

    impact = payload.get("impact", {})
    render_impact_overview(
        payload.get("scores", {}).get("overall", 0),
        impact.get("improvement_range", "-"),
        impact.get("priority_focus", "-"),
        lang,
    )

    previous = get_previous_analysis_for_target(
        user_id=user["id"],
        audit_type=detail["audit_type"],
        target=detail["target"],
        current_id=detail["id"],
    )
    previous_scores = (
        previous.get("payload", {}).get("scores", {}) if previous else None
    )
    trend_points = get_target_full_history(
        user_id=user["id"],
        audit_type=detail["audit_type"],
        target=detail["target"],
        limit=8,
    )
    render_delta_overview(
        payload.get("scores", {}),
        previous_scores,
        lang,
        detail["audit_type"],
        trend_points=trend_points,
    )

    render_website_results(payload, lang, is_premium=is_premium_user())


query_params = st.query_params


def _qp_get(name, default=""):
    val = query_params.get(name, default)
    if isinstance(val, list):
        return val[0] if val else default
    return val


lang = _qp_get("lang", "TR")
if lang not in ["TR", "EN"]:
    lang = "TR"

l = LANGS[lang]

# Product focus (V1): keep only website audit flow active.
audit_type = "website"

auth_view_param = _qp_get("auth_view", "")
if auth_view_param in ["login", "register"] and not st.session_state.get("user"):
    st.session_state["auth_view"] = auth_view_param

target_param = _qp_get("target", "")
if target_param and not st.session_state.get("user"):
    st.session_state["landing_url_input"] = target_param
    st.session_state["post_login_prefill_url"] = target_param
    # Auto-build teaser when user arrives from Next.js landing with a URL already set.
    # This lets render_landing skip its marketing content and jump straight to the result.
    if not st.session_state.get("teaser_preview"):
        _track_event("auto_teaser_from_landing", {"target": _compact_target(target_param)})
        audit_kind_param = _qp_get("audit", "website")
        st.session_state["teaser_preview"] = _build_teaser_preview(
            target=target_param,
            audit_kind=audit_kind_param,
            lang=lang,
        )
        st.session_state["scroll_to_teaser"] = True
        st.session_state["_from_next_landing"] = True

auth_token_param = _qp_get("auth_token", "")
if auth_token_param and not st.session_state.get("user"):
    valid_token, token_payload = _verify_bridge_token(auth_token_param)
    if valid_token:
        token_email = token_payload.get("email", "")
        token_version = int(token_payload.get("token_version", -1))
        bridged_user = get_user_by_email(token_email)
        if bridged_user and int(bridged_user.get("token_version", 0)) == token_version:
            st.session_state["user"] = bridged_user
            st.session_state["auth_view"] = None
            persist_preview_to_history_if_available(lang)
            if target_param and not st.session_state.get("website_url_input"):
                st.session_state["website_url_input"] = target_param
    if "auth_token" in st.query_params:
        del st.query_params["auth_token"]
    if st.session_state.get("user"):
        st.rerun()

# Security hardening: never accept credentials from URL query params.
for sensitive_key in ["auth_action", "auth_email", "auth_password"]:
    if sensitive_key in st.query_params:
        del st.query_params[sensitive_key]

if not st.session_state.get("user"):
    render_landing(lang)
    render_auth_popup(lang)
    render_legal_footer(lang)
    st.stop()

render_premium_sidebar(lang)

if st.session_state.get("profile_edit_open"):
    st.session_state["account_info_open"] = False
    render_profile_edit_popup(lang)
elif st.session_state.get("account_info_open"):
    st.session_state["profile_edit_open"] = False
    render_account_info_popup(lang)
render_admin_health_panel(lang)

if st.session_state.get("history_flash"):
    st.success(st.session_state["history_flash"])
    st.session_state["history_flash"] = ""

if st.session_state.get("sidebar_view") == "history":
    render_history_section(lang)
    st.stop()

render_client_premium_dashboard(lang)


if audit_type == "website":
    if st.session_state.get("post_login_prefill_url") and not st.session_state.get(
        "website_url_input"
    ):
        st.session_state["website_url_input"] = st.session_state[
            "post_login_prefill_url"
        ]
        st.session_state["website_form_open"] = True

    if not st.session_state.get("website_form_open"):
        if st.button(
            _t(lang, "Yeni Website Analizi Baslat", "Start New Website Analysis"),
            key="open_website_form_btn",
            use_container_width=True,
        ):
            st.session_state["website_form_open"] = True
            st.rerun()
        url_input, start = "", False
    else:
        url_input, start = render_intro_panels(
            l,
            input_label="Website URL",
            placeholder=(
                "https://yourwebsite.com" if lang == "EN" else "https://siteadresi.com"
            ),
            button_text=("Analyze Website" if lang == "EN" else "Web Siteyi Analiz Et"),
            input_key="website_url_input",
            default_value=st.session_state.get("website_url_input", ""),
        )
        if st.button(
            _t(lang, "Formu Gizle", "Hide Form"),
            key="close_website_form_btn",
            use_container_width=True,
        ):
            st.session_state["website_form_open"] = False
            st.rerun()

    if start:
        is_valid_url, normalized_website_url = _validate_website_url(url_input)
        if not is_valid_url:
            st.warning(
                _t(
                    lang,
                    "Lutfen gecerli bir URL gir.",
                    "Please enter a valid website URL.",
                )
            )
        else:
            _track_event(
                "website_analysis_start",
                {"target": _compact_target(normalized_website_url)},
            )
            _inc_runtime_metric("website_attempt")
            can_run, wait_sec = _check_rate_limit(
                "website_analysis", limit=4, window_seconds=60
            )
            if not can_run:
                st.warning(
                    _t(
                        lang,
                        f"Cok hizli istek yaptiniz. Lutfen {wait_sec} saniye bekleyin.",
                        f"Too many requests. Please wait {wait_sec} seconds.",
                    )
                )
                st.stop()
            with st.spinner(
                _t(lang, "Web sitesi analiz ediliyor...", "Analyzing website...")
            ):
                try:
                    baseline = get_latest_analysis_for_target(
                        user_id=st.session_state["user"]["id"],
                        audit_type="website",
                        target=normalized_website_url,
                    )
                    raw_response, shot = analyze_site(normalized_website_url, lang)
                    audit_data = parse_audit_response(raw_response)

                    ux = audit_data["scores"]["ux"]
                    speed = audit_data["scores"]["speed"]
                    trust = audit_data["scores"]["trust"]
                    overall = audit_data["scores"].get(
                        "overall", int(((ux + speed + trust) / 30) * 100)
                    )
                    improvement_range = audit_data.get("impact", {}).get(
                        "improvement_range", "-"
                    )
                    priority_focus = audit_data.get("impact", {}).get(
                        "priority_focus", "-"
                    )

                    st.markdown(
                        f'<div class="section-title">{l["screenshot_title"]}</div>',
                        unsafe_allow_html=True,
                    )
                    st.image(shot, use_container_width=True)

                    st.markdown(
                        f'<div class="section-title">{l["scores_title"]}</div>',
                        unsafe_allow_html=True,
                    )
                    c1, c2, c3 = st.columns(3)
                    with c1:
                        render_metric_card(l["ux"], f"{ux}/10")
                    with c2:
                        render_metric_card(l["speed"], f"{speed}/10")
                    with c3:
                        render_metric_card(l["trust"], f"{trust}/10")

                    render_impact_overview(
                        overall, improvement_range, priority_focus, lang
                    )
                    prev_scores = (
                        baseline.get("payload", {}).get("scores", {})
                        if baseline
                        else None
                    )
                    live_trend = get_target_full_history(
                        user_id=st.session_state["user"]["id"],
                        audit_type="website",
                        target=normalized_website_url,
                        limit=7,
                    )
                    live_trend.insert(
                        0, {"overall_score": overall, "created_at": "Now"}
                    )
                    render_delta_overview(
                        audit_data.get("scores", {}),
                        prev_scores,
                        lang,
                        "website",
                        trend_points=live_trend,
                    )
                    render_website_results(
                        audit_data, lang, is_premium=is_premium_user()
                    )

                    saved_id = save_analysis(
                        user_id=st.session_state["user"]["id"],
                        audit_type="website",
                        target=normalized_website_url,
                        lang=lang,
                        audit_data=audit_data,
                    )
                    st.session_state["history_flash"] = _t(
                        lang,
                        f"Analiz kaydedildi (#{saved_id}). Gecmis Analizlerim guncellendi.",
                        f"Analysis saved (#{saved_id}). History has been updated.",
                    )
                    _track_event(
                        "website_analysis_success",
                        {"target": _compact_target(normalized_website_url)},
                    )
                    _inc_runtime_metric("website_success")
                    st.rerun()

                    pdf_ready_text = audit_data_to_text(audit_data, lang)
                    pdf_file = create_pdf(pdf_ready_text, shot, lang)

                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            l["download_pdf"],
                            f,
                            pdf_file,
                            "application/pdf",
                            use_container_width=True,
                        )

                except Exception as e:
                    _inc_runtime_metric("website_fail")
                    _show_handled_error(
                        lang,
                        e,
                        context="website_analysis",
                        tr_generic=l["system_error"],
                        en_generic=l["system_error"],
                    )

render_legal_footer(lang)

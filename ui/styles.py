import streamlit as st


def load_global_styles():
    st.markdown(
        """
    <style>
    .stApp {
        background:
            radial-gradient(circle at 86% 18%, rgba(104, 241, 255, 0.24), transparent 24%),
            radial-gradient(circle at 52% 86%, rgba(76, 149, 255, 0.12), transparent 28%),
            radial-gradient(circle at 16% 16%, rgba(44, 118, 238, 0.10), transparent 30%),
            radial-gradient(1px 1px at 12% 22%, rgba(220, 242, 255, 0.26), transparent 60%),
            radial-gradient(1px 1px at 32% 64%, rgba(220, 242, 255, 0.22), transparent 60%),
            radial-gradient(1px 1px at 64% 38%, rgba(220, 242, 255, 0.24), transparent 60%),
            radial-gradient(1px 1px at 84% 48%, rgba(220, 242, 255, 0.20), transparent 60%),
            linear-gradient(180deg, #040b17 0%, #08182d 46%, #0a1f3a 100%);
        color: #ffffff;
    }

    .block-container {
        max-width: 1180px;
        padding-top: 2.2rem;
        padding-bottom: 4rem;
    }

    /* ── Sidebar: premium dark ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(170deg, rgba(5,14,30,0.99) 0%, rgba(6,16,32,0.98) 100%);
        border-right: 1px solid rgba(83,145,236,0.22);
        min-width: 240px !important;
        max-width: 240px !important;
    }
    section[data-testid="stSidebar"] > div:first-child {
        padding: 1.4rem 1rem 1rem 1rem;
    }
    .sb-logo {
        color: #f3f8ff; font-size: 26px; font-weight: 900;
        letter-spacing: -0.03em; margin-bottom: 20px; padding-bottom: 14px;
        border-bottom: 1px solid rgba(83,145,236,0.18);
    }
    .sb-logo span { color: #22d3ee; }
    .sb-nav-label {
        font-size: 10px; font-weight: 700; letter-spacing: 0.1em;
        color: #3b5a80; text-transform: uppercase; margin-bottom: 6px; padding-left: 4px;
    }
    .sb-nav-btn {
        display: block; width: 100%; padding: 9px 12px; border-radius: 10px;
        color: #a9bfd8; font-size: 13px; font-weight: 700; text-decoration: none;
        border: 1px solid transparent; margin-bottom: 4px; cursor: pointer;
        background: transparent; transition: all 0.15s;
    }
    .sb-nav-btn:hover { color: #e9f7ff; background: rgba(24,84,152,0.4); border-color: rgba(102,177,255,0.3); }
    .sb-nav-btn.active { color: #e9f7ff; background: rgba(24,84,152,0.55); border-color: rgba(102,177,255,0.38); }
    .sb-divider { border: none; border-top: 1px solid rgba(83,145,236,0.16); margin: 14px 0; }
    .sb-plan {
        padding: 10px 12px; border-radius: 10px;
        border: 1px solid rgba(83,145,236,0.22); background: rgba(13,33,59,0.7);
        color: #d4e5f8; margin-top: 8px;
    }
    .sb-plan b { display: block; font-size: 13px; font-weight: 800; }
    .sb-plan small { color: #6e90b4; font-size: 11px; line-height: 1.5; }
    .sb-plan .sb-upgrade-link {
        display: block; margin-top: 8px; padding: 6px 10px; border-radius: 8px;
        background: linear-gradient(90deg,rgba(34,211,238,0.18),rgba(56,189,248,0.14));
        border: 1px solid rgba(34,211,238,0.3); color: #7ee7ff;
        font-size: 12px; font-weight: 700; text-align: center; text-decoration: none;
    }
    .sb-user {
        margin-top: 10px; padding: 8px 12px; border-radius: 10px;
        border: 1px solid rgba(83,145,236,0.14); background: rgba(10,25,48,0.5);
        color: #7090b0; font-size: 12px; font-weight: 600;
    }
    .sb-user b { display: block; color: #b0cae4; font-size: 13px; }
    /* Override Streamlit sidebar button */
    section[data-testid="stSidebar"] .stButton > button {
        background: transparent !important;
        border: 1px solid rgba(83,145,236,0.18) !important;
        border-radius: 10px !important;
        color: #8aaccf !important;
        font-size: 13px !important; font-weight: 700 !important;
        text-align: left !important;
        padding: 9px 12px !important;
        width: 100% !important;
        transition: all 0.15s !important;
    }
    section[data-testid="stSidebar"] .stButton > button:hover {
        background: rgba(24,84,152,0.4) !important;
        border-color: rgba(102,177,255,0.32) !important;
        color: #e9f7ff !important;
    }
    section[data-testid="stSidebar"] .stButton > button:focus {
        outline: none !important; box-shadow: 0 0 0 2px rgba(34,211,238,0.22) !important;
    }
    section[data-testid="stSidebar"] [data-testid="stMarkdown"] p {
        color: #6e90b4; font-size: 12px;
    }

    header[data-testid="stHeader"],
    div[data-testid="stToolbar"],
    div[data-testid="stDecoration"] {
        display: none !important;
    }

    header [data-testid="stTextInput"],
    [data-testid="stHeader"] [data-testid="stTextInput"],
    [data-testid="stToolbar"] [data-testid="stTextInput"] {
        display: none !important;
    }


    .hero-shell {
        background: linear-gradient(135deg, #071325 0%, #10233e 60%, #14314b 100%);
        border: 1px solid rgba(34, 211, 238, 0.16);
        border-radius: 28px;
        padding: 34px 34px 30px 34px;
        box-shadow: 0 18px 60px rgba(0, 0, 0, 0.28);
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
    }

    .hero-shell::after {
        content: "";
        position: absolute;
        top: -40px;
        right: -50px;
        width: 220px;
        height: 220px;
        background: radial-gradient(circle, rgba(34,211,238,0.28), transparent 70%);
        pointer-events: none;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        padding: 8px 14px;
        border-radius: 999px;
        background: rgba(34,211,238,0.10);
        border: 1px solid rgba(34,211,238,0.18);
        color: #8be9f7;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 14px;
    }

    .hero-title {
        font-size: 46px;
        line-height: 1.03;
        font-weight: 800;
        letter-spacing: -0.03em;
        color: #ffffff;
        margin-bottom: 12px;
    }

    .hero-subtitle {
        max-width: 760px;
        color: #d3e4f7;
        font-size: 18px;
        line-height: 1.7;
    }

    .top-nav {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        gap: 34px;
        padding: 6px 0 14px 0;
    }

    .brand-line {
        color: #f5fbff;
        font-size: 40px;
        font-weight: 800;
        white-space: nowrap;
        letter-spacing: -0.03em;
    }

    .brand-green {
        color: #25d78f;
    }

    .landing-title {
        font-size: 72px;
        line-height: 0.98;
        font-weight: 900;
        letter-spacing: -0.03em;
        margin: 8px 0 14px 0;
    }

    .landing-sub {
        color: #cbdcf0;
        font-size: 17px;
        line-height: 1.8;
        max-width: 780px;
        margin-bottom: 8px;
    }

    .feature-strip {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 14px;
        margin: 22px 0 10px 0;
    }

    .feature-item {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 16px;
        padding: 14px 16px;
        color: #d9e7f6;
        font-size: 14px;
        line-height: 1.5;
    }

    .landing-shell {
        background: linear-gradient(145deg, rgba(6,17,33,0.90), rgba(10,30,54,0.88));
        border: 1px solid rgba(140, 224, 255, 0.22);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 24px 70px rgba(0,0,0,0.40), 0 0 32px rgba(78, 198, 245, 0.12);
        margin-bottom: 20px;
        backdrop-filter: blur(2px);
    }

    .menu-row {
        display: flex;
        gap: 28px;
        align-items: center;
        color: #b7cde3;
        font-size: 15px;
        margin: 2px 0 0 0;
    }

    .menu-item {
        position: relative;
        color: #c7dbef;
        cursor: default;
        font-weight: 600;
    }

    .menu-item > span {
        transition: color 0.2s ease, text-shadow 0.2s ease;
    }

    .menu-item:hover > span {
        color: #ecf7ff;
        text-shadow: 0 0 10px rgba(126, 228, 255, 0.35);
    }

    .menu-dropdown {
        position: absolute;
        top: 28px;
        left: 0;
        min-width: 280px;
        border: 1px solid rgba(129, 216, 255, 0.26);
        border-radius: 12px;
        background: linear-gradient(155deg, rgba(9, 27, 47, 0.96), rgba(11, 39, 66, 0.95));
        box-shadow: 0 14px 30px rgba(0,0,0,0.28), 0 0 14px rgba(97, 217, 255, 0.12);
        padding: 10px 12px;
        opacity: 0;
        transform: translateY(8px);
        pointer-events: none;
        transition: opacity 0.18s ease, transform 0.18s ease;
        z-index: 40;
    }

    .menu-item:hover .menu-dropdown {
        opacity: 1;
        transform: translateY(0);
        pointer-events: auto;
    }

    .menu-dd-title {
        color: #f2f8ff;
        font-size: 13px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .menu-dd-line {
        color: #c5dbef;
        font-size: 13px;
        line-height: 1.55;
        margin-bottom: 4px;
    }

    .landing-divider {
        height: 1px;
        background: rgba(144, 213, 255, 0.22);
        margin: 8px 0 20px 0;
    }

    .hero-visual {
        min-height: 378px;
        border-radius: 24px;
        border: 1px solid rgba(116, 227, 255, 0.32);
        background:
            radial-gradient(circle at 84% 12%, rgba(126, 245, 255, 0.36), transparent 34%),
            radial-gradient(circle at 18% 86%, rgba(30, 126, 255, 0.30), transparent 44%),
            linear-gradient(160deg, rgba(6, 20, 40, 0.94) 0%, rgba(14, 43, 70, 0.90) 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 18px;
        box-shadow: inset 0 0 80px rgba(0,0,0,0.30), 0 0 28px rgba(84, 220, 255, 0.18);
    }

    .hero-screen {
        width: 100%;
        background: linear-gradient(170deg, rgba(10, 24, 42, 0.92), rgba(8, 31, 52, 0.86));
        border: 1px solid rgba(141, 228, 255, 0.30);
        border-radius: 18px;
        padding: 16px;
        backdrop-filter: blur(4px);
        box-shadow: 0 20px 42px rgba(0,0,0,0.34), 0 0 24px rgba(113, 225, 255, 0.14);
    }

    .hero-screen-top {
        display: flex;
        justify-content: space-between;
        align-items: flex-start;
        color: #e8f4ff;
        margin-bottom: 10px;
    }

    .hero-top-title {
        font-size: 20px;
        font-weight: 800;
        letter-spacing: -0.01em;
        line-height: 1.2;
    }

    .hero-top-sub {
        font-size: 12px;
        color: #98b6d2;
        margin-top: 2px;
    }

    .hero-score-wrap {
        text-align: right;
        min-width: 64px;
    }

    .hero-score-label {
        font-size: 12px;
        color: #98b6d2;
        text-transform: uppercase;
        letter-spacing: 0.04em;
        line-height: 1;
        margin-bottom: 3px;
    }

    .hero-score-value {
        font-size: 28px;
        font-weight: 900;
        line-height: 0.95;
        letter-spacing: -0.02em;
        color: #eef8ff;
    }

    .hero-trend {
        margin-top: 5px;
        display: inline-block;
        font-size: 11px;
        font-weight: 700;
        color: #9df9d6;
        border: 1px solid rgba(107, 241, 198, 0.38);
        background: rgba(40, 126, 103, 0.20);
        border-radius: 999px;
        padding: 3px 8px;
    }

    .hero-bar {
        height: 10px;
        border-radius: 999px;
        background: rgba(255,255,255,0.14);
        overflow: hidden;
        margin-bottom: 14px;
    }

    .hero-bar-fill {
        width: 47%;
        height: 100%;
        background: linear-gradient(90deg, #ff9a4b, #ffd15e);
        box-shadow: 0 0 12px rgba(255, 192, 92, 0.45);
    }

    .hero-alert {
        color: #f7e5b5;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .hero-severity {
        font-size: 14px;
        color: #f5c982;
        font-weight: 600;
    }

    .hero-value {
        color: #ffd78f;
        font-size: 24px;
        font-weight: 900;
        letter-spacing: -0.02em;
        margin-bottom: 10px;
    }

    .hero-metric-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 9px 2px 7px 2px;
        color: #dbe9f8;
        border-top: 1px solid rgba(133, 207, 245, 0.16);
        font-size: 15px;
    }

    .hero-metric-row span:last-child {
        font-weight: 800;
        color: #eff7ff;
    }

    .hero-mini-progress {
        height: 5px;
        background: rgba(192, 224, 248, 0.16);
        border-radius: 999px;
        overflow: hidden;
        margin: 0 2px 6px 2px;
    }

    .hero-mini-progress-fill {
        height: 100%;
        border-radius: 999px;
    }

    .hero-mini-progress-fill-low {
        width: 22%;
        background: linear-gradient(90deg, #ff9250, #ffb45a);
        box-shadow: 0 0 10px rgba(255, 174, 91, 0.42);
    }

    .hero-mini-progress-fill-mid {
        width: 54%;
        background: linear-gradient(90deg, #5ec4ff, #72ddff);
        box-shadow: 0 0 10px rgba(110, 215, 255, 0.34);
    }

    .hero-chip-row {
        display: flex;
        gap: 8px;
        margin-top: 10px;
        margin-bottom: 12px;
    }

    .hero-mini-chip {
        font-size: 12px;
        color: #d8f5ff;
        border: 1px solid rgba(77, 205, 238, 0.42);
        background: rgba(24, 88, 120, 0.28);
        border-radius: 999px;
        padding: 5px 10px;
    }

    .hero-detail-btn {
        margin-top: 10px;
        border-radius: 999px;
        border: 1px solid rgba(145, 232, 255, 0.44);
        background: linear-gradient(135deg, rgba(23, 82, 116, 0.92), rgba(34, 116, 153, 0.88));
        color: #f0fbff;
        text-align: center;
        font-size: 18px;
        font-weight: 700;
        padding: 11px 16px;
        box-shadow: 0 0 14px rgba(101, 225, 255, 0.18);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    .hero-detail-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 0 18px rgba(101, 225, 255, 0.24);
    }

    .pitch-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 14px;
        margin-top: 18px;
    }

    .pitch-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.12);
        border-radius: 18px;
        padding: 16px;
    }

    .pitch-title {
        color: #ffffff;
        font-size: 17px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .pitch-sub {
        color: #cfe0f4;
        font-size: 14px;
        line-height: 1.7;
        margin-bottom: 10px;
    }

    .sample-chip {
        display: inline-block;
        margin-right: 8px;
        margin-bottom: 8px;
        padding: 5px 10px;
        border-radius: 999px;
        color: #d9f6ff;
        background: rgba(34,211,238,0.14);
        border: 1px solid rgba(34,211,238,0.30);
        font-size: 12px;
        font-weight: 700;
    }

    .trust-row {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 12px;
        margin: 18px 0 2px 0;
    }

    .trust-box {
        border-radius: 14px;
        border: 1px solid rgba(255,255,255,0.10);
        background: rgba(255,255,255,0.04);
        padding: 14px 12px;
        text-align: center;
    }

    .trust-big {
        color: #ffffff;
        font-size: 22px;
        font-weight: 900;
        line-height: 1.1;
    }

    .trust-small {
        color: #abc2da;
        font-size: 12px;
        margin-top: 5px;
    }

    .logo-strip {
        margin-top: 16px;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 14px;
        background: rgba(255,255,255,0.03);
        padding: 10px 12px;
        display: flex;
        justify-content: space-around;
        color: #93a8bc;
        font-weight: 700;
        text-transform: lowercase;
        letter-spacing: 0.03em;
    }

    .landing-section-card {
        margin-top: 18px;
        border: 1px solid rgba(136, 216, 255, 0.20);
        border-radius: 18px;
        background: linear-gradient(145deg, rgba(8, 25, 44, 0.84), rgba(10, 36, 63, 0.80));
        box-shadow: 0 12px 28px rgba(0,0,0,0.24);
        padding: 18px;
        scroll-margin-top: 80px;
    }

    .landing-section-title {
        color: #ecf6ff;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.01em;
        margin-bottom: 12px;
    }

    .landing-steps-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 12px;
    }

    .landing-step-item {
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 14px;
        background: rgba(255,255,255,0.03);
        padding: 12px;
    }

    .landing-step-head {
        color: #f2f8ff;
        font-size: 15px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .landing-step-text {
        color: #c8dcee;
        font-size: 14px;
        line-height: 1.6;
    }

    .landing-feature-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
    }

    .landing-feature-item {
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 14px;
        background: rgba(255,255,255,0.03);
        padding: 12px;
        color: #c8dcee;
        font-size: 14px;
        line-height: 1.6;
    }

    .landing-feature-item strong {
        color: #f2f8ff;
    }

    .pricing-card-grid {
        display: grid;
        grid-template-columns: repeat(2, minmax(0, 1fr));
        gap: 12px;
    }

    .pricing-card-mini {
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 14px;
        background: rgba(255,255,255,0.03);
        padding: 14px;
    }

    .pricing-card-mini-highlight {
        border-color: rgba(126, 228, 255, 0.40);
        background: linear-gradient(145deg, rgba(18, 66, 102, 0.62), rgba(11, 45, 74, 0.62));
        box-shadow: 0 0 14px rgba(106, 224, 255, 0.16);
    }

    .pricing-plan-name {
        color: #eaf6ff;
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 6px;
    }

    .pricing-plan-price {
        color: #ffffff;
        font-size: 26px;
        font-weight: 900;
        letter-spacing: -0.02em;
        margin-bottom: 6px;
    }

    .pricing-plan-note {
        color: #bfd6ea;
        font-size: 14px;
    }

    .proof-line {
        margin-top: 12px;
        color: #dbe8f7;
        font-size: 36px;
        text-align: center;
        letter-spacing: -0.02em;
    }

    .st-key-nav_login button,
    .st-key-nav_signup button {
        height: 52px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(117, 217, 255, 0.42) !important;
        background: linear-gradient(145deg, rgba(17, 44, 74, 0.92), rgba(18, 58, 92, 0.86)) !important;
        color: #e8f6ff !important;
        font-weight: 700 !important;
        font-size: 25px !important;
        box-shadow: 0 10px 26px rgba(0,0,0,0.28), 0 0 14px rgba(102, 225, 255, 0.12) !important;
    }

    .landing-url-wrap {
        margin-top: 12px;
        margin-bottom: 10px;
    }

    .st-key-landing_website_cta button {
        height: 58px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(147, 233, 255, 0.48) !important;
        background: linear-gradient(135deg, rgba(37, 98, 142, 0.96), rgba(66, 161, 201, 0.90)) !important;
        color: #f5fcff !important;
        font-weight: 800 !important;
        font-size: 22px !important;
        box-shadow: 0 12px 28px rgba(0,0,0,0.28), 0 0 20px rgba(108, 227, 255, 0.22) !important;
    }

    .st-key-landing_instagram_cta button {
        height: 58px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(108, 204, 242, 0.34) !important;
        background: linear-gradient(135deg, rgba(16, 47, 79, 0.94), rgba(21, 69, 108, 0.90)) !important;
        color: #deefff !important;
        font-weight: 700 !important;
        font-size: 19px !important;
    }


    .dash-side-shell {
        background: linear-gradient(180deg, rgba(9, 23, 42, 0.96), rgba(8, 29, 53, 0.92));
        border: 1px solid rgba(89, 219, 192, 0.22);
        border-radius: 18px;
        padding: 16px 14px;
        box-shadow: 0 20px 40px rgba(0,0,0,0.28);
        margin-top: 8px;
        margin-bottom: 10px;
    }

    .dash-brand {
        color: #f3fbff;
        font-size: 24px;
        font-weight: 800;
        letter-spacing: -0.02em;
        margin-bottom: 10px;
    }

    .dash-menu-title {
        color: #9dc0dd;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
    }

    .dash-main-title {
        color: #ffffff;
        font-size: 48px;
        font-weight: 900;
        line-height: 1.06;
        letter-spacing: -0.03em;
        margin-top: 4px;
        margin-bottom: 8px;
    }

    .dash-hero-card {
        margin-top: 14px;
        background: linear-gradient(160deg, rgba(8, 29, 52, 0.96), rgba(14, 47, 75, 0.92));
        border: 1px solid rgba(98, 225, 191, 0.32);
        border-radius: 22px;
        padding: 22px;
        box-shadow: inset 0 0 80px rgba(255,255,255,0.02), 0 22px 40px rgba(0,0,0,0.3);
    }

    .dash-hero-badge {
        display: inline-block;
        padding: 7px 12px;
        border-radius: 999px;
        border: 1px solid rgba(93, 220, 191, 0.34);
        color: #8ff3d7;
        font-size: 13px;
        font-weight: 700;
        margin-bottom: 10px;
    }

    .dash-hero-title {
        background: linear-gradient(90deg, #ffffff 0%, #d9f3ff 45%, #9fe7ff 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 56px;
        line-height: 1.02;
        font-weight: 900;
        letter-spacing: -0.03em;
        margin-bottom: 8px;
    }

    .dash-hero-sub {
        color: #d6e7f6;
        font-size: 18px;
        line-height: 1.65;
    }

    .right-topline {
        display: flex;
        justify-content: flex-start;
        align-items: center;
        gap: 8px;
        margin-top: 0;
        margin-bottom: 0;
        margin-left: 16px;
        min-height: 44px;
    }

    .right-user-dot {
        width: 38px;
        height: 38px;
        border-radius: 999px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        background: linear-gradient(135deg, rgba(19, 56, 88, 0.94), rgba(14, 39, 63, 0.94));
        border: 1px solid rgba(109, 226, 198, 0.34);
        font-size: 18px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.26);
    }

    .right-plan-pill {
        padding: 8px 14px;
        border-radius: 10px;
        border: 1px solid rgba(91, 221, 193, 0.36);
        color: #d8fff3;
        font-size: 20px;
        font-weight: 700;
        background: linear-gradient(135deg, rgba(10, 31, 54, 0.96), rgba(16, 52, 81, 0.92));
        line-height: 1;
        margin-left: 0;
    }

    .footer-site {
        margin-top: 24px;
        border-top: 1px solid rgba(255,255,255,0.12);
        padding-top: 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 12px;
    }

    .footer-brand {
        color: #cfe0f4;
        font-size: 13px;
        font-weight: 600;
    }

    .footer-links a {
        color: #8be9f7;
        text-decoration: none;
        margin-left: 12px;
        font-size: 13px;
        border-bottom: 1px solid rgba(139,233,247,0.0);
    }

    .footer-links a:hover {
        border-bottom-color: rgba(139,233,247,0.9);
    }

    .profile-shell {
        background: linear-gradient(135deg, rgba(12, 34, 56, 0.94), rgba(18, 53, 82, 0.92));
        border: 1px solid rgba(93, 220, 191, 0.28);
        border-radius: 18px;
        padding: 14px;
        box-shadow: 0 16px 36px rgba(0,0,0,0.24);
        margin-top: 8px;
    }

    .profile-email {
        color: #ffffff;
        font-size: 14px;
        font-weight: 700;
        line-height: 1.4;
        word-break: break-all;
    }

    .profile-plan {
        color: #8be9f7;
        font-size: 12px;
        font-weight: 700;
        margin-top: 4px;
        margin-bottom: 8px;
        letter-spacing: 0.04em;
        text-transform: uppercase;
    }

    div[role="radiogroup"] {
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(106, 210, 246, 0.26);
        border-radius: 12px;
        padding: 8px 10px;
        margin-top: 2px;
    }

    div[role="radiogroup"] label {
        color: #eaf6ff !important;
        opacity: 1 !important;
    }

    div[role="radiogroup"] p,
    div[role="radiogroup"] span {
        color: #dff0ff !important;
        -webkit-text-fill-color: #dff0ff !important;
        opacity: 1 !important;
    }

    div[role="radiogroup"] [aria-checked="true"] p,
    div[role="radiogroup"] [aria-checked="true"] span,
    div[role="radiogroup"] [data-checked="true"] p,
    div[role="radiogroup"] [data-checked="true"] span {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 700 !important;
    }

    .profile-topline {
        display: flex;
        justify-content: flex-end;
        margin-top: 8px;
        margin-bottom: 8px;
    }

    .profile-plan-pill {
        display: inline-block;
        padding: 6px 10px;
        border-radius: 999px;
        border: 1px solid rgba(93, 220, 191, 0.36);
        background: rgba(93, 220, 191, 0.14);
        color: #d5fff2;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.05em;
        text-transform: uppercase;
    }

    button[aria-haspopup="dialog"],
    button[aria-haspopup="menu"],
    div[data-testid="stPopover"] button {
        min-width: 72px !important;
        width: 72px !important;
        height: 44px !important;
        border-radius: 12px !important;
        min-height: 44px !important;
        padding: 0 10px !important;
        font-size: 18px !important;
        line-height: 1 !important;
        border: 1px solid rgba(109, 226, 198, 0.34) !important;
        background: linear-gradient(135deg, rgba(19, 56, 88, 0.94), rgba(14, 39, 63, 0.94)) !important;
        box-shadow: 0 10px 26px rgba(0,0,0,0.30) !important;
        color: #e7f4ff !important;
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;
        gap: 6px !important;
        letter-spacing: 0 !important;
        position: relative !important;
    }

    /* Hard override for Streamlit popover trigger variants */
    [data-testid="stPopover"] button,
    [data-testid="stPopoverButton"],
    button[data-testid="stPopoverButton"],
    div[data-testid*="Popover"] > button {
        min-width: 72px !important;
        width: 72px !important;
        max-width: 72px !important;
        height: 44px !important;
        min-height: 44px !important;
        max-height: 44px !important;
        border-radius: 12px !important;
        padding: 0 10px !important;
    }

    div[data-testid="stPopover"] button::after {
        content: "▾";
        position: absolute;
        right: 8px;
        top: 8px;
        font-size: 10px;
        color: #dff3ff;
        line-height: 1;
    }

    .avatar-default {
        width: 120px;
        height: 120px;
        border-radius: 999px;
        margin: 4px auto 10px auto;
        background: rgba(255,255,255,0.08);
        border: 1px solid rgba(255,255,255,0.16);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 56px;
    }

    .avatar-small {
        width: 72px;
        height: 72px;
        font-size: 34px;
        margin: 0 auto 10px auto;
    }

    .account-menu-head {
        text-align: center;
        margin-bottom: 12px;
        padding: 10px 12px;
        border-radius: 12px;
        background: linear-gradient(145deg, rgba(10, 31, 54, 0.96), rgba(16, 52, 81, 0.92));
        border: 1px solid rgba(104, 219, 202, 0.28);
    }

    .account-name {
        color: #f3fbff !important;
        font-size: 16px;
        font-weight: 700;
        margin-bottom: 4px;
        word-break: break-all;
        -webkit-text-fill-color: #f3fbff !important;
        text-shadow: none !important;
        opacity: 1 !important;
    }

    .account-sub {
        color: #bfe0ff !important;
        font-size: 13px;
        margin-bottom: 8px;
        -webkit-text-fill-color: #bfe0ff !important;
        text-shadow: none !important;
        opacity: 1 !important;
    }

    .account-info-line {
        margin-bottom: 12px;
        line-height: 1.6;
    }

    .account-info-label {
        color: #dcecff;
        font-weight: 700;
    }

    .account-info-value {
        color: #f4fbff;
        font-weight: 600;
    }

    /* SUPPORT EXPANDER */
    [data-testid="stExpander"] details,
    details[data-testid="stExpander"] {
        border: 1px solid rgba(89, 219, 192, 0.22) !important;
        border-radius: 16px !important;
        background: linear-gradient(180deg, rgba(9, 23, 42, 0.96), rgba(8, 29, 53, 0.92)) !important;
        box-shadow: 0 12px 28px rgba(0,0,0,0.22) !important;
        overflow: hidden;
    }

    [data-testid="stExpander"] summary,
    details[data-testid="stExpander"] summary {
        background: linear-gradient(135deg, rgba(16, 47, 79, 0.94), rgba(21, 69, 108, 0.90)) !important;
        color: #deefff !important;
        border: 1px solid rgba(108, 204, 242, 0.34) !important;
        border-radius: 14px !important;
        box-shadow: 0 10px 24px rgba(0,0,0,0.20) !important;
        font-weight: 700 !important;
        padding-top: 10px !important;
        padding-bottom: 10px !important;
    }

    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span,
    [data-testid="stExpander"] summary div,
    details[data-testid="stExpander"] summary p,
    details[data-testid="stExpander"] summary span,
    details[data-testid="stExpander"] summary div {
        color: #deefff !important;
        -webkit-text-fill-color: #deefff !important;
    }

    .support-box {
        margin-bottom: 10px;
        padding: 10px 12px;
        border: 1px solid rgba(104, 219, 202, 0.24);
        border-radius: 12px;
        background: rgba(255,255,255,0.03);
    }

    .support-title {
        color: #eaf6ff;
        font-size: 16px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .support-sub {
        color: #c9def2;
        font-size: 14px;
        margin-bottom: 6px;
    }

    .support-meta {
        color: #9ec0dc;
        font-size: 12px;
        line-height: 1.5;
    }

    .history-row-card {
        border: 1px solid rgba(115, 204, 241, 0.24);
        border-radius: 14px;
        background: linear-gradient(145deg, rgba(11, 30, 52, 0.88), rgba(12, 40, 66, 0.84));
        padding: 12px 14px;
        margin-bottom: 8px;
    }

    .history-row-top {
        color: #b8d7f0;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.02em;
        margin-bottom: 4px;
    }

    .history-row-main {
        color: #eef8ff;
        font-size: 16px;
        font-weight: 700;
        line-height: 1.45;
        margin-bottom: 3px;
    }

    .history-row-sub {
        color: #8fb3d1;
        font-size: 12px;
    }

    .history-trend-title {
        color: #cfe8ff;
        font-size: 14px;
        font-weight: 700;
        margin: 10px 0 8px 2px;
    }

    .history-trend-card {
        border: 1px solid rgba(115, 204, 241, 0.24);
        border-radius: 14px;
        background: linear-gradient(145deg, rgba(11, 30, 52, 0.88), rgba(12, 40, 66, 0.84));
        padding: 12px 14px 10px;
        margin-bottom: 12px;
    }

    .history-trend-row {
        margin-bottom: 10px;
    }

    .history-trend-row:last-child {
        margin-bottom: 0;
    }

    .history-trend-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #b8d7f0;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 5px;
    }

    .history-trend-track {
        width: 100%;
        height: 8px;
        border-radius: 999px;
        background: rgba(148, 176, 202, 0.24);
        overflow: hidden;
    }

    .history-trend-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #2ad8ff 0%, #62e7ff 48%, #9ff2ff 100%);
        box-shadow: 0 0 10px rgba(62, 218, 255, 0.45);
    }

    .cmp-main {
        border: 1px solid rgba(117, 217, 255, 0.28);
        border-radius: 14px;
        padding: 14px 16px;
        color: #ecf8ff;
        font-size: 24px;
        font-weight: 800;
        background: linear-gradient(135deg, rgba(10, 29, 52, 0.90), rgba(12, 39, 68, 0.88));
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.20);
        margin-bottom: 8px;
    }

    .cmp-hint {
        border: 1px solid rgba(115, 204, 241, 0.20);
        border-radius: 12px;
        padding: 14px;
        color: #b4d6ef;
        font-size: 13px;
        background: rgba(10, 29, 52, 0.55);
        text-align: center;
        margin-bottom: 8px;
    }

    .cmp-wrap {
        margin-top: 10px;
        border: 1px solid rgba(117, 217, 255, 0.24);
        border-radius: 14px;
        padding: 12px 14px;
        background: linear-gradient(145deg, rgba(11, 30, 52, 0.85), rgba(12, 40, 66, 0.80));
    }

    .cmp-title {
        color: #d9efff;
        font-size: 14px;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .cmp-row {
        margin-bottom: 8px;
    }

    .cmp-row:last-child {
        margin-bottom: 0;
    }

    .cmp-row-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #a8cce8;
        font-size: 12px;
        margin-bottom: 4px;
    }

    .cmp-track {
        width: 100%;
        height: 8px;
        border-radius: 999px;
        background: rgba(148, 176, 202, 0.24);
        overflow: hidden;
    }

    .cmp-fill {
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #2ad8ff 0%, #62e7ff 48%, #9ff2ff 100%);
        box-shadow: 0 0 10px rgba(62, 218, 255, 0.4);
    }

    [data-testid="stExpander"] [data-testid="stLinkButton"] a,
    details[data-testid="stExpander"] [data-testid="stLinkButton"] a {
        height: 52px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(108, 204, 242, 0.34) !important;
        background: linear-gradient(135deg, rgba(16, 47, 79, 0.94), rgba(21, 69, 108, 0.90)) !important;
        color: #deefff !important;
        font-weight: 700 !important;
        font-size: 16px !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-decoration: none !important;
        margin-top: 8px !important;
    }

    [data-testid="stExpander"] [data-testid="stLinkButton"] a:hover,
    details[data-testid="stExpander"] [data-testid="stLinkButton"] a:hover {
        border: 1px solid rgba(117, 217, 255, 0.42) !important;
        background: linear-gradient(145deg, rgba(17, 44, 74, 0.92), rgba(18, 58, 92, 0.86)) !important;
        color: #e8f6ff !important;
    }

    .main-form-card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 24px;
        padding: 24px;
        box-shadow: 0 14px 40px rgba(0,0,0,0.18);
        margin-bottom: 24px;
    }

    .form-label {
        color: #ffffff;
        font-size: 18px;
        font-weight: 700;
        margin-bottom: 12px;
    }

    .section-title {
        margin-top: 24px;
        margin-bottom: 14px;
        color: #ffffff;
        font-size: 28px;
        font-weight: 800;
        letter-spacing: -0.02em;
    }

    .metric-card {
        background: linear-gradient(180deg, rgba(255,255,255,0.06), rgba(255,255,255,0.03));
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 22px;
        min-height: 128px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.18);
    }

    .metric-title {
        color: #9fb3c8;
        font-size: 13px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        margin-bottom: 12px;
    }

    .metric-value {
        color: #ffffff;
        font-size: 34px;
        font-weight: 800;
        line-height: 1;
        margin-bottom: 6px;
    }

    .metric-sub {
        color: #7f94ab;
        font-size: 13px;
    }

    .section-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 22px;
        margin-bottom: 16px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.16);
    }

    .section-card-title {
        color: #ffffff;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .section-card-text {
        color: #d6e2ef;
        font-size: 15px;
        line-height: 1.8;
    }

    .section-card ul {
        margin: 0;
        padding-left: 20px;
    }

    .section-card li {
        margin-bottom: 8px;
        color: #d6e2ef;
    }

    .spotlight-card {
        background: linear-gradient(135deg, rgba(12, 31, 54, 0.88), rgba(20, 44, 69, 0.92));
        border: 1px solid rgba(34,211,238,0.25);
        border-radius: 22px;
        padding: 22px;
        margin-bottom: 16px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.18);
    }

    .spotlight-title {
        color: #8be9f7;
        font-size: 13px;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 700;
        margin-bottom: 8px;
    }

    .spotlight-text {
        color: #ffffff;
        font-size: 18px;
        line-height: 1.55;
        font-weight: 600;
    }

    .issue-card {
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 18px;
        padding: 18px;
        margin-bottom: 14px;
    }

    .issue-head {
        display: flex;
        justify-content: space-between;
        align-items: center;
        margin-bottom: 12px;
    }

    .issue-name {
        color: #ffffff;
        font-size: 18px;
        font-weight: 800;
    }

    .impact-badge {
        padding: 4px 10px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        border: 1px solid transparent;
    }

    .impact-high {
        color: #ffb4b4;
        background: rgba(255, 82, 82, 0.15);
        border-color: rgba(255, 82, 82, 0.35);
    }

    .impact-medium {
        color: #ffd8a8;
        background: rgba(255, 166, 77, 0.15);
        border-color: rgba(255, 166, 77, 0.35);
    }

    .impact-low {
        color: #b6f7d2;
        background: rgba(67, 207, 124, 0.15);
        border-color: rgba(67, 207, 124, 0.35);
    }

    .issue-block {
        color: #d6e2ef;
        line-height: 1.7;
        margin-bottom: 8px;
    }

    .premium-lock-shell {
        position: relative;
        border: 1px solid rgba(255,255,255,0.10);
        border-radius: 22px;
        overflow: hidden;
        margin-bottom: 16px;
    }

    .premium-lock-blur {
        filter: blur(6px);
        opacity: 0.5;
        pointer-events: none;
        padding: 18px;
        background: rgba(255,255,255,0.03);
        min-height: 120px;
    }

    .premium-lock-overlay {
        position: absolute;
        inset: 0;
        display: flex;
        align-items: center;
        justify-content: center;
        text-align: center;
        background: linear-gradient(180deg, rgba(6,17,31,0.30), rgba(6,17,31,0.72));
        padding: 18px;
    }

    .premium-lock-title {
        font-size: 20px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 8px;
    }

    .premium-lock-sub {
        color: #c7d9ef;
        font-size: 14px;
        line-height: 1.6;
    }

    .teaser-premium-wrap {
        border: 1px solid rgba(123, 90, 255, 0.28);
        border-radius: 22px;
        padding: 18px;
        margin-top: 12px;
        background:
            radial-gradient(circle at 78% -10%, rgba(114, 74, 255, 0.22), transparent 36%),
            radial-gradient(circle at 8% 120%, rgba(34, 211, 238, 0.12), transparent 40%),
            linear-gradient(165deg, rgba(6, 17, 34, 0.96), rgba(8, 24, 44, 0.92));
        box-shadow: 0 22px 58px rgba(0, 0, 0, 0.32), 0 0 36px rgba(114, 74, 255, 0.16);
    }
    .teaser-head {
        display: flex;
        justify-content: space-between;
        gap: 16px;
        align-items: flex-start;
        margin-bottom: 12px;
    }
    .teaser-head h3 {
        margin: 0;
        color: #f5fbff;
        font-size: 30px;
        font-weight: 900;
        letter-spacing: -0.03em;
    }
    .teaser-head p {
        margin: 8px 0 0;
        color: #91a8c1;
        font-size: 13px;
    }
    .teaser-score-grid {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 8px;
        min-width: 420px;
    }
    .teaser-score-item {
        border: 1px solid rgba(79, 138, 225, 0.34);
        border-radius: 12px;
        padding: 10px 12px;
        background: linear-gradient(160deg, rgba(11, 28, 50, 0.9), rgba(10, 24, 46, 0.76));
    }
    .teaser-score-item span {
        display: block;
        color: #82a0bf;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 0.05em;
    }
    .teaser-score-item b {
        display: block;
        margin-top: 4px;
        color: #f4fbff;
        font-size: 30px;
        letter-spacing: -0.03em;
    }
    .teaser-score-main {
        border-color: rgba(245, 158, 11, 0.44);
        box-shadow: 0 0 20px rgba(245, 158, 11, 0.18);
    }
    .teaser-score-main b { color: #ffd27a; }

    .teaser-finding-box {
        border: 1px solid rgba(103, 196, 255, 0.24);
        border-radius: 14px;
        padding: 12px 14px;
        background: rgba(9, 24, 44, 0.72);
        margin-bottom: 14px;
    }
    .teaser-finding-title {
        color: #f0f7ff;
        font-size: 15px;
        font-weight: 850;
        margin-bottom: 8px;
    }
    .teaser-finding-box ul {
        margin: 0;
        padding-left: 18px;
        display: grid;
        gap: 6px;
    }
    .teaser-finding-box li {
        color: #d0def0;
        font-size: 13px;
        line-height: 1.55;
    }
    .teaser-warning {
        margin-top: 10px;
        padding: 8px 10px;
        border-radius: 10px;
        border: 1px solid rgba(245, 158, 11, 0.35);
        color: #f8d08a;
        font-size: 12px;
        background: rgba(245, 158, 11, 0.08);
    }

    .teaser-lock-zone {
        border: 1px solid rgba(124, 84, 255, 0.38);
        border-radius: 14px;
        padding: 14px;
        margin-bottom: 14px;
        background:
            radial-gradient(circle at 30% 0%, rgba(124, 84, 255, 0.18), transparent 45%),
            linear-gradient(170deg, rgba(9, 19, 40, 0.95), rgba(8, 24, 44, 0.88));
    }
    .teaser-lock-zone-title {
        color: #eef4ff;
        font-size: 26px;
        font-weight: 900;
        letter-spacing: -0.02em;
    }
    .teaser-lock-zone-sub {
        margin-top: 6px;
        color: #9db0ca;
        font-size: 13px;
    }
    .teaser-lock-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
        margin-top: 12px;
    }
    .teaser-lock-card {
        position: relative;
        border: 1px solid rgba(129, 110, 255, 0.34);
        border-radius: 12px;
        min-height: 118px;
        padding: 12px;
        background: linear-gradient(170deg, rgba(13, 28, 53, 0.92), rgba(11, 23, 43, 0.88));
        overflow: hidden;
    }
    .teaser-lock-mock {
        position: absolute;
        inset: 10px 10px auto 10px;
        height: 62px;
        border-radius: 8px;
        border: 1px solid rgba(147, 197, 253, 0.24);
        background: linear-gradient(160deg, rgba(25, 47, 85, 0.45), rgba(20, 36, 68, 0.35));
        filter: blur(1.5px);
        opacity: 0.72;
    }
    .teaser-lock-line {
        height: 6px;
        border-radius: 999px;
        margin: 8px 10px 0;
        background: linear-gradient(90deg, rgba(125, 211, 252, 0.45), rgba(99, 102, 241, 0.38));
    }
    .teaser-lock-line.w1 { width: 72%; }
    .teaser-lock-line.w2 { width: 58%; }
    .teaser-lock-line.w3 { width: 44%; }
    .teaser-lock-bars {
        display: flex;
        gap: 5px;
        margin: 7px 10px 0;
        align-items: flex-end;
        height: 16px;
    }
    .teaser-lock-bars span {
        width: 7px;
        border-radius: 4px 4px 2px 2px;
        background: rgba(167, 139, 250, 0.55);
    }
    .teaser-lock-bars span:nth-child(1) { height: 7px; }
    .teaser-lock-bars span:nth-child(2) { height: 12px; }
    .teaser-lock-bars span:nth-child(3) { height: 9px; }
    .teaser-lock-bars span:nth-child(4) { height: 14px; }
    .teaser-lock-card::after {
        content: "";
        position: absolute;
        inset: 0;
        background: linear-gradient(180deg, rgba(5, 13, 26, 0.15), rgba(5, 13, 26, 0.60));
        backdrop-filter: blur(2.8px);
    }
    .teaser-lock-badge, .teaser-lock-title, .teaser-lock-sub { position: relative; z-index: 1; }
    .teaser-lock-badge {
        width: 28px;
        height: 28px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.10);
        border: 1px solid rgba(255, 255, 255, 0.28);
        margin-bottom: 8px;
    }
    .teaser-lock-title {
        color: #d7e3f3;
        font-size: 13px;
        line-height: 1.45;
        font-weight: 700;
        margin-top: 68px;
    }
    .teaser-lock-sub {
        margin-top: 8px;
        color: #b8a7ff;
        font-size: 12px;
        font-weight: 700;
    }
    .teaser-loss-row {
        margin-top: 12px;
        display: flex;
        justify-content: space-between;
        gap: 12px;
        color: #d9e6f5;
        font-size: 13px;
        padding: 10px;
        border-radius: 10px;
        border: 1px solid rgba(245, 158, 11, 0.22);
        background: rgba(245, 158, 11, 0.06);
    }
    .teaser-loss-row b { color: #ffd67f; }

    .teaser-bench-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
    }
    .teaser-bench-item {
        border: 1px solid rgba(94, 175, 255, 0.28);
        border-radius: 12px;
        padding: 12px;
        background: linear-gradient(165deg, rgba(12, 31, 56, 0.85), rgba(11, 25, 45, 0.78));
    }
    .teaser-bench-item span {
        color: #7ee7ff;
        font-size: 16px;
        font-weight: 900;
    }
    .teaser-bench-item b {
        display: block;
        color: #f0f8ff;
        font-size: 26px;
        line-height: 1.2;
        margin-top: 6px;
    }
    .teaser-bench-item small {
        display: block;
        color: #91a8c1;
        font-size: 12px;
    }

    .elite-wrap {
        border: 1px solid rgba(75, 136, 236, 0.28);
        border-radius: 18px;
        padding: 16px;
        margin-bottom: 18px;
        background:
            radial-gradient(circle at 82% 0%, rgba(45, 212, 191, 0.12), transparent 35%),
            linear-gradient(160deg, rgba(5, 14, 31, 0.95), rgba(7, 21, 42, 0.92));
        box-shadow: 0 20px 50px rgba(0, 0, 0, 0.34);
    }
    .elite-top {
        display: flex;
        justify-content: space-between;
        align-items: center;
        gap: 12px;
        margin-bottom: 12px;
    }
    .elite-welcome {
        color: #f3f8ff;
        font-size: 34px;
        font-weight: 900;
        letter-spacing: -0.03em;
    }
    .elite-sub { color: #9cb4ce; font-size: 14px; }
    .elite-date {
        padding: 8px 12px;
        border-radius: 10px;
        border: 1px solid rgba(107, 168, 255, 0.36);
        color: #d2e6fb;
        background: rgba(14, 31, 56, 0.7);
        font-size: 13px;
        font-weight: 700;
    }
    .elite-metrics {
        display: grid;
        grid-template-columns: repeat(4, minmax(0, 1fr));
        gap: 10px;
        margin-bottom: 12px;
    }
    .elite-card {
        border: 1px solid rgba(85, 148, 235, 0.3);
        border-radius: 12px;
        padding: 12px;
        background: linear-gradient(160deg, rgba(10, 27, 52, 0.92), rgba(10, 23, 45, 0.76));
    }
    .elite-card span { display:block; color:#8fa9c8; font-size:12px; font-weight:700; }
    .elite-card b { color:#f1f8ff; font-size:40px; line-height:1.05; letter-spacing:-0.03em; }
    .elite-card small { color:#8fa9c8; font-size:12px; }
    .elite-main-grid {
        display: grid;
        grid-template-columns: 1.55fr 1fr;
        gap: 10px;
        margin-bottom: 10px;
    }
    .elite-hero-card {
        border: 1px solid rgba(85, 148, 235, 0.28);
        border-radius: 14px;
        padding: 16px;
        background:
            radial-gradient(circle at 78% 26%, rgba(37, 99, 235, 0.2), transparent 32%),
            linear-gradient(165deg, rgba(8, 20, 39, 0.95), rgba(10, 31, 56, 0.85));
    }
    .elite-pill {
        display:inline-flex; padding:6px 10px; border-radius:999px;
        border:1px solid rgba(45,212,191,0.4); color:#7df0d6; font-size:12px; font-weight:800;
        background: rgba(45,212,191,0.08);
    }
    .elite-hero-card h2 { margin:10px 0 8px; color:#f3f9ff; font-size:46px; line-height:1.05; letter-spacing:-0.03em; }
    .elite-hero-card p { margin:0 0 12px; color:#9bb1c9; font-size:14px; }
    .elite-hero-cta {
        display:inline-flex; padding:10px 14px; border-radius:12px; font-weight:800;
        color:#e8f6ff; border:1px solid rgba(120,197,255,0.46);
        background: linear-gradient(135deg, #1d4ed8, #4f46e5);
        box-shadow:0 0 24px rgba(79,70,229,0.34);
    }
    .elite-issues {
        border: 1px solid rgba(85, 148, 235, 0.28);
        border-radius: 14px;
        padding: 12px;
        background: linear-gradient(165deg, rgba(8, 20, 39, 0.95), rgba(10, 31, 56, 0.85));
    }
    .elite-issues-head { color:#f3f9ff; font-size:16px; font-weight:850; margin-bottom:8px; }
    .elite-issue-item {
        display:flex; justify-content:space-between; gap:8px; align-items:center;
        border:1px solid rgba(250,204,21,0.22); border-radius:10px; padding:8px 10px; margin-bottom:7px;
        color:#dbe7f5; background: rgba(250,204,21,0.04); font-size:13px;
    }
    .elite-issue-item b { color:#fbbf24; font-size:12px; }
    .elite-bottom-grid {
        display:grid; grid-template-columns: repeat(3, minmax(0,1fr)); gap:10px;
    }
    .elite-mini-card {
        border: 1px solid rgba(85, 148, 235, 0.28);
        border-radius: 12px;
        padding: 12px;
        background: linear-gradient(160deg, rgba(10, 27, 52, 0.92), rgba(10, 23, 45, 0.76));
    }
    .elite-mini-title { color:#f3f9ff; font-size:15px; font-weight:800; margin-bottom:8px; }
    .elite-funnel-row { display:flex; justify-content:space-between; color:#c7d7ea; font-size:13px; margin-bottom:6px; }
    .elite-funnel-row b { color:#8bc3ff; }
    .elite-trend-mock {
        height: 110px; border-radius: 10px; border:1px solid rgba(99,102,241,0.24);
        background: linear-gradient(160deg, rgba(59,130,246,0.1), rgba(139,92,246,0.08));
        position: relative;
    }
    .elite-trend-mock::after {
        content:""; position:absolute; left:8%; right:8%; top:56%;
        height:3px; border-radius:99px; background:linear-gradient(90deg,#34d399,#22d3ee,#818cf8);
        transform: skewY(-12deg); box-shadow:0 0 14px rgba(34,211,238,0.4);
    }
    .elite-reco-item {
        color:#c9d9ec; font-size:13px; line-height:1.5; margin-bottom:6px;
    }

    .cp-shell {
        display: grid;
        grid-template-columns: 270px 1fr;
        gap: 14px;
        margin-bottom: 16px;
    }
    .cp-side {
        border: 1px solid rgba(83, 145, 236, 0.24);
        border-radius: 16px;
        padding: 16px;
        background: linear-gradient(170deg, rgba(7, 20, 40, 0.96), rgba(6, 16, 32, 0.9));
    }
    .cp-brand { color:#f3f8ff; font-size:36px; font-weight:900; letter-spacing:-0.03em; }
    .cp-brand span { color:#22d3ee; }
    .cp-brand em {
        font-style: normal; font-size: 12px; margin-left: 6px; padding: 2px 6px;
        border-radius: 8px; color:#7ee7ff; border:1px solid rgba(126,231,255,0.42);
    }
    .cp-nav { margin-top: 14px; display: grid; gap: 6px; }
    .cp-nav a {
        display: block; padding: 10px 12px; border-radius: 10px;
        color:#a9bfd8; text-decoration:none; font-size:14px; font-weight:700;
    }
    .cp-nav a.active, .cp-nav a:hover {
        color:#e9f7ff; background: rgba(24, 84, 152, 0.52); border: 1px solid rgba(102, 177, 255, 0.36);
    }
    .cp-plan {
        margin-top: 16px; padding: 12px; border-radius: 12px;
        border: 1px solid rgba(83,145,236,0.26); background: rgba(13, 33, 59, 0.76);
        color:#d4e5f8;
    }
    .cp-plan b { display:block; font-size:14px; }
    .cp-plan small { color:#88a2c0; font-size:12px; }
    .cp-user { margin-top: 10px; color:#9db6d2; font-size:13px; }

    .cp-main {
        border: 1px solid rgba(83, 145, 236, 0.24);
        border-radius: 16px;
        padding: 16px;
        background:
            radial-gradient(circle at 85% 0%, rgba(45, 212, 191, 0.12), transparent 36%),
            linear-gradient(170deg, rgba(6, 16, 32, 0.95), rgba(7, 21, 41, 0.9));
    }
    .cp-head { display:flex; justify-content:space-between; align-items:center; gap:10px; margin-bottom:12px; }
    .cp-head h2 { margin:0; color:#f4f9ff; font-size:36px; font-weight:900; letter-spacing:-0.03em; }
    .cp-head p { margin:6px 0 0; color:#91aac7; font-size:13px; }
    .cp-date {
        padding: 8px 12px; border-radius: 10px;
        border: 1px solid rgba(104, 173, 255, 0.33);
        color:#d8e9fb; font-size:13px; font-weight:700;
        background: rgba(13, 33, 59, 0.75);
    }
    .cp-metrics { display:grid; grid-template-columns: repeat(5, minmax(0,1fr)); gap:10px; margin-bottom:10px; }
    .mcard {
        border: 1px solid rgba(93, 154, 238, 0.28);
        border-radius: 12px; padding: 12px;
        background: linear-gradient(160deg, rgba(10, 27, 52, 0.92), rgba(10, 23, 45, 0.76));
    }
    .mcard span { display:block; color:#8fa9c8; font-size:12px; font-weight:700; }
    .mcard b { color:#f0f8ff; font-size:44px; line-height:1.05; letter-spacing:-0.03em; }
    .mcard small { color:#8fa9c8; font-size:12px; }
    .mcard i { display:block; color:#22c55e; font-style:normal; font-size:12px; font-weight:700; margin-top:6px; }
    .mcard i.down { color:#ef4444; }

    .cp-grid-2 { display:grid; grid-template-columns: 1fr 1fr; gap:10px; margin-bottom:10px; }
    .cp-card {
        border: 1px solid rgba(93, 154, 238, 0.28);
        border-radius: 12px; padding: 12px;
        background: linear-gradient(160deg, rgba(10, 27, 52, 0.92), rgba(10, 23, 45, 0.76));
    }
    .cp-title { color:#f0f8ff; font-size:16px; font-weight:850; }
    .cp-sub { color:#84a0bf; font-size:12px; margin-top:4px; margin-bottom:8px; }
    .cp-list { list-style:none; padding:0; margin:0; display:grid; gap:8px; }
    .cp-list li {
        display:flex; justify-content:space-between; align-items:center; gap:10px;
        border:1px solid rgba(89,142,222,0.2); border-radius:10px; padding:8px 10px;
        color:#cddcef; font-size:13px; background: rgba(12, 30, 54, 0.55);
    }
    .cp-list li b { color:#8bd4ff; font-size:12px; }
    .cp-list.actions li b { color:#fbbf24; }
    .cp-trend {
        height: 165px;
        border-radius: 10px;
        border: 1px solid rgba(87, 109, 214, 0.24);
        background: linear-gradient(160deg, rgba(59,130,246,0.1), rgba(16,185,129,0.1));
        position: relative;
        overflow: hidden;
    }
    .cp-trend-grid {
        position: absolute;
        inset: 8px;
        background-image: linear-gradient(to right, rgba(148,163,184,.18) 1px, transparent 1px), linear-gradient(to top, rgba(148,163,184,.16) 1px, transparent 1px);
        background-size: 20% 100%, 100% 25%;
    }
    .cp-trend-line {
        position:absolute; left:7%; right:7%; top:58%;
        height:3px; border-radius:99px; background:linear-gradient(90deg,#22d3ee,#34d399,#60a5fa);
        transform: skewY(-12deg); box-shadow:0 0 14px rgba(52,211,153,0.4);
    }
    .cp-point {
        position: absolute;
        width: 9px;
        height: 9px;
        margin-left: -4px;
        border-radius: 99px;
        background: #67e8f9;
        box-shadow: 0 0 0 3px rgba(103,232,249,0.18), 0 0 12px rgba(103,232,249,0.4);
        z-index: 2;
    }
    .cp-trend-meta {
        margin-top: 8px;
        display: flex;
        gap: 12px;
        flex-wrap: wrap;
        color: #9bb2cc;
        font-size: 12px;
    }
    .cp-trend-meta b { color: #dff3ff; }
    .cp-trend-meta b.up { color: #22c55e; }
    .cp-trend-meta b.down { color: #ef4444; }
    .cp-trend-note {
        margin-top: 6px;
        color: #89a8c8;
        font-size: 12px;
    }
    .cp-table-head, .cp-row {
        display:grid; grid-template-columns: 1.15fr 1fr 1fr .7fr; gap:8px; align-items:center;
        color:#9bb2cc; font-size:12px;
    }
    .cp-table-head { margin:8px 0 6px; font-weight:800; }
    .cp-row {
        border:1px solid rgba(89,142,222,0.2); border-radius:10px; padding:8px 10px;
        background: rgba(12, 30, 54, 0.55); margin-bottom:6px; color:#d5e4f5;
    }
    .dot { display:inline-block; width:8px; height:8px; border-radius:99px; margin-left:6px; }
    .dot.green { background:#22c55e; }
    .dot.yellow { background:#f59e0b; }
    .dot.red { background:#ef4444; }
    .cp-empty {
        color:#9db6d2; font-size:13px; padding:10px;
        border:1px dashed rgba(89,142,222,0.35); border-radius:10px;
    }

    /* TEXT INPUT */
    div[data-testid="stTextInput"] {
        width: 100%;
    }

    div[data-testid="stTextInput"] > div {
        background: transparent !important;
    }

    div[data-testid="stTextInput"] input,
    div[data-testid="stTextInput"] input:hover,
    div[data-testid="stTextInput"] input:focus,
    div[data-testid="stTextInput"] input:active,
    div[data-testid="stTextInput"] input:focus-visible {
        height: 56px !important;
        border-radius: 16px !important;
        background: rgba(255,255,255,0.08) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: 1px solid rgba(34,211,238,0.30) !important;
        font-size: 16px !important;
        line-height: 1.25 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
        padding-left: 16px !important;
        padding-right: 16px !important;
        outline: none !important;
        box-shadow: none !important;
        opacity: 1 !important;
        caret-color: #8be9f7 !important;
        transition: background-color 0.15s ease, border-color 0.15s ease !important;
    }

    div[data-testid="stTextInput"] input::placeholder {
        color: #8ca0b5 !important;
        -webkit-text-fill-color: #8ca0b5 !important;
        opacity: 1 !important;
    }

    div[data-baseweb="input"] input,
    div[data-baseweb="base-input"] input,
    div[data-testid="stTextInputRootElement"] input,
    div[data-testid="stTextInputRootElement"] input:focus,
    div[data-testid="stTextInputRootElement"] input:hover {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        caret-color: #8be9f7 !important;
        background: rgba(255,255,255,0.08) !important;
        line-height: 1.25 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    div[data-baseweb="input"] {
        background: rgba(255,255,255,0.08) !important;
        align-items: center !important;
    }

    div[data-baseweb="base-input"] {
        background: rgba(255,255,255,0.08) !important;
        align-items: center !important;
    }

    div[data-testid="stTextInput"] input:-webkit-autofill,
    div[data-testid="stTextInput"] input:-webkit-autofill:hover,
    div[data-testid="stTextInput"] input:-webkit-autofill:focus,
    div[data-testid="stTextInput"] input:-webkit-autofill:active {
        -webkit-text-fill-color: #ffffff !important;
        box-shadow: 0 0 0 1000px rgba(255,255,255,0.08) inset !important;
        -webkit-box-shadow: 0 0 0 1000px rgba(255,255,255,0.08) inset !important;
        caret-color: #8be9f7 !important;
        border: 1px solid rgba(34,211,238,0.30) !important;
    }

    div[data-testid="stTextInput"] label p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* SELECTBOX */
    div[data-testid="stSelectbox"] label p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] > div {
        min-height: 52px !important;
        border-radius: 14px !important;
        border: 1px solid rgba(34, 211, 238, 0.32) !important;
        background: rgba(255,255,255,0.08) !important;
        color: #eaf6ff !important;
        -webkit-text-fill-color: #eaf6ff !important;
        box-shadow: none !important;
    }

    div[data-testid="stSelectbox"] div[data-baseweb="select"] span,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] div,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] p,
    div[data-testid="stSelectbox"] div[data-baseweb="select"] input {
        color: #eaf6ff !important;
        -webkit-text-fill-color: #eaf6ff !important;
    }

    div[data-testid="stSelectbox"] svg {
        fill: #d7ecff !important;
        color: #d7ecff !important;
    }

    [role="listbox"] {
        background: linear-gradient(160deg, rgba(8, 27, 47, 0.98), rgba(10, 36, 62, 0.96)) !important;
        border: 1px solid rgba(104, 219, 202, 0.36) !important;
        border-radius: 12px !important;
        box-shadow: 0 18px 42px rgba(0,0,0,0.34) !important;
    }

    [data-baseweb="popover"] [role="listbox"] {
        background: linear-gradient(160deg, rgba(8, 27, 47, 0.98), rgba(10, 36, 62, 0.96)) !important;
        border: 1px solid rgba(104, 219, 202, 0.36) !important;
    }

    [role="option"] {
        background: transparent !important;
        color: #eaf6ff !important;
        -webkit-text-fill-color: #eaf6ff !important;
    }

    [role="option"] * {
        color: #eaf6ff !important;
        -webkit-text-fill-color: #eaf6ff !important;
        opacity: 1 !important;
    }

    [role="option"]:hover {
        background: rgba(98, 208, 255, 0.18) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
    }

    [role="option"]:hover * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        opacity: 1 !important;
    }

    [role="option"][aria-selected="true"] {
        background: rgba(98, 208, 255, 0.26) !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 700 !important;
    }

    [role="option"][aria-selected="true"] * {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        opacity: 1 !important;
        font-weight: 700 !important;
    }

    /* MAIN BUTTONS */
    div.stButton > button {
        height: 56px;
        border-radius: 16px;
        border: 1px solid rgba(79, 228, 193, 0.34);
        background: linear-gradient(135deg, #0f2743 0%, #144062 100%);
        color: #ffffff;
        font-size: 16px;
        font-weight: 800;
        letter-spacing: 0.01em;
        box-shadow: 0 14px 30px rgba(0,0,0,0.24);
    }

    div.stButton > button:hover,
    div.stButton > button:focus,
    div.stButton > button:active {
        color: #ffffff;
        border: 1px solid rgba(79, 228, 193, 0.52);
        background: linear-gradient(135deg, #163357 0%, #1c4f78 100%);
        box-shadow: 0 14px 30px rgba(0,0,0,0.24);
    }

    /* FILE UPLOADER */
    div[data-testid="stFileUploader"] section,
    div[data-testid="stFileUploaderDropzone"] {
        border-radius: 18px !important;
        background: rgba(255,255,255,0.04) !important;
        border: 1px dashed rgba(255,255,255,0.18) !important;
    }

    div[data-testid="stFileUploader"] small,
    div[data-testid="stFileUploader"] span,
    div[data-testid="stFileUploader"] p,
    div[data-testid="stFileUploader"] label,
    div[data-testid="stFileUploader"] div {
        color: #d6e2ef !important;
        -webkit-text-fill-color: #d6e2ef !important;
    }

    div[data-testid="stFileUploader"] [data-testid="stFileUploaderDropzone"] small {
        color: #8ca0b5 !important;
        -webkit-text-fill-color: #8ca0b5 !important;
    }

    div[data-testid="stFileUploader"] [data-testid="stFileUploaderFileName"] {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        font-weight: 500 !important;
    }

    div[data-testid="stFileUploader"] svg {
        fill: #9fb3c8 !important;
    }

    div[data-testid="stFileUploader"] button,
    div[data-testid="stFileUploader"] button:hover,
    div[data-testid="stFileUploader"] button:focus,
    div[data-testid="stFileUploader"] button:active {
        background: #183153 !important;
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        border: 1px solid rgba(255,255,255,0.16) !important;
        border-radius: 12px !important;
        box-shadow: none !important;
    }

    /* CAPTION / ALERT */
    div[data-testid="stCaptionContainer"],
    .stCaption {
        color: #c5dbf0 !important;
    }

    div[data-testid="stCaptionContainer"] a,
    .stCaption a {
        color: #7fd2ff !important;
        text-decoration: underline !important;
    }

    div[data-testid="stAlert"] {
        border-radius: 18px;
        border: 1px solid rgba(255,255,255,0.08);
    }

    /* AUTH DIALOG */
    div[data-testid="stDialog"] [role="dialog"] {
        background: linear-gradient(180deg, #08192e 0%, #0b2745 100%) !important;
        border: 1px solid rgba(96, 214, 188, 0.38) !important;
        border-radius: 16px !important;
        box-shadow: 0 30px 80px rgba(0,0,0,0.5) !important;
        max-width: 520px !important;
    }

    div[data-testid="stDialog"] [data-testid="stDialogContent"] {
        background: transparent !important;
    }

    div[data-testid="stDialog"] h1,
    div[data-testid="stDialog"] h2,
    div[data-testid="stDialog"] h3,
    div[data-testid="stDialog"] label,
    div[data-testid="stDialog"] p,
    div[data-testid="stDialog"] span {
        color: #e7f4ff !important;
        -webkit-text-fill-color: #e7f4ff !important;
    }

    div[data-testid="stDialog"] div[data-baseweb="input"],
    div[data-testid="stDialog"] div[data-baseweb="base-input"] {
        background: rgba(255,255,255,0.08) !important;
        border: 1px solid rgba(109, 226, 198, 0.24) !important;
        border-radius: 12px !important;
    }

    div[data-testid="stDialog"] input,
    div[data-testid="stDialog"] input:focus,
    div[data-testid="stDialog"] input:hover {
        color: #ffffff !important;
        -webkit-text-fill-color: #ffffff !important;
        background: transparent !important;
        caret-color: #69f1c8 !important;
        line-height: 1.25 !important;
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }

    div[data-testid="stDialog"] input::placeholder {
        color: #9ebddb !important;
        -webkit-text-fill-color: #9ebddb !important;
    }

    div[data-testid="stDialog"] input:-webkit-autofill,
    div[data-testid="stDialog"] input:-webkit-autofill:hover,
    div[data-testid="stDialog"] input:-webkit-autofill:focus,
    div[data-testid="stDialog"] input:-webkit-autofill:active {
        -webkit-text-fill-color: #ffffff !important;
        box-shadow: 0 0 0 1000px rgba(255,255,255,0.08) inset !important;
        -webkit-box-shadow: 0 0 0 1000px rgba(255,255,255,0.08) inset !important;
        caret-color: #69f1c8 !important;
    }

    div[data-baseweb="popover"] [role="dialog"] {
        background: linear-gradient(160deg, rgba(7, 25, 44, 0.98), rgba(8, 34, 58, 0.96)) !important;
        border: 1px solid rgba(104, 219, 202, 0.38) !important;
        border-radius: 18px !important;
        box-shadow: 0 28px 70px rgba(0,0,0,0.46), 0 0 22px rgba(58, 195, 226, 0.22) !important;
        backdrop-filter: blur(8px) !important;
    }

    div[data-baseweb="popover"] p,
    div[data-baseweb="popover"] span,
    div[data-baseweb="popover"] label,
    div[data-baseweb="popover"] li,
    div[data-baseweb="popover"] div {
        color: #d9eaff !important;
        -webkit-text-fill-color: #d9eaff !important;
    }

    div[data-testid="stDialog"] .stTabs [role="tab"] {
        color: #b8d3ea !important;
    }

    div[data-testid="stDialog"] .stTabs [aria-selected="true"] {
        color: #ffffff !important;
    }

    div[data-testid="stDialog"] .stButton > button {
        min-height: 46px !important;
    }

    /* V1 Premium Website Theme Overrides */
    .stApp {
        background:
            radial-gradient(950px 520px at 82% 12%, rgba(90, 194, 255, 0.16), transparent 64%),
            radial-gradient(760px 420px at 22% 86%, rgba(56, 124, 255, 0.10), transparent 68%),
            linear-gradient(180deg, #040a16 0%, #071327 44%, #091c35 100%) !important;
    }

    .dash-side-shell {
        background: linear-gradient(165deg, rgba(10, 20, 38, 0.96), rgba(8, 26, 48, 0.94)) !important;
        border: 1px solid rgba(98, 162, 255, 0.26) !important;
        border-radius: 20px !important;
        box-shadow: 0 24px 56px rgba(1, 8, 20, 0.62), 0 0 26px rgba(86, 174, 255, 0.18) !important;
    }

    .dash-brand {
        color: #f3f8ff !important;
        font-size: 36px !important;
        font-weight: 900 !important;
        letter-spacing: -0.028em !important;
    }

    .dash-menu-title {
        color: #88a9c7 !important;
        font-size: 11px !important;
        letter-spacing: 0.14em !important;
    }

    .dash-main-title {
        color: #f8fbff !important;
        font-size: 64px !important;
        line-height: 1.0 !important;
        letter-spacing: -0.042em !important;
        text-shadow: 0 10px 30px rgba(0, 0, 0, 0.38) !important;
    }

    .dash-hero-card {
        background: linear-gradient(155deg, rgba(8, 21, 40, 0.97), rgba(12, 33, 58, 0.94)) !important;
        border: 1px solid rgba(92, 162, 255, 0.34) !important;
        border-radius: 24px !important;
        box-shadow: inset 0 1px 0 rgba(190, 222, 255, 0.06), 0 24px 52px rgba(1, 10, 24, 0.56), 0 0 34px rgba(84, 171, 255, 0.18) !important;
    }

    .dash-hero-badge {
        background: linear-gradient(135deg, rgba(32, 96, 173, 0.30), rgba(20, 64, 116, 0.32)) !important;
        border: 1px solid rgba(124, 189, 255, 0.42) !important;
        color: #d6ebff !important;
        font-weight: 800 !important;
        letter-spacing: 0.02em !important;
    }

    .dash-hero-title {
        background: linear-gradient(92deg, #ffffff 0%, #deedff 54%, #9fd2ff 100%) !important;
        -webkit-background-clip: text !important;
        -webkit-text-fill-color: transparent !important;
        font-size: 62px !important;
        letter-spacing: -0.035em !important;
        text-shadow: none !important;
    }

    .dash-hero-sub {
        color: #c9d9ea !important;
        font-size: 20px !important;
        line-height: 1.68 !important;
    }

    .right-plan-pill {
        border: 1px solid rgba(117, 189, 255, 0.42) !important;
        background: linear-gradient(135deg, rgba(12, 31, 54, 0.96), rgba(15, 44, 75, 0.94)) !important;
        color: #eaf4ff !important;
        box-shadow: 0 12px 26px rgba(4, 14, 30, 0.34), 0 0 18px rgba(90, 172, 255, 0.14) !important;
        border-radius: 12px !important;
    }

    div[data-testid="stSidebar"] .stButton > button,
    .stButton > button[kind="secondary"],
    .stButton > button {
        border-radius: 14px !important;
        border: 1px solid rgba(106, 176, 248, 0.34) !important;
        background: linear-gradient(145deg, rgba(16, 45, 76, 0.96), rgba(13, 34, 60, 0.96)) !important;
        color: #e7f2ff !important;
        font-weight: 700 !important;
        box-shadow: 0 14px 28px rgba(3, 11, 25, 0.34) !important;
        transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease !important;
    }

    .stButton > button:hover {
        transform: translateY(-1px) !important;
        border-color: rgba(136, 201, 255, 0.52) !important;
        box-shadow: 0 18px 34px rgba(3, 11, 25, 0.42), 0 0 22px rgba(92, 178, 255, 0.2) !important;
    }

    .metric-card,
    .section-card,
    .history-row-card {
        background: linear-gradient(160deg, rgba(10, 25, 45, 0.92), rgba(11, 32, 56, 0.90)) !important;
        border: 1px solid rgba(105, 173, 246, 0.23) !important;
        box-shadow: 0 14px 30px rgba(2, 10, 23, 0.36), inset 0 1px 0 rgba(255,255,255,0.04) !important;
        border-radius: 18px !important;
    }

    .section-title {
        color: #f7fbff !important;
        letter-spacing: -0.026em !important;
        font-weight: 900 !important;
    }

    .metric-title { color: #92b1cc !important; }
    .metric-value { color: #f2f8ff !important; }
    .metric-sub { color: #9db8d1 !important; }
    .section-card-title { color: #f0f7ff !important; }
    .section-card-text { color: #bfd2e6 !important; }

    .pro-hero-wrap {
        margin-top: 10px;
        display: grid;
        grid-template-columns: 1.1fr 1fr;
        gap: 14px;
        border: 1px solid rgba(114, 178, 255, 0.32);
        border-radius: 22px;
        background: linear-gradient(160deg, rgba(7, 22, 43, 0.97), rgba(10, 31, 56, 0.94));
        box-shadow: 0 20px 46px rgba(0, 8, 20, 0.46), 0 0 28px rgba(67, 150, 255, 0.17);
        padding: 20px;
    }
    .pro-eyebrow {
        display: inline-block;
        border: 1px solid rgba(122, 194, 255, 0.42);
        border-radius: 999px;
        padding: 6px 12px;
        color: #d8ecff;
        font-size: 12px;
        font-weight: 700;
        margin-bottom: 10px;
    }
    .pro-title {
        color: #f7fbff;
        font-size: 56px;
        font-weight: 900;
        letter-spacing: -0.04em;
        line-height: 1.02;
        margin-bottom: 8px;
    }
    .pro-sub {
        color: #c3d8ed;
        font-size: 18px;
        line-height: 1.65;
    }
    .pro-hero-right {
        border: 1px solid rgba(114, 178, 255, 0.25);
        border-radius: 16px;
        padding: 16px;
        background: linear-gradient(160deg, rgba(8, 24, 44, 0.92), rgba(10, 33, 58, 0.90));
    }
    .pro-right-top {
        display: flex;
        align-items: end;
        justify-content: space-between;
        margin-bottom: 8px;
    }
    .pro-score-label {
        color: #cfe4f9;
        font-size: 14px;
        font-weight: 700;
    }
    .pro-score-value {
        color: #ffffff;
        font-size: 52px;
        font-weight: 900;
        line-height: 1;
    }
    .pro-score-value span {
        color: #a5c6e5;
        font-size: 24px;
        font-weight: 700;
        margin-left: 2px;
    }
    .pro-row {
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: #c5dcf3;
        font-size: 15px;
        margin-top: 8px;
    }
    .pro-row strong {
        color: #f3f8ff;
        font-weight: 800;
    }
    .pro-progress {
        margin-top: 10px;
        height: 8px;
        border-radius: 999px;
        background: rgba(138, 169, 196, 0.27);
        overflow: hidden;
    }
    .pro-progress-fill {
        width: 47%;
        height: 100%;
        border-radius: 999px;
        background: linear-gradient(90deg, #4e9dff 0%, #7d61ff 100%);
        box-shadow: 0 0 14px rgba(93, 142, 255, 0.45);
    }
    .pro-alert {
        margin-top: 12px;
        border: 1px solid rgba(255, 199, 86, 0.34);
        border-radius: 12px;
        padding: 10px 12px;
        background: rgba(255, 180, 74, 0.10);
        color: #ffd88b;
        font-size: 14px;
        font-weight: 700;
    }

    .premium-hero-visual {
        display: grid;
        grid-template-columns: 0.95fr 1.35fr;
        gap: 14px;
        padding: 14px;
        border: 1px solid rgba(101, 176, 255, 0.28);
        border-radius: 20px;
        background: linear-gradient(160deg, rgba(7, 20, 39, 0.96), rgba(10, 29, 52, 0.94));
        box-shadow: 0 18px 42px rgba(2, 10, 24, 0.48), 0 0 24px rgba(71, 153, 255, 0.17);
    }

    .hero-score-ring-shell {
        border: 1px solid rgba(110, 180, 255, 0.3);
        border-radius: 16px;
        padding: 14px 14px 12px;
        background: radial-gradient(circle at 50% 30%, rgba(44, 126, 255, 0.20), rgba(255, 182, 56, 0.08) 60%, rgba(12, 24, 42, 0.4) 100%);
    }
    .hero-ring-title { color: #d4e7ff; font-size: 14px; font-weight: 700; margin-bottom: 14px; }
    .hero-ring-value { color: #ffffff; font-size: 56px; font-weight: 900; line-height: 1; letter-spacing: -0.03em; }
    .hero-ring-value span { color: #aac6e6; font-size: 28px; margin-left: 2px; font-weight: 700; }
    .hero-ring-pill {
        margin-top: 10px;
        display: inline-block;
        padding: 6px 12px;
        border-radius: 999px;
        border: 1px solid rgba(255, 190, 72, 0.45);
        color: #ffd889;
        font-size: 13px;
        font-weight: 700;
    }

    .hero-score-unit { color: #a8c6e8; font-size: 18px; font-weight: 700; margin-left: 4px; }

    .premium-feature-strip {
        grid-template-columns: repeat(4, minmax(0, 1fr)) !important;
        gap: 12px !important;
    }
    .premium-feature-strip .feature-item {
        border: 1px solid rgba(109, 181, 255, 0.26);
        border-radius: 14px;
        background: linear-gradient(155deg, rgba(8, 24, 45, 0.92), rgba(11, 32, 58, 0.88));
        box-shadow: 0 10px 28px rgba(3, 10, 22, 0.34);
    }

    .landing-bottom-grid {
        margin-top: 12px;
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 12px;
    }
    .landing-bottom-card {
        border: 1px solid rgba(109, 181, 255, 0.28);
        border-radius: 16px;
        background: linear-gradient(160deg, rgba(8, 23, 44, 0.94), rgba(11, 34, 61, 0.90));
        box-shadow: 0 12px 30px rgba(2, 10, 23, 0.4), 0 0 18px rgba(67, 149, 255, 0.14);
        padding: 16px;
    }
    .landing-bottom-title { color: #dbeeff; font-size: 22px; font-weight: 800; margin-bottom: 10px; }
    .landing-bottom-main { color: #f5fbff; font-size: 32px; line-height: 1.15; font-weight: 800; margin-bottom: 10px; letter-spacing: -0.02em; }
    .landing-bottom-sub { color: #b8cfe6; font-size: 16px; }
    .landing-bottom-sub strong { color: #74ffcc; font-weight: 800; }
    .landing-trend-line {
        margin: 8px 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 24px;
        color: #bcd8ff;
        font-weight: 700;
    }
    .landing-trend-line .trend-up { color: #7dffcf; font-size: 30px; font-weight: 900; }

    @media (max-width: 900px) {
        .landing-title {
            font-size: 42px;
        }
        .pitch-grid {
            grid-template-columns: 1fr;
        }
        .feature-strip {
            grid-template-columns: 1fr;
        }
        .trust-row {
            grid-template-columns: repeat(2, minmax(0, 1fr));
        }
        .logo-strip {
            flex-wrap: wrap;
            gap: 10px;
        }
        .menu-row {
            gap: 14px;
            font-size: 13px;
            flex-wrap: wrap;
        }
        .menu-dropdown {
            position: static;
            opacity: 1;
            transform: none;
            pointer-events: auto;
            min-width: 100%;
            margin-top: 8px;
        }
        .landing-steps-grid,
        .landing-feature-grid,
        .pricing-card-grid {
            grid-template-columns: 1fr;
        }
        .top-nav {
            gap: 14px;
            flex-direction: column;
            align-items: flex-start;
        }
        .brand-line {
            font-size: 26px;
        }
        .dash-main-title {
            font-size: 42px;
        }
        .dash-hero-title {
            font-size: 46px;
        }
        .premium-hero-visual {
            grid-template-columns: 1fr;
        }
        .pro-hero-wrap {
            grid-template-columns: 1fr;
        }
        .pro-title {
            font-size: 40px;
        }
        .premium-feature-strip {
            grid-template-columns: 1fr !important;
        }
        .landing-bottom-grid {
            grid-template-columns: 1fr;
        }
        .landing-bottom-main {
            font-size: 26px;
        }
    }
    

    /* ==============================
       ConvAudit AI Premium Production UI
       Added by ChatGPT
    ============================== */
    :root {
        --ca-bg: #020711;
        --ca-panel: rgba(8, 19, 35, 0.82);
        --ca-panel-2: rgba(11, 28, 50, 0.74);
        --ca-cyan: #22d3ee;
        --ca-blue: #2563eb;
        --ca-purple: #8b5cf6;
        --ca-warm: #fbbf24;
        --ca-text: #f8fbff;
        --ca-muted: #a9bad0;
        --ca-border: rgba(125, 220, 255, .18);
    }

    .stApp {
        background:
            radial-gradient(circle at 72% 18%, rgba(34, 211, 238, .18), transparent 30%),
            radial-gradient(circle at 88% 68%, rgba(99, 102, 241, .16), transparent 26%),
            radial-gradient(circle at 24% 38%, rgba(37, 99, 235, .12), transparent 32%),
            linear-gradient(180deg, #020711 0%, #071426 48%, #081a2f 100%) !important;
        color: var(--ca-text) !important;
        font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    }

    .stApp::before {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background-image:
            linear-gradient(rgba(255,255,255,.025) 1px, transparent 1px),
            linear-gradient(90deg, rgba(255,255,255,.025) 1px, transparent 1px);
        background-size: 36px 36px;
        mask-image: linear-gradient(to bottom, rgba(0,0,0,.8), rgba(0,0,0,.15));
        z-index: 0;
    }

    .stApp::after {
        content: "";
        position: fixed;
        inset: 0;
        pointer-events: none;
        background: radial-gradient(ellipse at center, transparent 35%, rgba(0,0,0,.42) 100%);
        z-index: 0;
    }

    .block-container {
        position: relative;
        z-index: 1;
        max-width: 1400px !important;
        padding-top: 1.65rem !important;
    }

    .ca-landing-shell {
        position: relative;
        z-index: 4;
    }

    .ca-nav {
        min-height: 78px;
        border: 1px solid rgba(116, 214, 255, .18);
        background: linear-gradient(180deg, rgba(5, 13, 27, .84), rgba(5, 15, 30, .58));
        box-shadow: 0 18px 60px rgba(0,0,0,.28), inset 0 1px 0 rgba(255,255,255,.06);
        backdrop-filter: blur(18px);
        border-radius: 24px;
        padding: 18px 22px;
        display: grid;
        grid-template-columns: auto 1fr auto;
        align-items: center;
        column-gap: 28px;
        margin-bottom: 40px;
    }

    .ca-brand-wrap {display:flex; align-items:center; gap:14px;}
    .ca-logo-mark {
        width: 44px; height: 44px; border-radius: 15px;
        display:flex; align-items:center; justify-content:center;
        font-weight: 950; font-size: 25px; color: #00111e;
        background: linear-gradient(135deg, #38bdf8, #22d3ee 45%, #2563eb);
        box-shadow: 0 0 26px rgba(34,211,238,.38), inset 0 1px 0 rgba(255,255,255,.5);
    }
    .ca-brand-text {font-size: 30px; font-weight: 900; letter-spacing: -.045em; color:#fff;}
    .ca-brand-text span {color: var(--ca-cyan); text-shadow: 0 0 24px rgba(34,211,238,.38);}
    .ca-nav-links {display:flex; align-items:center; justify-content:center; gap:34px;}
    .ca-nav-item {position: relative; display: inline-flex; align-items: center;}
    .ca-nav-links a {color:#c7d6e8; text-decoration:none; font-weight:700; font-size:15px; transition:.2s;}
    .ca-nav-links a:hover {color:#fff; text-shadow:0 0 18px rgba(34,211,238,.45);}
    .ca-nav-popover {
        position: absolute;
        left: 50%;
        top: calc(100% + 12px);
        transform: translateX(-50%) translateY(6px);
        min-width: 260px;
        max-width: 320px;
        padding: 11px 12px;
        border-radius: 12px;
        border: 1px solid rgba(123, 211, 255, .34);
        background: linear-gradient(160deg, rgba(8, 20, 38, .95), rgba(12, 31, 56, .93));
        color: #d4e5f7;
        font-size: 12px;
        line-height: 1.45;
        box-shadow: 0 12px 34px rgba(0, 0, 0, .34), 0 0 22px rgba(34, 211, 238, .14);
        opacity: 0;
        pointer-events: none;
        transition: opacity .16s ease, transform .16s ease;
        z-index: 120;
    }
    .ca-nav-popover h4 {
        margin: 0 0 8px 0;
        font-size: 12px;
        font-weight: 900;
        letter-spacing: .03em;
        text-transform: uppercase;
        color: #9fe8ff;
    }
    .ca-nav-popover ul {
        margin: 0;
        padding-left: 16px;
        display: grid;
        gap: 6px;
    }
    .ca-nav-popover li {
        margin: 0;
        color: #d4e5f7;
        font-size: 12px;
        line-height: 1.45;
    }
    .ca-nav-item:hover .ca-nav-popover {
        opacity: 1;
        transform: translateX(-50%) translateY(0);
    }
    .ca-nav-actions {
        display: flex;
        align-items: center;
        justify-content: flex-end;
        gap: 12px;
        flex-shrink: 0;
    }
    .ca-nav-btn {
        min-width: 120px;
        height: 52px;
        padding: 0 20px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        border-radius: 14px;
        text-decoration: none;
        font-size: 16px;
        font-weight: 850;
        line-height: 1;
        transition: transform .18s ease, box-shadow .18s ease, filter .18s ease;
        white-space: nowrap;
    }
    .ca-nav-btn:hover {transform: translateY(-1px); filter: brightness(1.04);}
    .ca-nav-btn-ghost {
        color: #dbe9f8;
        border: 1px solid rgba(141, 201, 255, .38);
        background: linear-gradient(165deg, rgba(17, 39, 69, .78), rgba(11, 28, 52, .72));
        box-shadow: inset 0 1px 0 rgba(255,255,255,.08);
    }
    .ca-nav-btn-solid {
        color: #ffffff;
        border: 1px solid rgba(124, 226, 255, .58);
        background: linear-gradient(135deg, #0f4ea8 0%, #0ea5e9 55%, #22d3ee 100%);
        box-shadow: 0 0 26px rgba(14, 165, 233, .34), inset 0 1px 0 rgba(255,255,255,.22);
        text-shadow: 0 1px 2px rgba(0, 19, 38, .55);
    }
    .ca-anchor-section {
        margin-top: 18px;
        border: 1px solid rgba(92, 162, 255, 0.24);
        border-radius: 18px;
        background: linear-gradient(155deg, rgba(7, 21, 40, 0.92), rgba(10, 30, 54, 0.88));
        padding: 16px;
    }
    .ca-anchor-title {
        color: #f2f8ff;
        font-size: 24px;
        font-weight: 900;
        letter-spacing: -0.02em;
        margin-bottom: 12px;
    }
    .ca-anchor-grid {
        display: grid;
        grid-template-columns: repeat(3, minmax(0, 1fr));
        gap: 10px;
    }
    .ca-anchor-card {
        border: 1px solid rgba(109, 181, 255, 0.26);
        border-radius: 12px;
        background: linear-gradient(145deg, rgba(11, 28, 50, 0.9), rgba(13, 36, 62, 0.86));
        color: #cbe0f4;
        font-size: 14px;
        line-height: 1.6;
        padding: 12px 13px;
    }
    .ca-anchor-card strong {
        color: #ffffff;
    }

    .ca-hero-copy {padding: 8px 0 0 4px;}
    .ca-eyebrow {
        display:inline-flex; align-items:center; gap:8px;
        padding: 8px 13px; border:1px solid rgba(34,211,238,.24);
        background: rgba(34,211,238,.075); color:#9cf2ff;
        border-radius: 999px; font-size:13px; font-weight:850;
        margin-bottom: 20px; letter-spacing:.01em;
    }
    .ca-hero-copy h1 {
        margin:0 0 24px 0; font-size: clamp(54px, 6vw, 86px);
        line-height:.94; letter-spacing:-.065em; font-weight: 950;
        color:#fff;
    }
    .ca-hero-copy h1 span {
        display:block;
        background: linear-gradient(90deg, #fff 0%, #67e8f9 35%, #3b82f6 70%, #a78bfa 100%);
        -webkit-background-clip:text; background-clip:text; -webkit-text-fill-color:transparent;
        filter: drop-shadow(0 0 22px rgba(34,211,238,.16));
    }
    .ca-hero-copy p {
        max-width: 650px; color:#d3e2f3; font-size:19px; line-height:1.86;
        margin:0 0 24px 0;
    }

    .st-key-landing_url_input label {display:none !important;}
    .st-key-landing_url_input input,
    .st-key-landing_url_input [data-baseweb="input"] input {
        height: 66px !important; border-radius: 18px !important;
        border: 1px solid rgba(163, 211, 255, .22) !important;
        background: rgba(6, 15, 31, .74) !important;
        box-shadow: inset 0 0 0 1px rgba(255,255,255,.025), 0 16px 40px rgba(0,0,0,.22) !important;
        color: #f5fbff !important; font-size: 16px !important;
        padding-left: 22px !important;
        -webkit-text-fill-color: #f5fbff !important;
    }
    .st-key-landing_url_input input::placeholder {color:#8398b1 !important;}
    .st-key-landing_url_input input:focus,
    .st-key-landing_url_input input:active,
    .st-key-landing_url_input [data-baseweb="input"] input:focus,
    .st-key-landing_url_input [data-baseweb="input"] input:active {
        border-color: rgba(34,211,238,.62) !important;
        background: rgba(6, 15, 31, .86) !important;
        color: #f5fbff !important;
        -webkit-text-fill-color: #f5fbff !important;
        box-shadow: 0 0 0 4px rgba(34,211,238,.08), 0 0 36px rgba(34,211,238,.14) !important;
    }
    .st-key-landing_url_input input:-webkit-autofill,
    .st-key-landing_url_input input:-webkit-autofill:hover,
    .st-key-landing_url_input input:-webkit-autofill:focus {
        -webkit-text-fill-color: #f5fbff !important;
        -webkit-box-shadow: 0 0 0 1000px rgba(6, 15, 31, .86) inset !important;
        transition: background-color 9999s ease-out 0s !important;
    }

    .st-key-landing_website_cta button {
        height: 66px !important; border-radius: 18px !important;
        border: 1px solid rgba(140, 231, 255, .55) !important;
        background: linear-gradient(135deg, #0ea5e9, #2563eb 58%, #8b5cf6) !important;
        color: white !important; font-size: 18px !important; font-weight: 900 !important;
        box-shadow: 0 0 42px rgba(37, 99, 235, .34), inset 0 1px 0 rgba(255,255,255,.24) !important;
        transition: transform .18s ease, filter .18s ease, box-shadow .18s ease !important;
    }
    .st-key-landing_website_cta button:hover {
        transform: translateY(-2px) !important; filter: brightness(1.08) !important;
        box-shadow: 0 0 56px rgba(34, 211, 238, .42), inset 0 1px 0 rgba(255,255,255,.28) !important;
    }

    .st-key-teaser_continue_login {
        margin-top: 14px !important;
        padding-top: 6px !important;
    }
    .st-key-teaser_continue_login button {
        height: 62px !important;
        border-radius: 16px !important;
    }

    .ca-trust-row {display:flex; flex-wrap:wrap; gap:18px; margin-top:18px; color:#b8c9dc; font-size:14px; font-weight:700;}
    .ca-trust-row span {display:inline-flex; align-items:center; gap:6px;}

    .ca-demo-card {
        position:relative; overflow:hidden; min-height: 530px;
        border-radius: 32px; padding: 34px;
        border: 1px solid rgba(133, 220, 255, .24);
        background:
            radial-gradient(circle at 74% 20%, rgba(34,211,238,.20), transparent 26%),
            radial-gradient(circle at 12% 88%, rgba(37,99,235,.18), transparent 34%),
            linear-gradient(160deg, rgba(7, 17, 32, .92), rgba(6, 16, 31, .72));
        box-shadow: 0 30px 90px rgba(0,0,0,.42), 0 0 42px rgba(34,211,238,.14), inset 0 1px 0 rgba(255,255,255,.08);
        backdrop-filter: blur(18px);
    }
    .ca-demo-card::before {content:""; position:absolute; inset:0; background: linear-gradient(120deg, rgba(255,255,255,.08), transparent 22%, transparent 74%, rgba(34,211,238,.10)); pointer-events:none;}
    .ca-demo-card::after {content:""; position:absolute; left:54px; right:54px; bottom:0; height:2px; background:linear-gradient(90deg, transparent, #22d3ee, transparent); box-shadow:0 0 28px #22d3ee;}
    .ca-demo-orb {position:absolute; top:-120px; right:-90px; width:280px; height:280px; border-radius:50%; background:radial-gradient(circle, rgba(34,211,238,.32), transparent 60%); filter: blur(2px);}
    .ca-demo-head {display:flex; justify-content:space-between; align-items:flex-start; position:relative; z-index:1; margin-bottom:26px;}
    .ca-demo-kicker {font-size:25px; font-weight:950; color:#fff; letter-spacing:-.03em;}
    .ca-demo-sub {font-size:14px; color:#9fb3c8; margin-top:4px;}
    .ca-score-ring {width:116px; height:116px; border-radius:50%; display:flex; flex-direction:column; justify-content:center; align-items:center; background: conic-gradient(#22d3ee 0 47%, rgba(255,255,255,.10) 47% 100%); box-shadow:0 0 34px rgba(34,211,238,.22); position:relative;}
    .ca-score-ring::after {content:""; position:absolute; inset:13px; border-radius:50%; background:#071326; box-shadow: inset 0 0 18px rgba(0,0,0,.5);}
    .ca-ring-number, .ca-ring-label {position:relative; z-index:1;}
    .ca-ring-number {font-size:34px; font-weight:950; color:#fff; line-height:1;}
    .ca-ring-label {font-size:13px; color:#b8c9dc; margin-top:2px;}
    .ca-alert-box {position:relative; z-index:1; display:flex; gap:14px; align-items:center; border:1px solid rgba(251,191,36,.26); background:rgba(251,191,36,.075); border-radius:16px; padding:18px; color:#fde68a; margin-bottom:24px;}
    .ca-alert-box span {font-size:26px;}
    .ca-alert-box strong {display:block; color:#fde68a; font-size:18px;}
    .ca-alert-box small {display:block; color:#c8b57f; margin-top:4px;}
    .ca-loss-line {position:relative; z-index:1; display:flex; align-items:center; gap:14px; margin-bottom:18px; color:#e9f5ff; font-size:25px; font-weight:850;}
    .ca-loss-line strong {font-size:44px; letter-spacing:-.04em;}
    .ca-loss-icon {width:48px; height:48px; border-radius:15px; display:flex; align-items:center; justify-content:center; background:rgba(34,211,238,.12); border:1px solid rgba(34,211,238,.30); color:#67e8f9; font-weight:950;}
    .ca-metric-line {position:relative; z-index:1; display:flex; justify-content:space-between; color:#d7e7f8; font-weight:700; margin-top:15px;}
    .ca-track {position:relative; z-index:1; height:8px; border-radius:999px; background:rgba(255,255,255,.12); margin-top:8px; overflow:hidden;}
    .ca-fill {height:100%; border-radius:999px;}
    .ca-fill-warm {width:22%; background:linear-gradient(90deg,#f59e0b,#fbbf24); box-shadow:0 0 12px rgba(251,191,36,.5);}
    .ca-fill-cyan {width:45%; background:linear-gradient(90deg,#06b6d4,#22d3ee); box-shadow:0 0 12px rgba(34,211,238,.48);}
    .ca-chip-row {position:relative; z-index:1; display:flex; gap:10px; margin:18px 0 24px;}
    .ca-chip-row span {padding:8px 13px; border:1px solid rgba(34,211,238,.32); background:rgba(34,211,238,.08); color:#a5f3fc; border-radius:999px; font-weight:850; font-size:13px;}
    .ca-demo-btn {position:relative; z-index:1; text-align:center; padding:18px 20px; border-radius:18px; background:linear-gradient(135deg, rgba(14,165,233,.28), rgba(37,99,235,.26)); border:1px solid rgba(34,211,238,.38); color:#e8fbff; font-weight:950; font-size:18px; box-shadow:0 0 24px rgba(34,211,238,.16);}

    .ca-feature-grid {display:grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap:18px; margin-top:46px;}
    .ca-feature-card {display:flex; gap:18px; border:1px solid var(--ca-border); border-radius:24px; padding:26px; background:linear-gradient(180deg, rgba(10,24,42,.72), rgba(8,18,34,.54)); box-shadow:0 18px 50px rgba(0,0,0,.22), inset 0 1px 0 rgba(255,255,255,.05); transition:.18s ease;}
    .ca-feature-card:hover {transform:translateY(-3px); border-color:rgba(34,211,238,.34); box-shadow:0 24px 66px rgba(0,0,0,.30), 0 0 30px rgba(34,211,238,.10);}
    .ca-feature-icon {width:58px; height:58px; flex:0 0 auto; display:flex; align-items:center; justify-content:center; border-radius:18px; background:linear-gradient(145deg, rgba(37,99,235,.22), rgba(34,211,238,.10)); border:1px solid rgba(34,211,238,.26); color:#67e8f9; font-size:27px; box-shadow:0 0 22px rgba(37,99,235,.16);}
    .ca-feature-card span {color:#22d3ee; font-size:13px; font-weight:900;}
    .ca-feature-card h3 {margin:8px 0 8px; color:#fff; font-size:25px; line-height:1.1; letter-spacing:-.03em;}
    .ca-feature-card p {margin:0; color:#bdcadb; line-height:1.75; font-size:14px;}
    .ca-insight-grid {display:grid; grid-template-columns: 1.05fr 1fr; gap:20px; margin-top:22px;}
    .ca-ai-card, .ca-trend-card {border:1px solid var(--ca-border); border-radius:24px; padding:30px; min-height:250px; background:linear-gradient(165deg, rgba(8,20,38,.76), rgba(8,18,34,.58)); box-shadow:0 22px 70px rgba(0,0,0,.26), inset 0 1px 0 rgba(255,255,255,.05); position:relative; overflow:hidden;}
    .ca-ai-card::after {content:""; position:absolute; right:50px; bottom:34px; width:130px; height:130px; border-radius:30px; background:radial-gradient(circle, rgba(34,211,238,.24), transparent 62%); box-shadow:0 0 44px rgba(34,211,238,.18);}
    .ca-card-badge {display:inline-flex; padding:7px 12px; border-radius:999px; background:rgba(34,211,238,.08); border:1px solid rgba(34,211,238,.20); color:#93f4ff; font-weight:900; font-size:13px; margin-bottom:16px;}
    .ca-ai-card h3 {font-size:27px; color:#fff; margin:0 0 12px; letter-spacing:-.03em;}
    .ca-ai-card p, .ca-trend-card p {color:#bbc9da; line-height:1.7; margin:0 0 18px;}
    .ca-impact {display:inline-flex; color:#6ee7b7; font-size:25px; font-weight:950;}
    .ca-chart-line {height:110px; border-radius:18px; border:1px solid rgba(255,255,255,.08); background:linear-gradient(160deg, rgba(37,99,235,.08), rgba(139,92,246,.11)), linear-gradient(to right, rgba(255,255,255,.04) 1px, transparent 1px), linear-gradient(to bottom, rgba(255,255,255,.05) 1px, transparent 1px); background-size:auto, 25% 100%, 100% 33%; position:relative; margin-bottom:14px;}
    .ca-chart-line::before {content:""; position:absolute; left:8%; right:7%; top:62%; height:4px; border-radius:999px; background:linear-gradient(90deg,#3b82f6,#8b5cf6,#22d3ee); transform:skewY(-10deg); box-shadow:0 0 22px rgba(139,92,246,.42);}
    .ca-chart-points {display:flex; justify-content:space-between; color:#c6d6e9; font-weight:800; align-items:center;}
    .ca-chart-points b {color:#6ee7b7; font-size:22px;}
    .ca-proof-strip {margin-top:22px; padding:22px 26px; border-radius:22px; border:1px solid rgba(251,191,36,.20); background:linear-gradient(90deg, rgba(251,191,36,.06), rgba(34,211,238,.045)); display:flex; align-items:center; justify-content:space-between; gap:24px; color:#eaf4ff; font-size:18px; box-shadow:0 16px 46px rgba(0,0,0,.20);}
    .ca-proof-strip b {color:#fde68a;}
    .ca-logo-row {display:flex; gap:34px; color:#8c9db3; font-weight:950; text-transform:lowercase; letter-spacing:.02em;}

    @media (max-width: 900px) {
        .ca-nav {
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            gap: 18px;
        }
        .ca-nav-links {gap:18px; flex-wrap:wrap; justify-content:flex-start;}
        .ca-nav-actions {width: 100%; justify-content: flex-start; margin-left: 0;}
        .ca-nav-popover {left: 0; transform: translateX(0) translateY(6px);}
        .ca-nav-item:hover .ca-nav-popover {transform: translateX(0) translateY(0);}
        .ca-anchor-grid {grid-template-columns: 1fr;}
        .ca-feature-grid, .ca-insight-grid {grid-template-columns:1fr;}
        .ca-proof-strip {flex-direction:column; align-items:flex-start;}
        .ca-logo-row {flex-wrap:wrap; gap:18px;}
        .ca-demo-card {min-height:auto;}
        .teaser-head {flex-direction: column;}
        .teaser-score-grid {grid-template-columns: repeat(2, minmax(0, 1fr)); min-width: 100%;}
        .teaser-lock-grid, .teaser-bench-grid {grid-template-columns: 1fr;}
        .teaser-loss-row {flex-direction: column;}
        .elite-top {flex-direction: column; align-items: flex-start;}
        .elite-metrics {grid-template-columns: repeat(2, minmax(0, 1fr));}
        .elite-main-grid, .elite-bottom-grid {grid-template-columns: 1fr;}
        .cp-shell {grid-template-columns: 1fr;}
        .cp-metrics {grid-template-columns: repeat(2, minmax(0,1fr));}
        .cp-grid-2 {grid-template-columns: 1fr;}
        .ca-bridge-header {flex-direction: column; align-items: flex-start;}
        .ca-bridge-result-title {margin-left: 0;}
    }

    /* Dashboard action banners */
    .cp-action-banner {
        display: flex; align-items: flex-start; gap: 14px;
        background: rgba(34,211,238,0.06); border: 1px solid rgba(34,211,238,0.2);
        border-radius: 16px; padding: 18px 20px; margin-bottom: 4px;
    }
    .cp-action-icon { font-size: 24px; flex-shrink: 0; margin-top: 2px; }
    .cp-action-body { flex: 1; }
    .cp-action-title { font-size: 15px; font-weight: 700; color: #e2e8f0; margin-bottom: 4px; }
    .cp-action-sub { font-size: 13px; color: #94a3b8; line-height: 1.6; }
    .cp-last-score-banner {
        display: flex; align-items: center; justify-content: space-between;
        background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
        border-radius: 16px; padding: 18px 20px; margin-bottom: 4px;
    }
    .cp-last-score-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 4px; }
    .cp-last-score-target { font-size: 14px; font-weight: 600; color: #cbd5e1; }
    .cp-last-score-num { font-size: 40px; font-weight: 900; line-height: 1; }
    .cp-last-score-num span { font-size: 16px; color: #475569; font-weight: 400; }
    .cp-welcome-banner {
        display: flex; align-items: center; gap: 14px;
        background: rgba(99,102,241,0.07); border: 1px solid rgba(99,102,241,0.2);
        border-radius: 16px; padding: 18px 20px; margin-bottom: 4px;
    }
    .cp-welcome-icon { font-size: 24px; flex-shrink: 0; }
    .cp-welcome-title { font-size: 15px; font-weight: 700; color: #e2e8f0; margin-bottom: 4px; }
    .cp-welcome-sub { font-size: 13px; color: #94a3b8; line-height: 1.6; }

    /* Bridge header: shown when user arrives from Next.js landing with a pre-filled URL */
    .ca-bridge-header {
        display: flex;
        align-items: center;
        gap: 16px;
        padding: 16px 0 28px;
        border-bottom: 1px solid rgba(255,255,255,0.07);
        margin-bottom: 24px;
        flex-wrap: wrap;
    }
    .ca-bridge-back {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        font-size: 13px;
        font-weight: 600;
        color: #7dd3fc;
        text-decoration: none;
        padding: 6px 14px;
        border-radius: 999px;
        border: 1px solid rgba(125,211,252,0.25);
        background: rgba(125,211,252,0.06);
        transition: all 0.2s;
    }
    .ca-bridge-back:hover { background: rgba(125,211,252,0.14); color: #bae6fd; }
    .ca-bridge-result-title {
        font-size: 13px;
        font-weight: 700;
        color: #4ade80;
        letter-spacing: 0.01em;
        margin-left: auto;
    }

    /* ── Preview Detail (pd-*) ───────────────────────────────────────── */
    .pd-shell {
        background: linear-gradient(135deg, #071325 0%, #0d1f38 60%, #0a2540 100%);
        border: 1px solid rgba(34,211,238,0.18);
        border-radius: 24px;
        padding: 28px;
        margin-top: 18px;
    }
    .pd-header {
        display: flex; align-items: flex-start; justify-content: space-between;
        gap: 20px; margin-bottom: 18px; flex-wrap: wrap;
    }
    .pd-badge {
        display: inline-flex; align-items: center; gap: 6px;
        font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.06em;
        color: #67e8f9; background: rgba(34,211,238,0.1); border: 1px solid rgba(34,211,238,0.25);
        border-radius: 999px; padding: 4px 12px; margin-bottom: 8px;
    }
    .pd-target { font-size: 18px; font-weight: 800; color: #f1f5f9; margin-bottom: 4px; }
    .pd-date { font-size: 12px; color: #64748b; }
    .pd-score-block { text-align: right; flex-shrink: 0; }
    .pd-score-label { font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.06em; color: #64748b; margin-bottom: 4px; }
    .pd-score-num { font-size: 48px; font-weight: 900; line-height: 1; }
    .pd-score-num span { font-size: 18px; color: #475569; font-weight: 400; }
    .pd-risk-pill {
        display: inline-block; margin-top: 6px;
        font-size: 11px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.05em;
        padding: 3px 10px; border-radius: 999px; border: 1px solid;
    }
    .pd-bar-track { height: 8px; border-radius: 999px; background: rgba(255,255,255,0.07); margin-bottom: 18px; overflow: hidden; }
    .pd-bar-fill { height: 100%; border-radius: 999px; transition: width 1s cubic-bezier(.4,0,.2,1); }
    .pd-sub-grid { display: grid; grid-template-columns: repeat(3,1fr); gap: 10px; margin-bottom: 22px; }
    .pd-sub-item {
        text-align: center; background: rgba(255,255,255,0.03);
        border: 1px solid rgba(255,255,255,0.08); border-radius: 14px; padding: 12px 8px;
    }
    .pd-sub-item span { display: block; font-size: 11px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.05em; color: #64748b; margin-bottom: 4px; }
    .pd-sub-item b { font-size: 22px; font-weight: 900; color: #f1f5f9; }
    .pd-section-title { font-size: 13px; font-weight: 700; color: #e2e8f0; margin-bottom: 10px; }
    .pd-findings-list { list-style: none; padding: 0; margin: 0 0 22px 0; display: flex; flex-direction: column; gap: 8px; }
    .pd-finding-item {
        display: flex; align-items: flex-start; gap: 10px;
        background: rgba(251,191,36,0.06); border: 1px solid rgba(251,191,36,0.15);
        border-radius: 12px; padding: 12px 14px; font-size: 13px; color: #cbd5e1; line-height: 1.6;
    }
    .pd-finding-icon { color: #fbbf24; flex-shrink: 0; margin-top: 1px; }
    .pd-lock-zone {
        background: rgba(99,102,241,0.06); border: 1px solid rgba(99,102,241,0.2);
        border-radius: 18px; padding: 20px; margin-bottom: 22px;
    }
    .pd-lock-zone-title { font-size: 14px; font-weight: 700; color: #e2e8f0; margin-bottom: 6px; }
    .pd-lock-zone-sub { font-size: 12px; color: #94a3b8; line-height: 1.6; margin-bottom: 14px; }
    .pd-lock-cards { display: flex; flex-direction: column; gap: 8px; }
    .pd-lock-card {
        display: flex; align-items: center; gap: 10px;
        background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.07);
        border-radius: 10px; padding: 10px 14px;
    }
    .pd-lock-icon { flex-shrink: 0; }
    .pd-lock-text { font-size: 13px; color: #475569; filter: blur(5px); user-select: none; }
    .pd-upgrade-shell {
        background: linear-gradient(135deg, rgba(34,211,238,0.08), rgba(56,189,248,0.05));
        border: 1px solid rgba(34,211,238,0.25); border-radius: 20px; padding: 24px;
    }
    .pd-upgrade-title { font-size: 18px; font-weight: 800; color: #f1f5f9; margin-bottom: 6px; }
    .pd-upgrade-sub { font-size: 13px; color: #94a3b8; line-height: 1.6; margin-bottom: 16px; }
    .pd-upgrade-features { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-bottom: 20px; }
    .pd-upgrade-feat { font-size: 13px; color: #67e8f9; font-weight: 600; }
    .pd-upgrade-btn {
        display: block; text-align: center; text-decoration: none;
        background: linear-gradient(90deg, rgba(34,211,238,0.85), rgba(56,189,248,0.85));
        color: #fff; font-weight: 800; font-size: 14px;
        border-radius: 14px; padding: 14px 20px;
        box-shadow: 0 0 28px rgba(34,211,238,0.25);
        transition: opacity 0.2s, transform 0.2s;
    }
    .pd-upgrade-btn:hover { opacity: 0.92; transform: scale(1.01); }
    .pd-upgrade-note { font-size: 11px; color: #475569; text-align: center; margin-top: 10px; }
    @media (max-width: 600px) {
        .pd-header { flex-direction: column; }
        .pd-score-block { text-align: left; }
        .pd-upgrade-features { grid-template-columns: 1fr; }
    }
</style>
    """,
        unsafe_allow_html=True,
    )

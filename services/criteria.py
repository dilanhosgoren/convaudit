"""
Audit criteria definitions.

Statuses:
  PASS     — criterion clearly met
  PARTIAL  — partially met or insufficient
  FAIL     — clearly absent or broken
  OPTIONAL — criterion is not required for this site type (intentional absence ≠ failure)
  UNKNOWN  — cannot be verified from this screenshot alone
               (e.g. element lives in footer, checkout, or product pages)

Scoring:
  PASS     = full pts
  OPTIONAL = full pts (no penalty — deliberate brand/business choice)
  PARTIAL  = pts × 0.5
  UNKNOWN  = pts × 0.5 (benefit of the doubt; reduces confidence percentage)
  FAIL     = 0 pts

OPTIONAL vs UNKNOWN:
  OPTIONAL = AI can see the element is absent but this is intentional for the site type
  UNKNOWN  = AI cannot verify because the element is off-screen / on another page
"""

# ── Site type taxonomy ────────────────────────────────────────────────────────
SITE_TYPES: dict[str, str] = {
    "d2c":         "D2C Marka",
    "marketplace": "Pazar Yeri / Platform",
    "luxury":      "Premium / Lüks Marka",
    "saas":        "SaaS / Dijital Ürün",
    "b2b":         "B2B / Kurumsal",
    "local":       "Yerel İşletme",
    "content":     "İçerik / Blog",
    "other":       "Diğer / Karma",
}

# ── Criteria definitions ──────────────────────────────────────────────────────
CRITERIA: dict[str, dict] = {
    # ── UX — 6 × 5 = 30 pts ─────────────────────────────────────────────────
    "hero_clarity": {
        "category": "ux", "pts": 5, "severity": "critical",
        "needs_full_site": False,
        "optional_for": [],
        "tr": "Değer önerisi ilk 3 saniyede anlaşılıyor",
        "hint": (
            "Does the hero headline state WHAT the site sells and FOR WHOM without jargon? "
            "PASS=clear and specific. PARTIAL=vague or too generic. FAIL=no headline or completely unclear. "
            "UNKNOWN only if the hero area is entirely outside the screenshot. "
            "NOTE: Luxury/minimal brands may use short poetic copy — assess clarity for their audience, "
            "not by generic e-commerce standards."
        ),
    },
    "cta_above_fold": {
        "category": "ux", "pts": 5, "severity": "critical",
        "needs_full_site": False,
        "optional_for": ["content"],
        "tr": "Dönüşüm akışına yönlendiren birincil CTA görünür",
        "hint": (
            "Is there a primary action button visible without scrolling that leads the user toward "
            "a purchase or conversion flow (e.g. 'Satın Al', 'Koleksiyonu Keşfet', 'Ücretsiz Dene', "
            "'Teklif Al', 'Başla')? Evaluate the INTENT and PROMINENCE, not just button presence. "
            "PASS=clear high-contrast button leading toward conversion. "
            "PARTIAL=button exists but low contrast, generic label ('Daha Fazla'), or buried. "
            "FAIL=no visible primary action that leads toward conversion. "
            "OPTIONAL=content/editorial site where a purchase CTA is not the primary goal. "
            "UNKNOWN=screenshot cropped and fold not visible. "
            "BRAND NOTE: Luxury brands often use minimal CTAs ('Keşfet', 'Görüntüle') — "
            "evaluate whether the CTA fits the brand intent, not whether it matches d2c conventions."
        ),
    },
    "navigation_clear": {
        "category": "ux", "pts": 5, "severity": "high",
        "needs_full_site": False,
        "optional_for": [],
        "tr": "Navigasyon kategorileri net ve erişilebilir",
        "hint": (
            "Are main product/service categories clearly labelled in the header nav? "
            "PASS=clear menu visible. PARTIAL=menu exists but overcrowded or unclear labels. "
            "FAIL=no navigation visible. UNKNOWN only if the header is cut off."
        ),
    },
    "visual_hierarchy": {
        "category": "ux", "pts": 5, "severity": "medium",
        "needs_full_site": False,
        "optional_for": [],
        "tr": "Görsel hiyerarşi mantıklı, göz akışı temiz",
        "hint": (
            "Does the page guide the eye logically (headline → benefit → CTA)? "
            "PASS=clean hierarchy, no clutter. PARTIAL=some hierarchy but competing elements. "
            "FAIL=chaotic layout or heavy visual noise. UNKNOWN is rarely appropriate here. "
            "BRAND NOTE: Luxury/minimalist brands may use generous whitespace and single focal points — "
            "a restrained layout with intentional spacing is PASS, not FAIL."
        ),
    },
    "mobile_layout": {
        "category": "ux", "pts": 5, "severity": "high",
        "needs_full_site": False,
        "optional_for": [],
        "tr": "Mobil uyumlu görünüm sinyalleri",
        "hint": (
            "Does the layout appear responsive? Look for: readable text, large tap targets, "
            "no horizontal overflow, fluid columns. Screenshot is desktop — assess whether the design "
            "looks responsive (flexible grid, no fixed-width overflows). "
            "PARTIAL if some elements look fixed-width. UNKNOWN if genuinely cannot assess."
        ),
    },
    "no_popup_blocker": {
        "category": "ux", "pts": 5, "severity": "medium",
        "needs_full_site": False,
        "optional_for": [],
        "tr": "Pop-up deneyimi kullanıcıyı engellemiyor",
        "hint": (
            "Evaluate the pop-up situation based on what is visible. Three distinct types: "
            "1) COOKIE/KVKK CONSENT BAR (small bottom or top bar) — this is a legal requirement. "
            "   Its presence is PASS if unobtrusive; PARTIAL if it covers more than 20%% of the screen. "
            "2) NEWSLETTER/SUBSCRIPTION POPUP (appears with delay, dismissible) — "
            "   PARTIAL if it has a clear close button and appears mid-scroll; "
            "   FAIL if it fires immediately on load and blocks above-fold content. "
            "3) FULL-SCREEN INTERSTITIAL (blocks all content, no obvious close, or age gate) — "
            "   Always FAIL regardless of site type. "
            "If no popup is visible: PASS. "
            "UNKNOWN=screenshot shows a fully loaded page but you cannot determine if a popup "
            "fires dynamically (this is acceptable; mark UNKNOWN). "
            "OPTIONAL=newsletter popups may be strategically absent on luxury/b2b sites by design; "
            "use OPTIONAL only if the site type clearly makes such popups inappropriate AND none is visible."
        ),
    },

    # ── Trust — 5 × 5 = 25 pts ──────────────────────────────────────────────
    "ssl_visible": {
        "category": "trust", "trust_sub": "homepage", "pts": 5, "severity": "critical",
        "needs_full_site": False,
        "optional_for": [],
        "tr": "SSL / güvenlik rozeti görünür",
        "hint": (
            "Is there a padlock icon in the browser bar area, an explicit 'Güvenli Alışveriş' / "
            "'SSL' badge, or HTTPS-confirming text visible on the page? "
            "PASS=badge/indicator present. FAIL=no security indicator. "
            "Do NOT use UNKNOWN here — if you cannot see it, that itself is a trust failure."
        ),
    },
    "return_policy": {
        "category": "trust", "trust_sub": "site_wide", "pts": 5, "severity": "high",
        "needs_full_site": True,
        "optional_for": ["saas", "content"],
        "tr": "İade politikası bağlantısı erişilebilir",
        "hint": (
            "Is a return/refund policy link or text visible (typically in footer or product area)? "
            "PASS=visible link or text. PARTIAL=mentioned but not a clear link. "
            "FAIL=clearly absent (you can see the full footer and there is none). "
            "UNKNOWN=footer is not visible in this screenshot — do NOT assume FAIL. "
            "OPTIONAL=SaaS/content sites that don't sell physical goods."
        ),
    },
    "social_proof": {
        "category": "trust", "trust_sub": "product", "pts": 5, "severity": "high",
        "needs_full_site": True,
        "optional_for": ["b2b", "luxury"],
        "tr": "Sosyal kanıt görünür (yorum, puan, müşteri sayısı)",
        "hint": (
            "Are star ratings, review counts, testimonials, or 'X happy customers' visible? "
            "PASS=clear social proof on this page. "
            "PARTIAL=implied (e.g. 'Thousands of customers') but no specific numbers or reviews. "
            "FAIL=clearly no social proof anywhere on this page. "
            "UNKNOWN=this page is a homepage without product listings — reviews are typically on "
            "product pages. Use UNKNOWN if you cannot confirm either way. "
            "OPTIONAL=B2B sites that use case studies/logos instead of star ratings; "
            "luxury brands that intentionally omit reviews to preserve exclusivity. "
            "Use OPTIONAL only when the site type clearly makes traditional social proof inappropriate."
        ),
    },
    "payment_icons": {
        "category": "trust", "trust_sub": "site_wide", "pts": 5, "severity": "medium",
        "needs_full_site": True,
        "optional_for": ["saas", "b2b", "content"],
        "tr": "Ödeme yöntemi ikonları mevcut",
        "hint": (
            "Are Visa, Mastercard, iyzico, PayTR, or other payment icons visible? "
            "Usually found in the footer. PASS=icons visible. FAIL=footer is visible but no icons. "
            "UNKNOWN=footer is not in the screenshot — do NOT mark FAIL without seeing the footer. "
            "OPTIONAL=SaaS/B2B/content sites that handle payment via invoice or subscription portals."
        ),
    },
    "contact_accessible": {
        "category": "trust", "trust_sub": "site_wide", "pts": 5, "severity": "critical",
        "needs_full_site": True,
        "optional_for": [],
        "tr": "İletişim bilgisi veya destek görünür",
        "hint": (
            "Is a phone number, email, live chat widget, or 'İletişim' link clearly visible? "
            "Check header, footer, and any floating elements. "
            "PASS=contact info visible. PARTIAL=a contact link exists but no immediate info. "
            "FAIL=you can see header and footer clearly and there is no contact option. "
            "UNKNOWN=footer/header not fully visible in screenshot."
        ),
    },

    # ── Content — 5 × 5 = 25 pts ─────────────────────────────────────────────
    "benefits_stated": {
        "category": "content", "pts": 5, "severity": "high",
        "needs_full_site": False,
        "optional_for": [],
        "tr": "Fayda odaklı metin (özellik değil fayda)",
        "hint": (
            "Does the copy communicate customer GAINS, not just product specs? "
            "PASS=clear outcome-oriented language ('Drop weight faster', 'Ship in 24h'). "
            "PARTIAL=some benefits mentioned alongside feature lists. "
            "FAIL=only spec/feature lists with no outcome framing. "
            "BRAND NOTE: Luxury brands may use aspirational language instead of explicit benefits — "
            "evaluate whether the copy resonates with the target audience, not by d2c copy formulas."
        ),
    },
    "pricing_clear": {
        "category": "content", "pts": 5, "severity": "high",
        "needs_full_site": True,
        "optional_for": ["luxury", "b2b"],
        "tr": "Fiyat veya fiyat bulma yolu net",
        "hint": (
            "Are prices visible on this page, or is there a clear 'Fiyatları Gör' path? "
            "PASS=prices visible. PARTIAL='See pricing' CTA exists but no prices shown. "
            "FAIL=no price and no clear way to find price. "
            "UNKNOWN=this appears to be a homepage for a multi-product site where pricing "
            "lives on product pages — product pages were not captured. "
            "OPTIONAL=luxury brands where 'contact us for pricing' is a deliberate positioning choice; "
            "B2B sites with custom enterprise pricing."
        ),
    },
    "professional_copy": {
        "category": "content", "pts": 5, "severity": "medium",
        "needs_full_site": False,
        "optional_for": [],
        "tr": "Metin profesyonel ve hatasız",
        "hint": (
            "Is the visible text grammatically correct, consistently toned, no obvious typos? "
            "PASS=professional. PARTIAL=mostly professional but minor issues. "
            "FAIL=obvious errors, inconsistent tone, or machine-translated feel. "
            "UNKNOWN only if there is almost no text visible."
        ),
    },
    "urgency_present": {
        "category": "content", "pts": 5, "severity": "low",
        "needs_full_site": True,
        "optional_for": ["luxury", "b2b", "saas", "content"],
        "tr": "Satın alma motivasyonu / aciliyet unsuru var",
        "hint": (
            "Is there a countdown timer, 'Sınırlı Stok', discount badge, or promotional element? "
            "PASS=clear urgency element. PARTIAL=implied urgency without specifics. "
            "FAIL=no urgency element on this page (for D2C/Marketplace where urgency is expected). "
            "UNKNOWN=urgency elements typically appear on product/cart pages — use UNKNOWN "
            "if this is a category or homepage with no product listings. "
            "OPTIONAL=luxury, B2B, SaaS, and content sites where urgency tactics conflict with "
            "brand positioning or are simply not part of the business model. "
            "A luxury brand NOT using countdown timers is making a deliberate brand choice — mark OPTIONAL, not FAIL."
        ),
    },
    "audience_match": {
        "category": "content", "pts": 5, "severity": "medium",
        "needs_full_site": False,
        "optional_for": [],
        "tr": "İçerik net bir hedef kitleye hitap ediyor",
        "hint": (
            "Does the messaging clearly address a specific audience segment? "
            "PASS=clear persona ('For serious athletes', 'Küçük işletmeler için'). "
            "PARTIAL=somewhat targeted but still generic. "
            "FAIL=completely generic messaging suitable for everyone = no one."
        ),
    },

    # ── Content (extended) — 5 × 5 = 25 pts ─────────────────────────────────
    "content_value_prop": {
        "category": "content", "pts": 5, "severity": "critical",
        "needs_full_site": False,
        "optional_for": [],
        "tr": "Değer önerisi kristal netliğinde ve çekici",
        "hint": (
            "Is the core value proposition unmistakably clear within 5 seconds? "
            "PASS=visitor immediately understands WHO benefits, WHAT they get, and WHY this brand over others. "
            "PARTIAL=benefit is stated but generic ('high quality', 'best price') or unclear for the target audience. "
            "FAIL=the page does not communicate a distinct, compelling value proposition. "
            "BRAND NOTE: Luxury brands use aspirational positioning — evaluate whether the messaging conveys "
            "status/exclusivity for the luxury buyer, not by D2C copy-formula standards."
        ),
    },
    "content_readability": {
        "category": "content", "pts": 5, "severity": "medium",
        "needs_full_site": False,
        "optional_for": [],
        "tr": "Metin kolay okunuyor ve taranabiliyor",
        "hint": (
            "Is the visible text broken into short paragraphs, uses bullet lists, bold key phrases, "
            "and appropriate font size (minimum 14-16px visual impression)? "
            "PASS=text is scannable with clear structure, sub-headings, and short sentences. "
            "PARTIAL=text exists and is readable but dense blocks without visual breaks. "
            "FAIL=wall of text, tiny font, or text crammed without spacing. "
            "UNKNOWN=no significant text content visible in this screenshot."
        ),
    },
    "content_trust_signals": {
        "category": "content", "pts": 5, "severity": "high",
        "needs_full_site": True,
        "optional_for": ["content"],
        "tr": "Güven artırıcı içerik (garanti, sertifika, ödül, müşteri logosu)",
        "hint": (
            "Are there visible trust-enhancing content elements: money-back guarantees, certifications, "
            "industry awards, media mentions ('As seen in'), customer logos, security badges, or "
            "recognized quality marks (TSE, ISO, etc.)? "
            "PASS=at least 2 distinct trust content signals visible. "
            "PARTIAL=1 trust signal present. "
            "FAIL=no trust-enhancing content visible on this page. "
            "UNKNOWN=these elements typically appear in specific sections — use UNKNOWN if not visible. "
            "OPTIONAL=content/blog sites where trust is built through expertise signals (author bio, dates, sources)."
        ),
    },
    "content_cta_quality": {
        "category": "content", "pts": 5, "severity": "high",
        "needs_full_site": False,
        "optional_for": ["content"],
        "tr": "Harekete geçirici butonlar güçlü, net ve sonuç odaklı",
        "hint": (
            "Evaluate the quality of call-to-action copy, not just presence. "
            "PASS=CTAs use outcome/benefit language ('Ücretsiz Başla', 'Hemen Tasarruf Et', 'Koleksiyonu Keşfet') "
            "with high contrast and clear visual hierarchy. "
            "PARTIAL=CTAs exist but use generic labels ('Daha Fazla', 'Tıkla', 'Gönder') or low contrast. "
            "FAIL=CTAs are missing or completely ineffective as conversion drivers. "
            "OPTIONAL=editorial/blog sites where conversion is not the primary goal. "
            "BRAND NOTE: Luxury CTAs like 'Keşfet' or 'Görüntüle' are intentionally understated — "
            "evaluate whether the CTA fits the brand intention, not D2C verb-action standards."
        ),
    },
    "content_conversion_flow": {
        "category": "content", "pts": 5, "severity": "medium",
        "needs_full_site": False,
        "optional_for": ["content", "b2b"],
        "tr": "Sayfa dönüşüm odaklı bir akış sunuyor",
        "hint": (
            "Does the page layout guide the visitor toward a clear conversion action in a logical flow? "
            "Look for: hero → benefit summary → social proof → CTA pattern (or appropriate variation for site type). "
            "PASS=clear conversion-oriented flow with each section building toward a specific next step. "
            "PARTIAL=conversion intent exists but the flow is broken, jumps around, or lacks one key element. "
            "FAIL=page is informational/scattered with no clear conversion path. "
            "OPTIONAL=content/editorial sites and B2B lead-gen sites with non-standard flows. "
            "BRAND NOTE: Luxury brands often use beauty-first scrolling experiences — evaluate whether the "
            "flow feels intentional for their audience, not by standard D2C funnel criteria."
        ),
    },

    # ── Performance signals — 4 × 5 = 20 pts ──────────────────────────────────
    "lightweight_design": {
        "category": "perf", "pts": 5, "severity": "medium",
        "needs_full_site": False,
        "optional_for": [],
        "tr": "Tasarım hafif görünüyor",
        "hint": (
            "Does the page look clean with few heavy uncompressed images or complex backgrounds? "
            "PASS=clean minimal design. PARTIAL=some heavy elements but manageable. "
            "FAIL=visually heavy with many large images or complex animated backgrounds."
        ),
    },
    "no_heavy_sliders": {
        "category": "perf", "pts": 5, "severity": "low",
        "needs_full_site": False,
        "optional_for": ["luxury"],
        "tr": "Büyük render-blocking slider/karusel yok",
        "hint": (
            "Is the hero a static image or simple layout rather than a heavy auto-playing carousel? "
            "PASS=static or simple hero. PARTIAL=one carousel but not excessive. "
            "FAIL=multiple heavy auto-playing carousels or sliders dominating the page. "
            "OPTIONAL=luxury brands that use cinematic hero videos/carousels as intentional brand experience."
        ),
    },
    "image_quality": {
        "category": "perf", "pts": 5, "severity": "medium",
        "needs_full_site": False,
        "optional_for": [],
        "tr": "Görseller optimize ve tutarlı kalitede",
        "hint": (
            "Do images appear crisp and consistently sized? "
            "PASS=sharp, well-sized, consistent style. "
            "PARTIAL=mostly good but some inconsistency. "
            "FAIL=pixelated, stretched, broken, or wildly inconsistent images. "
            "UNKNOWN only if no images are visible."
        ),
    },
    "layout_stability": {
        "category": "perf", "pts": 5, "severity": "medium",
        "needs_full_site": False,
        "optional_for": [],
        "tr": "Sayfa düzeni stabil ve dengeli",
        "hint": (
            "Is the layout balanced with no obvious empty gaps, misaligned elements, or broken sections? "
            "PASS=clean stable layout. PARTIAL=minor misalignments. "
            "FAIL=obvious broken sections, large empty gaps, or overlapping elements."
        ),
    },
}

CATEGORY_LABELS: dict[str, str] = {
    "ux":      "UX & Kullanılabilirlik",
    "trust":   "Güven & Güvenlik",
    "content": "İçerik & Mesajlaşma",
    "perf":    "Performans Sinyalleri",
}

TRUST_SUB_LABELS: dict[str, str] = {
    "homepage":  "Ana Sayfa Güveni",
    "site_wide": "Site Geneli Güven",
    "product":   "Ürün Güveni",
}

SEVERITY_LABELS: dict[str, str] = {
    "critical": "Kritik",
    "high":     "Yüksek",
    "medium":   "Orta",
    "low":      "Düşük",
}

MAX_SCORE = sum(c["pts"] for c in CRITERIA.values())  # = 100

# ── Scoring functions — delegated to scoring_engine (single source of truth) ──
# scoring_engine.py lives in frontend/scripts/. We locate it relative to this
# file: ShopifyAudit/services/ → ../../frontend/scripts
import os as _os, sys as _sys
_se_path = _os.path.abspath(_os.path.join(_os.path.dirname(__file__), "..", "..", "frontend", "scripts"))
if _se_path not in _sys.path:
    _sys.path.insert(0, _se_path)

try:
    from scoring_engine import (
        compute_score       as calculate_score,
        compute_confidence  as calculate_confidence,
        compare_snapshots,
        normalise_criteria,
        normalise_status,
    )
except ImportError:
    # Fallback if scoring_engine is not yet available (keeps existing logic)
    def _status_pts(status: str, pts: float) -> float:
        s = status.upper()
        if s in ("PASS", "OPTIONAL"):  return pts
        if s in ("PARTIAL", "UNKNOWN", "NOT_FOUND"): return pts * 0.5
        return 0.0

    def calculate_score(criteria_results: dict) -> dict:
        cat_pts: dict = {}; cat_max: dict = {}
        for key, meta in CRITERIA.items():
            cat = meta["category"]; pts = meta["pts"]
            cat_pts.setdefault(cat, 0.0); cat_max.setdefault(cat, 0.0)
            cat_max[cat] += pts
            r = criteria_results.get(key, {})
            cat_pts[cat] += _status_pts(r.get("status", "FAIL") if isinstance(r, dict) else str(r), pts)
        def n10(c): return round((cat_pts.get(c,0)/cat_max[c])*10) if cat_max.get(c) else 5
        total = sum(cat_max.values()); earned = sum(cat_pts.values())
        return {"overall": max(0,min(100,round(earned/total*100) if total else 0)),
                "ux": n10("ux"), "trust": n10("trust"), "content": n10("content"), "perf": n10("perf")}

    def calculate_confidence(criteria_results: dict) -> dict:
        total = len(CRITERIA)
        unk = sum(1 for k in CRITERIA if (criteria_results.get(k) or {}).get("status","").upper()=="UNKNOWN")
        opt = sum(1 for k in CRITERIA if (criteria_results.get(k) or {}).get("status","").upper()=="OPTIONAL")
        vp  = round(((total-unk)/total)*100) if total else 0
        lv, lb = ("high","Yüksek") if vp>=80 else ("medium","Orta") if vp>=60 else ("low","Düşük")
        return {"level":lv,"label_tr":lb,"verified_pct":vp,"total":total,"unknown_count":unk,"optional_count":opt,"verified_count":total-unk}

    def compare_snapshots(prev: dict, curr: dict) -> dict:
        resolved=[]; ongoing=[]; new_issues=[]; delta=0.0
        for key, meta in CRITERIA.items():
            pts=float(meta["pts"]); label=meta["tr"]; cat=meta["category"]
            ps=(prev.get(key,{}).get("status") or "FAIL").upper()
            cs=(curr.get(key,{}).get("status") or "FAIL").upper()
            ev=curr.get(key,{}).get("evidence","") if isinstance(curr.get(key),dict) else ""
            if ps!="UNKNOWN" and cs!="UNKNOWN": delta+=_status_pts(cs,pts)-_status_pts(ps,pts)
            if ps in("UNKNOWN","OPTIONAL") or cs in("UNKNOWN","OPTIONAL"): continue
            if ps=="FAIL" and cs in("PASS","PARTIAL"): resolved.append({"key":key,"label":label,"category":cat,"evidence":ev,"status":cs})
            elif ps in("PASS","PARTIAL") and cs=="FAIL": new_issues.append({"key":key,"label":label,"category":cat,"evidence":ev})
            elif ps=="FAIL" and cs=="FAIL": ongoing.append({"key":key,"label":label,"category":cat,"evidence":ev})
        return {"resolved":resolved,"ongoing":ongoing,"new_issues":new_issues,"score_delta":round(delta)}

    def normalise_status(s: str) -> str:
        v = (s or "").strip().upper()
        return "UNKNOWN" if v == "NOT_FOUND" else (v if v in ("PASS","OPTIONAL","PARTIAL","UNKNOWN","FAIL") else "FAIL")

    def normalise_criteria(ai_criteria: dict) -> dict:
        return {k: ({**v, "status": normalise_status(v.get("status","FAIL"))} if isinstance(v,dict) else {"status":normalise_status(str(v)),"evidence":""})
                for k, v in ai_criteria.items()}

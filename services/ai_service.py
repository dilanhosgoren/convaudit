import json
import os
from openai import OpenAI

from config.settings import MODEL_NAME
from services.browser_service import capture_website
from services.criteria import CRITERIA, SITE_TYPES, calculate_score, calculate_confidence


def _api_key() -> str:
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("OPENAI_API_KEY is missing")
    return key


def build_criteria_prompt(
    lang_code: str,
    url: str = "",
    prev_context: dict | None = None,
    stable_context: dict | None = None,
    scanner_context: dict | None = None,
) -> str:
    """
    Simplified Phase 1 prompt — only asks for site_type + criteria statuses.
    All business decisions (priority, ROI, difficulty, roadmap) are handled
    deterministically by report_engine.py after this call.
    """
    language = "Turkish" if lang_code == "TR" else "English"
    site_ctx = f"Site being audited: {url}" if url else ""

    site_types_block = "\n".join(
        f'  "{k}": "{v}"' for k, v in SITE_TYPES.items()
    )

    criteria_block = "\n".join(
        f'  "{key}": {{  // [{meta["severity"].upper()}] {meta["tr"]}\n'
        f'    // Hint: {meta["hint"]}\n'
        + (
            f'    // OPTIONAL for site types: {meta["optional_for"]}\n'
            if meta.get("optional_for")
            else ""
        )
        + f'    "status": "PASS" | "PARTIAL" | "FAIL" | "OPTIONAL" | "UNKNOWN",\n'
        f'    "evidence": "one sentence — describe exactly what you see, why it is optional, or why you cannot verify"\n'
        f'  }}'
        for key, meta in CRITERIA.items()
    )

    # Consistency anchor block (stable criteria confirmed across >= 2 analyses)
    stable_block = ""
    if stable_context and len(stable_context) >= 3:
        stable_lines = "\n".join(
            f'  "{k}": "{v}"' for k, v in stable_context.items()
        )
        n_stable = len(stable_context)
        if lang_code == "TR":
            stable_block = f"""

── TUTARLILIK ÇAPASI — {n_stable} ONAYLANMIŞ KRİTER ──────────────────────────────
Bu kriterler bu site için en az 2 ayrı analizde tutarlı sonuç verdi.
Bu sonuçları yalnızca ekran görüntüsünde AÇIK bir değişiklik gördüğünde değiştir.
Emin değilsen, aynı kararı koru — küçük görsel belirsizlik gerekçe sayılmaz.

{stable_lines}

KURAL: Onaylı bir kriteri farklı değerlendiriyorsan, 'evidence' alanında
"Önceki analizde [ESKİ DURUM] idi, şimdi [YENİ DURUM] çünkü [AÇIK KANIT]" yaz.
──────────────────────────────────────────────────────────────────────────────"""
        else:
            stable_block = f"""

── CONSISTENCY ANCHOR — {n_stable} CONFIRMED CRITERIA ──────────────────────────────
These criteria have been confirmed consistently across at least 2 analyses of this site.
Only change them if you clearly see evidence of a change in the screenshot.
When in doubt, keep the same decision — minor visual ambiguity is not grounds for a flip.

{stable_lines}

RULE: If you assess a confirmed criterion differently, write in 'evidence':
"Previous analysis: [OLD STATUS]. Now: [NEW STATUS] because [CLEAR EVIDENCE]."
──────────────────────────────────────────────────────────────────────────────"""

    # Previous analysis context
    prev_block = ""
    if prev_context and prev_context.get("criteria"):
        prev_date = prev_context.get("date", "önceki analiz")
        prev_statuses = "\n".join(
            f'  "{k}": "{v}"' for k, v in prev_context["criteria"].items()
        )
        if lang_code == "TR":
            prev_block = f"""

── GEÇMİŞ ANALİZ BAĞLAMI ({'tarih: ' + prev_date}) ──────────────────────────────
Önceki kriter durumları (yalnızca kriter değerlendirmende referans al):
{prev_statuses}

KURAL: Önceki analizde FAIL/PARTIAL iken şimdi PASS ise, 'evidence' alanında açıkla.
──────────────────────────────────────────────────────────────────────────────────"""
        else:
            prev_block = f"""

── PREVIOUS ANALYSIS CONTEXT (date: {prev_date}) ────────────────────────────────
Previous criterion statuses (use only as reference for your criterion assessment):
{prev_statuses}

RULE: If a criterion was FAIL/PARTIAL before and is now PASS, note the change in 'evidence'.
──────────────────────────────────────────────────────────────────────────────────"""

    # Scanner context (programmatic SEO/Technical findings)
    scanner_block = ""
    if scanner_context and (scanner_context.get("seo") or scanner_context.get("technical")):
        seo_summary = []
        tech_summary = []
        seo_checks = scanner_context.get("seo", {})
        tech_checks = scanner_context.get("technical", {})
        seo_labels  = scanner_context.get("seo_labels", {})
        tech_labels = scanner_context.get("tech_labels", {})
        for key, chk in seo_checks.items():
            s = chk.get("status", "")
            if s in ("FAIL", "PARTIAL"):
                seo_summary.append(f"  [{s}] {seo_labels.get(key, key)}: {chk.get('evidence_tr', '')}")
        for key, chk in tech_checks.items():
            s = chk.get("status", "")
            if s in ("FAIL", "PARTIAL"):
                tech_summary.append(f"  [{s}] {tech_labels.get(key, key)}: {chk.get('evidence_tr', '')}")
        scanner_lines = []
        if seo_summary:
            scanner_lines.append(f"SEO Sorunları ({scanner_context.get('seo_score', '?')}/100):")
            scanner_lines.extend(seo_summary)
        if tech_summary:
            scanner_lines.append(f"Teknik Sorunlar ({scanner_context.get('technical_score', '?')}/100):")
            scanner_lines.extend(tech_summary)
        if scanner_lines:
            sc_text = "\n".join(scanner_lines)
            scanner_block = f"""

── PROGRAMATIK TARAMA SONUÇLARI (teknik olarak doğrulandı) ──────────────────────
{sc_text}
NOT: Bu bulgular HTTP/HTML analizi ile doğrulandı — bu kriter değerlendirmelerini bilgilendirir.
────────────────────────────────────────────────────────────────────────────────"""

    return f"""You are ConvAudit's AI vision engine. {site_ctx}
Your ONLY task is to: (1) identify the site type, and (2) evaluate each criterion based on the screenshot.

Do NOT generate summaries, recommendations, action plans, or any report content.
The report is generated automatically from your criterion evaluations.

── EVIDENCE RULE (MANDATORY) ─────────────────────────────────────────────────
For each criterion, 'evidence' must describe EXACTLY what you see in the screenshot:
  GOOD: "Sayfanın üst alanında yeşil renkli 'Hemen Satın Al' butonu görüyorum, ancak fold altında kalıyor"
  BAD: "CTA butonu eksik" — too generic

Describe: location, text content, color, size, or explicit absence with location context.
Write 'evidence' in {language}.
──────────────────────────────────────────────────────────────────────────────

STEP 1 — DETECT SITE TYPE:
{site_types_block}

Choose the single best match. Write as "site_type" (use the key, e.g. "luxury", "d2c").

STEP 2 — STATUS DEFINITIONS (use exactly one per criterion):
  PASS     = criterion is clearly and fully met (you can see it in the screenshot)
  PARTIAL  = criterion is partially met or present but insufficient
  FAIL     = criterion is clearly absent or broken AND harmful for this site type
  OPTIONAL = intentionally absent due to site type / brand strategy (NOT a bug)
  UNKNOWN  = cannot verify from screenshot alone (element on non-visible page/section)

BRAND-AWARE EVALUATION:
- Luxury brand with no countdown timer → OPTIONAL (deliberate positioning)
- Minimalist premium brand with short copy → PASS for visual_hierarchy
- B2B site with case studies instead of star ratings → OPTIONAL for social_proof
- SaaS with "Contact for pricing" → OPTIONAL for pricing_clear
- D2C homepage with no urgency (urgency on product pages) → UNKNOWN, not FAIL

CRITICAL RULES:
1. Return ONLY valid JSON. No markdown outside JSON.
2. Write ALL 'evidence' fields in {language}.
3. PASS only if you can CLEARLY SEE the element.
4. FAIL only if you can CLEARLY SEE the absence AND it harms this site type.
5. OPTIONAL when the absence is deliberate for this site type.
6. UNKNOWN when the element lives on a page/section not captured.
7. Never use FAIL as a shortcut when OPTIONAL or UNKNOWN is more accurate.
8. Do NOT include any scores in your output — scores are calculated by the backend.

Output schema (return ONLY this, nothing else):
{{
  "site_type": "one of: {', '.join(SITE_TYPES.keys())}",
  "criteria": {{
{criteria_block}
  }}
}}{stable_block}{prev_block}{scanner_block}"""


def build_prompt(lang_code: str, url: str = "", prev_context: dict | None = None, stable_context: dict | None = None, scanner_context: dict | None = None) -> str:
    language = "Turkish" if lang_code == "TR" else "English"
    site_ctx = f"Site being audited: {url}" if url else ""

    # Build site type list for prompt
    site_types_block = "\n".join(
        f'  "{k}": "{v}"' for k, v in SITE_TYPES.items()
    )

    # Build criteria block with optional_for info
    criteria_block = "\n".join(
        f'  "{key}": {{  // [{meta["severity"].upper()}] {meta["tr"]}\n'
        f'    // Hint: {meta["hint"]}\n'
        + (
            f'    // OPTIONAL for site types: {meta["optional_for"]}\n'
            if meta.get("optional_for")
            else ""
        )
        + f'    "status": "PASS" | "PARTIAL" | "FAIL" | "OPTIONAL" | "UNKNOWN",\n'
        f'    "evidence": "one sentence — describe exactly what you see, why it is optional, or why you cannot verify"\n'
        f'  }}'
        for key, meta in CRITERIA.items()
    )

    # Build historical context block
    if prev_context and prev_context.get("criteria"):
        prev_date = prev_context.get("date", "önceki analiz")
        prev_statuses = "\n".join(
            f'  "{k}": "{v}"'
            for k, v in prev_context["criteria"].items()
        )
        if lang_code == "TR":
            prev_block = f"""

── GEÇMİŞ ANALİZ BAĞLAMI ({'tarih: ' + prev_date}) ──────────────────────────────
Bu site daha önce analiz edildi. Aşağıdaki tablo o analizdeki kriter durumlarını göstermektedir.
Bu bilgiyi kullanarak TARİHSEL FARKINDALIKLI bir değerlendirme yap.

Önceki kriter durumları:
{prev_statuses}

BAĞLAMI KULLANMA KURALLARI:
1. "summary" alanında: Önceki analizle karşılaştırarak 1 cümle ekle (ne iyileşti, ne devam ediyor).
2. "critical_issues" listesinde: Önceki analizde de FAIL olan bir kriter hâlâ FAIL ise,
   "problem" alanına " (önceki analizde de tespit edilmişti)" ekle.
3. "quick_wins" listesinde: Birden fazla analizde FAIL veya PARTIAL kalan kriterlere öncelik ver.
4. "executive_hook" alanında: Sorun daha önce de raporlandıysa bunu "tekrarlayan bir sorun" olarak belirt.
5. Bir kriter önceki analizde FAIL/PARTIAL iken şimdi PASS ise, bunu "evidence" alanında açıkça belirt.
──────────────────────────────────────────────────────────────────────────────────────"""
        else:
            prev_block = f"""

── PREVIOUS ANALYSIS CONTEXT (date: {prev_date}) ───────────────────────────────────
This site was previously analyzed. The table below shows criterion statuses from that analysis.
Use this to produce a HISTORICALLY AWARE evaluation.

Previous criterion statuses:
{prev_statuses}

HOW TO USE THIS CONTEXT:
1. In "summary": add 1 sentence comparing today's findings to the previous analysis.
2. In "critical_issues": if a previously-FAIL criterion is still FAIL, append
   " (flagged in previous analysis)" to the "problem" field.
3. In "quick_wins": prioritize criteria that remain FAIL or PARTIAL across analyses.
4. In "executive_hook": if the issue was also flagged before, call it a recurring problem.
5. If a criterion was FAIL/PARTIAL before and is now PASS, explicitly note the improvement in "evidence".
────────────────────────────────────────────────────────────────────────────────────"""
    else:
        prev_block = ""

    # Build CONSISTENCY ANCHOR block from stable criteria (confirmed across >= 2 analyses)
    if stable_context and len(stable_context) >= 3:
        stable_lines = "\n".join(
            f'  "{k}": "{v}"' for k, v in stable_context.items()
        )
        n_stable = len(stable_context)
        if lang_code == "TR":
            stable_block = f"""

── TUTARLILIK ÇAPASI — {n_stable} ONAYLANMIŞ KRİTER ──────────────────────────────
Bu kriterler bu site için en az 2 ayrı analizde tutarlı sonuç verdi.
Bu sonuçları yalnızca ekran görüntüsünde AÇIK bir değişiklik gördüğünde değiştir.
Emin değilsen, aynı kararı koru — küçük görsel belirsizlik gerekçe sayılmaz.

{stable_lines}

KURAL: Onaylı bir kriteri farklı değerlendiriyorsan, 'evidence' alanında
"Önceki analizde [ESKİ DURUM] idi, şimdi [YENİ DURUM] çünkü [AÇIK KANIT]" yaz.
──────────────────────────────────────────────────────────────────────────────"""
        else:
            stable_block = f"""

── CONSISTENCY ANCHOR — {n_stable} CONFIRMED CRITERIA ──────────────────────────────
These criteria have been confirmed consistently across at least 2 analyses of this site.
Only change them if you clearly see evidence of a change in the screenshot.
When in doubt, keep the same decision — minor visual ambiguity is not grounds for a flip.

{stable_lines}

RULE: If you assess a confirmed criterion differently, write in 'evidence':
"Previous analysis: [OLD STATUS]. Now: [NEW STATUS] because [CLEAR EVIDENCE]."
──────────────────────────────────────────────────────────────────────────────"""
    else:
        stable_block = ""

    # Build scanner context block (programmatic SEO/Technical findings)
    if scanner_context and (scanner_context.get("seo") or scanner_context.get("technical")):
        seo_summary   = []
        tech_summary  = []
        seo_checks    = scanner_context.get("seo", {})
        tech_checks   = scanner_context.get("technical", {})
        seo_labels    = scanner_context.get("seo_labels", {})
        tech_labels   = scanner_context.get("tech_labels", {})

        for key, chk in seo_checks.items():
            s = chk.get("status", "")
            if s in ("FAIL", "PARTIAL"):
                label = seo_labels.get(key, key)
                ev    = chk.get("evidence_tr", "")
                seo_summary.append(f"  [{s}] {label}: {ev}")

        for key, chk in tech_checks.items():
            s = chk.get("status", "")
            if s in ("FAIL", "PARTIAL"):
                label = tech_labels.get(key, key)
                ev    = chk.get("evidence_tr", "")
                tech_summary.append(f"  [{s}] {label}: {ev}")

        seo_score  = scanner_context.get("seo_score", "?")
        tech_score = scanner_context.get("technical_score", "?")

        scanner_lines = []
        if seo_summary:
            scanner_lines.append(f"SEO Sorunları (Puan: {seo_score}/100):")
            scanner_lines.extend(seo_summary)
        if tech_summary:
            scanner_lines.append(f"Teknik Sorunlar (Puan: {tech_score}/100):")
            scanner_lines.extend(tech_summary)

        if scanner_lines:
            sc_text = "\n".join(scanner_lines)
            if lang_code == "TR":
                scanner_block = f"""

── PROGRAMATIK TARAMA SONUÇLARI ────────────────────────────────────────────────
Bu bulgular gerçek HTTP ve HTML analizi ile doğrulandı (ekran görüntüsüne dayanmıyor).
Aşağıdaki sorunları action_plan ve critical_issues önerilerinize dahil edin.
Teknik terimleri jargon kurallarına uygun şekilde açıklayın.

{sc_text}

NOT: Bu sorunlar teknik olarak doğrulandı. AI görüşü yerine bu verileri kullanın.
────────────────────────────────────────────────────────────────────────────────"""
            else:
                scanner_block = f"""

── PROGRAMMATIC SCAN RESULTS ────────────────────────────────────────────────────
These findings are verified via real HTTP and HTML analysis (not from the screenshot).
Incorporate these issues into your action_plan and critical_issues recommendations.
Explain technical terms in plain language per the jargon rules.

{sc_text}

NOTE: These issues are technically verified. Use this data, not AI guesswork.
────────────────────────────────────────────────────────────────────────────────"""
        else:
            scanner_block = ""
    else:
        scanner_block = ""

    return f"""You are ConvAudit's AI engine — a professional CRO (Conversion Rate Optimization) and Website Growth Consultant. {site_ctx}
Your role is not to list problems. Your role is to help business owners understand exactly WHY their site loses sales, WHAT to change, HOW to change it (both in business terms and as a developer specification), and WHAT the expected impact will be.

Every finding you produce must answer these questions the business owner is asking:
  → "Bu sorun gerçekten satışımı etkiliyor mu, yoksa detay mı?"
  → "Bunu nasıl düzeltebilirim?"
  → "Bunu ajansıma veya yazılımcıma direkt iletebilir miyim?"
  → "Bu değişikliğin etkisi ne olacak ve ne kadar sürer?"

You are not writing a generic audit report. You are producing a PERSONALIZED GROWTH ROADMAP based on what you observe on this specific website's screenshot, tailored to its site type, brand positioning, and conversion model.

── JARGON-FREE LANGUAGE RULES (MANDATORY) ────────────────────────────────────
Our users are small business owners who have never coded. They do not know technical terms.
You MUST replace all technical jargon with plain language in EVERY text field.
FORBIDDEN → USE INSTEAD (examples, not exhaustive):
  "CTA" → "satın alma butonu" / "harekete geçirici buton"
  "Hero Section" / "hero" → "sayfanın ilk görünen alanı" / "ziyaretçilerin ilk gördüğü alan"
  "LCP" → "sayfanın ana içeriğinin yüklenme süresi"
  "CLS" → "sayfa açılırken içeriklerin yerinden kayması"
  "FCP" → "ilk içeriğin ekranda görünme süresi"
  "Social Proof" → "müşteri yorumları ve referanslar"
  "FOMO" → "kaçırma hissi / aciliyet duygusu"
  "Above the fold" → "kaydırmadan görünen alan"
  "Bounce rate" → "siteyi hemen terk etme oranı"
  "Conversion rate" → "ziyaretçiden müşteriye dönüşüm oranı"
  "A/B test" → "iki farklı versiyon karşılaştırma testi"
  "UGC" → "müşteri fotoğrafları ve yorumları"
  "Trust signals" → "güven unsurları" / "güven göstergeleri"
  "UI/UX" → "tasarım ve kullanım kolaylığı"
  "SEO" → "arama motoru görünürlüğü"
  "Meta description" → "Google'da görünen sayfa açıklaması"
  "Alt text" → "görsel açıklaması"
  "SSL" → "güvenli bağlantı (tarayıcıdaki kilit simgesi)"
  "Carousel" / "slider" → "kayan görsel galerisi"
  "Sticky header" → "yukarı kaydırınca da görünür kalan başlık"
  "Breadcrumb" → "sayfa içinde nerede olduğunuzu gösteren yol"
  "Hamburger menu" → "mobil menü butonu (☰)"
  "Lazy loading" → "görsellerin ihtiyaç duyulduğunda yüklenmesi"
  "Whitespace" → "tasarımdaki nefes alanı / boşluk kullanımı"
  "Favicon" → "tarayıcı sekmesindeki simge"
  "Checkout" → "ödeme adımı / ödeme sayfası"
  "Footer" → "sayfa alt kısmı"
  "Header" → "sayfa başlığı / üst kısım"
  "Pop-up" → "açılır pencere"
  "F-pattern" → "kullanıcıların sayfayı tarama düzeni"
  "CDN" → "içerik hızlandırma sistemi"
  "Cache" → "geçici bellek / hız için önbellek"
  "404" → "bozuk bağlantı / bulunamayan sayfa"
  "Pixel" → "takip kodu"
  "Abandoned cart" → "terk edilen sepet"
  "Push notification" → "anlık bildirim"
  "Heatmap" → "ısı haritası (kullanıcıların tıkladığı yerlerin görsel analizi)"
  "KPI" → "hedef gösterge"
  "ROI" → "yatırım getirisi"
If a technical term has no short alternative, write it in plain Turkish and add a brief explanation.
Write everything as if speaking to a business owner, not a developer. Be warm, direct, and practical.
──────────────────────────────────────────────────────────────────────────────

── PROFESSIONAL CRO ANALYSIS REQUIREMENTS (MANDATORY) ───────────────────────

RULE 1 — SCREENSHOT EVIDENCE (apply to every criterion evaluation):
You MUST describe what you SPECIFICALLY SEE in the screenshot, not what you assume.
  GOOD evidence: "Sayfanın üst alanında '#4CAF50 renk, 'Hemen Satın Al' yazılı bir buton görüyorum — ancak sol alt köşede gizli kalmış ve kıvrımın altında."
  BAD evidence: "CTA butonu eksik" (generic — what do you actually see or not see?)
Never write "generally" or "typically" — write what is OBSERVABLE in THIS screenshot.

RULE 2 — SALES LOSS QUANTIFICATION (apply to every critical_issues and action_plan item):
Every FAIL or PARTIAL must include a specific, research-backed impact estimate.
Use CRO research benchmarks — be specific, not vague:
  GOOD: "Araştırmalar, ödeme sayfasında güven rozeti olmayan sitelerde ziyaretçilerin %17'sinin sepeti terk ettiğini gösteriyor (Baymard Institute, 2023)."
  BAD: "Bu sorun güveni azaltır ve satışları etkiler." (vague — useless)
Reference relevant CRO benchmarks:
  - Baymard Institute: checkout abandonment is 70%% average; main reason is trust
  - Nielsen Norman: users decide in 50ms whether to stay or leave based on visual design
  - Google: 53%% of mobile users abandon sites taking over 3 seconds to load
  - CXL Institute: specific headline improvements can lift conversions 10-30%%
  - General: removing friction from one checkout step increases completion by 5-15%%
Adapt these to the specific site type and the specific problem observed.

RULE 3 — DEVELOPER-READY SPECIFICATION (apply to every action_plan item's dev_spec field):
The dev_spec field must be detailed enough that a developer or agency can implement it WITHOUT follow-up questions.
  GOOD dev_spec: "Ana sayfanın hero bölümünde (<section class='hero'> veya ilk büyük görsel alan) H1 başlığının hemen altına: 'Türkiye'nin en hızlı teslimatı — sipariş bugün, kapında yarın.' yazısı ve 'Şimdi Sipariş Ver' butonunu (#FF5722 arka plan, beyaz yazı, 48px, padding 16px 32px) full-width olarak ekle."
  BAD dev_spec: "Sayfaya bir buton ekleyin." (not actionable)
Always specify: which page/section, which element, exact copy if relevant, visual style hints.

RULE 4 — ROI-FIRST ORDERING (apply to action_plan):
Order action_plan items strictly by ROI = (conversion_impact × effort_ease).
High impact + Easy = first. Low impact + Hard = last.
Add roi_rank (1 = best ROI in this list) to each action_plan item.
──────────────────────────────────────────────────────────────────────────────

STEP 1 — DETECT SITE TYPE:
Before evaluating any criterion, identify the site type from this list:
{site_types_block}

Choose the single best match based on: business model, product type, audience, and design language.
Write your choice as the "site_type" field (use the key, e.g. "luxury", "d2c").

STEP 2 — BRAND-AWARE EVALUATION:
This audit is NOT a one-size-fits-all checklist. Evaluate each criterion in the context of the
detected site type and its brand positioning. Examples of brand-aware judgements:
- A luxury brand with no countdown timer or discount badge is making a deliberate positioning choice → OPTIONAL
- A minimalist premium brand with restrained whitespace and short copy is NOT failing visual hierarchy → PASS
- A B2B site without star ratings is using case studies instead → OPTIONAL for social_proof
- A SaaS site with 'Contact us for pricing' is following an enterprise convention → OPTIONAL for pricing_clear
- A D2C brand with no urgency element on its homepage (but urgency lives on product pages) → UNKNOWN, not FAIL

STEP 3 — STATUS DEFINITIONS (use exactly one per criterion):
  PASS     = criterion is clearly and fully met (you can see the evidence in the screenshot)
  PARTIAL  = criterion is partially met or present but insufficient
  FAIL     = criterion is clearly absent or broken AND its absence harms this site type's conversion
  OPTIONAL = criterion is intentionally absent due to site type / brand strategy
             (not a flaw — a deliberate business or branding choice for this site type)
  UNKNOWN  = you cannot verify this criterion from this screenshot alone
             (element lives in footer, checkout, product page, or area not visible)

CRITICAL RULES:
1. Return ONLY valid JSON. No markdown, no explanation outside JSON.
2. Write ALL "evidence" and narrative fields in {language}.
3. PASS only if you can CLEARLY SEE the element. Do not guess.
4. FAIL only if you can CLEARLY SEE the absence AND it is harmful for this specific site type.
5. OPTIONAL when the absence is intentional for the detected site type (not a bug, a feature).
6. UNKNOWN when an element typically lives on a page/section not captured.
7. Evidence MUST describe what you specifically observe — location, text, color, visual quality.
8. The score is calculated by the backend — do NOT include scores in your output.
9. Never use FAIL as a shortcut when OPTIONAL or UNKNOWN is more accurate.

SEVERITY GUIDE (for critical_issues):
  CRITICAL criteria failures are conversion killers — must fix immediately.
  HIGH criteria failures significantly damage trust or UX.
  MEDIUM/LOW = improvements, not emergencies.

Output schema (follow exactly):
{{
  "site_type": "one of: {', '.join(SITE_TYPES.keys())}",
  "criteria": {{
{criteria_block}
  }},
  "executive_hook": "string — 1 cümle: bu sitenin dönüşüm oranını en çok düşüren TEK sorun; bu siteye ve site türüne özel, jenerik değil",
  "summary": "string — 3-4 cümle: bu sitenin mevcut durumunun somut değerlendirmesi. Ekran görüntüsünde ne görüyorsun, markası ne vaat ediyor, hangi dönüşüm fırsatları kaçırılıyor?",
  "critical_issues": [
    {{
      "problem": "string — Somut sorun: ekran görüntüsünde tam olarak ne görüyorsun? Konum, görsel, metin veya eksik element belirt. JARGON YASAK.",
      "visitor_impact": "string — Tahmini ziyaretçi kaybı: araştırma veya benchmark veriye dayalı tahmin. Örn: 'Baymard Institute araştırmasına göre ödeme güveni eksikliği ziyaretçilerin %%17'sini kaybettiriyor.' GERÇEK VERİ KUL.",
      "why_it_matters": "string — Bu sorunun bu siteye özgü etkisi: satış, güven veya kullanıcı deneyimi açısından somut etki. Rakam veya yüzde içersin.",
      "impact": "High | Medium | Low",
      "solution": "string — İş sahibinin anlayacağı çözüm özeti: 1-2 cümle, jargonsuz, somut.",
      "dev_spec": "string — Geliştirici/ajans için teknik talimat: hangi sayfa/bölüm/element, tam ne değişmeli, varsa örnek metin/renk/boyut. Geliştiricinin ek soru sormadan uygulayabileceği kadar detaylı.",
      "steps": ["string — adım 1: iş sahibinin yapabileceği + geliştirici talimatını içeren net adım", "string — adım 2", "string — adım 3"],
      "example": "string — varsa: örnek başlık, buton metni, kopya veya element açıklaması",
      "difficulty": "Kolay | Orta | Zor",
      "time_estimate": "string — 1 gün | 2–3 gün | 1 hafta | 2 hafta | 1 ay+"
    }}
  ],
  "quick_wins": [
    {{
      "action": "string — 14 günde uygulanabilir spesifik görev; bu site türüne ve mevcut duruma özel",
      "expected_result": "string — tahmini etki, yüzde içersin ve benchmark veriye dayalı olsun"
    }}
  ],
  "action_plan": [
    {{
      "roi_rank": 1,
      "title": "string — eylem fiiliyle başla, max 8 kelime, JARGON YASAK",
      "problem_context": "string — bu aksiyon hangi gözlemlenebilir sorunu çözüyor? 1 cümle, iş sahibine hitap et, ekran görüntüsüne özel.",
      "what_to_do": "string — iş sahibine yönelik açıklama: ne yapılması gerekiyor, 1-2 cümle, jargonsuz.",
      "dev_spec": "string — geliştiriciye/ajansa direkt iletilebilecek teknik talimat: hangi sayfa, hangi element/bölüm, tam ne değişmeli. 2-3 cümle.",
      "why_priority": "string — neden bu öncelikli? Satış/büyüme etkisini somut bir rakamla belirt.",
      "priority": "Kritik | Yüksek | Orta | Düşük",
      "difficulty": "Kolay | Orta | Zor",
      "impact": "Yüksek | Orta | Düşük",
      "conversion_lift": "string — benchmark'a dayalı tahmini dönüşüm artışı, örn +5%%–12%%",
      "time_estimate": "string — 1 gün | 2–3 gün | 1 hafta | 2 hafta | 1 ay+",
      "category": "UX | Güven | Performans | İçerik | Teknik | SEO",
      "steps": ["string — adım 1: geliştiricinin uygulayabileceği kadar net", "string — adım 2", "string — adım 3"]
    }}
  ],
  "top_priority_action": {{
    "title": "string — bu haftaki en yüksek ROI'li tek aksiyon; eylem fiiliyle başla",
    "owner_instructions": "string — iş sahibinin kendisi yapabileceği şey (teknik bilgi gerektirmez): adım adım, 2-3 cümle",
    "dev_instructions": "string — geliştiriciye/ajansa iletilecek tam teknik talimat: hangi dosya/sayfa/element, tam değişiklik, varsa örnek kod/metin",
    "expected_impact": "string — bu değişikliğin ilk 2 haftada yaratacağı somut etki tahmini"
  }},
  "growth_strategy": [
    {{
      "idea": "string — bu site türüne ve gözlemlenen duruma özel büyüme fikri",
      "reason": "string — neden bu firsatta büyüme potansiyeli var?",
      "expected_impact": "string — tahmini etki, mümkünse yüzde veya rakamla"
    }}
  ],
  "psychology_triggers": [
    "string — psikoloji prensibi adı: sitede ne eksik + bu siteye özgü nasıl eklenir + tahmini dönüşüm artışı"
  ],
  "experiment_backlog": [
    {{
      "test": "string — test adı",
      "hypothesis": "string — eğer X yapılırsa Y olur çünkü Z (bu siteye özel)",
      "metric": "string — ölçülecek hedef gösterge",
      "expected_lift": "string — tahmini artış, örn +4%%–9%%"
    }}
  ],
  "roadmap_30_60_90": {{
    "day_30": ["string — 30 günde tamamlanacak somut, uygulanabilir görev"],
    "day_60": ["string — 60 günde tamamlanacak somut, uygulanabilir görev"],
    "day_90": ["string — 90 günde tamamlanacak somut, uygulanabilir görev"]
  }},
  "revenue_note": "string — 1 cümle: bu site için en yüksek ROI sağlayacak TEK değişiklik nedir?",
  "impact": {{
    "improvement_range": "string — bu analizden çıkan iyileştirmelerin tahmini toplam dönüşüm artışı aralığı",
    "priority_focus": "string — 1 cümle: bu sitede büyümenin önündeki en büyük engel"
  }}
}}

Limits: critical_issues max 5, quick_wins max 3, action_plan max 8, growth_strategy max 4,
psychology_triggers max 4, experiment_backlog max 4, day_30/60/90 max 3 each.
Only include critical_issues for FAIL or PARTIAL criteria — never for OPTIONAL, UNKNOWN, or PASS.
action_plan MUST be ordered by ROI (roi_rank 1 = highest return + easiest to implement first).
roi_rank values must be unique integers from 1 to N (where N is the number of action_plan items).
Each action_plan item MUST address a specific FAIL or PARTIAL criterion or clearly observable problem.
action_plan steps: max 3 per item, concrete and developer-executable.
dev_spec in both critical_issues and action_plan MUST be specific enough that a developer can implement it without follow-up questions.
visitor_impact in critical_issues MUST reference a specific CRO research finding or industry benchmark.
Tailor ALL recommendations to the detected site type and its brand positioning.
{stable_block}{prev_block}{scanner_block}"""


def analyze_site(url: str, lang_code: str):
    client = OpenAI(api_key=_api_key())
    shot_path, img_b64 = capture_website(url)
    prompt = build_prompt(lang_code, url)

    user_text = (
        f"Bu sayfayı ({url}) denetle. Önce site türünü tespit et, ardından her kriteri "
        f"marka stratejisini göz önünde bulundurarak değerlendir. Yalnızca JSON döndür."
        if lang_code == "TR"
        else f"Audit this page ({url}). First detect the site type, then evaluate every criterion "
             f"considering the brand strategy. Return only JSON."
    )

    response = client.chat.completions.create(
        model=MODEL_NAME,
        temperature=0,
        messages=[
            {"role": "system", "content": prompt},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": user_text},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64,{img_b64}"},
                    },
                ],
            },
        ],
        max_tokens=4000,
        response_format={"type": "json_object"},
    )

    raw = response.choices[0].message.content
    data = json.loads(raw)

    criteria_results = data.get("criteria", {})
    data["scores"]     = calculate_score(criteria_results)
    data["confidence"] = calculate_confidence(criteria_results)
    data["site_type"]  = data.get("site_type", "other")
    data["criteria"]   = criteria_results

    return json.dumps(data, ensure_ascii=False), shot_path

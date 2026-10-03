import os
import re
from fpdf import FPDF

from config.languages import LANGS


class AuditPDF(FPDF):
    def __init__(self, lang_config):
        super().__init__()
        self.l = lang_config

    def header(self):
        self.set_fill_color(16, 22, 36)
        self.rect(0, 0, 210, 38, "F")
        self.set_xy(15, 13)
        self.set_font("Arial", "B", 18)
        self.set_text_color(0, 230, 170)
        self.cell(100, 10, "CONVAUDIT AI PRO", ln=0)
        self.set_font("Arial", "I", 9)
        self.set_text_color(255, 255, 255)
        self.cell(80, 10, self.l["pdf_sub_title"], align="R", ln=1)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(140, 140, 140)
        self.cell(0, 10, f"{self.l['pdf_page']} {self.page_no()}", align="C")


def fix_pdf_text(text):
    if not text:
        return ""

    rep = {
        "İ": "I", "ı": "i", "Ş": "S", "ş": "s",
        "Ğ": "G", "ğ": "g", "Ü": "U", "ü": "u",
        "Ö": "O", "ö": "o", "Ç": "C", "ç": "c"
    }

    for s, r in rep.items():
        text = text.replace(s, r)

    return text.encode("latin-1", "replace").decode("latin-1")


def create_pdf(report_text, screenshot_path, lang_code):
    l = LANGS[lang_code]

    def extract_score(tag):
        match = re.search(rf"{tag}_SCORE:\s*([\d\.]+)", report_text)
        return match.group(1) if match else "8.0"

    pdf = AuditPDF(l)
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    labels = [l["ux"], l["speed"], l["trust"]]
    vals = [extract_score("UX"), extract_score("SPEED"), extract_score("TRUST")]

    pdf.set_xy(15, 50)
    for i in range(3):
        x_pos = 15 + (i * 63)
        pdf.set_fill_color(245, 247, 250)
        pdf.rect(x_pos, 50, 58, 24, "F")
        pdf.set_xy(x_pos, 54)
        pdf.set_font("Arial", "B", 8)
        pdf.set_text_color(110, 110, 110)
        pdf.cell(58, 5, fix_pdf_text(labels[i]), align="C", ln=True)
        pdf.set_font("Arial", "B", 14)
        pdf.set_text_color(0, 150, 110)
        pdf.set_x(x_pos)
        pdf.cell(58, 10, f"{vals[i]} / 10", align="C")

    if os.path.exists(screenshot_path):
        pdf.ln(24)
        pdf.image(screenshot_path, x=15, w=180)
        pdf.ln(115)

    pdf.set_font("Arial", "B", 14)
    pdf.set_text_color(20, 20, 20)
    pdf.cell(0, 10, fix_pdf_text(l["pdf_main_title"]), ln=True)
    pdf.ln(2)

    clean_text = re.sub(r"(UX|SPEED|TRUST)_SCORE:\s*[\d\.]+", "", report_text).strip()
    clean_text = clean_text.replace("**", "")
    clean_text = clean_text.replace("#", "")
    clean_text = clean_text.replace("📊", "")
    clean_text = clean_text.replace("🛑", "")
    clean_text = clean_text.replace("💡", "")
    clean_text = clean_text.replace("✅", "")
    clean_text = clean_text.replace("✔", "")

    pdf.set_font("Arial", "", 10.5)
    pdf.set_text_color(40, 40, 40)

    for line in clean_text.split("\n"):
        safe_line = fix_pdf_text(line).strip()

        if not safe_line:
            continue

        safe_line = safe_line.replace("•", "-")
        safe_line = safe_line.replace("—", "-")
        safe_line = safe_line.replace("–", "-")
        safe_line = safe_line.replace("\t", " ")

        try:
            pdf.multi_cell(180, 6, safe_line)
        except Exception:
            continue

    path = l["pdf_file_name"]
    pdf.output(path)
    return path
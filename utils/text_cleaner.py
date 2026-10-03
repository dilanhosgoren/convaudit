import re


def clean_report_text(report_text):
    return re.sub(r"(UX|SPEED|TRUST)_SCORE:\s*[\d\.]+", "", report_text).strip()
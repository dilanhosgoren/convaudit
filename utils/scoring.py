import re


def extract_numeric_score(tag, report_text):
    match = re.search(rf"{tag}_SCORE:\s*([\d\.]+)", report_text)
    return float(match.group(1)) if match else 8.0
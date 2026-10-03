import base64
from playwright.sync_api import sync_playwright

def capture_website(url: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": 1440, "height": 900})

        full_url = url if url.startswith("http") else f"https://{url}"
        page.goto(full_url, wait_until="domcontentloaded", timeout=50000)
        page.wait_for_timeout(3000)

        shot_path = "shot.png"
        page.screenshot(path=shot_path, full_page=True)

        with open(shot_path, "rb") as f:
            img_b64 = base64.b64encode(f.read()).decode("utf-8")

        browser.close()
        return shot_path, img_b64
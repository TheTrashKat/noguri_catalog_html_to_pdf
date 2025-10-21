from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto("file:///D:/proyecto/GIT/noguri_catalog_html_to_pdf/index.html")
    page.pdf(path="salida.pdf", format="A4", print_background=True)
    page.screenshot(path="1.png", full_page=True)
    browser.close()
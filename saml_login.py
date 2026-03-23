from playwright.sync_api import sync_playwright
import time

def perform_saml_login(app_homepage_url, expected_auth_url):
    """
    Perform SAML login using Playwright and return captured cookies.

    Args:
        app_homepage_url (str): The URL to navigate to for login.

    Returns:
        list: A list of cookies captured after login.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # importante: no headless
        context = browser.new_context()
        page = context.new_page()

        print("➡️ Abriendo login...")
        page.goto(app_homepage_url)

        print("⏳ Esperando que completes el login SAML en el browser...")

        # Esperar hasta que la URL sea la del sitio autenticado
        page.wait_for_url(expected_auth_url, timeout=300000)  # 5 minutos

        print("✅ Login detectado!")

        # Opcional: pequeña espera para asegurar cookies
        time.sleep(2)

        # Obtener cookies del contexto
        cookies = context.cookies()

        print("🍪 Cookies capturadas:")
        for c in cookies:
            print(f"{c['name']} = {c['value']}")

        browser.close()

    return cookies
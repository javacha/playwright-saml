from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
from playwright._impl._errors import Error as PlaywrightError
import time

def perform_saml_login(app_homepage_url, expected_auth_url):
    """
    Perform SAML login using Playwright and return captured cookies.

    Args:
        app_homepage_url (str): The URL to navigate to for login.
        expected_auth_url (str): The expected URL after successful login.

    Returns:
        list: A list of cookies captured after login, or None if login fails.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # importante: no headless
        context = browser.new_context()
        page = context.new_page()

        print("➡️ Abriendo login...")
        try:
            page.goto(app_homepage_url)
        except PlaywrightError as e:
            if "net::ERR_CONNECTION_REFUSED" in str(e):
                print("❌ Error: No se pudo conectar al proveedor de servicios. Verifica que el servidor esté en ejecución.")
            else:
                print(f"❌ Error inesperado al intentar abrir la página: {e}")
                
            return None  # Exit early if the page cannot be loaded

        print("⏳ Esperando que completes el login SAML en el browser...")

        try:
            # Wait until the URL matches the expected authenticated URL
            page.wait_for_url(expected_auth_url, timeout=300000)  # 5 minutos
            print("✅ Login detectado!")

            # Optional: small delay to ensure cookies are set
            time.sleep(2)

            # Get cookies from the context
            cookies = context.cookies()

            print("🍪 Cookies capturadas:")
            for c in cookies:
                print(f"{c['name']} = {c['value']}")

        except PlaywrightTimeoutError:
            print("❌ Error: El tiempo de espera para el login ha expirado.")
            cookies = None  # Return None to indicate failure

        except PlaywrightError:
            print("❌ Error: El navegador o la página se cerró antes de completar el login.")
            cookies = None  # Return None to indicate failure

        finally:
            try:
                browser.close()
            except PlaywrightError:
                print("⚠️ El navegador ya estaba cerrado.")

    return cookies
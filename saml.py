from playwright.sync_api import sync_playwright
import requests
import time
from requests.cookies import create_cookie


 # URL final post-login
TARGET_URL = "http://localhost:5000/app"
API_ENDPOINT = "http://localhost:5000/api/data"

def main():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # importante: no headless
        context = browser.new_context()
        page = context.new_page()

        print("➡️ Abriendo login...")
        page.goto(TARGET_URL)

        print("⏳ Esperando que completes el login SAML en el browser...")

        # Esperar hasta que la URL sea la del sitio autenticado
        page.wait_for_url("**/app", timeout=300000)  # 5 minutos

        print("✅ Login detectado!")

        # Opcional: pequeña espera para asegurar cookies
        time.sleep(2)

        # Obtener cookies del contexto
        cookies = context.cookies()

        print("🍪 Cookies capturadas:")
        for c in cookies:
            print(f"{c['name']} = {c['value']}")

        browser.close()

    # Convertir cookies a formato requests
    session = requests.Session()

    for c in cookies:
        cookie = create_cookie(
            name=c['name'],
            value=c['value'],
            path=c['path']
        )
    session.cookies.set_cookie(cookie)


    print("➡️ Consumiento API con cookies...")

    response = session.get(API_ENDPOINT)

    print("Status:", response.status_code)
    print("Response:", response.text)


if __name__ == "__main__":
    main()
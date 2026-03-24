from saml_login import perform_saml_login
from requests.cookies import create_cookie
import requests

# URL final post-login
TARGET_URL = "http://localhost:5000/app"
EXPECTED_AUTH_URL = "**/app"
API_ENDPOINT = "http://localhost:5000/api/data" 

def main():
    print("➡️ Iniciando programa principal...")

    # Perform SAML login and capture cookies
    cookies = perform_saml_login(TARGET_URL, EXPECTED_AUTH_URL)

    if not cookies:
        print("❌ Error: El login SAML no se completó correctamente.")
        return  # Exit the program if login fails

    # Convert cookies to requests format
    session = requests.Session()
    for c in cookies:
        cookie = create_cookie(
            name=c['name'],
            value=c['value'],
            path=c['path']
        )
        session.cookies.set_cookie(cookie)

    print("➡️ Consumiento API con cookies...")

    # Make API request with cookies
    response = session.get(API_ENDPOINT)

    print("Status:", response.status_code)
    print("Response:", response.text)

if __name__ == "__main__":
    main()
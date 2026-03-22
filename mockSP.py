# sp.py
from flask import Flask, request, redirect, make_response
import base64

app = Flask(__name__)

SESSION_COOKIE = "mock_session"


@app.route("/app")
def app_home():
    session = request.cookies.get(SESSION_COOKIE)

    if not session:
        # Redirige al IdP
        return redirect(
            "http://localhost:5001/login?RelayState=http://localhost:5000/assert"
        )

    return f"""
    <h2>Bienvenido!</h2>
    <p>Usuario autenticado: {session}</p>
    """


@app.route("/assert")
def assert_saml():
    saml_response = request.args.get("SAMLResponse")

    if not saml_response:
        return "Error: no SAMLResponse", 400

    decoded = base64.b64decode(saml_response).decode()
    user = decoded.split(":")[1]

    resp = make_response(redirect("/app"))
    resp.set_cookie(SESSION_COOKIE, user)

    return resp


@app.route("/api/data")
def api_data():
    session = request.cookies.get(SESSION_COOKIE)

    if not session:
        return {"error": "unauthorized"}, 401

    return {"message": f"Hola {session}, data segura!"}


if __name__ == "__main__":
    app.run(port=5000, debug=True)
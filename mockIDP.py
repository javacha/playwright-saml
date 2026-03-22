# idp.py
from flask import Flask, request, redirect, render_template_string
import base64

app = Flask(__name__)

LOGIN_FORM = """
<h2>Mock IdP Login</h2>
<form method="post">
  Usuario: <input name="username"><br>
  Password: <input name="password" type="password"><br>
  <button type="submit">Login</button>
</form>
"""

@app.route("/login", methods=["GET", "POST"])
def login():
    relay_state = request.args.get("RelayState")

    if request.method == "POST":
        username = request.form.get("username")

        # "SAMLResponse" fake (base64)
        saml_response = base64.b64encode(f"user:{username}".encode()).decode()

        return redirect(f"{relay_state}?SAMLResponse={saml_response}")

    return render_template_string(LOGIN_FORM)


if __name__ == "__main__":
    app.run(port=5001, debug=True)
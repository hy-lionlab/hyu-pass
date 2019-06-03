from flask import render_template
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash
from baro import app


auth = HTTPBasicAuth()
users = {
    app.config["ADMIN_USERNAME"]: generate_password_hash(app.config["ADMIN_PASSWORD"])
}


@auth.verify_password
def verify_password(username, password):
    if username in users:
        return check_password_hash(users.get(username), password)
    return False


@app.route("/admin")
@auth.login_required
def index():
    return render_template("index.html")

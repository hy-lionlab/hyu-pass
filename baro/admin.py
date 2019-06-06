from flask import render_template, jsonify, make_response, request
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash
from baro import app, db
from baro.models import Request, Url


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
def admin():
    return render_template("index.html")


# TODO: 개발시 auth.login_required 할 경우 CORS Not Applying
@app.route("/admin/api/requests", methods=["GET"])
def admin_requests():
    requests = Request.query.order_by(desc(Request.created_at)).all()
    return make_response(jsonify(requests=Request.serialize_list(requests)))


# TODO: 개발시 auth.login_required 할 경우 CORS Not Applying
@app.route("/admin/api/keywords", methods=["GET", "POST"])
def admin_keywords():
    if request.method == "GET":
        keywords = Url.query.order_by(desc(Url.created_at)).all()
        return make_response(jsonify(keywords=Url.serialize_list(keywords)))

    if request.method == "POST":
        args = request.get_json(silent=True)

        keyword = Url(args["keyword"], args["url"], "", "")
        db.session.add(keyword)
        db.session.commit()

        return make_response(jsonify({"message": "키워드 생성을 완료했습니다."}), 201)

    return make_response(None, 200)

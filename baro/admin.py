from flask import render_template, jsonify, make_response, request
from flask_classful import FlaskView, route
from flask_httpauth import HTTPBasicAuth
from sqlalchemy import desc
from werkzeug.security import generate_password_hash, check_password_hash

from baro import app, db, email
from baro.models import Request, Url, Support


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
@app.route("/admin/requests")
@app.route("/admin/keywords")
@app.route("/admin/supports")
@auth.login_required
def admin():
    return render_template("index.html")


# TODO: 개발시 auth.login_required 할 경우 CORS Not Applying
class AdminKeywordView(FlaskView):
    route_base = "keywords"
    route_prefix = "/admin/api/"

    def index(self):
        keywords = Url.query.order_by(desc(Url.created_at)).all()
        return make_response(jsonify(keywords=Url.serialize_list(keywords)))

    def post(self):
        args = request.get_json(silent=True)

        keyword = Url(args["keyword"], args["url"], args["title"], args["description"])
        db.session.add(keyword)
        db.session.commit()

        return make_response(jsonify({"message": "키워드 생성을 완료했습니다."}), 201)

    @route("/<id>", methods=["POST"])
    def update(self, id):
        args = request.get_json(silent=True)

        url = Url.query.get(id)
        url.keyword = args["keyword"]
        url.url = args["url"]
        url.title = args["title"]
        url.description = args["description"]

        db.session.commit()

        return make_response(jsonify({"message": "수정을 완료했습니다."}), 200)

    @route("/active/status", methods=["POST"])
    def change_active_status(self):
        args = request.get_json(silent=True)

        keyword = Url.query.get(args["id"])
        keyword.is_active = bool(args["is_active"])

        db.session.commit()

        return make_response(jsonify({"message": "활성화 상태를 변경했습니다."}), 200)


# TODO: 개발시 auth.login_required 할 경우 CORS Not Applying
class AdminRequestView(FlaskView):
    route_base = "requests"
    route_prefix = "/admin/api/"

    def index(self):
        requests = Request.query.order_by(desc(Request.created_at)).all()
        return make_response(jsonify(requests=Request.serialize_list(requests)))

    @route("/approve/", methods=["POST"])
    def approve(self):
        args = request.get_json(silent=True)

        request_obj = Request.query.get(args["id"])
        request_obj.is_approved = True
        request_obj.disapproved_reason = None

        keyword = Url(
            request_obj.keyword,
            request_obj.url,
            request_obj.title,
            request_obj.description,
        )

        db.session.add(keyword)
        db.session.commit()

        # 승인 결과 메일 발송
        html_string = render_template(
            "email/approved.html",
            keyword=request_obj.keyword,
            name=request_obj.name,
            url=request_obj.url,
            created_at=keyword.created_at,
        )
        email.send_email(
            request_obj.email, "[한양 하이패스] 신청하신 단축 주소가 승인되었습니다.", html_string
        )

        return make_response(jsonify({"message": "승인 처리를 완료했습니다."}), 200)

    @route("/disapprove/", methods=["POST"])
    def disapprove(self):
        args = request.get_json(silent=True)

        request_obj = Request.query.get(args["id"])
        request_obj.is_approved = False
        request_obj.disapproved_reason = args["disapproved_reason"]

        db.session.commit()

        # 반려 결과 메일 발송
        html_string = render_template(
            "email/disapproved.html",
            keyword=request_obj.keyword,
            reason=args["disapproved_reason"],
            created_at=request_obj.created_at,
        )
        email.send_email(request_obj.email, "[한양 하이패스] 신청하신 단축 주소 반려 안내", html_string)

        return make_response(jsonify({"message": "반려 처리를 완료했습니다."}), 200)


# TODO: 개발시 auth.login_required 할 경우 CORS Not Applying
class AdminSupportView(FlaskView):
    route_base = "supports"
    route_prefix = "/admin/api/"

    def index(self):
        supports = Support.query.order_by(desc(Support.created_at)).all()
        return make_response(jsonify(supports=Support.serialize_list(supports)))


AdminKeywordView.register(app)
AdminRequestView.register(app)
AdminSupportView.register(app)

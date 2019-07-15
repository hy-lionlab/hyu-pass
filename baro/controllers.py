import os
import geoip2.errors
import geoip2.database
import fnmatch

from sqlalchemy import exc, desc
from flask import render_template, request, jsonify, make_response, redirect, send_file
from flask_classful import FlaskView, route

from baro import app, db, email, qrcode
from baro.models import Request, Url, Log, Support


def get_reserved_keywords():
    return ["list", "list*", "make", "make*", "admin", "admin*", "change", "change*"]


def get_country_code(ip_address):
    try:
        dirname = os.path.dirname(__file__)
        filename = os.path.join(dirname, "../resources/GeoLite2-Country.mmdb")

        reader = geoip2.database.Reader(filename)
        response = reader.country(ip_address)

        return response.country.iso_code.lower()
    except geoip2.errors.AddressNotFoundError:
        return None


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    # ROOT PATH 접근 시 Redirect
    if not path:
        return redirect(app.config["MAIN_REDIRECT_PAGE"])

    # 등록된 Keywords 확인 - Redirect 302
    url_obj = Url.query.filter(Url.keyword == path and Url.deleted_at.is_(None)).first()
    if url_obj and url_obj.is_active:
        url_obj.hit_count = int(url_obj.hit_count) + 1

        try:
            headers_list = request.headers.getlist("X-Forwarded-For")
            user_ip = headers_list[0] if headers_list else request.remote_addr
            referrer = request.headers.get("Referer")
            user_agent = request.headers.get("User-Agent")
            country_code = get_country_code(user_ip)

            log = Log(url_obj.id, referrer, user_agent, user_ip, country_code)

            db.session.add(log)
            db.session.commit()
        except exc.SQLAlchemyError:
            pass

        return redirect(url_obj.url)

    # 등록된 키워드 X + NO ROOT PATH + RESERVED KEYWORDS X
    return redirect("/sorry")


@app.route("/qrcode", methods=["GET"])
def get_qrcode():
    data = request.args.get("data", "")

    return send_file(
        qrcode(data, mode="raw", error_correction="H"),
        mimetype="image/png",
        attachment_filename="qrcode.png",
        as_attachment=True,
    )


@app.route("/sorry")
@app.route("/list")
@app.route("/make")
@app.route("/change")
def index():
    return render_template("index.html")


class SupportView(FlaskView):
    route_base = "supports"
    route_prefix = "/api/"

    def post(self):
        args = request.get_json(silent=True)

        support = Support(
            args["keyword"],
            args["url"],
            args["email"] + "@hanyang.ac.kr",
            args["description"],
            request.remote_addr,
        )
        db.session.add(support)
        db.session.commit()

        # 문의 접수 메일 발송
        html_string = render_template(
            "email/change.html",
            keyword=args["keyword"],
            description=args["description"],
            email=args["email"],
            url=args["url"],
            created_at=support.created_at,
        )
        email.send_email(
            [args["email"] + "@hanyang.ac.kr", app.config["EMAIL_FROM"]],
            "[한양 하이패스] 문의가 접수되었습니다.",
            html_string,
        )

        return make_response(jsonify({"message": "문의 접수가 되었습니다."}), 201)


class KeywordView(FlaskView):
    route_base = "keywords"
    route_prefix = "/api/"

    def index(self):
        keywords = Url.query.order_by(desc(Url.created_at)).all()
        return make_response(jsonify(keywords=Url.serialize_list(keywords)))

    def post(self):
        args = request.get_json(silent=True)

        keyword = Request(
            args["keyword"],
            args["url"],
            args["title"],
            args["description"],
            args["person_type"],
            args["email"] + "@hanyang.ac.kr",
            args["name"],
            args["group"],
            request.remote_addr,
        )
        db.session.add(keyword)
        db.session.commit()

        # 신청 완료 메일 발송
        html_string = render_template(
            "email/requested.html",
            keyword=args["keyword"],
            title=args["title"],
            name=args["name"],
            email=args["email"],
            url=args["url"],
            created_at=keyword.created_at,
        )
        email.send_email(
            [args["email"] + "@hanyang.ac.kr", app.config["EMAIL_FROM"]],
            "[한양 하이패스] 신청하신 단축 주소가 접수되었습니다.",
            html_string,
        )

        return make_response(jsonify({"message": "키워드 신청을 완료했습니다."}), 201)

    @route("/check/")
    def check(self):
        keyword = request.args.get("q")

        # / 비허용
        if '/' in keyword:
            return make_response("", 400)

        # 예약 키워드 등록 불가
        for reserved_keyword in get_reserved_keywords():
            if fnmatch.fnmatch(keyword, reserved_keyword):
                return make_response("", 400)

        query = Url.query.filter(Url.keyword == keyword).exists()
        if db.session.query(query).scalar():
            return make_response("", 400)

        return make_response("", 200)


SupportView.register(app)
KeywordView.register(app)


@app.errorhandler(Exception)
def catch_error(e):
    if app.config["DEBUG"]:
        return e

    return make_response(jsonify({"message": e.message}), e.code)

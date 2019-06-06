import os
import geoip2.errors
import geoip2.database

from sqlalchemy import exc
from flask import render_template, request, jsonify, make_response, redirect
from flask_classful import FlaskView, route

from baro import app, db
from baro.models import Request, Url, Log


def get_reserved_keywords():
    return []


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
        return redirect(app.confg("MAIN_REDIRECT_PAGE"))

    # 등록된 Keywords 확인 - Redirect 302
    url_obj = Url.query.filter(Url.keyword == path and Url.deleted_at.is_(None)).first()
    if url_obj:
        url_obj.hit_count = int(url_obj.hit_count) + 1

        try:
            remote_addr = request.remote_addr
            referrer = request.headers.get("Referer")
            user_agent = request.headers.get("User-Agent")
            country_code = get_country_code(remote_addr)

            log = Log(url_obj.id, referrer, user_agent, remote_addr, country_code)

            db.session.add(log)
            db.session.commit()
        except exc.SQLAlchemyError:
            pass

        return redirect(url_obj.url)

    # 등록된 키워드 X + NO ROOT PATH + RESERVED KEYWORDS X
    return redirect("/sorry")


@app.route("/sorry")
@app.route("/keywords")
@app.route("/requests")
@app.route("/supports")
def index():
    return render_template("index.html")


class KeywordView(FlaskView):
    route_base = "keywords"
    route_prefix = "/api/"

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

        return make_response(jsonify({"message": "키워드 신청을 완료했습니다."}), 201)

    @route("/check/")
    def check(self):
        keyword = request.args.get("q")

        # TODO: Reserved Keywords 가 있는지 체크
        if keyword in get_reserved_keywords():
            return make_response("", 400)

        query = Url.query.filter(Url.keyword == keyword).exists()
        if db.session.query(query).scalar():
            return make_response("", 400)

        return make_response("", 200)


KeywordView.register(app)


# FIXME: 개발 완료 시 해제
# @app.errorhandler(Exception)
# def catch_error(e):
#     return make_response(jsonify({"message": e.message}), e.code)

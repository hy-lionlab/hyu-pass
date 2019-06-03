from flask import render_template, request, jsonify, make_response, redirect
from sqlalchemy import and_
from baro import app, db
from baro.models import Request, Url


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
    return render_template("index.html")


@app.route("/keywords/check")
def keywords_check():
    if request.method == "GET":
        keyword = request.args.get("q")

        query = Url.query.filter(
            and_(Url.keyword == keyword, Url.deleted_at.isnot(None))
        ).exists()

        if db.session.query(query).scalar():
            return make_response("", 400)

        return make_response("", 200)

    return redirect("/")


@app.route("/keywords")
def keywords():
    if request.method == "POST":
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

    return redirect("/")


@app.errorhandler(Exception)
def catch_error(e):
    return make_response(jsonify({"message": e.message}), e.code)

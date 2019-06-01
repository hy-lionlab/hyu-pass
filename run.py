from flask import Flask, render_template
from flask_dotenv import DotEnv

app = Flask(__name__, static_folder="./app/dist/static", template_folder="./app/dist")
env = DotEnv(app)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def main(path):
    return render_template("index.html")


if __name__ == "__main__":
    app.run()

import os
import jinja2

from flask import Flask
from flask_cors import CORS
from flask_dotenv import DotEnv
from flask_qrcode import QRcode
from flask_wtf.csrf import CSRFProtect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="../app/dist/static")
app.url_map.strict_slashes = False

dist = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../app/dist")

jinja_loader = jinja2.ChoiceLoader([app.jinja_loader, jinja2.FileSystemLoader(dist)])
app.jinja_loader = jinja_loader

csrf = CSRFProtect(app)
env = DotEnv(app)
db = SQLAlchemy(app)
qrcode = QRcode(app)

import os
import rollbar
import rollbar.contrib.flask
from flask import got_request_exception


@app.before_first_request
def init_rollbar():
    """init rollbar module"""
    rollbar.init(
        app.config["ROLLBAR_TOKEN"],
        "debug" if app.config["DEBUG"] else "production",
        root=os.path.dirname(os.path.realpath(__file__)),
        allow_logging_basic_config=False,
    )

    got_request_exception.connect(rollbar.contrib.flask.report_exception, app)


# 디버그 모드일 경우 CORS 허용 및 CSRF CHECK EXEMPT
if app.config["DEBUG"]:
    CORS(app, supports_credentials=True)
    app.config["WTF_CSRF_CHECK_DEFAULT"] = False

# 디버그 모드에서 CSRF CHECK EXEMPT 처리를 위해 Handle
@app.before_request
def check_csrf():
    if not app.config["DEBUG"]:
        csrf.protect()


from baro import controllers, models, admin

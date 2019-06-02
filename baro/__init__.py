from flask import Flask
from flask_wtf.csrf import CSRFProtect
from flask_cors import CORS
from flask_dotenv import DotEnv
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_folder="../app/dist/static", template_folder="../app/dist")
csrf = CSRFProtect(app)
env = DotEnv(app)
db = SQLAlchemy(app)

# 디버그 모드일 경우 CORS 허용 및 CSRF CHECK EXEMPT
if app.debug:
    CORS(app)
    app.config["WTF_CSRF_CHECK_DEFAULT"] = False

# 디버그 모드에서 CSRF CHECK EXEMPT 처리를 위해 Handle
@app.before_request
def check_csrf():
    if not app.debug:
        csrf.protect()


from baro import controllers, models

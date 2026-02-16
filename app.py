from flask import Flask
from flask_cors import CORS
from models import CleanHistory, User  # noqa: F401
from routes.auth_route import auth_bp
from routes.clean_route import clean_bp
from routes.download_route import download_bp
from routes.history_route import history_bp
from services.db import db
import os
from urllib.parse import quote_plus
from werkzeug.middleware.proxy_fix import ProxyFix


def resolve_database_uri():
    database_url = os.getenv("DATABASE_URL")
    if database_url:
        if database_url.startswith("postgres://"):
            database_url = database_url.replace("postgres://", "postgresql://", 1)
        return database_url

    mysql_host = os.getenv("MYSQL_HOST")
    if mysql_host:
        mysql_user = os.getenv("MYSQL_USER", "root")
        mysql_password = quote_plus(os.getenv("MYSQL_PASSWORD", ""))
        mysql_port = os.getenv("MYSQL_PORT", "3306")
        mysql_db = os.getenv("MYSQL_DB", "cleandata")
        return (
            f"mysql+pymysql://{mysql_user}:{mysql_password}"
            f"@{mysql_host}:{mysql_port}/{mysql_db}?charset=utf8mb4"
        )

    return "sqlite:///users.db"


app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1)

is_production = bool(os.getenv("RENDER")) or os.getenv("FLASK_ENV") == "production"
cors_origins = os.getenv("CORS_ORIGINS", "*")
CORS(app, supports_credentials=True, origins=cors_origins)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-secret-change-me")
if is_production and app.config["SECRET_KEY"] == "dev-secret-change-me":
    raise RuntimeError("SECRET_KEY must be set in production")
app.config["SQLALCHEMY_DATABASE_URI"] = resolve_database_uri()
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ENGINE_OPTIONS"] = {"pool_pre_ping": True}
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SECURE"] = is_production
app.config["SESSION_COOKIE_SAMESITE"] = "None" if is_production else "Lax"
db.init_app(app)
with app.app_context():
    db.create_all()

app.register_blueprint(clean_bp)
app.register_blueprint(download_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(history_bp)


@app.route("/")
def index():
    return{"message": "API IS RUNNING"}

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask
from flask_cors import CORS
from routes.clean_route import clean_bp
from routes.download_route import download_bp
import os


app = Flask(__name__)
CORS(app)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.register_blueprint(clean_bp)
app.register_blueprint(download_bp)
@app.route("/")
def index():
    return{"message": "API IS RUNNING"}


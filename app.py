from flask import Flask
from flask_cors import CORS
from routes.clean_route import clean_bp
from routes.download_route import download_bp


app = Flask(__name__)
CORS(app)
app.register_blueprint(clean_bp)
app.register_blueprint(download_bp)
@app.route("/")
def index():
    return{"message": "API IS RUNNING"}

if __name__ == "__main__":
    app.run(debug=True)
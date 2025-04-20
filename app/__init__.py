from flask import Flask
from flask_cors import CORS
from app.routes import bp as routes_bp
from config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    CORS(app)
    app.register_blueprint(routes_bp)
    return app

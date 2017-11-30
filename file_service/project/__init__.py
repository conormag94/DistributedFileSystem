import os

from flask import Flask
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    CORS(app)

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    from project.api import files_blueprint
    app.register_blueprint(files_blueprint)

    return app

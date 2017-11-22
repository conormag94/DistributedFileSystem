import os
import datetime
from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

CORS(app)

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

db = SQLAlchemy(app)

from project import api, models

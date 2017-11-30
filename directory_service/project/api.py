import os

from flask import Blueprint, jsonify, request, send_from_directory
from sqlalchemy import exc
from werkzeug.utils import secure_filename

from project import db
from project.models import File

from flask import current_app as app

directory = Blueprint('directory', __name__)

@directory.route('/', methods=['GET'])
def index():
    return "Directory Server", 200




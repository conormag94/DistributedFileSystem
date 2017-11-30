import os

from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from werkzeug.utils import secure_filename

from project import db
from project.models import File

from flask import current_app as app

directory = Blueprint('directory', __name__)

@directory.route('/', methods=['GET'])
def index():
    return "Directory Server", 200

@directory.route('/locate/<filename>', methods=['GET'])
def locate_file(filename):
    """TODO: Remove hardcoded file server location"""
    
    file_url = f'http://192.168.99.100:5001/files/{filename}'
    response = {
        "status": "success",
        "file_location": file_url
    }

    return jsonify(response), 200




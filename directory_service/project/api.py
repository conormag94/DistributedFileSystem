import os
import random
import sys

import requests

from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from werkzeug.utils import secure_filename

from project import db
from project.models import File

from flask import current_app as app

directory = Blueprint('directory', __name__)

file_server_1 = os.environ.get("FS1_URL")
file_server_2 = os.environ.get("FS2_URL")

file_servers = [
    file_server_1,
    file_server_2
]

@directory.route('/', methods=['GET'])
def index():
    return "Directory Server", 200

@directory.route('/files', methods=['GET'])
def list_files():

    filenames = []
    files = File.query.all()
    for file in files:
        filenames.append(file.to_dict())

    response = {
        "status": "success",
        "files": filenames
    }
    return jsonify(response), 200

@directory.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    """Get a file from whichever file server its stored on."""
    fail_response = {
        'status': 'fail',
        'message': 'File does not exist'
    }
    try:
        file_url = File.query.filter_by(filename=filename).first()
        if not file_url:
            return jsonify(fail_response), 404
        else:
            file_url = file_url.to_dict()["url"]
            r = requests.get(f"{file_url}/{filename}")
            return r.content, r.status_code
    except ValueError:
        return jsonify(fail_response), 404

@directory.route('/files', methods=['POST'])
def create_file():
    if 'user_file' not in request.files:
        return "No file attached", 400
    file = request.files["user_file"]
    fs = random.choice(file_servers)
    r = requests.post(f"{fs}/files", files={"user_file": (file.filename, file)})
    if r.status_code == 200:

        try:
            filename = secure_filename(file.filename)
            url = f"{fs}/files"
        
            file_obj = File(filename=filename, url=url)
            db.session.add(file_obj)
            db.session.commit()

            return jsonify(file_obj.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return "Unable to store in directory server. Was database created? File still exists on FS", 500
    else:
        return (r.content), r.status_code



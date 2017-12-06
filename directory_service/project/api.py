import os
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

@directory.route('/locate/<filename>', methods=['GET'])
def locate_file(filename):
    """TODO: Remove hardcoded file server location"""
    
    file_url = file_servers[0]
    response = {
        "status": "success",
        "file_location": file_url,
    }

    return jsonify(response), 200

@directory.route('/files', methods=['GET'])
def list_files():

    filenames = []
    for server in file_servers:
        r = requests.get(f"{server}/files")
        data = r.json()
        filenames += data["files"] 

    response = {
        "status": "success",
        "files": filenames
    }
    return jsonify(response), 200

@directory.route('/files', methods=['POST'])
def create_file():
    if 'user_file' not in request.files:
        return "No file attached", 400
    file = request.files["user_file"]
    r = requests.post(f"{file_server_1}/files", files={"user_file": (file.filename, file)})
    if r.status_code == 200:

        try:
            filename = secure_filename(file.filename)
            url = f"{file_server_1}/files"
        
            file_obj = File(filename=filename, url=url)
            db.session.add(file_obj)
            db.session.commit()

            return jsonify(file_obj.to_dict()), 200
        except Exception as e:
            db.session.rollback()
            return "Unable to store in directory server. Was database created? File still exists on FS", 500
    else:
        return (r.content), r.status_code



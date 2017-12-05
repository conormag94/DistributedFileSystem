import os

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

@directory.route('/list', methods=['GET'])
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



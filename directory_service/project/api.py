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
lock_service = os.environ.get("LOCK_URL")

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
        file_object = File.query.filter_by(filename=filename).first()
        if not file_object:
            return jsonify(fail_response), 404
        else:
            file_object = file_object.to_dict()
            
            lock_url = f"{lock_service}/locks"
            user = request.headers.get('user')
            lock_obj = {"id": file_object["id"], "filename": file_object["filename"], "user": user}

            aquire_lock = requests.post(lock_url, json=lock_obj)
            if aquire_lock.status_code == 201:
                file_url = file_object["url"]
                r = requests.get(f"{file_url}/{filename}")
                return r.content, r.status_code
            else:
                return aquire_lock.content, aquire_lock.status_code
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

@directory.route('/files/<filename>', methods=['PUT'])
def update_file(filename):
    if 'user_file' not in request.files:
        return "No file attached", 400
    file = request.files["user_file"]
    existing_file = File.query.filter_by(filename=filename).first()
    if not existing_file:
        return "File doesn't exist already, must POST to /files instead", 404
    else:
        existing_file = existing_file.to_dict()
        # Check if locked by user
        lock_url = f"{lock_service}/locks/{existing_file['id']}"
        user = request.headers.get('user')
        lock_status = requests.get(lock_url, headers={'user': user})
        if lock_status.status_code == 200:      
            server = existing_file["url"]
            r = requests.post(server, files={"user_file": (file.filename, file)})
            if r.status_code == 200:
                unlock = requests.delete(lock_url, headers={'user': user})
                if unlock.status_code == 200:
                    return r.content, r.status_code
                else:
                    return unlock.content, unlock.status_code
            else:
                return r.content, r.status_code
        else:
            return lock_status.content, lock_status.status_code

@directory.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):

    fail_response = {
        'status': 'fail',
        'message': 'File does not exist'
    }
    try:
        file = File.query.filter_by(filename=filename).first()
        if not file:
            return jsonify(fail_response), 404
        else:
            url = file.to_dict()["url"] + f"/{filename}"
            r = requests.delete(url)
            if r.status_code == 200:
                db.session.delete(file)
                db.session.commit()
            return r.content, r.status_code
    except Exception as e:
        return jsonify(fail_response), 404



from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project import db
from project.models import FileLock

from flask import current_app as app

lock = Blueprint('lock', __name__)

@lock.route('/', methods=['GET'])
def index():
    return "Lock Service", 200

@lock.route('/locks', methods=['GET'])
def list_locks():

    filelocks = []
    locks = FileLock.query.all()
    for lock in locks:
        filelocks.append(lock.to_dict())

    response = {
        "status": "success",
        "locks": filelocks
    }
    return jsonify(response), 200

@lock.route('/locks/<file_id>', methods=['GET'])
def check_lock(file_id):

    lock = FileLock.query.filter_by(file_id=file_id).first()
    if not lock:
        response = {
            "status": "fail",
            "message": "Lock not found"
        }
        code = 404
    else:
        response = {
            "status": "success",
            "lock": lock.to_dict()
        }
        code = 200
    return jsonify(response), code


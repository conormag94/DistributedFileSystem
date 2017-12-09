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
            "status": "unlocked",
            "message": "Lock not found"
        }
        code = 404
    else:
        response = {
            "status": "locked",
            "lock": lock.to_dict()
        }
        code = 200
    return jsonify(response), code

@lock.route('/locks', methods=['POST'])
def create_lock():
    params = request.get_json()
    filename = params.get('filename')
    file_id = params.get('file_id')
    owner = params.get('owner')

    if filename is None or file_id is None or owner is None:
        response = {
            "status": "fail",
            "message": "Bad request. Need filename, file_id, and owner fields"
        }
        return jsonify(response), 400
    else:
        try:
            lock = FileLock(filename=filename, file_id=file_id, owner=owner)
            db.session.add(lock)
            db.session.commit()
            response = {
                "status": "success",
                "lock": lock.to_dict()
            }
            return jsonify(response), 201
        except Exception as e:
            print(e)
            return jsonify({"status": "fail", "message": "Unable to lock file"}), 500

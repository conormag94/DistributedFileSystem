import sys

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

@lock.route('/locks/<id>', methods=['GET'])
def check_lock(id):

    lock = FileLock.query.filter_by(id=id).first()
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
def lock_file():
    params = request.get_json()
    print(params)
    filename = params.get('filename')
    file_id = params.get('id')
    user = params.get('user')

    if filename is None or file_id is None or user is None:
        response = {
            "status": "fail",
            "message": "Bad request. Need filename, id, and user fields"
        }
        return jsonify(response), 400
    else:
        already_locked = FileLock.query.filter_by(id=file_id).first()
        if already_locked:
            return jsonify({
                "status": "fail", 
                "message": f"Already locked by {already_locked.to_dict()['user']}"
            }), 403
        try:
            lock = FileLock(filename=filename, id=file_id, user=user)
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

@lock.route('/locks/<id>', methods=['DELETE'])
def unlock_file(id):
    user = request.headers.get('user')
    if not user:
        response = {
            "status": "fail",
            "message": "No user specified"
        }
        return jsonify(response), 400

    lock = FileLock.query.filter_by(id=id).first()
    if not lock:
        return jsonify({"status": "fail", "message": "Lock not found"}), 404
    
    if user != lock.to_dict()["user"]:
        return jsonify({"status": "fail", "message": f"User {user} does not own lock"}), 403
    else:
        try:
            db.session.delete(lock)
            db.session.commit()
            return jsonify({"status": "success", "message": "File unlocked"}), 200
        except Exception as e:
            print(e, file=sys.stdout)
            return jsonify({"status": "fail", "message": "Something went wrong"}), 500
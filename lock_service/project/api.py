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


import sys

from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project import db
from project.models import User

from flask import current_app as app

security = Blueprint('security', __name__)

@security.route('/', methods=['GET'])
def index():
    return "Security Service", 200

@security.route('/users', methods=['GET'])
def list_users():

    users = []
    userObjs = User.query.all()
    for user in userObjs:
        users.append(user.to_dict())

    response = {
        "status": "success",
        "users": users
    }
    return jsonify(response), 200
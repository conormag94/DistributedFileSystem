import sys

from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project import db
from project.models import User, SessionToken

from flask import current_app as app

security = Blueprint('security', __name__)

def generate_token(username, password):
    if SessionToken.query.filter_by(username=username.lower()).first() is not None:
        return jsonify({"status": "fail", "message": "User already logged in"}), 403

    user = User.query.filter_by(username=username.lower()).first()
    if not user:
        return jsonify({"status": "fail", "message": "User not registered"}), 404
    
    if user.verify_password(password):
        token = SessionToken(username=username)
        db.session.add(token)
        db.session.commit()
        return jsonify({"status": "success", "token": token.to_hex}), 200

    else:
        return jsonify({"status": "fail", "message": "Incorrect password"}), 403


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

@security.route('/tokens', methods=['GET'])
def list_session_tokens():

    tokens = []
    tokenObjs = SessionToken.query.all()
    for token in tokenObjs:
        tokens.append(token.to_dict())

    response = {
        "status": "success",
        "tokens": tokens
    }
    return jsonify(response), 200

@security.route('/register', methods=['POST'])
def create_user():

    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "fail", "message": "Bad request, need username and password"}), 403
    
    if User.query.filter_by(username=username.lower()).first() is not None:
        return jsonify({"status": "fail", "message": "User already exists"}), 403
    
    try:
        new_user = User(username=username.lower(), password=password.lower())
        db.session.add(new_user)
        db.session.commit()
        return jsonify({"status": "success", "user": username}), 200
    except:
        return jsonify({"status": "fail", "message": "Unable to create user"}), 500

@security.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"status": "fail", "message": "Bad request, need username and password"}), 403

    response = generate_token(username, password)

    return response
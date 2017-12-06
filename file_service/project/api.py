import os

from flask import Blueprint, jsonify, request, send_from_directory
from werkzeug.utils import secure_filename

from flask import current_app as app

files_blueprint = Blueprint('files', __name__)

@files_blueprint.route('/files', methods=['GET'])
def index():
    files_list = os.listdir(app.config['FILES_FOLDER'])
    response = {
        "status": "success",
        "files": files_list
    }
    return jsonify(response)

@files_blueprint.route('/files/<filename>', methods=['GET'])
def get_file(filename):
    if filename not in os.listdir(app.config['FILES_FOLDER']):
        return "File not found", 404
    return send_from_directory(app.config['FILES_FOLDER'], filename)

@files_blueprint.route('/files', methods=['POST'])
def create_file():
    if 'user_file' not in request.files:
        return "No file attached", 400
    try:
        file = request.files['user_file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['FILES_FOLDER'], filename))
        return "File saved", 200
    except Exception as e:
        print(e)
        return "Unable to create or delete file", 500

@files_blueprint.route('/files/<filename>', methods=['DELETE'])
def delete_file(filename):
    if filename not in os.listdir(app.config['FILES_FOLDER']):
        return "File not found", 404
    try:
        filepath = os.path.join(app.config['FILES_FOLDER'], filename)
        os.remove(filepath) 
        return "File deleted", 200
    except OSError:
        return "Error while deleting file", 500


from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from project import db
from project.models import File

files_blueprint = Blueprint('files', __name__)

@files_blueprint.route('/', methods=['GET'])
def index():
    """Root endpoint - does nothing"""
    return jsonify({
        'response': 'Index of the file service. Try the /files endpoint to get started'
    })

@files_blueprint.route('/files', methods=['GET'])
def list_files():
    """List all files in db"""
    file_objects = File.query.all()
    files_list = []
    for file in file_objects:
        files_list.append(file.to_dict())
    
    response = {
        'status': 'success',
        'data': {
            'files': files_list
        }
    }
    return jsonify(response), 200

@files_blueprint.route('/files', methods=['POST'])
def create_file():
    """
    Create a new file.
    Params:
        - filename
        - content
    """
    data = request.get_json()
    filename = data.get('filename')
    content = data.get('content')
    try:
        file = File.query.filter_by(filename=filename).first()
        if not file:
            db.session.add(File(filename=filename, content=content))
            db.session.commit()
            
            response = {
                'status': 'success',
                'message': f'{filename} was added'
            }
            return jsonify(response), 201
        else:
            response_object = {
                'status': 'fail',
                'message': 'Sorry. That filename already exists.'
            }
            return jsonify(response_object), 400
    except exc.IntegrityError as e:
        db.session.rollback()
        response_object = {
            'status': 'fail',
            'message': 'Invalid payload.'
        }
        return jsonify(response_object), 400

@files_blueprint.route('/files/<file_id>', methods=['GET'])
def get_file(file_id):
    """Get file by id."""
    fail_response = {
        'status': 'fail',
        'message': 'File does not exist'
    }
    try:
        file = File.query.filter_by(id=file_id).first()
        if not file:
            return jsonify(fail_response), 404
        else:
            response = {
                'status': 'success',
                'data': file.to_dict()
            }
            return jsonify(response), 200
    except ValueError:
        return jsonify(fail_response), 404

    
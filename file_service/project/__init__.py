import os
from flask import Flask, jsonify
from flask_cors import CORS

app = Flask(__name__)

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

CORS(app)

sample_files = [
        {
            'id': 1,
            'name': 'hello.txt',
            'content': 'This is a sample txt file'
        },
        {
            'id': 2,
            'name': 'foo.txt',
            'content': 'I\'m another file'
        },
        {
            'id': 3,
            'name': 'bar.txt',
            'content': 'A third file to test updating'
        }
]

@app.route('/', methods=['GET'])
def index():
    return jsonify({
        'response': 'Index of the file service. Try the /files endpoint to get started'
    })

@app.route('/files', methods=['GET'])
def files_index():
    return jsonify({
        'files': sample_files
    })

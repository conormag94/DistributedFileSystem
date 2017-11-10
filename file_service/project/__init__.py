import os
import datetime
from flask import Flask, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

CORS(app)

app_settings = os.getenv('APP_SETTINGS')
app.config.from_object(app_settings)

db = SQLAlchemy(app)

class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, filename, content):
        self.filename = filename
        self.content = content
        self.created_at = datetime.datetime.utcnow()

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

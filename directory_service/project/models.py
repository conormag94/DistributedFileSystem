import datetime

from project import db

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

    def to_dict(self):
        """Export user to dictionary data structure"""
        return {
            'id': self.id,
            'filename': self.filename,
            'content': self.content,
            'created_at': self.created_at
        }
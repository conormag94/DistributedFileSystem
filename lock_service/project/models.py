from project import db

class FileLock(db.Model):
    __tablename__ = "locks"
    file_id = db.Column(db.Integer, primary_key=True, nullable=False)
    filename = db.Column(db.String(128), nullable=False)
    owner = db.Column(db.String(128), nullable=False)

    def __init__(self, filename, file_id, owner):
        self.filename = filename
        self.file_id = file_id
        self.owner = owner

    def to_dict(self):
        """Export user to dictionary data structure"""
        return {
            'filename': self.filename,
            'file_id': self.file_id,
            'owner': self.owner
        }
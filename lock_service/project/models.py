from project import db

class FileLock(db.Model):
    __tablename__ = "locks"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    filename = db.Column(db.String(128), nullable=False)
    user = db.Column(db.String(128), nullable=False)

    def __init__(self, filename, id, user):
        self.filename = filename
        self.id = id
        self.user = user

    def to_dict(self):
        """Export user to dictionary data structure"""
        return {
            'filename': self.filename,
            'id': self.id,
            'user': self.user
        }
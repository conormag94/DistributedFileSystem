from project import db

class File(db.Model):
    __tablename__ = "files"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(128), nullable=False)
    #version = db.Column(db.Integer, nullable=False)

    def __init__(self, filename, url):
        self.filename = filename
        self.url = url

    def to_dict(self):
        """Export user to dictionary data structure"""
        return {
            'id': self.id,
            'filename': self.filename,
            'url': self.url,
        }
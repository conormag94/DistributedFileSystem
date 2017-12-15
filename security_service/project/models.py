import secrets

from project import db

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(128), nullable=False)
    password = db.Column(db.String(128), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def verify_password(self, password):
        return self.password == password

    def to_dict(self):
        """Export user to dictionary data structure"""
        return {
            'id': self.id,
            'username': self.username
        }

class SessionToken(db.Model):
    username = db.Column(db.String(128), primary_key=True, nullable=False)
    token = db.Column(db.String(128), nullable=False)

    def __init__(self, username):
        self.username = username
        self.token = secrets.token_hex(16)

    @property
    def to_hex(self):
        return self.token

    def to_dict(self):
        """Export user to dictionary data structure"""
        return {
            'username': self.username,
            'token': self.token
        }
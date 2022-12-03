from db import db


class Client(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)

    def __init__(self, username: str, password: str):
        self.username: str = username
        self.password: str = password

from db import db


class Drone(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    drone_mac = db.Column(db.String, unique=True, nullable=False)
    key = db.Column(db.String, unique=True, nullable=False)

    def __init__(self, drone_mac: str, key: str):
        self.drone_mac: str = drone_mac
        self.key: str = key

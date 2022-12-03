from db import db


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.String, nullable=False)

    def __init__(self, task_id: str):
        self.task_id: str = task_id

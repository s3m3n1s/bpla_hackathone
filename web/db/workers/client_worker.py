from db.models.client_model import Client
from db import db


class ClientWorker:
    @staticmethod
    def add(client: Client):
        db.session.add(client)
        db.session.commit()

    @staticmethod
    def get(client_id: int) -> Client:
        client = db.get_or_404(Client, client_id)
        return client

    @staticmethod
    def get_all() -> Client:
        clients = db.session.query(Client).all()
        return clients

    @staticmethod
    def delete(client_id: int):
        client = db.get_or_404(Client, client_id)

        db.session.delete(client)
        db.session.commit()

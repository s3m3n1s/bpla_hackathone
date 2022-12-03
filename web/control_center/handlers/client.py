import flask
from flask import request
from typing import Tuple
from starlette import status

from db.models.client_model import Client
from db.workers.client_worker import ClientWorker

from __main__ import info_logger


class ClientHandler:
    @staticmethod
    def client_create() -> Tuple[flask.Response, int]:
        try:
            data = request.json
            client = Client(
                username=data["username"],
                password=data["password"],
            )
            ClientWorker.add(client=client)
            info_logger.info("client added")
            return flask.make_response("client added"), status.HTTP_200_OK
        except Exception:
            info_logger.error("client not added", Exception)
            return flask.make_response(Exception), status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def client_get() -> Tuple[flask.Response, int]:
        try:
            client_id = request.args.get("client_id", 0)
            client = ClientWorker.get(client_id=client_id)
            info_logger.info("client was gotten")
            return flask.make_response(f"client: {client.username}"), status.HTTP_200_OK
        except Exception:
            info_logger.error("client was not gotten", Exception)
            return flask.make_response(Exception), status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def client_get_all() -> Tuple[flask.Response, int]:
        try:
            # client_id = request.args.get("client_id", 0)
            clients = ClientWorker.get_all()
            for client in clients:
                print(client.username)
            info_logger.info("clients were gotten")
            return flask.make_response(f"clients: {clients}"), status.HTTP_200_OK
        except Exception:
            info_logger.error("clients were not gotten", Exception)
            return flask.make_response(Exception), status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def client_delete() -> Tuple[flask.Response, int]:
        try:
            client_id = request.json["client_id"]
            ClientWorker.delete(client_id=client_id)
            info_logger.info("client deleted")
            return flask.make_response(f"client with id: {id} deleted"), status.HTTP_200_OK
        except Exception:
            info_logger.error("client was not deleted", Exception)
            return flask.make_response(Exception), status.HTTP_500_INTERNAL_SERVER_ERROR

    # @staticmethod
    # def update():
    #     try:
    #         client = db.get_or_404(Client, id)
    #         client = Client(
    #             username=request.form["username"],
    #             email=request.form["password"],
    #         )
    #         db.session.add(client)
    #         db.session.commit()

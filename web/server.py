import bcrypt
from os import environ
# from flask import Flask
from flask_jwt import JWT, jwt_required, current_identity


from control_center.handlers.client import ClientHandler
from control_center.handlers.drone import DroneHandler
from control_center.handlers.task_manager import TaskManager

from flask_app import app


from db import Client, ClientWorker, db


# @jwt.authentication_handler
def authenticate(username, password):
    client = Client.query.filter(Client.username == username).scalar()
    if bcrypt.checkpw(password.encode('utf-8'), client.password.encode('utf-8')):
        return client

jwt = JWT(app, authenticate)


@jwt.identity_handler
def identify(payload):
    client = Client.query.filter(Client.id == payload['identity']).scalar()
    client.password = None
    return client


@app.route('/protected')
@jwt_required()
def protected():
    return '%s' % current_identity.username


@app.route('/health_app')
def health_app():
    return "App live", 200


def api_add_url():
    # ----------------------------------CLIENT-----------------------------------
    app.add_url_rule("/client", view_func=ClientHandler.client_get, methods=["GET"])
    app.add_url_rule("/client/all", view_func=ClientHandler.client_get_all, methods=["GET"])
    app.add_url_rule("/client", view_func=ClientHandler.client_create, methods=["POST"])
    app.add_url_rule("/client", view_func=ClientHandler.client_delete, methods=["DELETE"])
    # app.add_url_rule("/client", view_func=ClientHandler.update, methods=["UPDATE"])

    # ----------------------------------DRONE-----------------------------------
    app.add_url_rule("/drone", view_func=DroneHandler.drone_get, methods=["GET"])
    app.add_url_rule("/drone/all", view_func=DroneHandler.drone_get_all, methods=["GET"])
    app.add_url_rule("/drone", view_func=DroneHandler.drone_create, methods=["POST"])
    app.add_url_rule("/drone", view_func=DroneHandler.drone_delete, methods=["DELETE"])

    app.add_url_rule("/drone/task/drop_mix_by_route", view_func=TaskManager.drop_mix_by_route, methods=["POST"])
    app.add_url_rule("/drone/task/drop_mix_by_route", view_func=TaskManager.drop_mix_by_coordinate, methods=["POST"])
    app.add_url_rule("/drone/task/return", view_func=TaskManager.return_base, methods=["POST"])


def init_server():
    api_add_url()

    # with app.app_context():
    #     # client = ClientWorker.get(1)
    #     db.create_all()
    #     ClientWorker.add(Client(username='admin', password=bcrypt.hashpw('admin'.encode('utf-8'), bcrypt.gensalt()).decode()))

    app.run(host=str(environ.get("APP_HOST", "127.0.0.1")),
            port=int(environ.get("APP_PORT", 8080)))

import flask
from flask import request
from typing import Tuple
from starlette import status

from db.models.drone_model import Drone
from db.workers.drone_worker import DroneWorker

from __main__ import info_logger


class DroneHandler:
    @staticmethod
    def drone_create() -> Tuple[flask.Response, int]:
        try:
            data = request.json
            drone = Drone(
                drone_mac=data["drone_mac"],
                key=data["key"],
            )
            DroneWorker.add(drone=drone)
            info_logger.info(f"drone with {drone.drone_mac} added")
            return flask.make_response("200"), status.HTTP_200_OK
        except Exception:
            info_logger.error("drone was not added")
            return flask.make_response(Exception), status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def drone_get() -> Tuple[flask.Response, int]:
        drone_mac = request.args.get("drone_mac", "0")
        try:
            drone = DroneWorker.get(drone_mac=drone_mac)
            info_logger.info(f"drone with mac: {drone_mac} was gotten")
            return flask.make_response(f"drone with mac: {drone_mac} is {drone.key}"), status.HTTP_200_OK
        except Exception:
            info_logger.error(f"drone with mac: {drone_mac} was not gotten")
            return flask.make_response(Exception), status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def drone_get_all() -> Tuple[flask.Response, int]:
        try:
            drones = DroneWorker.get_all()
            drones_list = []
            for drone in drones:
                drones_list.append(drone.drone_mac)
            info_logger.info("drones gotten")
            return flask.make_response(f"drones: {drones_list}"), status.HTTP_200_OK
        except Exception:
            info_logger.error("drones ware not gotten")
            return flask.make_response(Exception), status.HTTP_500_INTERNAL_SERVER_ERROR

    @staticmethod
    def drone_delete() -> Tuple[flask.Response, int]:
        drone_mac = request.args.get("drone_mac", "0")
        try:
            DroneWorker.delete(drone_mac)
            info_logger.info(f"drone with mac: {drone_mac} deleted")
            return flask.make_response(f"drone with mac: {drone_mac} deleted"), status.HTTP_200_OK
        except Exception:
            info_logger.error(f"drone with mac: {drone_mac} was not deleted")
            return flask.make_response(Exception), status.HTTP_500_INTERNAL_SERVER_ERROR


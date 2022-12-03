import flask
import requests
from flask import request
from typing import Tuple
from starlette import status

from control_center.dto import Coordinate


class TaskManager:

    @staticmethod
    def drop_mix_by_route():
        """
        start:
        finish:
        :return:
        """
        coordinates = request.json()
        start = Coordinate(x=coordinates["start"]["x"],
                           y=coordinates["start"]["y"])
        finish = Coordinate(x=coordinates["finish"]["x"],
                            y=coordinates["finish"]["y"])

        drone_addr = "http://..."
        response = requests.post(drone_addr, data=coordinates)
        return response.status_code

    @staticmethod
    def drop_mix_by_coordinate(start: Coordinate, finish: Coordinate):
        """

        :return:
        """
        coordinates = request.json()
        start = Coordinate(x=coordinates["start"]["x"],
                           y=coordinates["start"]["y"])
        finish = Coordinate(x=coordinates["finish"]["x"],
                            y=coordinates["finish"]["y"])

        drone_addr = "http://..."
        response = requests.post(drone_addr, data=coordinates)
        return response.status_code

    @staticmethod
    def return_base():
        drone_addr = "http://..."
        response = requests.post(drone_addr)
        return response.status_code

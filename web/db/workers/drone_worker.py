from db.models.drone_model import Drone
from db import db
# from flask_app import app


class DroneWorker:
    @staticmethod
    def add(drone: Drone):
        print("drone-->", drone.drone_mac)
        db.session.add(drone)
        db.session.commit()

    @staticmethod
    def get(drone_mac: str) -> Drone:
        drone = db.session.query(Drone).filter(Drone.drone_mac == drone_mac).one()
        return drone

    @staticmethod
    def get_all() -> Drone:
        drones = db.session.query(Drone).all()
        return drones

    @staticmethod
    def delete(drone_mac: str):
        drone = db.session.query(Drone).filter(Drone.drone_mac == drone_mac).one()

        db.session.delete(drone)
        db.session.commit()


# drone = Drone(key='Nik1',
#               drone_mac="3rdsasd23rrsd")
# # print(drone)
# with app.app_context():
#     # db.create_all()
#     #
#     # db.session.add(drone)
#     # db.session.commit()
#     # drone = db.get_or_404(Drone, 1)
#
#     drone = db.session.query(Drone).filter(Drone.drone_mac == "3rdsasd23rrsd").one()
#     print(drone)
#     drones = db.session.query(Drone).all()
#     for drone in drones:
#         print(drone.id)

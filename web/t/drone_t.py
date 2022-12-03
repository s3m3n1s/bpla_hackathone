# import requests
#
#
# drone_mac = "fafdas3r3"
#
#
# class DroneTest:
#     @staticmethod
#     def test_add_drone():
#         address = "http://127.0.0.1:8080/drone"
#
#         data = {
#             "drone_mac": drone_mac,
#             'key': '5Nikw5',
#             }
#
#         response = requests.post(address, json=data)
#         # assert response.status_code == 200
#         return "OK" if response.status_code == 200 else "False"
#
#     @staticmethod
#     def test_get_drone():
#         address = "http://127.0.0.1:8080/drone"
#         drone_mac_ = {"drone_mac": drone_mac}
#         response = requests.get(address, params=drone_mac_)
#         print(response.text)
#         # assert response.status_code == 200
#         return "OK" if response.status_code == 200 else "False"
#
#     @staticmethod
#     def test_get_all_drone():
#         address = "http://127.0.0.1:8080/drone/all"
#         response = requests.get(address)
#         print(response.text)
#         # assert response.status_code == 200
#         return "OK" if response.status_code == 200 else "False"
#
#     @staticmethod
#     def test_delete_drone():
#         address = "http://127.0.0.1:8080/drone"
#         drone_mac_ = {"drone_mac": drone_mac}
#         response = requests.delete(address, params=drone_mac_)
#         # assert response.status_code == 200
#         return "OK" if response.status_code == 200 else "False"
#
#
# if __name__ == "__main__":
#     print(DroneTest.test_add_drone())
#     print(DroneTest.test_get_all_drone())
#     print(DroneTest.test_get_drone())
#     print(DroneTest.test_delete_drone())

# import requests
#
#
# class ClientTest:
#     @staticmethod
#     def test_add_client():
#         address = "http://127.0.0.1:8080/client"
#
#         user = {
#                 'username': '5Nik5',
#                 'password': '1234'
#                 }
#
#         response = requests.post(address, json=user)
#         # assert response.status_code == 200
#         return "OK" if response.status_code == 200 else "False"
#
#     @staticmethod
#     def test_get_client():
#         address = "http://127.0.0.1:8080/client"
#         client_id = {"client_id": 1}
#         response = requests.get(address, params=client_id)
#         print(response.text)
#         # assert response.status_code == 200
#         return "OK" if response.status_code == 200 else "False"
#
#     @staticmethod
#     def test_get_all_client():
#         address = "http://127.0.0.1:8080/client/all"
#         response = requests.get(address)
#         print(response.text)
#         # assert response.status_code == 200
#         return "OK" if response.status_code == 200 else "False"
#
#     @staticmethod
#     def test_delete_client():
#         address = "http://127.0.0.1:8080/client"
#         client_id = {"client_id": 1}
#         response = requests.delete(address, params=client_id)
#         # assert response.status_code == 200
#         return "OK" if response.status_code == 200 else "False"
#
#
# if __name__ == "__main__":
#     print(ClientTest.test_add_client())
#     # print(ClientTest.test_get_all_client())
#     # print(ClientTest.test_get_client())
#     # print(ClientTest.test_delete_client())

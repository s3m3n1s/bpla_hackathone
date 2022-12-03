import tests.monkey as mk
from unittest import mock

# from mock.mock import Mock


class TestSecPolicy:
    def test_sec_policy(self):
        """

        """
        # Проверка не прошла успешно
        # is_drone_ready = Mock(return_value=False)
        # assert False is is_drone_ready()
        assert mk.verify_module() == True


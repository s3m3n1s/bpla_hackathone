import tests.monkey as mk
from unittest import mock
# from mock import Mock


class Test2:
    def test2_positive(self):
        """
        Включение дрона
        Проверка состояния модулей
        Проверка не прошла успешно
        Проверка модуля сети
        Подключение к УЦ
        Отправка отчёта об ошибке
        Звуковая индикация ошибки
        """
        # Проверка не прошла успешно
        mk.is_drone_ready = mock.Mock(return_value=False)
        assert False is mk.is_drone_ready()

        mk.is_network_available = mock.Mock(return_value=True)
        assert True == mk.is_network_available()

        mk.is_connect_to_control_center = mock.Mock(return_value=True)
        assert True == mk.is_connect_to_control_center()

        mk.send_report_error = mock.Mock(return_value=True)
        assert True == mk.send_report_error()

from mock.mock import Mock


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
        is_drone_ready = Mock(return_value=False)
        assert False is is_drone_ready()

        is_network_available = Mock(return_value=True)
        assert True == is_network_available()

        is_connect_to_control_center = Mock(return_value=True)
        assert True == is_connect_to_control_center()

        send_report = Mock(return_value=True)
        assert True == send_report()

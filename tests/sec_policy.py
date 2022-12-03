import tests.monkey
from mock.mock import Mock


class SecPolicy:
    def test_sec_policy(self):
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
        # is_drone_ready = Mock(return_value=False)
        # assert False is is_drone_ready()
        assert verify_module() == True


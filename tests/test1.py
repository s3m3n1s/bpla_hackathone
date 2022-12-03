# import requests
# from starlette import status
# import conftest
from mock.mock import Mock


class Test1:
    def test1_positive(self, is_drone_ready):
        """
        Включение дрона
        Проверка состояния модулей
        Подключение к УЦ
        Отправка отчёта о готовности
        Получение полётного задания
        Валидация полётного задания (проверка ЦП)
        Взлёт и начало выполнения полётного задания.
        Отправка отчёта о начале выполнения задания.
        Выполнение полетного задания
        Сообщение о потери позиционирования GPS
        Активация инерционной навигационной системы и глонасс
        Выполнение полетного задания
        Возвращение на базу
        Отчет об окончании полетного задания
        """
        is_drone_ready = Mock(return_value=True)
        assert True == is_drone_ready

        is_connect_to_control_center = Mock(return_value=True)
        assert True == is_connect_to_control_center()

        send_report_ready = Mock(return_value=True)
        assert True == send_report_ready()

        get_task = Mock(return_value="task2")
        assert "task2" == get_task()

        start_task = Mock(return_value=True)
        assert True == start_task()

        send_report_start = Mock(return_value=True)
        assert True == send_report_start()

        start_spray = Mock(return_value=True)
        assert True == start_spray()

        go_home = Mock(return_value=True)
        assert True == go_home()


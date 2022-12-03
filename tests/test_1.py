# import requests
# from starlette import status
import tests.monkey as mk
from mock import Mock


class Test1:
    def test1_positive(self):
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
        mk.is_drone_ready = Mock(return_value=True)
        assert True == mk.is_drone_ready()

        mk.is_connect_to_control_center = Mock(return_value=True)
        assert True == mk.is_connect_to_control_center()

        mk.send_report_ready = Mock(return_value=True)
        assert True == mk.send_report_ready()

        mk.get_task = Mock(return_value="task2")
        assert "task2" == mk.get_task()

        mk.start_task = Mock(return_value=True)
        assert True == mk.start_task()

        mk.send_report_start = Mock(return_value=True)
        assert True == mk.send_report_start()

        mk.start_spray = Mock(return_value=True)
        assert True == mk.start_spray()

        mk.go_home = Mock(return_value=True)
        assert True == mk.go_home()


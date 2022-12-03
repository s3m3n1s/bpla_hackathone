import pytest


@pytest.fixture
def connect_mc():
    pass


@pytest.fixture
def is_drone_ready():
    """
    собираю сообщение у /HW_control
    :return:
    """
    return True


def is_network_available():
    return True


def is_connect_to_control_center():
    """
    успешно ли соединение с control center
    :return:
    """
    return True


def send_report_ready():
    """
    отправка сообщения о готовности control center
    :return:
    """
    return True


def send_report_start():
    """
    отправка сообщения о начал работы control center
    :return:
    """
    return True


def send_report_error():
    return True


def get_task():
    """
        получееие одного из n заданий для дрона
        GET http://task
        :return:
        task1
        task2
    """
    return "task1"


def start_task(task: str):
    """
        получееие одного из n заданий для дрона
        GET http://task
        :return:
        task1
        task2
    """
    return True


def start_spray():
    return False


def go_home():
    return False

def verify_module():
    #
    pass
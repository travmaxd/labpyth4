import sys
import pytest
from PySide6.QtWidgets import QApplication

# Импорты всей логики проекта
from main_logic import abs_generator, password_generator, multiply_lists
from parallel import parallel_passwords
from app import App


# -----------------------------------------
#            ТЕСТЫ ЛОГИКИ
# -----------------------------------------

def test_abs_generator_normal():
    gen = abs_generator(-2, 2)
    assert [next(gen), next(gen), next(gen)] == [2, 1, 0]


def test_abs_generator_stop():
    gen = abs_generator(1, 2)
    assert next(gen) == 1
    assert next(gen) == 2
    with pytest.raises(StopIteration):
        next(gen)


def test_abs_generator_invalid_range():
    with pytest.raises(ValueError):
        list(abs_generator(5, 1))


def test_password_generator_length():
    gen = password_generator(12)
    p = next(gen)
    assert len(p) == 12


def test_password_generator_values_unique():
    gen = password_generator()
    p1 = next(gen)
    p2 = next(gen)
    assert p1 != p2


def test_multiply_lists_basic():
    gen = multiply_lists([1, 2, 3], [4, 5, 6])
    assert [next(gen), next(gen), next(gen)] == [4, 10, 18]


def test_multiply_lists_short_lists():
    gen = multiply_lists([2, 3], [10])
    assert next(gen) == 20
    with pytest.raises(StopIteration):
        next(gen)


# -----------------------------------------
#     ТЕСТЫ ПАРАЛЛЕЛЬНОЙ ВЕРСИИ
# -----------------------------------------

def test_parallel_passwords_count():
    res = parallel_passwords(5)
    assert len(res) == 5


def test_parallel_passwords_unique():
    res = parallel_passwords(5)
    assert len(set(res)) == 5


# -----------------------------------------
#                ТЕСТ GUI
# -----------------------------------------

@pytest.fixture(scope="session")
def app_qt():
    """Гарантируем наличие QApplication."""
    qapp = QApplication.instance()
    if qapp is None:
        qapp = QApplication(sys.argv)
    return qapp


def test_gui_window_exists(app_qt):
    win = App()
    assert win.windowTitle() == "Генераторы — лабораторная работа"
    assert win.isVisible() is False  # окно только создано, но не показано

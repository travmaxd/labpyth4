import sys
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel,
    QLineEdit, QTabWidget, QTextEdit, QMessageBox
)
from utils.benchmark import benchmark
from main_logic import abs_generator, password_generator, multiply_lists
from parallel import parallel_passwords


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Генераторы — лабораторная работа")
        self.resize(750, 500)

        tabs = QTabWidget()
        tabs.addTab(self.make_task1_tab(), "Задание 1")
        tabs.addTab(self.make_task2_tab(), "Задание 2")
        tabs.addTab(self.make_task3_tab(), "Задание 3")
        tabs.addTab(self.make_bench_tab(), "Бенчмарк")

        layout = QVBoxLayout()
        layout.addWidget(tabs)
        self.setLayout(layout)

    # ---------- ЗАДАНИЕ 1 ----------
    def make_task1_tab(self):
        w = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Генератор абсолютных значений от a до b")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        self.a_edit = QLineEdit()
        self.a_edit.setPlaceholderText("Введите число a (например: -3)")

        self.b_edit = QLineEdit()
        self.b_edit.setPlaceholderText("Введите число b (например: 2)")

        btn = QPushButton("Показать первые 4 значения")

        self.result1 = QTextEdit()
        self.result1.setReadOnly(True)

        def run():
            try:
                a = int(self.a_edit.text())
                b = int(self.b_edit.text())
                gen = abs_generator(a, b)

                out = []
                for _ in range(4):
                    try:
                        out.append(str(next(gen)))
                    except StopIteration:
                        break

                self.result1.setPlainText("\n".join(out))
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

        btn.clicked.connect(run)

        layout.addWidget(title)
        layout.addWidget(QLabel("Введите диапазон:"))
        layout.addWidget(self.a_edit)
        layout.addWidget(self.b_edit)
        layout.addWidget(btn)
        layout.addWidget(QLabel("Результат:"))
        layout.addWidget(self.result1)

        w.setLayout(layout)
        return w

    # ---------- ЗАДАНИЕ 2 ----------
    def make_task2_tab(self):
        w = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Генерация случайных паролей")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        note = QLabel("Будет сгенерировано 5 случайных паролей.\n"
                      "Варианты: генерация последовательно и параллельно.")
        note.setStyleSheet("color: gray;")

        btn_seq = QPushButton("Сгенерировать 5 паролей (последовательно)")
        btn_par = QPushButton("Сгенерировать 5 паролей (параллельно)")

        self.result2 = QTextEdit()
        self.result2.setReadOnly(True)

        def run_seq():
            gen = password_generator()
            self.result2.setPlainText("\n".join(next(gen) for _ in range(5)))

        def run_par():
            pw = parallel_passwords(5)
            self.result2.setPlainText("\n".join(pw))

        btn_seq.clicked.connect(run_seq)
        btn_par.clicked.connect(run_par)

        layout.addWidget(title)
        layout.addWidget(note)
        layout.addWidget(btn_seq)
        layout.addWidget(btn_par)
        layout.addWidget(QLabel("Результат:"))
        layout.addWidget(self.result2)

        w.setLayout(layout)
        return w

    # ---------- ЗАДАНИЕ 3 ----------
    def make_task3_tab(self):
        w = QWidget()
        layout = QVBoxLayout()

        self.l1_edit = QLineEdit()
        self.l1_edit.setPlaceholderText("Например: 1 2 3 4")

        self.l2_edit = QLineEdit()
        self.l2_edit.setPlaceholderText("Например: 5 6 7 8")

        btn = QPushButton("Перемножить первые 3 значения")

        self.result3 = QTextEdit()
        self.result3.setReadOnly(True)

        def run():
            try:
                list1 = list(map(int, self.l1_edit.text().split()))
                list2 = list(map(int, self.l2_edit.text().split()))

                if len(list1) < 3 or len(list2) < 3:
                    raise ValueError("В каждом списке должно быть минимум 3 числа.")

                gen = multiply_lists(list1, list2)
                res = [str(next(gen)) for _ in range(3)]

                self.result3.setPlainText("\n".join(res))

            except Exception as e:
                QMessageBox.critical(self, "Ошибка", str(e))

        btn.clicked.connect(run)

        layout.addWidget(QLabel("Введите список 1:"))
        layout.addWidget(self.l1_edit)
        layout.addWidget(QLabel("Введите список 2:"))
        layout.addWidget(self.l2_edit)
        layout.addWidget(btn)
        layout.addWidget(QLabel("Результат:"))
        layout.addWidget(self.result3)

        w.setLayout(layout)
        return w

    # ---------- БЕНЧМАРК ----------
    def make_bench_tab(self):
        w = QWidget()
        layout = QVBoxLayout()

        title = QLabel("Бенчмарк генерации 50 000 паролей")
        title.setStyleSheet("font-size: 16px; font-weight: bold;")

        note = QLabel("Замеряется скорость последовательного и параллельного генератора.")
        note.setStyleSheet("color: gray;")

        btn = QPushButton("Запустить бенчмарк")

        self.bench_result = QTextEdit()
        self.bench_result.setReadOnly(True)

        def run():
            res = benchmark(50000)
            txt = "\n".join(f"{k}: {v:.4f} сек" for k, v in res.items())
            self.bench_result.setPlainText(txt)

        btn.clicked.connect(run)

        layout.addWidget(title)
        layout.addWidget(note)
        layout.addWidget(btn)
        layout.addWidget(QLabel("Результаты:"))
        layout.addWidget(self.bench_result)
        w.setLayout(layout)
        return w


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = App()
    window.show()
    sys.exit(app.exec())

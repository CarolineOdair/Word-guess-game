from PyQt5.QtWidgets import QApplication

from sys import argv, exit

from core.gui import App
from core.config import main_style


if __name__ == "__main__":

    with open("static\word_list.csv", "r", encoding="utf-8") as f:
        file = f.readlines()

    q_application = QApplication(argv)
    app = App(file)

    q_application.setStyleSheet(main_style)

    app.show()

    exit(q_application.exec())
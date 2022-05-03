from sys import argv, exit

from PyQt5.QtWidgets import QApplication

from core.gui import App


if __name__ == "__main__":

    with open("static\word_list.csv", "r", encoding="utf-8") as f:
        file = f.readlines()
        file = [word.strip() for word in file]

    q_application = QApplication(argv)
    app = App(file)

    app.show()

    exit(q_application.exec())

from PyQt5.QtWidgets import QApplication

from sys import argv, exit

from utils import get_main_word
from gui import App


if __name__ == "__main__":

    with open("word_list.csv", "r", encoding="utf-8") as f:
        file = f.readlines()

    word, id_ = get_main_word(file)
    print(word)

    q_application = QApplication(argv)
    app = App(word, id_)

    app.show()

    exit(q_application.exec())
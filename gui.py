from PyQt5 import QtGui, QtWidgets, QtCore, Qt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QLabel

from connect import LocalDb, WordStatus
from utils import labels_features


class WrongListIdGiven(Exception):
    pass

class App(QtWidgets.QMainWindow):
    LEFT_CHANCES = 15

    def __init__(self, word, id_):
        self.connector = LocalDb(word, id_)
        self.main_word = word

        super(App, self).__init__()
        self.setWindowTitle("Słownikowo")
        self.init_UI()

    def init_UI(self) -> None:
        self.setWindowState(Qt.WindowMaximized)

        upper_frame = QFrame()
        self.upper_frame_config(upper_frame)

        main_frame = QFrame()
        self.main_frame_config(main_frame)

        window_layout = QtWidgets.QVBoxLayout()
        window_layout.setSpacing(0)
        window_layout.setContentsMargins(0,0,0,0)
        window_layout.addWidget(upper_frame, 1)
        window_layout.addWidget(main_frame, 8)

        widget1 = QtWidgets.QWidget(self)
        widget1.setLayout(window_layout)
        self.setCentralWidget(widget1)

    def upper_frame_config(self, frame: QFrame) -> None:
        game_name_label = QLabel()
        game_name_label.setText("SŁOWNIKOWO")
        game_name_label.setAlignment(Qt.AlignCenter)
        game_name_label.setStyleSheet("border: 2px solid orange;"
                                      "color: orange;"
                                      "font-size: 55px;")

        layout = QtWidgets.QVBoxLayout(frame)
        layout.addWidget(game_name_label)

    def main_frame_config(self, frame: QFrame) -> None:
        self.left_frame = QFrame()
        self.left_frame_config()

        self.right_frame = QFrame()
        self.right_frame_config()

        main_layout = QtWidgets.QHBoxLayout(frame)
        main_layout.addWidget(self.left_frame, 1)
        main_layout.addWidget(self.right_frame, 9)

        # optional, I guess
        # I think that if it was added, it would be easier to set one stylesheet
        # but for now it's not really useful
        # self.widget2 = QtWidgets.QWidget(self.main_frame)
        # self.setCentralWidget(self.widget2)

    def left_frame_config(self) -> None:
        layout = QtWidgets.QVBoxLayout(self.left_frame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        path = "grey_circle.svg"
        for i in range(15):

            label = QtWidgets.QLabel()
            pixmap = QtGui.QPixmap(path)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)

            layout.addWidget(label)

        # widget = self.create_chances_box(CHANCES, pawn_img_path)
        #
        # self.x = QtWidgets.QGridLayout(self.left_frame)
        # self.x.addWidget(widget, 0, 0)
        # def create_chances_box(self, chances, path):
        #     frame = QtWidgets.QFrame()
        #     layout = QtWidgets.QVBoxLayout(frame)
        #
        #     for i in range(chances):
        #         label = QtWidgets.QLabel(frame)
        #         pixmap = QtGui.QPixmap(path)
        #         label.setPixmap(pixmap)
        #         layout.addWidget(label, i)
        #     return frame

    def right_frame_config(self) -> None:
        guessing_frame = QFrame()
        guessing_frame.setStyleSheet("border: 2px solid purple;")
        self.guessing_frame_config(guessing_frame)

        alphabet_label = QLabel()
        self.alphabet_label_config(alphabet_label)

        layout = QtWidgets.QVBoxLayout(self.right_frame)
        layout.addWidget(guessing_frame, 10)
        layout.addWidget(alphabet_label, 1)

    def guessing_frame_config(self, frame: QFrame) -> None:
        self.upper_words_frame = QFrame()
        self.upper_list_frame_config()

        self.typing_editline = QtWidgets.QLineEdit()
        self.typing_editline_config()

        self.lower_words_frame = QFrame()
        self.lower_list_frame_config()

        layout = QtWidgets.QVBoxLayout(frame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.upper_words_frame, 6)
        layout.addWidget(self.typing_editline, 1)
        layout.addWidget(self.lower_words_frame, 6)

    def typing_editline_config(self) -> None:
        font = QtGui.QFont("Times", 32)

        self.typing_editline.setPlaceholderText("WPISZ SŁOWO")
        self.typing_editline.setAlignment(Qt.AlignCenter)
        self.typing_editline.setFont(font)
        self.typing_editline.setStyleSheet("text-transform: uppercase;")
        self.typing_editline.returnPressed.connect(self.enter_pressed_action)

    def upper_list_frame_config(self) -> None:
        self.upper_layout = QtWidgets.QVBoxLayout(self.upper_words_frame)
        self.upper_layout.setSpacing(0)
        self.upper_layout.setContentsMargins(0, 0, 0, 0)
        self.init_words_labels(self.upper_layout, labels_features[::-1])

    def lower_list_frame_config(self) -> None:
        self.down_layout = QtWidgets.QVBoxLayout(self.lower_words_frame)
        self.down_layout.setSpacing(0)
        self.down_layout.setContentsMargins(0, 0, 0, 0)
        self.init_words_labels(self.down_layout, labels_features)

    def init_words_labels(self, layout: QtWidgets.QLayout, features:list) -> None:

        for feat in features:
            label = QLabel()
            label.setText("")
            label.setFixedHeight(feat["height"])
            label.setAlignment(Qt.AlignHCenter)

            opacity_effect = QtWidgets.QGraphicsOpacityEffect()
            opacity_effect.setOpacity(feat["opacity"])
            label.setGraphicsEffect(opacity_effect)

            font = QtGui.QFont("Times", feat["size"])
            label.setFont(font)

            layout.addWidget(label)

    def alphabet_label_config(self, label: QLabel) -> None:
        label.setText(" A Ą B C D E Ę F G H I J K L Ł M N Ń O Ó P R S Ś T U W X Y Z Ź Ż ")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("border: 2px solid blue;"
                                     "color: blue;"
                                     "font-size: 35px;")



    def enter_pressed_action(self):
        # get typed word
        word = self.typing_editline.text().lower()

        # connect with db and return word info -> status, id_, list, of words
        resp = self.connector.check_word(word)

        # depending on word_status do something
        if resp["status"] == WordStatus.MAIN:
            print("won")

        elif resp["status"] == WordStatus.ALREADY_GUESSED:
            self.display_msg("To słowo zostało już wpisane")
            print("To słowo zostało już wpisane")

        elif resp["status"] == WordStatus.NEW:
            print("Add to guessed")
            if self.LEFT_CHANCES == 0:
                print(f"Koniec gry. Szukane słowo: {self.main_word}")
            self.LEFT_CHANCES -= 1
            self.label.setText(str(self.LEFT_CHANCES))

            self.update_(resp["list"], resp["list_id"])

        elif resp["status"] == WordStatus.UNKNOWN:
            self.display_msg("Brak podanego słowa w bazie")
            print("Brak podanego słowa w bazie")

        print(resp["word"])

        self.typing_editline.clear()

    def update_(self, word_list: list, list_id: int) -> None:
        turn_list = self.get_current_turn_list(word_list, list_id)

        if list_id == 0:
            self.update_ui(turn_list[-5:], self.upper_layout)
        elif list_id == 1:
            self.update_ui(turn_list, self.down_layout)
        else:
            raise WrongListIdGiven(f"List id must be `0` for upper list and `1` for lower list, not given `{list_id}`.")

    def get_current_turn_list(self, word_list:list, list_id:int) -> list:
        empty_word = {'word': '', 'id': 0, 'n_letters': 0}

        turn_list = word_list.copy()
        while len(turn_list) < 5:
            if list_id == 0:
                turn_list.insert(0, empty_word)
            elif list_id == 1:
                turn_list.append(empty_word)
            else:
                raise WrongListIdGiven(f"List id must be `0` for upper list and `1` for lower list, not given `{list_id}`.")

        return turn_list

    def update_ui(self, turn_list:list, layout:QtWidgets.QLayout) -> None:
        widgets = (layout.itemAt(i).widget() for i in range(layout.count()))
        for widget, word in zip(widgets, turn_list):
            if isinstance(widget, QtWidgets.QLabel):
                word["word"] = word["word"].upper()
                widget.setText(
                    f'<font color="green">{word["word"][:word["n_letters"]]}</font><font color="black">{word["word"][word["n_letters"]:]}</font>')

    def display_msg(self, msg:str) -> None:
        MSG = 1200
        msg_label = QLabel(self)
        msg_label.setText(msg)

        msg_label.move(900, 135)
        msg_label.setStyleSheet("border-style: solid;"
                                "border-width: 3px;"
                                "border-radius: 5px;"
                                "border-color: red;"
                                "background: grey;"
                                "font-size: 15px;"
                                "padding: 3px 3px 3px 3px;")
        msg_label.adjustSize()

        msg_label.show()
        QtCore.QTimer.singleShot(MSG, msg_label.deleteLater)

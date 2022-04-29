from PyQt5 import QtGui, QtWidgets, QtCore, Qt
from PyQt5.QtCore import Qt

from connect import LocalDb, WordStatus
from utils import labels_features


WORD_LIST = [{"word": "cat", "n":2}, {"word": "house", "n":4}, {"word": "education", "n":9}, {"word": "brother", "n": 0}]

class App(QtWidgets.QMainWindow):
    LEFT_CHANCES = 15

    def __init__(self, word, id_):
        self.connector = LocalDb(word, id_)

        super(App, self).__init__()
        self.setWindowTitle("Słownikowo")
        self.init_UI()

    def enter_pressed(self):
        # get typed word
        word = self.main_word_edit.text().lower()
        # connect with db and return word info -> status, id_, list, of words
        resp = self.connector.check_word(word)
        print(resp["word"])
        if resp["status"] == WordStatus.MAIN:
            print(resp["msg"])
        elif resp["status"] == WordStatus.GUESSED:
            print(resp["msg"])
        elif resp["status"] == WordStatus.NEW:
            print(resp["msg"])
            self.update_(resp["list"], resp["list_id"])
        elif resp["status"] == WordStatus.UNKNOWN:
            print(resp["msg"])

        self.main_word_edit.clear()

    def init_UI(self):
        self.setWindowState(Qt.WindowMaximized)

        upper_frame = QtWidgets.QFrame()
        self.init_upper_frame(upper_frame)

        main_frame = QtWidgets.QFrame()
        self.init_main_frame(main_frame)

        window_layout = QtWidgets.QVBoxLayout()
        window_layout.setSpacing(0)
        window_layout.setContentsMargins(0,0,0,0)
        window_layout.addWidget(upper_frame, 1)
        window_layout.addWidget(main_frame, 8)

        widget1 = QtWidgets.QWidget(self)
        widget1.setLayout(window_layout)
        self.setCentralWidget(widget1)

    def init_upper_frame(self, frame):
        game_name_label = QtWidgets.QLabel()
        game_name_label.setText("SŁOWNIKOWO")
        game_name_label.setAlignment(Qt.AlignCenter)
        game_name_label.setStyleSheet("border: 2px solid orange;"
                                      "color: orange;"
                                      "font-size: 35px;")

        layout = QtWidgets.QVBoxLayout(frame)
        layout.addWidget(game_name_label)

    def init_main_frame(self, frame):

        self.left_frame = QtWidgets.QFrame()
        self.init_left_frame()

        self.right_frame = QtWidgets.QFrame()
        self.init_right_frame()

        main_layout = QtWidgets.QHBoxLayout(frame)
        main_layout.addWidget(self.left_frame, 1)
        main_layout.addWidget(self.right_frame, 9)

        # optional, I guess
        # I think that if it was added, it would be easier to set one stylesheet
        # but for now it's not really useful
        # self.widget2 = QtWidgets.QWidget(self.main_frame)
        # self.setCentralWidget(self.widget2)


    def init_left_frame(self):
        CHANCES = 15
        self.label = QtWidgets.QLabel()
        self.label.setText("AA")
        self.label.setStyleSheet("border: 2px solid green;")

        layout = QtWidgets.QVBoxLayout(self.left_frame)
        layout.addWidget(self.label)

        pawn_img_path = "img_pawn.svg"
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


    def init_right_frame(self):
        guessing_frame = QtWidgets.QFrame()
        guessing_frame.setStyleSheet("border: 2px solid purple;")
        self.init_guessing_frame(guessing_frame)

        alphabet_label = QtWidgets.QLabel()
        alphabet_label.setText(" A Ą B C D E Ę F G H I J K L Ł M N Ń O Ó P R S Ś T U W X Y Z Ź Ż ")
        alphabet_label.setAlignment(Qt.AlignCenter)
        alphabet_label.setStyleSheet("border: 2px solid blue;"
                                     "color: blue;"
                                     "font-size: 35px;")

        layout = QtWidgets.QVBoxLayout(self.right_frame)
        layout.addWidget(guessing_frame, 10)
        layout.addWidget(alphabet_label, 1)

    def init_guessing_frame(self, frame):
        font = QtGui.QFont("Times", 32)

        self.upper_words_frame = QtWidgets.QFrame()
        self.upper_layout = QtWidgets.QVBoxLayout(self.upper_words_frame)
        self.upper_layout.setSpacing(0)
        self.upper_layout.setContentsMargins(0, 0, 0, 0)
        self.init_words_labels(self.upper_layout, labels_features[::-1])

        self.main_word_edit = QtWidgets.QLineEdit()
        self.main_word_edit.setPlaceholderText("WPISZ SŁOWO")
        self.main_word_edit.setAlignment(Qt.AlignCenter)
        self.main_word_edit.setFont(font)
        self.main_word_edit.setStyleSheet("text-transform: uppercase;")
        self.main_word_edit.returnPressed.connect(self.enter_pressed)

        self.down_words_frame = QtWidgets.QFrame()
        self.down_layout = QtWidgets.QVBoxLayout(self.down_words_frame)
        self.down_layout.setSpacing(0)
        self.down_layout.setContentsMargins(0, 0, 0, 0)
        self.init_words_labels(self.down_layout, labels_features)

        layout = QtWidgets.QVBoxLayout(frame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.upper_words_frame, 6)
        layout.addWidget(self.main_word_edit, 1)
        layout.addWidget(self.down_words_frame, 6)

    def init_words_labels(self, layout, features):

        for feat in features:
            label = QtWidgets.QLabel()
            label.setText("")
            label.setFixedHeight(feat["height"])
            label.setAlignment(Qt.AlignHCenter)

            opacity_effect = QtWidgets.QGraphicsOpacityEffect()
            opacity_effect.setOpacity(feat["opacity"])
            label.setGraphicsEffect(opacity_effect)

            font = QtGui.QFont("Times", feat["size"])
            label.setFont(font)

            layout.addWidget(label)


    def update_(self, list_, list_id):
        turn_list = self.get_current_turn_list(list_, list_id)

        if list_id == "up":
            self.update_ui(turn_list[-5:], self.upper_layout)
        elif list_id == "down":
            self.update_ui(turn_list, self.down_layout)
        else:
            print("!!!!!!!!")

    def get_current_turn_list(self, list_, list_id):
        empty_word_up = {'word': '', 'id': 0, 'n_letters': 0}
        empty_word_down = {'word': '', 'id': 100000000000, 'n_letters': 0}

        turn_list = list_.copy()
        while len(turn_list) < 5:
            if list_id == "up":
                turn_list.append(empty_word_up)
            else:
                turn_list.append(empty_word_down)
        turn_list = sorted(turn_list, key=lambda x: x["id"])

        return turn_list


    def update_ui(self, turn_list, layout):
        widgets = (layout.itemAt(i).widget() for i in range(layout.count()))
        for widget, word in zip(widgets, turn_list):
            if isinstance(widget, QtWidgets.QLabel):
                word["word"] = word["word"].upper()
                widget.setText(
                    f'<font color="green">{word["word"][:word["n_letters"]]}</font><font color="black">{word["word"][word["n_letters"]:]}</font>')
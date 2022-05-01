from PyQt5 import QtGui, QtWidgets, QtCore, Qt
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame, QLabel

from connect import CurrentGameDataAnalyzer, WordStatus
from utils import labels_features, color, Text, detailed_style, FontSize


class WrongListIdGiven(Exception):
    pass

class AppFont(QtGui.QFont):
    def __init__(self, font_size):
        super(AppFont, self).__init__()
        self.setBold(True)
        self.setWeight(700)
        self.setFamily("Segoe UI")
        self.setStyleHint(self.SansSerif)
        self.setBold(True)
        self.setPointSize(font_size)


class App(QtWidgets.QMainWindow):
    MAX_CHANCES = 15
    LEFT_CHANCE_PATH = "grey_circle.svg"
    LOST_CHANCE_PATH = "yellow_circle.svg"

    def __init__(self, words:list):
        super(App, self).__init__()
        self.words = words
        self.setWindowTitle(Text.WINDOW_TITLE)
        self.setWindowState(Qt.WindowMaximized)
        self.init_data()
        self.init_UI()

    def init_data(self) -> None:
        self.LEFT_CHANCES = 15
        self.connector = CurrentGameDataAnalyzer(self.words)
        self.main_word = self.connector.main_word["word"]

    def reset_game(self) -> None:
        self.end_game_frame.close()
        self.end_game_frame.deleteLater()
        self.init_data()
        self.reset_label_layout(self.upper_layout)
        self.reset_label_layout(self.down_layout)
        self.init_words_labels(self.upper_layout, labels_features[::-1])
        self.init_words_labels(self.down_layout, labels_features)
        self.add_chances_vis()

    def init_UI(self) -> None:
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
        font = AppFont(FontSize.GAME_NAME)
        game_name_label.setFont(font)
        game_name_label.setText(Text.GAME_NAME)
        game_name_label.setAlignment(Qt.AlignCenter)

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

    def left_frame_config(self) -> None:
        self.dot_layout = QtWidgets.QVBoxLayout(self.left_frame)
        self.dot_layout.setSpacing(0)
        self.dot_layout.setContentsMargins(0, 0, 0, 0)
        self.add_chances_vis()

    def add_chances_vis(self) -> None:
        self.reset_dot_layout()

        for i in range(self.MAX_CHANCES):
            label = QtWidgets.QLabel()
            if i < self.MAX_CHANCES - self.LEFT_CHANCES:
                pixmap = QtGui.QPixmap(self.LOST_CHANCE_PATH)
            else:
                pixmap = QtGui.QPixmap(self.LEFT_CHANCE_PATH)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)

            self.dot_layout.addWidget(label)

    def right_frame_config(self) -> None:
        guessing_frame = QFrame()
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
        layout.addWidget(self.typing_editline, 1, Qt.AlignHCenter)
        layout.addWidget(self.lower_words_frame, 6)

    def typing_editline_config(self) -> None:
        WIDTH = 800
        font = AppFont(FontSize.EDITLINE)

        self.typing_editline.setFixedWidth(WIDTH)
        self.typing_editline.setAlignment(Qt.AlignCenter)
        self.typing_editline.setFont(font)
        self.typing_editline.returnPressed.connect(self.enter_pressed_action)
        self.typing_editline.setPlaceholderText(Text.TYPING_EDITLINE)

    # TODO
    # seems nice but indicates problem - just after pressing enter app an empty string
    # is given as if Enter was pressed twice
    #     self.setFocus()
    #
    # def keyPressEvent(self, event):
    #     self.typing_editline.setFocus()
    #     self.typing_editline.keyPressEvent(event)

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

            font = AppFont(feat["size"])
            label.setFont(font)

            layout.addWidget(label)

    def alphabet_label_config(self, label: QLabel) -> None:
        label.setText(Text.ALPHABET)
        label.setAlignment(Qt.AlignCenter)
        font = AppFont(FontSize.ALPHABET)
        label.setFont(font)
        label.setStyleSheet(detailed_style["alphabet_label"])

    def reset_label_layout(self, layout: QtWidgets.QLayout) -> None:
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def reset_dot_layout(self) -> None:
        for i in reversed(range(self.dot_layout.count())):
            self.dot_layout.itemAt(i).widget().setParent(None)


    def enter_pressed_action(self) -> None:
        # get typed word
        word = self.typing_editline.text().lower()

        # connect with db and return word info -> status, id_, list, of words
        resp = self.connector.check_word(word)

        self.typing_editline.clear()

        # depending on word_status do something
        if resp["status"] == WordStatus.MAIN:
            self.display_end_game_frame(Text.WIN, self.main_word)
            return

        elif resp["status"] == WordStatus.ALREADY_GUESSED:
            self.display_msg(Text.WORD_ALREADY_GUESSED)

        elif resp["status"] == WordStatus.NEW:
            if self.LEFT_CHANCES == 0:
                self.display_end_game_frame(Text.LOST, self.main_word)
                return
            else:
                self.LEFT_CHANCES -= 1
                self.update_(resp["list"], resp["list_id"])

        elif resp["status"] == WordStatus.UNKNOWN:
            self.display_msg(Text.WORD_UNKNOWN)

    def update_(self, word_list: list, list_id: int) -> None:
        turn_list = self.get_current_turn_list(word_list, list_id)

        if list_id == 0:
            self.update_word_ui(turn_list[-5:], self.upper_layout)
        elif list_id == 1:
            self.update_word_ui(turn_list, self.down_layout)
        else:
            raise WrongListIdGiven(f"List id must be `0` for upper list and `1` for lower list, not given `{list_id}`.")

        self.add_chances_vis()

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

    def update_word_ui(self, turn_list:list, layout:QtWidgets.QLayout) -> None:
        widgets = (layout.itemAt(i).widget() for i in range(layout.count()))
        for widget, word in zip(widgets, turn_list):
            if isinstance(widget, QtWidgets.QLabel):
                word["word"] = word["word"].upper()
                widget.setText(
                    f'<font color={color["font_3_green"]}>{word["word"][:word["n_letters"]]}</font>'
                    f'<font color={color["font_1"]}>{word["word"][word["n_letters"]:]}</font>')

    def display_msg(self, msg:str) -> None:
        MSG_TIME_DISPL = 1500
        X_MOVE = 900
        Y_MOVE = 405

        msg_label = QLabel(self)
        msg_label.setText(msg)

        msg_label.move(X_MOVE, Y_MOVE)
        msg_label.setStyleSheet(detailed_style["msg_label"])
        msg_label.adjustSize()

        msg_label.show()
        QtCore.QTimer.singleShot(MSG_TIME_DISPL, msg_label.deleteLater)

    def display_end_game_frame(self, msg, word) -> None:
        # TODO reorganise the function so it would be shorter
        # TODO fix width of the frame if word is long ("stowarzyszenie" f.ex.)
        # TODO blur main window while displaying end_game_frame

        X_WIDTH = 400
        Y_HEIGHT = X_WIDTH
        X_MOVE = 850
        Y_MOVE = 200

        # init frame
        self.end_game_frame = QFrame(self)
        self.end_game_frame.move(X_MOVE, Y_MOVE)
        self.end_game_frame.setMinimumSize(X_WIDTH, Y_HEIGHT)
        # self.end_game_frame.set
        self.end_game_frame.show()
        self.end_game_frame.setStyleSheet(detailed_style["end_game_frame"])


        # creating frame widgets
        msg_label = QLabel(msg)
        end_game_label = QLabel(Text.GAME_END)
        word_label =QLabel(word.upper())

        restart_button = QtWidgets.QPushButton("Zagraj jeszcze raz")
        restart_button.clicked.connect(self.reset_game)

        exit_button = QtWidgets.QPushButton("Wyjdź z gry")
        exit_button.clicked.connect(self.close)

        widgets = [msg_label, end_game_label, word_label, restart_button, exit_button]
        self.get_end_game_frame_widgets(widgets)


        layout = QtWidgets.QVBoxLayout(self.end_game_frame)
        layout.addWidget(msg_label, 1)
        layout.addWidget(end_game_label, 1)
        layout.addWidget(word_label, 3)
        layout.addWidget(restart_button, 1)
        layout.addWidget(exit_button, 1)

    def get_end_game_frame_widgets(self, widgets: list) -> list:
        FONT = AppFont(FontSize.END_GAME_FRAME)

        for widget in widgets:
            widget.setFont(FONT)
            if isinstance(widget, QLabel):
                widget.setAlignment(Qt.AlignCenter)
                widget.setStyleSheet(detailed_style["end_game_label"])

        font = AppFont(FontSize.END_GAME_WORD)
        widgets[2].setFont(font)

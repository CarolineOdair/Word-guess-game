from PyQt5 import Qt, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame

from .config import FontSize, Text
from .config import color, detailed_style, labels_features
from .connect import CurrentGameDataAnalyzer, WordStatus
from .widgets import QEndGameFrame, QGuessedWordsLabel, QMsgLabel, QNoSpacingVBoxLayout, QTypicalLabel, QTypingLine


class WrongListIdGiven(Exception):
    pass

class App(QtWidgets.QMainWindow):
    MAX_CHANCES = 15
    LEFT_CHANCE_PATH = ".\static\grey_circle.svg"
    LOST_CHANCE_PATH = ".\static\yellow_circle.svg"

    def __init__(self, words:list):
        super().__init__()
        self.words = words
        self.setWindowTitle(Text.WINDOW_TITLE)
        self.setWindowState(Qt.WindowMaximized)
        self.init_data()
        self.init_UI()

    def init_data(self) -> None:
        self.LEFT_CHANCES = 15
        self.connector = CurrentGameDataAnalyzer(self.words)
        self.main_word = self.connector.main_word["word"]
        # self.main_word = "stowarzyszenie"
        print(self.main_word)

    def init_UI(self) -> None:
        game_name_label = QTypicalLabel(text=Text.GAME_NAME, font_size=FontSize.GAME_NAME)

        main_frame = QFrame()
        self.main_frame_config(main_frame)

        window_layout = QNoSpacingVBoxLayout()
        window_layout.addWidget(game_name_label, 1)
        window_layout.addWidget(main_frame, 8)

        self.root_widget = QtWidgets.QWidget(self)
        self.root_widget.setLayout(window_layout)
        self.setCentralWidget(self.root_widget)

    def main_frame_config(self, frame: QFrame) -> None:
        self.left_frame = QFrame()
        self.dot_layout = QNoSpacingVBoxLayout(self.left_frame)
        self.add_chances_vis()

        self.right_frame = QFrame()
        self.right_frame_config()

        main_layout = QtWidgets.QHBoxLayout(frame)
        main_layout.addWidget(self.left_frame, 1)
        main_layout.addWidget(self.right_frame, 9)

    def right_frame_config(self) -> None:
        guessing_frame = QFrame()
        self.guessing_frame_config(guessing_frame)

        alphabet_label = QTypicalLabel(text=Text.ALPHABET,
                                       font_size=FontSize.ALPHABET, style_sheet=detailed_style["alphabet_label"])

        layout = QtWidgets.QVBoxLayout(self.right_frame)
        layout.addWidget(guessing_frame, 10)
        layout.addWidget(alphabet_label, 1)

    def guessing_frame_config(self, frame: QFrame) -> None:
        self.upper_words_frame = QFrame()
        self.upper_layout = QNoSpacingVBoxLayout(self.upper_words_frame)
        self.init_words_labels(self.upper_layout, labels_features[::-1])

        self.typing_editline = QTypingLine()
        self.typing_editline.returnPressed.connect(self.enter_pressed_action)

        self.lower_words_frame = QFrame()
        self.down_layout = QNoSpacingVBoxLayout(self.lower_words_frame)
        self.init_words_labels(self.down_layout, labels_features)

        layout = QNoSpacingVBoxLayout(frame)
        layout.addWidget(self.upper_words_frame, 6)
        layout.addWidget(self.typing_editline, 1, Qt.AlignHCenter)
        layout.addWidget(self.lower_words_frame, 6)

    def init_words_labels(self, layout: QtWidgets.QLayout, features:list) -> None:
        for feat in features:
            h = feat["height"]
            op = feat["opacity"]
            f_size = feat["size"]
            label = QGuessedWordsLabel(height=h, opacity=op, font_size=f_size)
            layout.addWidget(label)

    def turn_off_root_widget_opacity(self, turn_off: bool) -> None:
        self.opacity = QtWidgets.QGraphicsOpacityEffect()
        self.opacity.setOpacity(0.3)
        self.root_widget.setGraphicsEffect(self.opacity)
        self.opacity.setEnabled(turn_off)

    def enter_pressed_action(self) -> None:
        # get typed word
        word = self.typing_editline.text().lower()
        # connect with db and return word info -> status, id_, list, of words
        resp = self.connector.check_word(word)
        # clear edit line
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

    def add_chances_vis(self) -> None:
        self.reset_layout(self.dot_layout)

        for i in range(self.MAX_CHANCES):
            label = QtWidgets.QLabel()
            if i < self.MAX_CHANCES - self.LEFT_CHANCES:
                pixmap = QtGui.QPixmap(self.LOST_CHANCE_PATH)
            else:
                pixmap = QtGui.QPixmap(self.LEFT_CHANCE_PATH)
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)

            self.dot_layout.addWidget(label)

    def reset_layout(self, layout: QtWidgets.QLayout) -> None:
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def display_msg(self, msg:str) -> None:
        msg_label = QMsgLabel(self, msg)
        msg_label.show()

    def display_end_game_frame(self, msg, word) -> None:
        # TODO fix width of the frame if word is long ("stowarzyszenie" f.ex.)

        self.turn_off_root_widget_opacity(True)
        self.end_game_frame = QEndGameFrame(self, msg=msg, word=word)
        self.end_game_frame.restart_button.clicked.connect(self.reset_game)
        self.end_game_frame.exit_button.clicked.connect(self.close)
        self.end_game_frame.show()

    def reset_game(self) -> None:
        self.end_game_frame.close()
        self.end_game_frame.deleteLater()

        self.init_data()

        self.turn_off_root_widget_opacity(False)
        self.reset_layout(self.upper_layout)
        self.reset_layout(self.down_layout)
        self.init_words_labels(self.upper_layout, labels_features[::-1])
        self.init_words_labels(self.down_layout, labels_features)
        self.add_chances_vis()

import ctypes

from PyQt5 import Qt, QtGui, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFrame

from .config import FontSize, Text
from .config import color, detailed_style, labels_features, main_style
from .connect import CurrentGameDataAnalyzer, WordStatus
from .window_widgets import QGuessedWordsLabel, QNoSpacingVBoxLayout, QTypicalLabel, QTypingLine
from .pop_up_widgets import QEndGameFrame, QMsgLabel


class WrongListIdGiven(Exception):
    pass

class App(QtWidgets.QMainWindow):
    MAX_CHANCES = 15
    LEFT_CHANCE_PATH = ".\static\grey_circle.svg"
    LOST_CHANCE_PATH = ".\static\yellow_circle.svg"
    ICON = ".\static\icon.ico"

    def __init__(self, words:list):
        super().__init__()
        self.words = words

        self.setWindowState(Qt.WindowMaximized)
        self.set_icons_and_title()

        self.init_data()
        self.init_UI()

        self.setStyleSheet(main_style)

    def init_data(self) -> None:
        """ Configure data that has to be configured every time game starts. """
        # chances for entering invalid words
        self.LEFT_CHANCES = 15
        # new CurrentGameDataAnalyzer object
        self.connector = CurrentGameDataAnalyzer(self.words)
        # word to be guessed
        self.main_word = self.connector.main_word["word"]

    def set_icons_and_title(self):
        # window title and icon
        self.setWindowTitle(Text.WINDOW_TITLE)
        self.setWindowIcon(QtGui.QIcon(self.ICON))
        # taskbar icon, copied from StackOverflow
        my_app_id = u'mycompany.myproduct.subproduct.version'
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(my_app_id)

    def init_UI(self) -> None:
        """ Init user interface needed while opening the window. """
        # label with game name
        game_name_label = QTypicalLabel(text=Text.GAME_NAME, font_size=FontSize.GAME_NAME)

        # main frame displaying info about current game
        main_frame = QFrame()
        self.main_frame_config(main_frame)

        # layout
        window_layout = QNoSpacingVBoxLayout()
        window_layout.addWidget(game_name_label, 1)
        window_layout.addWidget(main_frame, 9)

        # set root_widget as a central, main widget of a window
        self.root_widget = QtWidgets.QWidget(self)
        self.root_widget.setLayout(window_layout)
        self.setCentralWidget(self.root_widget)

    def main_frame_config(self, frame: QFrame) -> None:
        """ Config frame displaying left chances and guessing frame. """
        # left, 'dot' frame with left chances
        self.left_frame = QFrame()
        self.dot_layout = QNoSpacingVBoxLayout(self.left_frame)
        self.add_chances_vis()

        # right, 'guessing' frame
        self.right_frame = QFrame()
        self.right_frame_config()

        # layout
        main_layout = QtWidgets.QHBoxLayout(frame)
        main_layout.addWidget(self.left_frame, 1)
        main_layout.addWidget(self.right_frame, 9)

    def right_frame_config(self) -> None:
        """ Config frame displaying guessing frame and label with alphabet. """
        # guessing frame - display word being typed in a moment and already entered ones
        guessing_frame = QFrame()
        self.guessing_frame_config(guessing_frame)

        # label with alphabet
        alphabet_label = QTypicalLabel(text=Text.ALPHABET,
                                       font_size=FontSize.ALPHABET, style_sheet=detailed_style["alphabet_label"])

        # layout
        layout = QtWidgets.QVBoxLayout(self.right_frame)
        layout.addWidget(guessing_frame, 10)
        layout.addWidget(alphabet_label, 1)

    def guessing_frame_config(self, frame: QFrame) -> None:
        """ Config frame displaying word being typed in a moment and already entered ones """
        # frame above typing line
        self.upper_words_frame = QFrame()
        self.upper_layout = QNoSpacingVBoxLayout(self.upper_words_frame)
        self.init_words_labels(self.upper_layout, labels_features[::-1])

        # typing line
        self.typing_editline = QTypingLine()
        self.typing_editline.returnPressed.connect(self.enter_pressed_action)

        # frame below typing line
        self.lower_words_frame = QFrame()
        self.down_layout = QNoSpacingVBoxLayout(self.lower_words_frame)
        self.init_words_labels(self.down_layout, labels_features)

        # layout
        layout = QNoSpacingVBoxLayout(frame)
        layout.addWidget(self.upper_words_frame, 6)
        layout.addWidget(self.typing_editline, 1, Qt.AlignHCenter)
        layout.addWidget(self.lower_words_frame, 6)

    def init_words_labels(self, layout: QtWidgets.QLayout, properties:list) -> None:
        """ Looping through given properties create labels with such properties and add them to given layout. """
        for prop in properties:
            h = prop["height"]
            op = prop["opacity"]
            f_size = prop["size"]
            label = QGuessedWordsLabel(height=h, opacity=op, font_size=f_size)
            layout.addWidget(label)

    def turn_off_root_widget_opacity(self, turn_off: bool) -> None:
        """ Turn on and off root_widget's opacity so it's fully or partly visible. """
        self.opacity = QtWidgets.QGraphicsOpacityEffect()
        self.opacity.setOpacity(0.3)
        self.root_widget.setGraphicsEffect(self.opacity)
        self.opacity.setEnabled(turn_off)

    def fix_widget_window_pos(self, widget, width:int = 2, height:int = 2):
        """
        Move widget to 1/width of a window and 1/height of a window.
        Default values (width=2 and height=2) center the widget.
        """
        x_move = self.width()/width - widget.width()/width
        y_move = self.height()/height - widget.height()/height
        widget.move(x_move, y_move)

    def enter_pressed_action(self) -> None:
        """ Action after pressing enter. """

        # get typed word
        word = self.typing_editline.text().lower().strip()
        # connect with db and return word info -> status, id_, list of words, list's id
        resp = self.connector.check_word_and_get_info(word)
        # clear edit line
        self.typing_editline.clear()

        # depending on word_status
        # word not in db
        if resp["status"] == WordStatus.UNKNOWN:
            self.display_msg(Text.WORD_UNKNOWN)

        # word has already been entered
        elif resp["status"] == WordStatus.ALREADY_GUESSED:
            self.display_msg(Text.WORD_ALREADY_GUESSED)

        # word is equal to the main_word
        elif resp["status"] == WordStatus.MAIN:
            # game ends
            self.display_end_game_frame(Text.WIN, self.main_word)
            return

        # word hasn't been entered but is not the main_word
        elif resp["status"] == WordStatus.NEW:

            if self.LEFT_CHANCES == 0:  # if no more chances
                # game ends
                self.display_end_game_frame(Text.LOST, self.main_word)
                return

            else:  # if still have some chances
                # subtract one chance
                self.LEFT_CHANCES -= 1
                # update ui
                self.update_(resp["list"], resp["list_id"])

    def update_(self, word_list: list, list_id: int) -> None:
        """ Update ui after entering new word """
        # update left, 'dot' frame
        self.add_chances_vis()

        # get prepared list of words which have to be displayed
        turn_list = self.get_current_turn_list(word_list, list_id)

        # update one - upper or down frame depending on list id
        if list_id == 0:
            self.update_word_ui(turn_list[-5:], self.upper_layout)
        elif list_id == 1:
            self.update_word_ui(turn_list[:5], self.down_layout)
        else:
            raise WrongListIdGiven(f"List id must be `0` for upper list and `1` for lower list, not given `{list_id}`.")

    def get_current_turn_list(self, word_list:list, list_id:int) -> list:
        """ Prepare list of words which have to be displayed in current turn. """

        empty_word = {'word': '', 'id': 0, 'n_letters': 0}

        turn_list = word_list.copy()

        # list has to have at least 5 elements, otherwise frame will be displayed incorrect
        while len(turn_list) < 5:
            if list_id == 0:  # if upper list, empty elements have to be added on the beginning
                turn_list.insert(0, empty_word)

            elif list_id == 1:  # if down list, empty elements have to be added on the end
                turn_list.append(empty_word)

            else:
                raise WrongListIdGiven(
                    f"List id must be `0` for upper list and `1` for down list, not given `{list_id}`.")

        return turn_list

    def update_word_ui(self, turn_list:list, layout:QtWidgets.QLayout) -> None:
        """ Update already guessed words frame. """
        widgets = (layout.itemAt(i).widget() for i in range(layout.count()))

        # loop through widgets and list of words
        for widget, word in zip(widgets, turn_list):
            if isinstance(widget, QtWidgets.QLabel):  # only if widget is a label
                word["word"] = word["word"].upper()
                # display word in proper colors
                # green for the n first letters which are the same for the current word and main_word
                widget.setText(
                    f'<font color={color["font_3_green"]}>{word["word"][:word["n_letters"]]}</font>'
                    f'<font color={color["font_1"]}>{word["word"][word["n_letters"]:]}</font>')

    def add_chances_vis(self) -> None:
        """ Change visual representation of left changes """
        # delete all widgets from a layout
        self.reset_layout(self.dot_layout)

        for i in range(self.MAX_CHANCES):
            # prepare pixmap from a picture
            if i < self.MAX_CHANCES - self.LEFT_CHANCES:  # for used chances
                pixmap = QtGui.QPixmap(self.LOST_CHANCE_PATH)
            else:  # for left chances
                pixmap = QtGui.QPixmap(self.LEFT_CHANCE_PATH)

            # prepare label, add pixmap and set alignment
            label = QtWidgets.QLabel()
            label.setPixmap(pixmap)
            label.setAlignment(Qt.AlignCenter)

            # add label to the layout
            self.dot_layout.addWidget(label)

    def reset_layout(self, layout: QtWidgets.QLayout) -> None:
        """ Reset given layout from all widgets to the init form. """
        for i in reversed(range(layout.count())):
            layout.itemAt(i).widget().setParent(None)

    def display_msg(self, msg:str) -> None:
        """ Display label with given message. """
        msg_label = QMsgLabel(self, msg)
        self.fix_widget_window_pos(msg_label, width=1.8, height=2.5)
        msg_label.show()

    def display_end_game_frame(self, msg, word) -> None:
        """ Display end game frame and change root_widget (in main window) visual settings """
        # turn on lower opacity
        self.turn_off_root_widget_opacity(True)

        # create frame and connect its buttons to function
        self.end_game_frame = QEndGameFrame(self, fail_or_win_msg=msg, main_word=word)
        self.end_game_frame.restart_button.clicked.connect(self.reset_game)
        self.end_game_frame.exit_button.clicked.connect(self.close)
        self.fix_widget_window_pos(self.end_game_frame)
        self.end_game_frame.show()

    def reset_game(self) -> None:
        """ Reset game settings """
        # close and delete end game frame
        self.end_game_frame.close()
        self.end_game_frame.deleteLater()

        # init new data - for the new game
        self.init_data()

        # turn on 100% opacity
        self.turn_off_root_widget_opacity(False)

        # display updated chances (max chances)
        self.add_chances_vis()

        # delete labels displaying already guessed words and init them (empty)
        self.reset_layout(self.upper_layout)
        self.init_words_labels(self.upper_layout, labels_features[::-1])
        self.reset_layout(self.down_layout)
        self.init_words_labels(self.down_layout, labels_features)

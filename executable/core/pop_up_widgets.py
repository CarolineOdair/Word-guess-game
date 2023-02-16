from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFrame, QLabel

from .config import AppFont, FontSize, Text, detailed_style
from .window_widgets import QTypicalLabel


class QMsgLabel(QLabel):
    """
    Label appearing for specified time.
    In Word-guessing-game is used for displaying messages to user that
    their word has been already typed or is not present in database.
    """
    DISPLAY_TIME = 1500
    X_MOVE = 900
    Y_MOVE = 405
    FONT = AppFont(FontSize.END_GAME_FRAME)

    def __init__(self, parent=None, text:str = ""):
        QLabel.__init__(self, parent=parent)
        self.setText(text)
        self.move(self.X_MOVE, self.Y_MOVE)
        self.setStyleSheet(detailed_style["msg_label"])
        self.adjustSize()
        QtCore.QTimer.singleShot(self.DISPLAY_TIME, self.deleteLater)

class QEndGameFrame(QFrame):
    """
    Word-guess-game's end frame with message to user:
    - if their failed or won,
    - what was the main word (the one to be guessed)
    and two buttons by default prepared to be connected to methods:
    - exit
    - restart
    """
    X_WIDTH = 400
    Y_HEIGHT = X_WIDTH
    X_MOVE = 750
    Y_MOVE = 230
    FONT = AppFont(FontSize.END_GAME_FRAME)

    def __init__(self, parent=None, **kwargs):
        QFrame.__init__(self, parent=parent)
        self.restart_button = QtWidgets.QPushButton()
        self.exit_button = QtWidgets.QPushButton()
        self.init_UI(**kwargs)

    def init_UI(self, fail_or_win_msg:str, main_word:str, word_sound_msg:str = Text.WORD_SOUNDED) -> None:
        """
        Init graphical interface: frame config, widgets (3 labels and 2 buttons), their style and layout
        """
        # main frame config
        self.move(self.X_MOVE, self.Y_MOVE)
        self.setMinimumSize(self.X_WIDTH, self.Y_HEIGHT)
        self.setStyleSheet(detailed_style["end_game_frame"])

        # init and config labels
        msg_label = QTypicalLabel(text=fail_or_win_msg, font_size=FontSize.END_GAME_FRAME,
                                  style_sheet=detailed_style["end_game_label"])

        end_game_label = QTypicalLabel(text=word_sound_msg, font_size=FontSize.END_GAME_FRAME,
                                       style_sheet=detailed_style["end_game_label"])

        word_label = QTypicalLabel(text=main_word.upper(), font_size=FontSize.END_GAME_WORD,
                                   style_sheet=detailed_style["end_game_label"])

        # init and config buttons
        self.restart_button.setText("Zagraj jeszcze raz")
        self.restart_button.setFont(self.FONT)

        self.exit_button.setText("Wyjdź z gry")
        self.exit_button.setFont(self.FONT)

        self.resize_frame_width_by_widget_text(word_label)

        # init layout and add above created widgets with proper height proportions
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(msg_label, 1)
        layout.addWidget(end_game_label, 1)
        layout.addWidget(word_label, 3)
        layout.addWidget(self.restart_button, 1)
        layout.addWidget(self.exit_button, 1)

    def resize_frame_width_by_widget_text(self, widget):
        """ Resize main frame width if default one is too narrow. """
        font_metrics = widget.fontMetrics()
        text_length = QtGui.QFontMetrics(font_metrics).width(widget.text())
        if self.width() < text_length * 1.2:
            self.setFixedWidth(text_length * 1.2)

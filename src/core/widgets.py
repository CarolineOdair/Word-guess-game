from PyQt5 import Qt, QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QLineEdit, QFrame, QVBoxLayout

from .config import AppFont, FontSize, detailed_style


class QNoSpacingVBoxLayout(QVBoxLayout):
    def __init__(self, parent=None):
        super(QNoSpacingVBoxLayout, self).__init__(parent)
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

class QTypicalLabel(QLabel):
    def __init__(self, parent=None, text:str ="", font_size:int =12, style_sheet:str =None):
        super().__init__(parent=parent)
        font = AppFont(font_size)
        self.setFont(font)
        self.setText(text)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(style_sheet)

class QGuessedWordsLabel(QLabel):
    def __init__(self, height:int, opacity:float, font_size:int):
        super().__init__()
        self.setFixedHeight(height)
        self.setText("")
        self.setAlignment(Qt.AlignHCenter)

        opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        opacity_effect.setOpacity(opacity)
        self.setGraphicsEffect(opacity_effect)

        font = AppFont(font_size)
        self.setFont(font)

class QTypingLine(QLineEdit):
    WIDTH = 800
    FONT = AppFont(FontSize.EDITLINE)
    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent=parent)
        self.setFixedWidth(self.WIDTH)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(self.FONT)

class QMsgLabel(QLabel):
    MSG_TIME_DISPL = 1500
    X_MOVE = 900
    Y_MOVE = 405
    FONT = AppFont(FontSize.END_GAME_FRAME)
    def __init__(self, parent=None, text:str=""):
        QLabel.__init__(self, parent=parent)
        self.setText(text)
        self.move(self.X_MOVE, self.Y_MOVE)
        self.setStyleSheet(detailed_style["msg_label"])
        self.adjustSize()
        QtCore.QTimer.singleShot(self.MSG_TIME_DISPL, self.deleteLater)

class QEndGameFrame(QFrame):
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

    def init_UI(self, msg:str, word:str) -> None:
        self.move(self.X_MOVE, self.Y_MOVE)
        self.setMinimumSize(self.X_WIDTH, self.Y_HEIGHT)
        self.setStyleSheet(detailed_style["end_game_frame"])

        msg_label = QTypicalLabel(text=msg, font_size=FontSize.END_GAME_FRAME,
                                  style_sheet=detailed_style["end_game_label"])

        end_game_label = QTypicalLabel(text="Szukane słowo brzmiało:", font_size=FontSize.END_GAME_FRAME,
                                  style_sheet=detailed_style["end_game_label"])

        word_label = QTypicalLabel(text=word.upper(), font_size=FontSize.END_GAME_WORD,
                                  style_sheet=detailed_style["end_game_label"])

        self.restart_button.setText("Zagraj jeszcze raz")
        self.restart_button.setFont(self.FONT)

        self.exit_button.setText("Wyjdź z gry")
        self.exit_button.setFont(self.FONT)

        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(msg_label, 1)
        layout.addWidget(end_game_label, 1)
        layout.addWidget(word_label, 3)
        layout.addWidget(self.restart_button, 1)
        layout.addWidget(self.exit_button, 1)
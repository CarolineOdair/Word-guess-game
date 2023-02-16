from PyQt5 import Qt, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QLineEdit, QVBoxLayout

from .config import AppFont, FontSize


class QNoSpacingVBoxLayout(QVBoxLayout):
    """ Qt5 QVBoxLayout with no Spacing and no margins. """
    def __init__(self, parent=None):
        super(QNoSpacingVBoxLayout, self).__init__(parent)
        self.setSpacing(0)
        self.setContentsMargins(0, 0, 0, 0)

class QTypicalLabel(QLabel):
    """ Qt5 QLabel with specified properties for the app. """
    def __init__(self, parent=None, text:str = None, font_size:int = 12, style_sheet:str = None):
        super().__init__(parent=parent)
        font = AppFont(font_size)
        self.setFont(font)
        self.setText(text)
        self.setAlignment(Qt.AlignCenter)
        self.setStyleSheet(style_sheet)

class QGuessedWordsLabel(QTypicalLabel):
    """
    QTypicalLabel with specified properties (height, opacity and font's size).
    Created with thought of generating labels for already guessed words in Word-guess-game.
    """
    def __init__(self, opacity:float, height:int, font_size:int, parent=None):
        QTypicalLabel.__init__(self, parent, font_size=font_size)
        # height
        self.setFixedHeight(height)
        # opacity effect
        opacity_effect = QtWidgets.QGraphicsOpacityEffect()
        opacity_effect.setOpacity(opacity)
        self.setGraphicsEffect(opacity_effect)

class QTypingLine(QLineEdit):
    """ Qt5 QLineEdit with specified properties (font, width and alignment). """
    WIDTH = 800
    FONT = AppFont(FontSize.EDITLINE)

    def __init__(self, parent=None):
        QLineEdit.__init__(self, parent=parent)
        self.setFixedWidth(self.WIDTH)
        self.setAlignment(Qt.AlignCenter)
        self.setFont(self.FONT)

from PyQt5.QtGui import QFont

class Text:
    # window title
    WINDOW_TITLE = " --  Słownikowo dla Kuby  -- "
    # inside window
    GAME_NAME = "SŁOWNIKOWO"
    TYPING_EDITLINE = "WPISZ SŁOWO"
    ALPHABET = " A Ą B C D E Ę F G H I J K L Ł M N Ń O Ó P R S Ś T U W X Y Z Ź Ż "
    # on pop-up widgets - on msg_labels
    WORD_UNKNOWN = "Brak podanego słowa w bazie"
    WORD_ALREADY_GUESSED = "To słowo zostało już wpisane"
    # on pop-up widgets - on end_game_frame
    WORD_SOUNDED = "Szukane słowo brzmiało:"
    WIN = "Brawo! Wygrałeś!"
    LOST = "Nie tym razem."

class AppFont(QFont):
    """ Font (family, weight, thickness, size) used in the app. """
    def __init__(self, font_size):
        super(AppFont, self).__init__()
        self.setFamily("Segoe UI")
        self.setStyleHint(self.SansSerif)
        self.setWeight(700)
        self.setBold(True)
        self.setPointSize(font_size)

class FontSize:
    """ Font sizes used in the app. """
    GAME_NAME = 45
    EDITLINE = 32
    ALPHABET = 25
    END_GAME_FRAME = 15
    END_GAME_WORD = 25


labels_features = [{"size": 35, "opacity": 0.85, "height": 70}, {"size": 30, "opacity": 0.80, "height": 65},
                   {"size": 25, "opacity": 0.70, "height": 55}, {"size": 20, "opacity": 0.5, "height": 45},
                   {"size": 15, "opacity": 0.3, "height": 40}]

color = {
    "background": "#202020",  # very dark gray (mostly black)
    "font_1": "#F9F9F9",  # very light gray (mostly white)
    "font_2_grey": "#606060",  # very dark gray
    "font_3_green": "#3F9442",  # dark moderate lime green
    "warning_yellow": "#DCC966"  # soft yellow
    }

main_style = f"""

    QWidget{{
        background: {color["background"]};
        color: {color["font_1"]};
        }}
        
    QLineEdit{{
        color: {color["font_1"]};
        border: 2px solid {color["warning_yellow"]};
        border-radius: 3px;
        padding: 3px 3px 3px 3px;
        text-transform: uppercase;
        }}
        
    QPushButton{{
        color: {color["font_1"]};
        border: 2px solid {color["font_2_grey"]};
        border-radius: 3px;
        padding: 3px 3px 3px 3px;
        }}
        
    QPushButton:hover{{
        color: {color["font_2_grey"]};
        }}
        
    """

detailed_style = {
    "msg_label":
        f"""border-style: solid;
        border-width: 2px;
        border-radius: 5px;
        border-color: {color["font_2_grey"]};
        background: {color["background"]};
        font-size: 25px;
        padding: 5px 5px 5px 5px;
        """,

    "alphabet_label":
        f"color: {color['font_2_grey']};",

    "end_game_frame":
        f"""border-style: solid;
        border-width: 2px;
        border-radius: 5px;
        border-color: {color['warning_yellow']};
        background: {color['background']};
        padding: 5px 5px 5px 5px;""",

    "end_game_label":
        "border: none;"
}

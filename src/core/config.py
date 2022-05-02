from PyQt5.QtGui import  QFont

class Text:
    WINDOW_TITLE =  "SŁOWNIKOWO"
    GAME_NAME = "SŁOWNIKOWO"
    TYPING_EDITLINE = "WPISZ SŁOWO"
    ALPHABET = " A Ą B C D E Ę F G H I J K L Ł M N Ń O Ó P R S Ś T U W X Y Z Ź Ż "
    WORD_UNKNOWN =  "Brak podanego słowa w bazie"
    WORD_ALREADY_GUESSED = "To słowo zostało już wpisane"
    WIN = "Brawo! Wygrałeś!"
    LOST = "Nie tym razem."

class AppFont(QFont):
    def __init__(self, font_size):
        super(AppFont, self).__init__()
        self.setBold(True)
        self.setWeight(700)
        self.setFamily("Segoe UI")
        self.setStyleHint(self.SansSerif)
        self.setBold(True)
        self.setPointSize(font_size)

class FontSize:
    GAME_NAME = 45
    EDITLINE = 32
    ALPHABET = 25
    END_GAME_FRAME = 15
    END_GAME_WORD = 25


labels_features = [{"size": 35, "opacity": 0.85, "height": 70}, {"size": 30, "opacity": 0.80, "height": 65},
                   {"size": 25, "opacity": 0.70, "height": 55}, {"size": 20, "opacity": 0.5, "height": 45},
                   {"size": 15, "opacity": 0.3, "height": 40}]

color = {
    "background": "#202020",
    "font_1": "#F9F5F5",
    "font_2_grey": "#606060",
    "font_3_green": "#3F9442",
    "warning_yellow": "#DCC966"
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
        background: #FFFFFF;
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
        "border: none",

}

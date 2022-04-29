from utils import get_word_id_or_None

class WrongIdError(Exception):
    print("Something has gone really wrong. ")
    pass

class WordStatus:
    MAIN = "main_word"
    GUESSED = "already_guessed_word"
    NEW = "new_word"
    UNKNOWN = "word_not_in_db"


class LocalDb:
    URL = "https://betsapi.sraka.online/slowas?slowo="

    def __init__(self, word, id_):
        self.main_word = {"word": word, "id":id_}
        self.upper_list = []
        self.down_list = []
        self.already_guessed_words = []

    def check_word(self, word):
        if self.is_main_word(word):
            return {"word": word, "status": WordStatus.MAIN, "msg": "WYGRAŁEŚ"}
        elif self.has_been_already_typed(word):
            return {"word": word, "status": WordStatus.GUESSED, "msg": "JUŻ WPISAŁEŚ WCZEŚNIEJ TO SŁOWO"}

        id_ = get_word_id_or_None(word)
        if id_:
            self.already_guessed_words.append(word)
            word_list, list_id = self.get_list_of_words(word, id_)
            return ({"word": word, "status": WordStatus.NEW, "msg": "DODAJĘ", "list": word_list, "list_id": list_id})
        else:
            return ({"word": word, "status": WordStatus.UNKNOWN, "msg": "NIE MA TAKIEGO SŁOWA"})

    def is_main_word(self, word):
        if word == self.main_word["word"]:
            return True

    def has_been_already_typed(self, word):
        if word in self.already_guessed_words:
            return True

    def get_list_of_words(self, word, id_):
        word_dict = {"word": word, "id": id_, "n_letters": self.get_n_mutual_letters(word)}

        if id_ < self.main_word["id"]:
            self.upper_list =  self.append_and_sort_list(word_dict, self.upper_list)
            return (self.upper_list, "up")

        elif id_ > self.main_word["id"]:
            self.down_list =  self.append_and_sort_list(word_dict, self.down_list)
            return (self.down_list, "down")

        else:
            return WrongIdError()

    def get_n_mutual_letters(self, word: str) -> int:
        n_letters = 0
        for main_w_letter, guessed_w_letter in zip(self.main_word["word"], word):
            if main_w_letter == guessed_w_letter:
                n_letters += 1
            else:
                break
        return n_letters

    def append_and_sort_list(self, word_data, list_):
        list_.append(word_data)
        temp_list = sorted(list_, key=lambda x: x["id"])
        return temp_list

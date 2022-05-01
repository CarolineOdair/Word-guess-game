# from utils import get_word_id_or_None
import random
import requests


class WordStatus:
    MAIN = "main_word"
    ALREADY_GUESSED = "already_guessed_word"
    NEW = "new_word"
    UNKNOWN = "word_not_in_db"


class CurrentGameDataAnalyzer:
    URL = "https://betsapi.sraka.online/slowas?slowo="

    def __init__(self, words):
        word, id_ = self.get_main_word(words)
        self.main_word = {"word": word, "id":id_}
        self.upper_list = []
        self.down_list = []
        self.already_guessed_words = []

    def check_word(self, word: str) -> dict:
        """
        Check given word and return dictionary with it's data such as
        "word" (str): return given word,
        "status" (str): main/already_guessed/new/unknown,
        for new word dictionary contains also:
        "list" (list): list that contains given word,
        "list_id (int): id to tell them apart
        """

        # check if the given word is the one to be guessed
        if self.is_main_word(word):
            return {"word": word, "status": WordStatus.MAIN}
        # check if the given word has already been entered by user
        elif self.has_been_already_typed(word):
            return {"word": word, "status": WordStatus.ALREADY_GUESSED}

        id_ = self.get_word_id_or_None(word) # int for word in db, None for not found word
        # if word in db: id_ [int]
        if id_:
            self.already_guessed_words.append(word)
            word_list, list_id = self.get_list_of_words(word, id_)
            return ({"word": word, "status": WordStatus.NEW, "list": word_list, "list_id": list_id})
        # else - word not in db: id_ [None]
        else:
            return ({"word": word, "status": WordStatus.UNKNOWN})

    def draw_main_word(self, words: list) -> str:
        num_of_words = len(words)
        word_number = random.randrange(0, num_of_words - 1)
        main_word = words[word_number].strip()
        return main_word.lower()

    def get_word_id_or_None(self, word: str) -> (int or None):
        word_url = "https://betsapi.sraka.online/slowas?slowo="
        headers = {'Accept': 'application/json'}
        url = word_url + word
        req = requests.get(url, headers=headers)
        response = req.json()
        if len(response) == 0:
            return None
        else:
            id_ = response[0]["id"]
            return id_

    def get_main_word(self, words) -> (str, int or None):
        while True:
            word = self.draw_main_word(words)
            id_ = self.get_word_id_or_None(word)
            if id_:
                return (word, id_)

    def is_main_word(self, word: str) -> bool:
        """ Return `True` if the given word is the one to be guessed. """
        if word == self.main_word["word"]:
            return True

    def has_been_already_typed(self, word:str) -> bool:
        """ Return `True` if the given word has already been guessed. """
        if word in self.already_guessed_words:
            return True

    def get_list_of_words(self, word:str, id_:int) -> (list, int):
        """
        Using id_ modify list with words either before or after the main one.
        Return list and it's id (`0` for words before main one or `1` for the one after it).
        """
        # every word data
        word_dict = {"word": word, "id": id_, "n_letters": self.get_n_mutual_letters(word)}

        if id_ < self.main_word["id"]:
            self.upper_list =  self.append_and_sort_list(word_dict, self.upper_list)
            return (self.upper_list, 0)

        elif id_ > self.main_word["id"]:
            self.down_list =  self.append_and_sort_list(word_dict, self.down_list)
            return (self.down_list, 1)

    def get_n_mutual_letters(self, word: str) -> int:
        """ Return number of initial mutual letters in given and main word. """
        n_letters = 0
        for main_w_letter, guessed_w_letter in zip(self.main_word["word"], word):
            if main_w_letter == guessed_w_letter:
                n_letters += 1
            else:
                break
        return n_letters

    def append_and_sort_list(self, word_data:dict, words_list:list) -> list:
        """ Add word to given list. Return sorted list. """
        words_list.append(word_data)
        temp_list = sorted(words_list, key=lambda x: x["id"])
        return temp_list

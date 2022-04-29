import requests
import random

labels_features = [{"size": 35, "opacity": 1, "height": 70}, {"size": 30, "opacity": 0.85, "height": 65},
                   {"size": 25, "opacity": 0.75, "height": 55}, {"size": 20, "opacity": 0.6, "height": 45},
                   {"size": 15, "opacity": 0.5, "height": 40}]

def draw_main_word(words:list) -> str:
    num_of_words = len(words)
    word_number = random.randrange(0, num_of_words - 1)
    main_word = words[word_number].strip()
    return main_word.lower()

def get_word_id_or_None(word:str) -> (int or None):
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

def get_main_word(words:list):
    while True:
        word = draw_main_word(words)
        id_ = get_word_id_or_None(word)
        if id_:
            return (word, id_)
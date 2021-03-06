import requests
from bs4 import BeautifulSoup
import time

def main():
    words_processor = WordSearcherAndAnalyzer()
    words = words_processor.main()

    # save to csv file
    with open('..\src\static\word_list.csv', 'w', encoding="utf-8") as file:
        for word in words:
            file.write(word + '\n')

class WordSearcherAndAnalyzer:
    def __init__(self):
        self.pages = ["1-2000", "2001-4000", "4001-6000", "6001-8000", "8001-10000"]
        self.WIKI_URL = "https://pl.wiktionary.org/wiki/Indeks:Polski_-_Najpopularniejsze_s%C5%82owa_"
        self.SLOWNIKOWO_URL = "https://betsapi.sraka.online/slowas?slowo="
        self.HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0',
                   'Accept': 'application/json'}

    def main(self):
        """ Main function which gets and filter data """
        words = self.get_list_of_words(self.pages)
        words = self.filter_phrases(words)
        words = self.filter_too_short_words(words)
        words = self.check_if_words_in_database(words)
        return words

    def get_list_of_words(self, pages:list) -> list:
        """ Get words from wikipedia and return as a list """
        words_all = []
        for page in pages:
            url = self.WIKI_URL + page
            words = self.get_data(url)
            words_all.extend(words)
        return words_all

    def get_data(self, url:str) -> list:
        """ Get list of all words from a request """
        # make request
        req = requests.get(url, headers=self.HEADERS)
        req = req.text
        soup = BeautifulSoup(req, 'html.parser')

        # search in html
        table = soup.find("div", class_="mw-parser-output")
        p = table.find_all("p")[1]

        # make a list of words
        words = [word.text for word in p.find_all("a")]
        return words

    def filter_phrases(self, words:list) -> list:
        """ Dividing phrases into separate words """
        extended_words = []
        for word in words:
            if " " in word:
                current_words = word.split(" ")
                extended_words.extend(current_words)
            else:
                pass
                extended_words.append(word)
        return extended_words

    def filter_too_short_words(self, words:list) -> list:
        """ Remove words shorter than 3 letters """
        LENGHT = 3
        words_ = [word for word in words if len(word) > LENGHT]
        return words_

    def check_if_words_in_database(self, words:list) -> list:
        """
        Check if words are in slownikowo's database, return list with words which are there
        """
        start = time.time()
        i = 0
        words_ = []
        for x in range(0, len(words)):
            url = self.SLOWNIKOWO_URL + words[x]
            req = requests.get(url, headers=self.HEADERS)
            response = req.json()
            if len(response) > 0:
                words_.append(words[x])
                print(i)
                i += 1
        print(time.time()-start)
        return words_


if __name__ == "__main__":

    main()

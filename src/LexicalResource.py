from typing import List

# Class used to store information about each tweet: its sentiment e how many words of which sentiment are in that tweet
class LexicalResource:
    filename: str
    sentiment: str
    word_list: List[str]

    def __init__(self, filename: str, sentiment: str):
        self.filename = filename
        self.sentiment = sentiment
        self.word_list = []

    def __str__(self):
        lex_res_string = "LexicalResource: " + self.filename + \
                         "\n\t sentiment: " + self.sentiment + \
                         "\n\t wordlist: " + self.word_list.__str__()
        return lex_res_string

    def add_word(self, word: str):
        if not '_' in word:
            self.word_list.append(word)

    def add_word_list(self, word_list: List[str]):
        for word in word_list:
            if not '_' in word:
                self.word_list.append(word)

    def get_number_of_words(self) -> int:
        return len(self.word_list)
from typing import List, Set


# Class used to store information about each tweet: its sentiment e how many words of which sentiment are in that tweet
class LexicalResource:
    filename: str
    sentiment: str
    words: Set[str]

    def __init__(self, filename: str, sentiment: str, words: Set[str] = None):
        if words is None:
            words = set()
        self.filename = filename
        self.sentiment = sentiment
        self.words = words

    def __str__(self):
        lex_res_string = "LexicalResource: " + self.filename + \
                         "\n\t sentiment: " + self.sentiment + \
                         "\n\t wordlist: " + self.words.__str__()
        return lex_res_string

    def __eq__(self, other):
        if isinstance(other, LexicalResource):
            return self.filename == other.filename
        return False

    def add_word(self, word: str):
        if not '_' in word:
            self.words.add(word)

    def add_word_list(self, word_list: List[str]):
        for word in word_list:
            if not '_' in word:
                self.words.add(word)

    def get_number_of_words(self) -> int:
        return len(self.words)

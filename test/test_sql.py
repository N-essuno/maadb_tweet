from typing import List

from src.LexicalResource import LexicalResource
from src.MySql import DBConnection, Token
from src.Tweet import Tweet

# test tokens
token1 = Token("ciao", "word")
token1_copy = Token("ciao", "word")
token2 = Token("ciao2", "word")
token_list = [token1, token2]

# test lexical resources
lex_res_1: LexicalResource = LexicalResource("filename1", "Joy")
lex_res_2: LexicalResource = LexicalResource("filename2", "Sadness")

lex_res_1.add_word("angry")
lex_res_1.add_word("banana")
lex_res_1.add_word("Gianguria")

lex_res_2.add_word("pinocchio")
lex_res_2.add_word("ginocchio")

# test tweets
tweet1: Tweet = Tweet("i'm getting shapy again 😑 😐 😕 😔 😞 😣 😖 😩😫", 5, "Sadness")
tweet2: Tweet = Tweet("angry Pensa is imho imho imho imho imho imho imho imho imho imho imho angry pensa sad #gervaso "
                      "banana no", 0, "Joy")
tweet3: Tweet = Tweet("i am embarrassed that you were even with me lol. #yuck #fuckyou ", 0, "Sadness")


def test_db_connection():
    db_connection = DBConnection()
    db_connection.connect_to_db()
    return db_connection


def test_select_tokens_from_list() -> List[Token]:
    connection = test_db_connection()
    tokens = connection.select_tokens_from_list(token_list)
    for token in tokens:
        print(token)
    return tokens


def test_insert_lexical_resources():
    connection = test_db_connection()
    connection.insert_lexical_resources([lex_res_1, lex_res_2])


def test_insert_contents(content_type: str):
    connection = test_db_connection()
    contents = ["oh", "bella", "ciao", "miau"]
    connection.insert_contents(contents, content_type)


def test_insert_tweets():
    connection = test_db_connection()
    connection.insert_tweets([tweet1, tweet2, tweet3])


def test_delete_all_tweets():
    connection = test_db_connection()
    connection.delete_tweets()


def test_delete_lex_res():
    connection = test_db_connection()
    connection.delete_lex_res()


def test_delete_contents(content_type: str):
    connection = test_db_connection()
    connection.delete_contents(content_type)


def test_insert_delete_lex_res():
    test_insert_lexical_resources()
    test_delete_lex_res()


def test_pipeline1():
    conn = test_db_connection()
    result = conn.pipeline1(5, "Joy", "word")
    print(result)


def test_pipeline2():
    conn = test_db_connection()
    words = conn.pipeline2(lex_res_1)
    print(words)


def test_pipeline3():
    conn = test_db_connection()
    words = conn.pipeline3("Joy")
    print(words)


if __name__ == "__main__":
    test_pipeline1()

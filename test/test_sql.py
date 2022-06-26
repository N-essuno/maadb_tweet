from src.LexicalResource import LexicalResource
from src.MySqlQueries import DBConnection


def test_db_connection():
    db_connection = DBConnection()
    db_connection.connect_to_db()
    return db_connection


def test_insert_lexical_resources():
    lex_res_1: LexicalResource = LexicalResource("filename1", "sentiment1")
    lex_res_2: LexicalResource = LexicalResource("filename2", "sentiment2")

    lex_res_1.add_word("pino")
    lex_res_1.add_word("gino")

    lex_res_2.add_word("pinocchio")
    lex_res_2.add_word("ginocchio")

    connection = test_db_connection()
    connection.insert_lexical_resources([lex_res_1, lex_res_2])


def test_delete_lex_res():
    connection = test_db_connection()
    connection.delete_lex_res()


if __name__ == "__main__":
    test_insert_lexical_resources()
    test_delete_lex_res()


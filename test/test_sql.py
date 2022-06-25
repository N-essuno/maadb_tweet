from src.MySqlQueries import DBConnection


def test_db_connection():
    db_connection = DBConnection()
    db_connection.connect_to_db()
    return db_connection


def test_insert_sentiment():
    connection = test_db_connection()
    connection.insert_sentiment("Pinocchio")


def test_delete_lex_res():
    connection = test_db_connection()
    connection.delete_lex_res()


if __name__ == "__main__":
    test_insert_sentiment()

from src.MySqlQueries import connect_to_db


def test_db_connection():
    connect_to_db()


if __name__ == "__main__":
    test_db_connection()

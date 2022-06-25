import sys
from typing import Tuple

import mariadb


class DBConnection:
    already_connected_mariadb = False
    cursor = None
    db_connection = None

    def connect_to_db(self):
        # Connect to MariaDB Platform
        if not self.already_connected_mariadb:
            try:
                self.db_connection = mariadb.connect(
                    user="root",
                    password="test",
                    host="localhost",
                    port=3306,
                    database="progetto"
                )
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
                sys.exit(1)

            # Get Cursor
            self.cursor = self.db_connection.cursor()

        self.cursor.execute("SHOW TABLES")

        for (table_name,) in self.cursor:
            print(table_name)

    def insert_sentiment(self, sentiment: str):
        insert_query = "INSERT INTO sentiment VALUES ('{}');".format(sentiment)
        self.launch_query(insert_query)

    def delete_lex_res(self):
        delete_query = "DELETE FROM lexicalresources"
        self.launch_query(delete_query)
        print(self.cursor.rowcount, "record(s) deleted")

    def launch_query(self, query):
        self.cursor.execute(query)
        self.db_connection.commit()


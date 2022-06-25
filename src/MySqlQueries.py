import sys

import mariadb

already_connected_mariadb = False


def connect_to_db():
    cur = None

    # Connect to MariaDB Platform
    if not already_connected_mariadb:
        try:
            conn = mariadb.connect(
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
        cur = conn.cursor()

    cur.execute("SHOW TABLES")

    for (table_name,) in cur:
        print(table_name)

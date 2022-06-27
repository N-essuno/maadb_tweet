import sys
from typing import List

import mariadb

from src.LexicalResource import LexicalResource
from src.Tweet import Tweet


def insert_int_or_string(query_string, value):
    if isinstance(value, int):
        query_string += str(value) + ","
    else:
        query_string += "'{}',".format(value)
    return query_string


def append_values_to_query(query_string, values):
    query_string += "("
    for value in values:
        query_string = insert_int_or_string(query_string, value)
    # remove last comma
    query_string = query_string[:-1]
    query_string += "), "
    return query_string


def convert_list_of_values_to_query_format(list_of_values: List[List]) -> str:
    query_string = ""

    # append all values except last
    for values in list_of_values[:-1]:
        query_string = append_values_to_query(query_string, values)
    query_string += "("

    # append last values followed by );
    for value in list_of_values[-1]:
        query_string = insert_int_or_string(query_string, value)
    query_string = query_string[:-1]

    query_string += ")"
    return query_string


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

        # self.cursor.execute("SHOW TABLES")
        #
        # for (table_name,) in self.cursor:
        #     print(table_name)

    def insert_lexical_resources(self, lexical_resources: List[LexicalResource]):
        lexical_resources_values = []
        for lexical_resource in lexical_resources:
            # compose values to insert
            name = lexical_resource.filename
            sentiment = lexical_resource.sentiment
            num_words = lexical_resource.get_number_of_words()

            lexical_resources_values.append([name, num_words, sentiment])

        lexical_resources_values_query_format = convert_list_of_values_to_query_format(lexical_resources_values)

        insert_query = "INSERT INTO lexicalresource (name, num_words, sentiment) VALUES {};".format(
            lexical_resources_values_query_format)

        self.launch_query(insert_query)
        print(self.cursor.rowcount, "record(s) inserted")

    def insert_tweets(self, tweets: List[Tweet]):
        for tweet in tweets:
            # insert tweet
            insert_tweet_query = "INSERT INTO tweet (sentiment) VALUES ('{}');".format(tweet.sentiment)
            print(insert_tweet_query)
            exit()
            words = tweet.words
            emojis = tweet.emojis
            emoticons = tweet.emoticons
            # insert words
            # insert emojis
            # insert emoticons


        # for lexical_resource in lexical_resources:
        #     # compose values to insert
        #     name = lexical_resource.filename
        #     sentiment = lexical_resource.sentiment
        #     num_words = lexical_resource.get_number_of_words()
        #
        #     lexical_resources_values.append([name, num_words, sentiment])
        #
        # lexical_resources_values_query_format = convert_list_of_values_to_query_format(lexical_resources_values)
        #
        # insert_query = "INSERT INTO lexicalresource (name, num_words, sentiment) VALUES {};".format(
        #     lexical_resources_values_query_format)
        #
        # self.launch_query(insert_query)
        # print(self.cursor.rowcount, "record(s) inserted")

    def delete_lex_res(self):
        delete_query = "DELETE FROM lexicalresource"
        self.launch_query(delete_query)
        print(self.cursor.rowcount, "record(s) deleted")

    def delete_tweets(self):
        # TODO delete tweet contents in cascade
        delete_query = "DELETE FROM tweets"
        self.launch_query(delete_query)
        print(self.cursor.rowcount, "record(s) deleted")

    def launch_query(self, query):
        self.cursor.execute(query)
        self.db_connection.commit()

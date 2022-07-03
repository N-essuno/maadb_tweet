import sys
from typing import List, Tuple, Dict

import mariadb
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursor

from src.LexicalResource import LexicalResource
from src.Token import Token
from src.Tweet import Tweet


def get_contents_of_tokens(tokens: List[Token]) -> List[str]:
    list_of_contents: List[str] = []
    for token in tokens:
        list_of_contents.append(token.content)
    return list_of_contents


def list_of_tokens_to_list_of_tuples(tokens: List[Token]) -> List[Tuple[str, str]]:
    list_of_tuples: List[Tuple[str, str]] = []
    for token in tokens:
        list_of_tuples.append((token.content, token.content_type))
    return list_of_tuples


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
    query_string += ")"
    return query_string


def convert_list_of_values_to_query_format(list_of_values: List[List]) -> str:
    query_string = ""

    # append all values except last
    for values in list_of_values[:-1]:
        query_string = append_values_to_query(query_string, values)
        query_string += ", "
    query_string += "("

    # append last values followed by );
    for value in list_of_values[-1]:
        query_string = insert_int_or_string(query_string, value)
    query_string = query_string[:-1]

    query_string += ")"
    return query_string


class DBConnection:
    already_connected_mariadb = False
    cursor: MySQLCursor = None
    db_connection: MySQLConnection = None

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
                self.db_connection.autocommit = False
            except mariadb.Error as e:
                print(f"Error connecting to MariaDB Platform: {e}")
                sys.exit(1)

            # Get Cursor
            self.cursor = self.db_connection.cursor()

        # self.cursor.execute("SHOW TABLES")
        #
        # for (table_name,) in self.cursor:
        #     print(table_name)

    def select_tokens_from_list(self, tokens: List[Token]) -> List[Token]:
        # returns tokens contents are already in db
        # for token in tokens:
        #     print(token)

        tokens_content = get_contents_of_tokens(tokens)

        select_query = "SELECT * FROM token WHERE content IN (%s);"

        # add tokens_content to select_query
        self.cursor.execute(select_query % ','.join(['%s'] * len(tokens_content)), tokens_content)
        select_result: List[Tuple] = self.cursor.fetchall()

        tokens_found: List[Token] = []
        for token_tuple in select_result:
            # append token to tokens_found
            token_found = Token(token_tuple[0], token_tuple[1])
            tokens_found.append(token_found)
        return tokens_found

    def insert_lexical_resources(self, lexical_resources: List[LexicalResource]):
        lexical_resources_values = []
        lexical_resources_words_values = []
        for lexical_resource in lexical_resources:
            # compose values to insert
            name = lexical_resource.filename
            sentiment = lexical_resource.sentiment
            num_words = lexical_resource.get_number_of_words()
            word_list = lexical_resource.word_list

            # append lexical resource record to insert
            lexical_resources_values.append([name, num_words, sentiment])

            for word in word_list:
                lexical_resources_words_values.append([name, word])

        insert_lex_res_query = "INSERT INTO lexicalresource (name, num_words, sentiment) VALUES (%s, %s, %s);"
        insert_lex_res_words_query = "INSERT INTO lexicalresourceword (lexicalresource, word) VALUES (%s, %s);"
        self.cursor.executemany(insert_lex_res_query, lexical_resources_values)
        print(self.cursor.rowcount, "lexical resource(s) inserted")
        self.cursor.executemany(insert_lex_res_words_query, lexical_resources_words_values)
        print(self.cursor.rowcount, "lexical resource word(s) inserted")
        self.db_connection.commit()

    def insert_contents(self, contents: List[str], contents_type: str, check_duplicates: bool = True):
        tokens = []
        for content in contents:
            tokens.append(Token(content, contents_type))
        self.insert_tokens(tokens, check_duplicates)

    def insert_tokens(self, tokens: List[Token], check_duplicates: bool = True):
        # insert a list of tokens.

        # remove duplicate tokens
        tokens = list(set(tokens))

        # if check_duplicates is true removes tokens already in DB
        if check_duplicates:
            tokens_already_in_db = self.select_tokens_from_list(tokens)
            # remove contents already in DB
            tokens = [tokens for tokens in tokens if tokens not in tokens_already_in_db]
            if len(tokens) == 0:
                # all the contents are already in db
                return

        insert_query = "INSERT INTO token (content, content_type) VALUES (%s, %s);"
        tokens_tuples = list_of_tokens_to_list_of_tuples(tokens)
        self.cursor.executemany(insert_query, tokens_tuples)
        print(self.cursor.rowcount, "record(s) inserted")

    # def insert_tweets(self, tweets: List[Tweet]):
    #     tokens_list: List[Token] = []
    #     for tweet in tweets:
    #         # insert tweet
    #         # insert_tweet_query = "INSERT INTO tweet (sentiment) VALUES ('{}');".format(tweet.sentiment)
    #         # self.launch_query(insert_tweet_query)
    #
    #         # words = tweet.words
    #         # emojis = tweet.emojis
    #         # emoticons = tweet.emoticons
    #         # hashtags = tweet.hashtags
    #
    #         tokens_list += tweet.get_tokens()
    #     # get contents that already exist in db and exclude it from insert query. Doing it now avoids checking
    #     # duplicates on each insert
    #     tokens_already_in_db = self.select_tokens_from_list(tokens_list)
    #
    #     self.insert_tokens(new_words, "word", False)
    #     self.insert_tokens(new_emojis, "emoji", False)
    #     self.insert_tokens(new_emoticons, "emoticon", False)
    #     self.insert_tokens(new_hashtags, "hashtag", False)
    #
    #     words_token_list: List[List[str]] = []
    #     emojis_token_list: List[List[str]] = []
    #     emoticons_token_list: List[List[str]] = []
    #     hashtags_token_list: List[List[str]] = []
    #
    #     for word in words:
    #         words_token_list.append([word, "word"])
    #     for emoji in emojis:
    #         words_token_list.append([emoji, "emoji"])
    #     for emoticon in emoticons:
    #         words_token_list.append([emoticon, "emoticon"])
    #     for hashtag in hashtags:
    #         words_token_list.append([hashtag, "hashtag"])
    #
    #         # insert words
    #         # insert emojis
    #         # insert emoticons
    #
    #     # for lexical_resource in lexical_resources:
    #     #     # compose values to insert
    #     #     name = lexical_resource.filename
    #     #     sentiment = lexical_resource.sentiment
    #     #     num_words = lexical_resource.get_number_of_words()
    #     #
    #     #     lexical_resources_values.append([name, num_words, sentiment])
    #     #
    #     # lexical_resources_values_query_format = convert_list_of_values_to_query_format(lexical_resources_values)
    #     #
    #     # insert_query = "INSERT INTO lexicalresource (name, num_words, sentiment) VALUES {};".format(
    #     #     lexical_resources_values_query_format)
    #     #
    #     # self.launch_query(insert_query)
    #     # print(self.cursor.rowcount, "record(s) inserted")

    def insert_tweets_records_get_ids(self, sentiments: List[str]) -> List[int]:
        tweet_ids = []
        for sentiment in sentiments:
            insert_tweet_query = "INSERT INTO tweet(sentiment) VALUES (%s);"
            self.cursor.execute(insert_tweet_query, (sentiment,))
            tweet_ids.append(self.cursor.lastrowid)
        return tweet_ids

    def insert_tweets_tokens(self, tweet_id_tokens_list: List[Tuple[int, List[Token]]]):
        # TODO write this, pass the tuple with tweets and tokens to insert

        tweet_token_records = []
        for tweet_id_tokens in tweet_id_tokens_list:
            tweet_id = tweet_id_tokens[0]
            tweet_tokens = tweet_id_tokens[1]
            for token in tweet_tokens:
                tweet_token_records.append((tweet_id, token.content, token.content_type))
        insert_tweets_records_query = \
            "INSERT INTO tweettoken(tweet, content, content_type) VALUES (%s, %s, %s);"
        self.cursor.executemany(insert_tweets_records_query, tweet_token_records)

    def insert_tweets(self, tweets: List[Tweet]):
        tweets_tokens: Dict[Tweet, List[Token]] = {}
        tokens_list: List[Token] = []
        tweets_sentiments: List[str] = []

        # fill lists
        for tweet in tweets:
            tokens = tweet.get_tokens()
            tweets_tokens[tweet] = tokens
            tokens_list += tokens
            tweets_sentiments.append(tweet.sentiment)
        # insert tokens
        self.insert_tokens(tokens_list)

        # insert tweets
        tweet_ids = self.insert_tweets_records_get_ids(tweets_sentiments)

        # list of tuples containing tweet id and list of tokens for tweet
        tweet_ids_token_list: List[Tuple[int, List[Token]]] = []
        for index, tweet in enumerate(tweets):
            # get tweet id in db
            tweet_id = tweet_ids[index]
            # get tokens for tweet
            token_list = tweet.get_tokens()
            tweet_id_tokens_tuple = (tweet_id, token_list)
            tweet_ids_token_list.append(tweet_id_tokens_tuple)

        # insert tweet_tokens
        self.insert_tweets_tokens(tweet_ids_token_list)

        self.db_connection.commit()

    def delete_lex_res(self):
        delete_query = "DELETE FROM lexicalresource"
        self.launch_query(delete_query)
        print(self.cursor.rowcount, "record(s) deleted")

    def delete_contents(self, content_type: str):
        delete_query = "DELETE FROM token WHERE content_type = %s"
        self.cursor.execute(delete_query, (content_type,))
        self.db_connection.commit()
        print(self.cursor.rowcount, "record(s) deleted")

    def delete_tweets(self):
        # TODO delete tweet contents in cascade
        delete_query = "DELETE FROM tweet"
        self.launch_query(delete_query)
        print(self.cursor.rowcount, "record(s) deleted")

    def launch_query(self, query):
        self.cursor.execute(query)
        self.db_connection.commit()

    def get_x_most_used_words_for_sentiment(self, x: int, sentiment: str):
        print(sentiment)
        query = ("SELECT tok.content, COUNT(tok.content) "
                 "FROM tweet AS t "
                 "JOIN	tweettoken AS tt ON t.id = tt.tweet "
                 "JOIN	token tok ON tt.content = tok.content "
                 "    AND tt.content_type = tok.content_type "
                 "WHERE t.sentiment = %s "
                 "    AND tok.content_type = 'word' "
                 "GROUP BY tok.content "
                 "ORDER BY COUNT(tok.content) DESC "
                 "LIMIT %s; ")
        # query = "SELECT COUNT(tok.content), tok.content FROM tweet AS t JOIN	tweettoken AS tt ON t.id = tt.tweet
        # JOIN	token tok ON tt.content = tok.content AND tt.content_type = tok.content_type WHERE t.sentiment = %s
        # AND tok.content_type = 'word' GROUP BY tok.content ORDER BY COUNT(tok.content) DESC LIMIT %s;"
        query_parameters: Tuple[str, int] = (sentiment, x)
        self.cursor.execute(query, query_parameters)
        result = self.cursor.fetchall()
        print(result)

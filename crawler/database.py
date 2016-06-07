import sqlite3 as lite
import sys


con = lite.connect('index.db')


def add_inverted_index(inverted_index):
    with con:
        for word in inverted_index.keys():
            word_to_add = '_' + word
            l = []
            cur = con.cursor()
            cur.execute("DROP TABLE IF EXISTS Cars")
            cur.execute(
                "CREATE TABLE IF NOT EXISTS {}(Url TEXT, Positions TEXT)".format(word_to_add))
            for url, pos in inverted_index[word].items():
                l.append([url, str(pos)])
            cur.executemany(
                "INSERT INTO {} VALUES(?, ?)".format(word_to_add), l)


def get_word_data(word):
    with con:
        word_to_get = '_' + word
        cur = con.cursor()
        try:
            cur.execute("SELECT * FROM {}".format(word_to_get))
            res = [(data[0], eval(data[1])) for data in cur.fetchall()]
            return res
        except:
            return []

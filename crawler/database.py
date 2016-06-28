import sqlite3 as lite
import sys
import search
from search.models import Index, InvertedIndex


# def add_index(index, titles):
#     con = lite.connect('index.db')
#     with con:
#         cur = con.cursor()
#         cur.execute(
#             "CREATE TABLE IF NOT EXISTS Indexes(Url TEXT, Positions TEXT, Title Text)")
#         for url in index.keys():
#             cur.execute(
#                 "INSERT INTO Indexes VALUES(?,?,?)", (url, str(index[url]), titles[url]))


# def check_visited(url):
#     con = lite.connect('index.db')
#     with con:
#         cur = con.cursor()
#         cur.execute(
#             "CREATE TABLE IF NOT EXISTS Indexes(Url TEXT, Positions TEXT, Title Text)")
#         cur.execute(
#             "SELECT rowid FROM Indexes WHERE url = '{}'".format(url))
#         return bool(cur.fetchone())


# def get_urls():
#     con = lite.connect('index.db')
#     with con:
#         cur = con.cursor()
#         cur.execute(
#             "SELECT Url, Title FROM Indexes")
#         return cur.fetchall()


# def add_inverted_index(inverted_index):
#     print "INVERTED_INDEX: ", inverted_index
#     con = lite.connect('inverted_index.db')
#     with con:
#         cur = con.cursor()
#         for word in inverted_index.keys():
#             word_to_add = '_' + word
#             l = []
#             cur.execute(
#                 "CREATE TABLE IF NOT EXISTS {}(Url TEXT, Positions TEXT)".format(word_to_add))
#             for url, pos in inverted_index[word].items():
#                 l.append([url, str(pos)])
#             cur.executemany(
#                 "INSERT INTO {} VALUES(?, ?)".format(word_to_add), l)


# def get_word_data(word):
#     con = lite.connect('inverted_index.db')
#     with con:
#         word_to_get = '_' + word
#         cur = con.cursor()
#         try:
#             cur.execute("SELECT * FROM {}".format(word_to_get))
#             res = [(data[0], eval(data[1])) for data in cur.fetchall()]
#             return res
#         except:
#             return []


def add_index(index, titles):
    for url in index.keys():
        index_object = Index()
        index_object.url = url
        index_object.positions = str(index[url])
        index_object.title = titles[url]
        index_object.save()


def check_visited(url):
    visited = Index.objects.all()
    return bool(url in visited)


def get_urls():
    return [(obj.url, obj.title) for obj in Index.objects.all()]


def add_inverted_index(inverted_index):
    for word in inverted_index.keys():
        word_to_add = '_' + word
        l = []
        inv_index_object = InvertedIndex()
        for url, pos in inverted_index[word].items():
            l.append([url, str(pos)])
        for elem in l:
            inv_index_object.word = word_to_add
            inv_index_object.url = elem[0]
            inv_index_object.position = elem[1]
            inv_index_object.save()


def get_word_data(word):
    word_to_get = '_' + word
    res = [(obj.url, eval(obj.position))
           for obj in InvertedIndex.objects.filter(word=word_to_get)]
    return res

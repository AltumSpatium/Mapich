import sqlite3 as lite
import sys
import search
from search.models import Index, InvertedIndex


def add_index(index, titles):
    print "Addition to index in db started"
    for url in index.keys():
        print "URL:", url
        index_object = Index()
        index_object.url = url
        index_object.positions = str(index[url])
        index_object.title = titles[url]
        index_object.save()
        print "Another element added"


def check_visited(url):
    print "Checking for visited:"
    visited = bool(Index.objects.filter(url=url))
    if visited:
        print "VISITED"
    if not visited:
        print "NOT VISITED"
    return visited


def get_urls():
    return [(obj.url, obj.title) for obj in Index.objects.all()]


def add_inverted_index(inverted_index):
    print "Addition to inverted index in db started"
    for word in inverted_index.keys():
        word_to_add = '_' + word
        print "Word to add:", word_to_add
        l = []
        inv_index_object = InvertedIndex()
        print "Object done"
        for url, pos in inverted_index[word].items():
            l.append([url, str(pos)])
        print "Array l filled"
        for elem in l:
            inv_index_object.word = word_to_add
            inv_index_object.url = elem[0]
            inv_index_object.position = elem[1]
            inv_index_object.save()
            print "Another element added"


def get_word_data(word):
    word_to_get = '_' + word
    res = [(obj.url, eval(obj.position))
           for obj in InvertedIndex.objects.filter(word=word_to_get)]
    return res

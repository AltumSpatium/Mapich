import database as db
import crawler
from nltk.stem.porter import PorterStemmer
import re


def get_words(text):
    stemmer = PorterStemmer()
    pattern = re.compile('[\W_]+')
    text = text.lower()
    text = pattern.sub(' ', text)
    re.sub(r'[\W_]+', '', text)
    words = text.split()
    result = [stemmer.stem(word)
              for word in words if word not in crawler.cached_stopwords]
    return result


def simple_ranked_results(urls):
    urls_freq = {}
    for url, pos in urls:
        if url in urls_freq:
            urls_freq[url] += len(pos)
        else:
            urls_freq[url] = len(pos)
    urls_freq = urls_freq.items()
    res = sorted(urls_freq, key = lambda x : x[-1], reverse = True)
    return res 



def word_query(word):
    data = db.get_word_data(word)
    print data
    return data


def free_query(query):
    res = []
    query = db.get_word_data(query)
    for word in query:
        res += word_query(word)
    print res
    return res

def phrase_query(query):
    pass

word_query('parser')

# free_query('parser true')

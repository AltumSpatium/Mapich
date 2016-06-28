import requests
import re
from bs4 import BeautifulSoup
import time
import urlparse
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import robotparser
import database as db

cached_stopwords = set(stopwords.words('english'))


def visible(element):
    if element == '\n' or element == ' ':
        return False
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
        # need to write str(element), but there are some problems with encoding
    elif re.match('<!--.*-->', element, re.DOTALL):
        return False
    return True


class Crawler:
    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.depth_links = []
        self.visited = set()
        self.index = {}
        self.inverted_index = {}
        self.titles = {}

    def get_domain(self, link):
        parsed_url = urlparse.urlparse(link)
        domain = '{url.scheme}://{url.netloc}/'.format(url=parsed_url)
        return domain

    def parsing_robots(self, link):
        domain = self.get_domain(link)
        parser = robotparser.RobotFileParser()
        parser.set_url(urlparse.urljoin(domain, 'robots.txt'))
        parser.read()
        return parser

    def get_site(self, link):
        links = []
        try:
            start_page = requests.get(link)
        except:
            return None
        soup = BeautifulSoup(start_page.text, 'lxml')
        text = filter(visible, soup.findAll(text=True))
        parser = self.parsing_robots(link)
        for tag in soup.find_all('a', href=True):
            new_link = urlparse.urljoin(link, tag['href'])
            try:
                if new_link not in self.visited and parser.can_fetch('*', new_link) and not db.check_visited(new_link):
                    links.append(new_link)
                    self.visited.add(new_link)
            except Exception as e:
                print e
                continue
        try:
            title = soup.title.string
        except:
            title = 'Standard title'
        return Site(link, text, links, title)

    def crawl(self):
        site = self.get_site(self.starting_url)
        if not db.check_visited(site.name):
            self.index[site.name] = site.index()
        self.depth_links.append(site.links)
        self.titles[site.name] = site.title
        for current_depth in xrange(self.depth):
            current_links = []
            for link in self.depth_links[current_depth]:
                current_site = self.get_site(link)
                if not current_site or not current_site.links:
                    continue
                current_links.extend(current_site.links)
                self.index[current_site.name] = current_site.index()
                self.titles[current_site.name] = current_site.title
                # time.sleep(1)
            self.depth_links.append(current_links)
        if self.index:
            db.add_inverted_index(self.invert_index(self.index))
            db.add_index(self.index, self.titles)

    def invert_index(self, index):
        inverted_index = {}
        for site_name in index.keys():
            for word in index[site_name].keys():
                if word in inverted_index.keys():
                    if site_name in inverted_index[word].keys():
                        inverted_index[word][site_name].extend(
                            index[site_name][word][:])
                    else:
                        inverted_index[word][
                            site_name] = index[site_name][word]
                else:
                    inverted_index[word] = {site_name: index[site_name][word]}
        return inverted_index


class Site(object):
    """docstring for Site"""

    def __init__(self, name, text, links, title):
        self.name = name
        self.text = text
        self.links = links
        self.title = title

    def get_words(self):
        stemmer = PorterStemmer()
        words = []
        pattern = re.compile('[\W_]+')
        for t in self.text:
            t = t.lower()
            t = pattern.sub(' ', t)
            re.sub(r'[\W_]+', '', t)
            words.extend(t.split())
        result = [stemmer.stem(word)
                  for word in words if word not in cached_stopwords]
        return result

    def index(self):
        termlist = self.get_words()
        word_index = {}
        for index, word in enumerate(termlist):
            try:
                word_index[word].append(index)
            except:
                word_index[word] = [index]
        return word_index
        
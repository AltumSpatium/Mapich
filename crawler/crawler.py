import requests
import re
from bs4 import BeautifulSoup
import time
import urlparse
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import robotparser

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
        self.sites = []
        self.visited = set()
        self.index = {}
        self.inverted_index = {}

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
        start_page = requests.get(link)
        soup = BeautifulSoup(start_page.text, 'lxml')
        text = filter(visible, soup.findAll(text=True))
        parser = self.parsing_robots(link)
        for tag in soup.find_all('a', href=True):
            new_link = urlparse.urljoin(link, tag['href'])
            if new_link not in self.visited and parser.can_fetch('*', new_link):
                links.append(new_link)
                self.visited.add(new_link)
        return Site(link, text, links)

    def crawl(self):
        site = self.get_site(self.starting_url)
        self.sites.append(site)  # maybe we don't need to save our sites
        self.index[site.name] = site.index()
        self.depth_links.append(site.links)
        for current_depth in xrange(self.depth):
            current_links = []
            for link in self.depth_links[current_depth]:
                current_site = self.get_site(link)
                current_links.extend(current_site.links)
                self.sites.append(current_site)
                self.index[current_site.name] = current_site.index()
                print self.index
                # time.sleep(1)
            self.depth_links.append(current_links)
        print self.invert_index(self.index)

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

    def __init__(self, name, text, links):
        self.name = name
        self.text = text
        self.links = links

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

c = Crawler(
    'https://pymotw.com/2/robotparser/', 1)
c.crawl()

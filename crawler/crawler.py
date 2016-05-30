import requests
import re
from bs4 import BeautifulSoup
import time
import urlparse


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

    def crawl(self):
        site = self.get_site(self.starting_url)
        self.sites.append(site)
        self.depth_links.append(site.links)
        for current_depth in xrange(self.depth):
            current_links = []
            for link in self.depth_links[current_depth]:
                current_site = self.get_site(link)
                current_links.extend(current_site.links)
                self.sites.append(current_site)
                # time.sleep(1)
            self.depth_links.append(current_links)

    def get_site(self, link):
        links = []
        start_page = requests.get(link)
        soup = BeautifulSoup(start_page.text, 'lxml')
        text = filter(visible, soup.findAll(text=True))
        for tag in soup.find_all('a', href=True):
            new_link = urlparse.urljoin(link, tag['href'])
            if new_link not in self.visited:
                links.append(new_link)
                self.visited.add(new_link)
        print links
        return Site(text, links)


class Site(object):
    """docstring for Site"""

    def __init__(self, text, links):
        self.text = text
        self.links = links


c = Crawler(
    'http://www.apple.com/itunes/download', 1)
c.crawl()

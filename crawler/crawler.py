import requests
import re
from bs4 import BeautifulSoup
import time

def visible(element):
    if element == '\n' or element == ' ':
        return False
    if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
        return False
        # need to write str(element), but there are some problems with encoding
    elif re.match('<!--.*-->', element,re.DOTALL):
        return False
    return True

class Crawler:
    def __init__(self, starting_url, depth):
        self.starting_url = starting_url
        self.depth = depth
        self.current_depth = 0
        self.depth_links = []
        self.sites = []

    def crawl(self):
        site = self.get_site(self.starting_url)
        self.sites.append(site)
        self.depth_links.append(site.links)
        print site.links
        while self.current_depth < self.depth:
            current_links = []
            for link in self.depth_links[self.current_depth]:
                current_site = self.get_site(link)
                current_links.extend(current_site.links)
                self.sites.append(current_site)
                time.sleep(1)
            self.current_depth += 1
            self.depth_links.append(current_links)

    def get_site(self, link):
        links = []
        start_page = requests.get(link)
        soup = BeautifulSoup(start_page.text,'lxml')
        text = filter(visible, soup.findAll(text = True))
        for link in soup.find_all('a'):
            links.append(link.get('href'))
        return Site(text,links)

class Site(object):
    """docstring for Site"""
    def __init__(self, text, links):
        self.text = text
        self.links = links
    

c = Crawler(
    'http://www.apple.com/itunes/download', 0)
c.crawl()

from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import time
import logging

from database.data_shering import DataBase_exchanging

logging.basicConfig(
    filename='log.log', 
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

class WebPages:
    def __init__(self, start_page, last_page):
        self.start_page: int = start_page
        self.last_page: int = last_page
        self.pages = []

    def generating(self):
        for i in range(self.start_page, self.last_page):
            self.pages.append(f"https://book24.ru/catalog/page-{i}/")
        return list(self.pages)

class LinkAdmin:
    def __init__(self, pages):
        self.pages = pages
        self.link = []
        self.counter=0

    def set_links(self):
            for p in self.pages:
                bs = BeautifulSoup(urlopen(p), 'lxml')
                links = bs.find_all('a', {'class': 'product-card__name'})
                for l in links:
                    self.link.append(f"https://book24.ru{l['href']}")
                    time.sleep(0.1)
                self.counter+=1
                logging.info(f'The end of links on page initialization {self.counter}/18601')
            logging.info('THE END OF LINKS INITIALIZATION')
            return list(self.link)

time.sleep(120)
wp = WebPages(2, 18601)
la = LinkAdmin(wp.generating())


class Crawler:
    def __init__(self, urls):
        self.urls = urls

    def get_info(self):
        logging.info('Start of parsing')
        for url in self.urls:
            try:
                bs = BeautifulSoup(urlopen(url), 'lxml')
                time.sleep(0.1)
            except HTTPError:
                pass

            try:
                title = (
                    bs.h1
                    .get_text()
                    .split(':', 1)[1]
                    .strip()
                )
                author = (
                    bs.find('dd', {'class': 'product-characteristic__value'})
                    .a.get_text()
                )
                rating = (
                    bs.find('button', {'class': 'rating-widget__button'})
                    .find('span', {'class', 'rating-widget__main-text'})
                    .get_text()
                    .strip().replace(',', '.')
                )
                publisher = (
                    bs.find('dl', {'class': 'product-characteristic__list'})
                    .find_all('div', {'class': 'product-characteristic__item'})[3]
                    .a
                    .get_text()
                )
                publication_year = (
                    bs.find('dl', {'class': 'product-characteristic__list'})
                    .find_all('div', {'class': 'product-characteristic__item'})[6]
                    .find('dd', {'class': 'product-characteristic__value'})
                    .get_text()
                    .strip()
                )
                isbn = (
                    bs.find('dl', {'class': 'product-characteristic__list'})
                    .find_all('div', {'class': 'product-characteristic__item'})[4]
                    .find('button', {'class': 'app-copy-button isbn-product _right'})
                    .get_text()
                    .strip()
                )
                db = DataBase_exchanging(title, author, rating, publisher, publication_year, isbn)
                db.exchanging()
            except (Exception, HTTPError):
                pass
        logging.info('Pasring has ended')

if __name__ == '__main__':
    cw = Crawler(la.set_links())
    cw.get_info()


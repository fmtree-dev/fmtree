import pathlib2
from scraper import Scraper
from filter import MarkdownFilter

if __name__ == '__main__':
    path_ = pathlib2.Path('/Users/huakunshen/Local/Dev/OSCP')
    scraper = Scraper(path_, scrape_now=False)
    scraper.add_filter(filter_=MarkdownFilter())
    scraper.scrape()

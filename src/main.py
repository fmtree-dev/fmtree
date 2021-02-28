import io
import sys
import pathlib2
from scraper import Scraper
from filter import MarkdownFilter
from node import Node
from format import TabFormatter


def compare(a: Node):
    name = a.get_path().name
    if a.get_depth() == 2 and a.get_path().parent.name == "Exercises":
        if name == "README.md":
            return 0
        else:
            return int(a.get_path().name.replace('.', ''))
    else:
        return a.get_path().name


if __name__ == '__main__':
    path_ = pathlib2.Path('/Users/huakunshen/Local/Dev/OSCP')
    scraper = Scraper(path_, scrape_now=False, compare=compare)
    scraper.add_filter(filter_=MarkdownFilter())
    scraper.scrape()
    formatter = TabFormatter(scraper.get_tree())
    stringio = formatter.generate()
    print(stringio.getvalue())



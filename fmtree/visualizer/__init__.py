import sys
import argparse

import pathlib2

from fmtree.core.scraper import Scraper
from fmtree.core.filter import ImageFilter
from fmtree.core.format import TreeCommandFormatter, ListFileFormatter


def main(args):
    print(args)
    scraper = Scraper(pathlib2.Path(args['path']), scrape_now=False, keep_empty_dir=False)
    scraper.add_filter(ImageFilter())
    scraper.run()
    tree = scraper.get_tree()
    formatter = TreeCommandFormatter(tree)
    stringio = formatter.generate()
    formatter.to_stream(sys.stdout)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Fmtree Visualizer Parser")
    args = parser.parse_args()
    main(dict(args.__dict__, **{'path': 'D:\OneDrive\Collection\Pictures\Wallpaper'}))

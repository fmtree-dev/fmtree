import io
import sys
import pathlib2
from src.scraper import Scraper
from src.filter import MarkdownFilter, markdown_filter, ExtensionFilter, RegexFilter
from src.node import FileNode
from src.format import TabFormatter, TreeCommandFormatter, ListFileFormatter, MarkdownContentFormatter, \
    MarkdownLinkContentFormatter, GithubMarkdownContentFormatter
from src import sorter


if __name__ == '__main__':
    path_ = pathlib2.Path('/Users/huakunshen/Local/Dev/OSCP')
    # path_ = pathlib2.Path('/home/huakun/Documents/gdrive/OSCP')
    scraper = Scraper(path_, scrape_now=False, keep_empty_dir=False, filter_=RegexFilter(['.+\.md']))
    scraper.run()
    # formatter = TabFormatter(scraper.get_tree())
    # stringio = formatter.generate()
    # print(stringio.getvalue())

    formatter = TreeCommandFormatter(scraper.get_tree())
    stringio = formatter.generate()
    print(stringio.getvalue())

    # formatter = ListFileFormatter(scraper.get_tree())
    # stringio = formatter.generate()
    # print(stringio.getvalue())
    # print(formatter.get_paths())

    # formatter = MarkdownContentFormatter(scraper.get_tree())
    # stringio = formatter.generate()
    # print(stringio.getvalue())

    # formatter = MarkdownLinkContentFormatter(scraper.get_tree())
    # stringio = formatter.generate()
    # print(stringio.getvalue())

    # formatter = GithubMarkdownContentFormatter(scraper.get_tree())
    # stringio = formatter.generate()
    # print(stringio.getvalue())
    # formatter.to_stream(sys.stdout)

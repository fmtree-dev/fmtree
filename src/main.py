import io
import sys
import pathlib2
from scraper import Scraper
from filter import MarkdownFilter
from node import FileNode
from format import TabFormatter, TreeCommandFormatter, ListFileFormatter, MarkdownContentFormatter, \
    MarkdownLinkContentFormatter, GithubMarkdownContentFormatter


def compare(a: FileNode):
    name = a.get_path().name
    if a.get_depth() == 2 and a.get_path().parent.name == "Exercises":
        if name == "README.md":
            return 0
        else:
            return int(a.get_path().name.replace('.', ''))
    else:
        return a.get_path().name


if __name__ == '__main__':
    # path_ = pathlib2.Path('/Users/huakunshen/Local/Dev/OSCP')
    path_ = pathlib2.Path('/home/huakun/Documents/gdrive/OSCP')
    scraper = Scraper(path_, scrape_now=False, keep_empty_dir=False)
    scraper.add_filter(filter_=MarkdownFilter())
    scraper.run()
    # formatter = TabFormatter(scraper.get_tree())
    # stringio = formatter.generate()
    # print(stringio.getvalue())
    #
    # formatter = TreeCommandFormatter(scraper.get_tree())
    # stringio = formatter.generate()
    # print(stringio.getvalue())

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

    formatter = GithubMarkdownContentFormatter(scraper.get_tree())
    stringio = formatter.generate()
    print(stringio.getvalue())
    formatter.to_stream(sys.stdout)
    formatter.to_file("/home/huakun/Desktop/tmp.md", append=True)

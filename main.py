import io
import re
import sys
from typing import List, Iterable
from functools import cmp_to_key
import pathlib2
from src.scraper import Scraper
from src.filter import MarkdownFilter, markdown_filter, ExtensionFilter, RegexFilter
from src.node import FileNode
from src.format import TabFormatter, TreeCommandFormatter, ListFileFormatter, MarkdownContentFormatter, \
    MarkdownLinkContentFormatter, GithubMarkdownContentFormatter
from src import sorter


class OSCPExerciseSorter(sorter.BaseSorter):
    exercise_re_pattern = re.compile("^(\d+\.)+\d+$")

    def sorted(self, nodes: List[FileNode]) -> Iterable:
        relative_path = nodes[0].get_path().parent.relative_to(nodes[0].get_root())
        filenames = [node.get_filename() for node in nodes]
        max_num_count = max([len(filename.split(".")) for filename in filenames])

        def comparator(node1: FileNode, node2: FileNode):
            filename1, filename2 = node1.get_filename(), node2.get_filename()
            nums1 = list(map(int, filename1.split(".")))
            nums2 = list(map(int, filename2.split(".")))
            i = -1
            while i < max_num_count and i < len(nums1) and i < len(nums2):
                i += 1
                if nums1[i] == nums2[i]:
                    continue
                elif nums1[i] < nums2[i]:
                    return -1
                else:
                    return 1
            return 0

        if relative_path.name == "Exercises":
            nodes = list(filter(lambda node: OSCPExerciseSorter.exercise_re_pattern.match(node.get_filename()), nodes))
            nodes = sorted(nodes, key=cmp_to_key(comparator))
            for i in range(len(nodes) - 1):
                assert int(nodes[i].get_filename().split('.')[0]) <= int(nodes[i + 1].get_filename().split('.')[0])
            return nodes
        else:
            return sorted(nodes, key=lambda node: node.get_filename())


if __name__ == '__main__':
    path_ = pathlib2.Path('/Users/huakunshen/Local/Dev/OSCP')
    # path_ = pathlib2.Path('/home/huakun/Documents/gdrive/OSCP')
    scraper = Scraper(path_, scrape_now=False, keep_empty_dir=False, filter_=RegexFilter(['.+\.md']))
    scraper.run()
    # formatter = TabFormatter(scraper.get_tree())
    # stringio = formatter.generate()
    # print(stringio.getvalue())
    sorter_ = OSCPExerciseSorter()
    tree = sorter_(scraper.get_tree())
    # tree = scraper.get_tree()
    formatter = TreeCommandFormatter(tree)
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

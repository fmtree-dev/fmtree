import pathlib2
import re
import sys
import argparse
from typing import List, Iterable

import pathlib2
from fmtree.scraper import Scraper
from fmtree.filter import MarkdownFilter, BaseFileFilter, IdentityFilter
import fmtree.filter as filter_
from fmtree.format import GithubMarkdownContentFormatter, TreeCommandFormatter
from fmtree import sorter
from fmtree.node import FileNode
from functools import cmp_to_key

path = pathlib2.Path("/Users/huakunshen/Local/Dev/OSCP")


class OSCPExerciseSorter(sorter.BaseSorter):
    exercise_re_pattern = re.compile("^(\\d+\\.)+\\d+$")

    def sorted(self, nodes: List[FileNode]) -> Iterable:
        relative_path = nodes[0].get_path().parent.relative_to(nodes[0].get_root())
        filenames = [node.get_filename() for node in nodes]
        max_num_count = max([len(filename.split("."))
                             for filename in filenames])

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
            nodes = list(filter(lambda node: OSCPExerciseSorter.exercise_re_pattern.match(
                node.get_filename()), nodes))
            nodes = sorted(nodes, key=cmp_to_key(comparator))
            for i in range(len(nodes) - 1):
                assert int(nodes[i].get_filename().split('.')[0]) <= int(
                    nodes[i + 1].get_filename().split('.')[0])
            return nodes
        else:
            return sorted(nodes, key=lambda node: node.get_filename())


if __name__ == '__main__':
    scraper = Scraper(path, scrape_now=False, keep_empty_dir=True, depth=1)
    # scraper.add_filter(IdentityFilter(ignore_list=['Exercises.*', 'build-tools.*', '\\.git.*'],
    #                                   mode=filter_.ACCEPT_MODE))

    scraper.run()
    sorter_ = OSCPExerciseSorter()
    tree = sorter_(scraper.get_tree())
    formatter = GithubMarkdownContentFormatter(tree, ignore_top_level=True)
    # formatter = TreeCommandFormatter(tree)
    stringio = formatter.generate()
    formatter.to_stream(sys.stdout)

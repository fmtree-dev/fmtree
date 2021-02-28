from node import Node
from typing import Callable, Tuple
from filter import Filter

import pathlib2


class Scraper:
    """
    Scraper of file system
    Scrape a given path with given properties such as filters, sort functions..., and turn it into a tree structure
    """

    def __init__(self, path: pathlib2.Path, filter_: Callable = None, scrape_now: bool = False, keep_empty_dir: bool = False) -> None:
        """
        Initialize Scraper with different properties and addons
        :param path: target path to scrape
        :param filter_: filter for filtering out unwanted files
        :param scrape_now: start scraping right after initialization
        """
        self._root = path.absolute()
        self._keep_empty_dir = keep_empty_dir
        if not self._root.exists():
            raise ValueError(f"Path Not Exist: {str(self._root)}")
        self._filters = [filter_] if filter_ else []
        self._history = set()
        self._tree = self._scrape(self._root, 0)[0] if scrape_now else None

    def scrape(self, inplace: bool = True) -> Node:
        """
        scrape the given path and form a tree structure
        :param inplace: bool: set tree inplace
        :return: the scraped tree of file nodes
        """
        self._history = set()
        tree, found_any = self._scrape(self._root, 0)
        if inplace:
            self._tree = tree
        return tree

    def _scrape(self, path: pathlib2.Path, depth: int) -> Tuple[Node, bool]:
        """
        Use recursion to scrape a given path and return a tree structure
        :param path: target file path to scrape
        :param depth: depth of node with respect to the root node
        :return: the scraped file node tree and whether any target files set by filters were found
        """
        children = []
        found_any = False
        for filepath in path.iterdir():
            if sum(map(lambda filter_: filter_(filepath), self._filters)) != len(self._filters):
                continue
            node = Node(filepath, depth=depth + 1, root=self._root)
            if (filepath.is_symlink() or filepath.is_dir()) and node.get_id() not in self._history:
                subtree, found_any_ = self._scrape(filepath, depth + 1)
                if found_any_:
                    found_any = True
                if self._keep_empty_dir or found_any_:
                    children.append(subtree)
            elif filepath.is_file():
                children.append(node)
                found_any = True
            else:
                pass
            self._history.add(node.get_id())
        return Node(path, children=children, depth=depth, root=self._root), found_any

    def add_filter(self, filter_: Filter) -> None:
        """
        add an extra filter to the scraper to apply more filtering
        a file path must satisfy every filter in order to be kept
        :param filter_: a new filter for filtering
        :return: None
        """
        self._filters.append(filter_)

    def clear_filter(self) -> None:
        """
        Clear all filters
        :return: None
        """
        self._filters = []

    def get_tree(self) -> Node:
        """
        :return: root node of the scraped file tree
        """
        return self._tree

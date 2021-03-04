from .node import FileNode
from typing import Callable, Tuple, Union
from .filter import BaseFilter
from abc import ABC, abstractmethod
import pathlib2


class BaseScraper(ABC):
    def __init__(self, path: pathlib2.Path, scrape_now: bool = False, filter_: Callable = None):
        self._root = path.absolute()
        self._history = set()
        self._tree = self.scrape(self._root, 0)[0] if scrape_now else None
        self._filter = filter_

    @abstractmethod
    def scrape(self, path: pathlib2.Path, depth: int) -> Tuple[FileNode, bool]:
        raise NotImplementedError

    def run(self, inplace: bool = True) -> FileNode:
        """
        scrape the given path and form a tree structure
        :param inplace: bool: set tree inplace
        :return: the scraped tree of file nodes
        """
        self._history = set()
        tree, found_any = self.scrape(self._root, 0)
        if inplace:
            self._tree = tree
        return tree

    def get_tree(self) -> FileNode:
        """
        :return: root node of the scraped file tree
        """
        return self._tree


class Scraper(BaseScraper):
    """
    Scraper of file system
    Scrape a given path with given properties such as filters, sort functions..., and turn it into a tree structure
    """

    def __init__(self, path: pathlib2.Path, filter_: Callable = None, scrape_now: bool = False,
                 keep_empty_dir: bool = False) -> None:
        """
        Initialize Scraper with different properties and addons
        :param path: target path to scrape
        :param filter_: filter for filtering out unwanted files
        :param scrape_now: start scraping right after initialization
        """
        super(Scraper, self).__init__(path, scrape_now=scrape_now, filter_=filter_)
        self._keep_empty_dir = keep_empty_dir
        if not self._root.exists():
            raise ValueError(f"Path Not Exist: {str(self._root)}")

    def scrape(self, path: pathlib2.Path, depth: int) -> Tuple[FileNode, bool]:
        """
        Use recursion to scrape a given path and return a tree structure
        :param path: target file path to scrape
        :param depth: depth of node with respect to the root node
        :return: the scraped file node tree and whether any target files set by filters were found
        """
        children = []
        found_any = False
        paths = self._filter(list(path.iterdir()))
        for filepath in paths:
            node = FileNode(filepath, depth=depth + 1, root=self._root)
            if (filepath.is_symlink() or filepath.is_dir()) and node.get_id() not in self._history:
                subtree, found_any_ = self.scrape(filepath, depth + 1)
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
        return FileNode(path, children=children, depth=depth, root=self._root), found_any

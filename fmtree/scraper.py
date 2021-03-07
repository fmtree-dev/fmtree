from fmtree.node import FileNode
from fmtree.filter import BaseFilter, BaseFileFilter
from typing import Callable, Tuple, Iterable
from abc import ABC, abstractmethod
import pathlib2


class BaseScraper(ABC):
    def __init__(self, path: pathlib2.Path, scrape_now: bool = False, filters: Iterable[BaseFileFilter] = None):
        self.root = path.resolve().absolute()
        self.history = set()
        self.tree = self.scrape(self.root, 0)[0] if scrape_now else None
        self.filters = filters if filters else []
        for filter_ in self.filters:
            filter_.set_root_path(self.root)

    @abstractmethod
    def scrape(self, path: pathlib2.Path, depth: int) -> Tuple[FileNode, bool]:
        raise NotImplementedError

    def run(self, inplace: bool = True) -> FileNode:
        """
        scrape the given path and form a tree structure
        :param inplace: bool: set tree inplace
        :return: the scraped tree of file nodes
        """
        self.history = set()
        tree, found_any = self.scrape(self.root, 0)
        if inplace:
            self.tree = tree
        return tree

    def get_tree(self) -> FileNode:
        """
        :return: root node of the scraped file tree
        """
        return self.tree


class Scraper(BaseScraper):
    """
    Scraper of file system
    Scrape a given path with given properties such as filters, sort functions..., and turn it into a tree structure
    """

    def __init__(self, path: pathlib2.Path, filters: Iterable[BaseFileFilter] = None, scrape_now: bool = False,
                 keep_empty_dir: bool = False) -> None:
        """
        Initialize Scraper with different properties and addons
        :param path: target path to scrape
        :param filters: filters for filtering out unwanted files
        :param scrape_now: start scraping right after initialization
        """
        super(Scraper, self).__init__(path, scrape_now=scrape_now, filters=filters)
        self._keep_empty_dir = keep_empty_dir
        if not self.root.exists():
            raise ValueError(f"Path Not Exist: {str(self.root)}")

    def scrape(self, path: pathlib2.Path, depth: int) -> Tuple[FileNode, bool]:
        """
        Use recursion to scrape a given path and return a tree structure
        :param path: target file path to scrape
        :param depth: depth of node with respect to the root node
        :return: the scraped file node tree and whether any target files set by filters were found
        """
        children = []
        found_any = False
        paths = list(path.iterdir())
        for filter_ in self.filters:
            paths = filter_(paths)
        for filepath in paths:
            node = FileNode(filepath, depth=depth + 1, root=self.root)
            if (filepath.is_symlink() or filepath.is_dir()) and node.get_id() not in self.history:
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
            self.history.add(node.get_id())
        return FileNode(path, children=children, depth=depth, root=self.root), found_any

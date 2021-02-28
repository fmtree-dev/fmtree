from node import Node
from typing import Callable, Tuple

import pathlib2


class Scraper:
    def __init__(self, path: pathlib2.Path, filter_: Callable = None, scrape_now: bool = False):
        self._root = path.absolute()
        if not self._root.exists():
            raise ValueError(f"Path Not Exist: {str(self._root)}")
        self._filters = [filter_] if filter_ else []
        self._history = set()
        self._tree = self._scrape(self._root, 0)[0] if scrape_now else None

    def scrape(self) -> Node:
        self._tree, found_any = self._scrape(self._root, 0)
        return self._tree

    def _scrape(self, path: pathlib2.Path, depth: int) -> Tuple[Node, bool]:
        children = []
        found_any = False
        for filepath in path.iterdir():
            if sum(map(lambda filter_: filter_(filepath), self._filters)) != len(self._filters):
                continue
            node = Node(filepath, depth=depth + 1, root=self._root)
            if filepath.is_symlink() or filepath.is_dir() and node.get_id() not in self._history:
                self._history.add(node.get_id())
                subtree, found_any_ = self._scrape(filepath, depth + 1)
                if found_any_:
                    children.append(subtree)
            elif filepath.is_file():
                self._history.add(node.get_id())
                children.append(node)
                found_any = True
            else:
                pass
        return Node(path, children=children, depth=depth, root=self._root), found_any

    def add_filter(self, filter_):
        self._filters.append(filter_)

    def clear_filter(self):
        self._filters = []

    def get_tree(self):
        return self._tree

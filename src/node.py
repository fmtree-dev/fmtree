from __future__ import annotations

import os
import pathlib2
from abc import ABC, abstractmethod
from typing import List, Union


class UniqueFileIdentifier:
    def __init__(self, path: pathlib2.Path):
        self.st_dev = path.stat().st_dev
        self.st_ino = path.stat().st_ino

    def __str__(self):
        return str(self.st_dev) + str(self.st_ino)

    def __eq__(self, other: UniqueFileIdentifier):
        return self.st_dev == other.st_dev and self.st_ino == other.st_ino

    def __hash__(self):
        return hash((self.st_dev, self.st_ino))


class Node(ABC):
    def __init__(self, path: pathlib2.Path, depth: int = None, root: pathlib2.Path = None,
                 children: Union[List, None] = None):
        self._path = path
        self._root = root
        self._relative_path = self._path.relative_to(self._root) if self._root else None
        self._depth = depth
        self._filename = path.name
        self._stat = path.stat()
        self._children = children
        self._id = UniqueFileIdentifier(self._path)

    def __str__(self):
        return str(self._path.absolute())

    def __eq__(self, other: Node):
        return self._id == other.get_id()

    def get_children(self):
        return self._children

    def get_path(self):
        return self._path

    def get_filename(self):
        return self._filename

    def get_stat(self):
        return self._stat

    def get_id(self):
        return self._id

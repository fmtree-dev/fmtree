from __future__ import annotations

import pathlib2
from abc import ABC
from typing import List, Union


class UniqueFileIdentifier:
    """
    Unique File Identifier
    Used to identify a unique file within a file system
    st_dev and st_ino of a file are used together to uniquely identify a file in a file system
    __eq__ function and __hash__ implemented so objects of this type can be hashed and used in a set/dictionary for
    detecting duplicate files
    """

    def __init__(self, path: pathlib2.Path):
        """
        Initialize UniqueFile Identifier by setting st_dev and st_ino
        :param path: a file path of type pathlib2.Path
        """
        self.st_dev = path.stat().st_dev
        self.st_ino = path.stat().st_ino

    def __str__(self) -> str:
        """
        Convert to string type by concatenating st_dev and st_ino, which should be unique in a file system
        :return: concatenate st_dev and st_ino
        """
        return str(self.st_dev) + str(self.st_ino)

    def __eq__(self, other: UniqueFileIdentifier) -> bool:
        """
        Decide whether 2 file identifiers are identical
        They are identical if they have the same st_dev and st_ino
        :param other: another UniqueFileIdentifier to compare with
        :return: whether 2 file identifiers are identical
        """
        return self.st_dev == other.st_dev and self.st_ino == other.st_ino

    def __hash__(self):
        """
        Since __eq__ is overwritten, __hash__ function has to be overwritten too in order for this class to be hashable
        :return: hash of tuple(std_dev, st_ino)
        """
        return hash((self.st_dev, self.st_ino))


class Node(ABC):
    """
    File Node Abstract Class
    """

    def __init__(self, path: pathlib2.Path, depth: int = None, root: pathlib2.Path = None, children: List = []) -> None:
        """
        Initializer of Node class
        :param path: file path
        :param depth: depth of file/directory relative to root
        :param root: root path, can be None
        :param children: List of Node when current node is a directory, None if current node is a file
        """
        self._path = path
        self._root = root
        self._relative_path = self._path.relative_to(self._root) if self._root else None
        self._depth = depth
        self._filename = path.name
        self._stat = path.stat()
        self._children = children
        self._id = UniqueFileIdentifier(self._path)

    def __str__(self) -> str:
        """
        File Node to String Form
        :return: absolute path of current file node in string form
        """
        return str(self._path.absolute())

    def __eq__(self, other: Node) -> bool:
        """
        decide whether 2 file nodes are identical
        :param other: Another File Node to compare with
        :return: The two nodes' id (UniqueFileIdentifier) are identical
        """
        return self._id == other.get_id()

    def get_children(self) -> List[Node]:
        """
        :return: child file nodes
        """
        return self._children

    def get_path(self) -> pathlib2.Path:
        """
        :return: file path of this file node
        """
        return self._path

    def get_filename(self) -> str:
        """
        :return: filename of this file node
        """
        return self._filename

    def get_stat(self):
        """
        :return: stat of this file node
        """
        return self._stat

    def get_id(self):
        """
        :return: UniqueFileIdentifier (id) of this file node
        """
        return self._id

    def get_depth(self):
        """
        :return: depth of this file node with respect to root path
        """
        return self._depth

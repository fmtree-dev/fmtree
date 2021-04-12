from __future__ import annotations
import os
import copy
import stat
import pickle
import pathlib2
from abc import ABC, abstractmethod
from typing import List, Union, io
import json


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


class BaseNode(ABC):
    @abstractmethod
    def __str__(self):
        raise NotImplementedError

    def __copy__(self):
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo):
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    @abstractmethod
    def to_bytes(self) -> bytes:
        raise NotImplementedError

    @abstractmethod
    def to_stream(self, stream: io) -> None:
        raise NotImplementedError


class FileNode(BaseNode):
    """
    File Node Abstract Class
    """

    def __init__(self, path: pathlib2.Path, depth: int = None, root: pathlib2.Path = None,
                 children: Union[List, None] = None) -> None:
        """
        Initializer of Node class
        :param path: file path
        :param depth: depth of file/directory relative to root
        :param root: root path, can be None
        :param children: List of Node when current node is a directory, None if current node is a file
        """
        self._path = path
        self._root = root
        self._relative_path = self._path.relative_to(
            self._root) if self._root else None
        self._depth = depth
        self._filename = path.name
        self._stat = path.stat()
        self._children = children if children else []
        self._id = UniqueFileIdentifier(self._path)

    def __str__(self) -> str:
        """
        File Node to String Form
        :return: absolute path of current file node in string form
        """
        return str(self._path.absolute())

    def __eq__(self, other: FileNode) -> bool:
        """
        decide whether 2 file nodes are identical
        :param other: Another File Node to compare with
        :return: The two nodes' id (UniqueFileIdentifier) are identical
        """
        return self._id == other.get_id()

    def get_children(self) -> List[FileNode]:
        """
        :return: child file nodes
        """
        return self._children

    def set_children(self, children: List[FileNode]) -> None:
        """
        setter
        :param children: child nodes of a file node
        :return: NOne
        """
        self._children = children

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

    def get_stat(self) -> os.stat_result:
        """
        :return: stat of this file node
        """
        return self._stat

    def get_id(self) -> UniqueFileIdentifier:
        """
        :return: UniqueFileIdentifier (id) of this file node
        """
        return self._id

    def get_depth(self) -> int:
        """
        :return: depth of this file node with respect to root path
        """
        return self._depth

    def get_root(self) -> pathlib2.Path:
        """
        :return: node's root path
        """
        return self._root

    def get_relative_path(self) -> pathlib2.Path:
        return self._relative_path

    def is_dir(self) -> bool:
        return stat.S_ISDIR(self._stat.st_mode)

    def is_file(self):
        return stat.S_ISREG(self._stat.st_mode)

    def to_bytes(self) -> bytes:
        return pickle.dumps(self)

    def to_stream(self, stream: io) -> None:
        return pickle.dump(self, stream)

    def to_dict(self) -> dict:
        children = [child.to_dict() for child in self._children]
        return {
            'id': str(self._id),
            'depth': self._depth,
            'filename': self._filename,
            'path': str(self._path),
            'relative_path': str(self._relative_path),
            'root': str(self._root),
            'children': children,
            'st_size': self._stat.st_size
        }

    def to_json(self, indent=None):
        return json.dumps(self.to_dict(), indent=indent)

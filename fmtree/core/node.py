from __future__ import annotations
import os
import copy
import stat
import pickle
import pathlib2
from abc import ABC, abstractmethod
from typing import List, Union, io, Dict, Generator
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
        """Initialize UniqueFile Identifier by setting st_dev and st_ino

        :param path: a file path of type pathlib2.Path
        :type path: pathlib2.Path
        """
        self.st_dev = path.stat().st_dev
        self.st_ino = path.stat().st_ino

    def __str__(self) -> str:
        """Convert to string type by concatenating st_dev and st_ino, which should be unique in a file system

        :return: concatenate st_dev and st_ino
        :rtype: str
        """
        return str(self.st_dev) + str(self.st_ino)

    def __eq__(self, other: UniqueFileIdentifier) -> bool:
        """Decide whether 2 file identifiers are identical
        They are identical if they have the same st_dev and st_ino

        :param other: another UniqueFileIdentifier to compare with
        :type other: UniqueFileIdentifier
        :return: whether 2 file identifiers are identical
        :rtype: bool
        """
        return self.st_dev == other.st_dev and self.st_ino == other.st_ino

    def __hash__(self) -> int:
        """Since __eq__ is overwritten, __hash__ function has to be overwritten too in order for this class to be hashable

        :return: hash of tuple(std_dev, st_ino)
        :rtype: int
        """
        return hash((self.st_dev, self.st_ino))


class BaseNode(ABC):
    @abstractmethod
    def __str__(self) -> str:
        """__str__ as an abstract method every child class must implement

        :raises NotImplementedError: Abstract method must be implemented in child class
        :return: string describing Node
        :rtype: str
        """
        raise NotImplementedError

    def __copy__(self) -> BaseNode:
        """Make a shallow copy of BaseNode objects

        :return: the shallow copy
        :rtype: BaseNode
        """
        cls = self.__class__
        result = cls.__new__(cls)
        result.__dict__.update(self.__dict__)
        return result

    def __deepcopy__(self, memo: Dict) -> BaseNode:
        """Make a deep copy of BaseNode objects

        :param memo: memo
        :type memo: Dict
        :return: A deepcopy of self
        :rtype: BaseNode
        """
        cls = self.__class__
        result = cls.__new__(cls)
        memo[id(self)] = result
        for k, v in self.__dict__.items():
            setattr(result, k, copy.deepcopy(v, memo))
        return result

    @abstractmethod
    def to_bytes(self) -> bytes:
        """Serialize Node

        :raises NotImplementedError: Implement this abstract method in child classes
        :return: serialized node (binary data)
        :rtype: bytes
        """
        raise NotImplementedError

    @abstractmethod
    def to_stream(self, stream: io) -> None:
        """Serialize Node and dump to given stream

        :param stream: stream to output to
        :type stream: io
        :raises NotImplementedError: Implement this abstract method in child classes
        """
        raise NotImplementedError


class FileNode(BaseNode):
    """
    File Node Abstract Class
    """

    def __init__(
        self,
        path: pathlib2.Path,
        depth: int = None,
        root: pathlib2.Path = None,
        children: Union[List, None] = None,
    ) -> None:
        """FileNode Initializer

        :param path: file path
        :type path: pathlib2.Path
        :param depth: depth of file/directory relative to root, defaults to None
        :type depth: int, optional
        :param root: root path, can be None, defaults to None
        :type root: pathlib2.Path, optional
        :param children: List of Node when current node is a directory, None if current node is a file, defaults to None
        :type children: Union[List, None], optional
        """
        self._path = path
        self._root = root
        self._relative_path = self._path.relative_to(self._root) if self._root else None
        self._depth = depth
        self._filename = path.name
        self._stat = path.stat()
        self._children = children if children else []
        self._id = UniqueFileIdentifier(self._path)

    def __str__(self) -> str:
        """File Node to String Form

        :return: absolute path of current file node in string form
        :rtype: str
        """
        return str(self._path.absolute())

    def __eq__(self, other: FileNode) -> bool:
        """decide whether 2 file nodes are identical

        :param other: Another File Node to compare with
        :type other: FileNode
        :return: The two nodes' id (UniqueFileIdentifier) are identical
        :rtype: bool
        """
        return self._id == other.get_id()

    def get_children(self) -> List[FileNode]:
        """Get children nodes of current file node

        :return: child file nodes
        :rtype: List[FileNode]
        """
        return self._children

    def set_children(self, children: List[FileNode]) -> None:
        """children attribute setter

        :param children: child nodes of a file node
        :type children: List[FileNode]
        """
        self._children = children

    def get_path(self) -> pathlib2.Path:
        """file path getter

        :return: file path of this file node
        :rtype: pathlib2.Path
        """
        return self._path

    def get_filename(self) -> str:
        """Filename getter

        :return: filename of this file node
        :rtype: str
        """
        return self._filename

    def get_stat(self) -> os.stat_result:
        """file node stat getter

        :return: stat of this file node
        :rtype: os.stat_result
        """
        return self._stat

    def get_id(self) -> UniqueFileIdentifier:
        """FileNode id getter

        :return: UniqueFileIdentifier (id) of this file node
        :rtype: UniqueFileIdentifier
        """
        return self._id

    def get_depth(self) -> int:
        """FileNode depth relative to root getter

        :return: depth of this file node with respect to root path
        :rtype: int
        """
        return self._depth

    def get_root(self) -> pathlib2.Path:
        """root getter

        :return: node's root path
        :rtype: pathlib2.Path
        """
        return self._root

    def get_relative_path(self) -> pathlib2.Path:
        """file node's relative path to root getter

        :return: file node's relative path
        :rtype: pathlib2.Path
        """
        return self._relative_path

    def is_dir(self) -> bool:
        """Test if self is a directory

        :return: whether this is a directory FileNode
        :rtype: bool
        """
        return stat.S_ISDIR(self._stat.st_mode)

    def is_file(self) -> bool:
        """Test if self is a file

        :return: whether this is a file FileNode
        :rtype: bool
        """
        return stat.S_ISREG(self._stat.st_mode)

    def to_bytes(self) -> bytes:
        return pickle.dumps(self)

    def to_stream(self, stream: io) -> None:
        return pickle.dump(self, stream)

    def to_dict(self) -> Dict:
        """Generate dict style file node tree using self as root node

        :return: dict representing file tree rooted at self
        :rtype: Dict
        """
        children = [child.to_dict() for child in self._children]
        return {
            "id": str(self._id),
            "depth": self._depth,
            "filename": self._filename,
            "path": str(self._path),
            "relative_path": str(self._relative_path),
            "root": str(self._root),
            "children": children,
            "st_size": self._stat.st_size,
        }

    def to_json(self, indent: int = 0) -> str:
        """Generate json style file node tree using self as root node

        :param indent: number of space for indent, defaults to None
        :type indent: int, optional
        :return: json str representing file tree rooted at self
        :rtype: str
        """
        return json.dumps(self.to_dict(), indent=indent)

    def walk(
        self, recursive: bool = False, no_dir: bool = False
    ) -> Generator[FileNode]:
        """Walk through the children (recursively)

        >>> scraper = Scraper(Path("/Users/hacker/Documents/Learn/brain/docs"), filters=[MarkdownFilter()], scrape_now=True)
        >>> for node in scraper.get_tree().walk(recursive=True):
                print(node.get_path())
        
        :param recursive: Recursive Search, defaults to False
        :type recursive: bool, optional
        :param no_dir: Don't consider directory, defaults to False
        :type no_dir: bool, optional
        :yield: A file node
        :rtype: Generator[FileNode]
        """
        if not no_dir:
            yield self
        for child in self._children:
            if child.is_dir() and recursive:
                yield from child.walk(recursive, no_dir)
            elif child.is_file():
                yield child
import io
import sys
from typing import Iterable

import pathlib2
from abc import ABC, abstractmethod
from node import Node
from scraper import Scraper
from filter import MarkdownFilter


class Formatter(ABC):
    def __init__(self, root: Node):
        self.root = root
        self.stringio = io.StringIO()

    @abstractmethod
    def generate(self) -> io.StringIO:
        raise NotImplementedError

    def get_stringio(self) -> io.StringIO:
        return self.stringio

    def to_file(self, filename: pathlib2):
        with open(str(filename.absolute())) as f:
            f.write(self.stringio.getvalue())

    def to_stream(self, stream: io.TextIOBase):
        stream.write(self.stringio.getvalue())


class TabFormatter(Formatter):
    def __init__(self, root: Node):
        super(TabFormatter, self).__init__(root)

    def generate(self) -> io.StringIO:
        def iterate(node_: Node) -> None:
            print("\t" * node_.get_depth() + node_.get_filename(), file=self.stringio)
            if node_.get_children():
                for node in node_.get_children():
                    iterate(node)

        iterate(self.root)
        return self.stringio


class TreeCommandFormatter(Formatter):
    # prefix components:
    space = '    '
    branch = '│   '
    # pointers:
    tee = '├── '
    last = '└── '

    def __init__(self, root: Node):
        super(TreeCommandFormatter, self).__init__(root)

    def generate(self) -> io.StringIO:
        def iterate(node_: Node, prefix: str = '') -> Iterable:
            children = node_.get_children()
            # contents each get pointers that are ├── with a final └── :
            pointers = [TreeCommandFormatter.tee] * (len(children) - 1) + [TreeCommandFormatter.last]
            for pointer, node in zip(pointers, children):
                yield prefix + pointer + node.get_filename()
                if children:  # extend the prefix and recurse:
                    extension = TreeCommandFormatter.branch if pointer == TreeCommandFormatter.tee else TreeCommandFormatter.space
                    # i.e. space because last, └── , above so no more |
                    yield from iterate(node, prefix=prefix + extension)

        self.stringio.write(self.root.get_filename() + "\n")
        for line in iterate(self.root):
            self.stringio.write(line + "\n")
        return self.stringio


class MarkdownContentFormatter(Formatter):
    def __init__(self, root, filename=None, stream=None):
        super(MarkdownContentFormatter, self).__init__(root)
        self.filename = filename
        self.stream = stream

    def generate(self):
        pass

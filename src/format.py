import io
import sys
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
    def generate(self):
        raise NotImplementedError

    def to_file(self, filename: pathlib2):
        with open(str(filename.absolute())) as f:
            f.write(self.stringio.getvalue())

    def to_stream(self, stream: io.TextIOBase):
        stream.write(self.stringio.getvalue())


class TabFormatter(Formatter):
    def __init__(self, root: Node):
        super(TabFormatter, self).__init__(root)

    def generate(self):
        def iterate(node_: Node):
            print("\t" * node_.get_depth() + node_.get_filename(), file=self.stringio)
            if node_.get_children() is not None:
                for node in node_.get_children():
                    iterate(node)

        iterate(self.root)
        return self.stringio


class TreeCommandFormatter(Formatter):
    vertical = "\u2502"
    horizontal = "\u2500"
    three = "\u251C"
    two = "\u2514"

    def __init__(self, root: Node):
        super(TreeCommandFormatter, self).__init__(root)

    def generate(self):
        pass


class MarkdownContentFormatter(Formatter):
    def __init__(self, root, filename=None, stream=None):
        super(MarkdownContentFormatter, self).__init__(root)
        self.filename = filename
        self.stream = stream

    def generate(self):
        pass

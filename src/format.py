import io
import sys
import pathlib2
from abc import ABC, abstractmethod


class Formatter(ABC):
    def __init__(self, root):
        self.root = root

    @abstractmethod
    def generate(self):
        pass

    @abstractmethod
    def to_file(self, filename: pathlib2):
        pass

    @abstractmethod
    def to_stream(self, stream):
        pass


class MarkdownContentFormatter(Formatter):
    def __init__(self, root, filename=None, stream=None):
        super(MarkdownContentFormatter, self).__init__(root)
        self.filename = filename
        self.stream = stream

    def generate(self):
        pass

    def to_file(self, filename: pathlib2):
        pass

    def to_stream(self, stream):
        pass


if __name__ == '__main__':
    output = io.StringIO()
    output.write('First line.\n')
    print('Second line.', file=output)
    print('Second line.', file=sys.stderr)
    print(output.getvalue())
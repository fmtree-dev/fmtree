import re
import pathlib
from abc import ABC, abstractmethod


class Parser(ABC):
    def __init__(self, parse_function):
        self.history = set()
        self.parse_function = parse_function

    @abstractmethod
    def get_valid_children(self, path: pathlib.Path):
        raise NotImplementedError


if __name__ == '__main__':
    pass

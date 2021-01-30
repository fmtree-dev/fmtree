import os
import pathlib2
from abc import ABC, abstractmethod


class Node(ABC):
    def __init__(self, path: pathlib2.Path):
        self.path = path
        self.filename = path.name
        self.stat = path.stat()

import copy
from typing import Iterable, List
from abc import ABC, abstractmethod

from .node import FileNode


class BaseSorter(ABC):

    def run(self, root_node: FileNode) -> FileNode:
        tree = copy.deepcopy(root_node)

        def traverse(node: FileNode):
            if node.get_children():
                node.set_children(self.sorted(node.get_children()))
            for child in node.get_children():
                traverse(child)

        traverse(tree)
        return tree

    @abstractmethod
    def sorted(self, nodes: List[FileNode]) -> List[FileNode]:
        raise NotImplementedError

    def __call__(self, node: FileNode) -> FileNode:
        return self.run(node)


class Sorter(BaseSorter):
    def sorted(self, nodes: List[FileNode]) -> Iterable:
        return sorted(nodes, key=lambda node: node.get_filename())

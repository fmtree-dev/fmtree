import copy
from typing import Iterable, List
from abc import ABC, abstractmethod

from fmtree.core.node import FileNode


class BaseSorter(ABC):
    """
    Sorter Base Class for sorting child nodes
    """
    def run(self, root_node: FileNode) -> FileNode:
        """
        Traverse through the tree and run sorting algorithm implemented by child class
        :param root_node: root node
        :return: another tree root node
        """
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
        """
        Abstract method for sorting children nodes
        :param nodes: a list of nodes which is children of another node
        :return: a list of sorted nodes
        """
        raise NotImplementedError

    def __call__(self, node: FileNode) -> FileNode:
        return self.run(node)


class Sorter(BaseSorter):
    def sorted(self, nodes: List[FileNode]) -> Iterable:
        return sorted(nodes, key=lambda node: node.get_filename())

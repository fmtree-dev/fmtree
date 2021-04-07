import pathlib2

from fmtree.core.node import FileNode


def reproduce_fs_tree(target_dir: pathlib2.Path, root: FileNode) -> None:
    """
    Given a tree, recreate the tree structure in the file system
    :param target_dir: directory the structure is going to be reproduced in
    :param root: tree root node
    :return: None
    """
    target_dir.mkdir(parents=True, exist_ok=True)
    if root and root.get_filename():
        target_dir /= root.get_filename()

    def traverse(node: FileNode):
        if node.get_root() is None or node.get_relative_path() is None:
            raise ValueError("To reproduce given tree in file system, every node much have relative path,"
                             "since relative path is calculated with root path, FileNode has to be initialized"
                             "with root path. both root and relative path must be available")
        path = target_dir / node.get_relative_path()
        if node.is_dir():
            path.mkdir(parents=True, exist_ok=True)
        elif node.is_file():
            path.touch(exist_ok=True)
        if node.get_children():
            for child_node in node.get_children():
                traverse(child_node)

    traverse(root)

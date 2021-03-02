import io
from typing import Iterable, List, Union
from abc import ABC, abstractmethod

import pathlib2

from .node import FileNode


class BaseFormatter(ABC):
    def __init__(self, root: FileNode) -> None:
        self.root = root
        self.stringio = io.StringIO()

    @abstractmethod
    def generate(self) -> io.StringIO:
        raise NotImplementedError

    def get_stringio(self) -> io.StringIO:
        return self.stringio

    def to_file(self, filename: Union[pathlib2.Path, str], append: bool = False) -> None:
        path = str(filename.absolute()) if isinstance(filename, pathlib2.Path) else filename
        file_mode = "a" if append else "w"
        with open(path, file_mode) as f:
            f.write(self.stringio.getvalue())

    def to_stream(self, stream: io.TextIOBase) -> None:
        stream.write(self.stringio.getvalue())


class TabFormatter(BaseFormatter):
    def __init__(self, root: FileNode) -> None:
        super(TabFormatter, self).__init__(root)

    def generate(self) -> io.StringIO:
        def iterate(node_: FileNode) -> None:
            print("\t" * node_.get_depth() + node_.get_filename(), file=self.stringio)
            if node_.get_children():
                for node in node_.get_children():
                    iterate(node)

        iterate(self.root)
        return self.stringio


class TreeCommandFormatter(BaseFormatter):
    # prefix components:
    space = '    '
    branch = '│   '
    # pointers:
    tee = '├── '
    last = '└── '

    def __init__(self, root: FileNode) -> None:
        super(TreeCommandFormatter, self).__init__(root)

    def generate(self) -> io.StringIO:
        def iterate(node_: FileNode, prefix: str = '') -> Iterable:
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


class ListFileFormatter(BaseFormatter):
    def __init__(self, root: FileNode) -> None:
        super(ListFileFormatter, self).__init__(root)
        self.paths = []

    def generate(self) -> io.StringIO:
        def iterate(node_: FileNode) -> Iterable:
            if node_.get_path().is_file():
                yield node_.get_path()
            children = node_.get_children()
            for child_node in children:
                yield from iterate(child_node)

        for path in iterate(self.root):
            self.stringio.write(str(path) + "\n")
            self.paths.append(path)
        return self.stringio

    def get_paths(self) -> List[pathlib2.Path]:
        return self.paths


class MarkdownContentFormatter(BaseFormatter):
    def __init__(self, root: FileNode) -> None:
        super(MarkdownContentFormatter, self).__init__(root)

    def generate(self) -> io.StringIO:
        def iterate(node_: FileNode) -> Iterable:
            prefix_tabs = node_.get_depth() * '\t'
            yield f"{prefix_tabs}- {node_.get_filename()}"
            children = node_.get_children()
            for child_node in children:
                yield from iterate(child_node)

        for line in iterate(self.root):
            self.stringio.write(line + "\n")
        return self.stringio


class MarkdownLinkContentFormatter(BaseFormatter):
    def __init__(self, root: FileNode) -> None:
        super(MarkdownLinkContentFormatter, self).__init__(root)

    def generate(self) -> io.StringIO:
        def iterate(node_: FileNode) -> Iterable:
            prefix_tabs = node_.get_depth() * '\t'
            if node_.get_path().is_file():
                link = './' + str(node_.get_path().relative_to(self.root.get_path()))
                yield f"{prefix_tabs}- [{node_.get_filename()}]({link})"
            else:
                yield f"{prefix_tabs}- {node_.get_filename()}"

            children = node_.get_children()
            for child_node in children:
                yield from iterate(child_node)

        for line in iterate(self.root):
            self.stringio.write(line + "\n")

        return self.stringio


class GithubMarkdownContentFormatter(BaseFormatter):
    def __init__(self, root: FileNode, no_readme_link: bool = True, dir_link: bool = True,
                 full_dir_link: bool = False, remove_md_ext: bool = True) -> None:
        super(GithubMarkdownContentFormatter, self).__init__(root)
        self.no_readme_link = no_readme_link
        self.full_dir_link = full_dir_link
        self.dir_link = dir_link
        self.remove_md_ext = remove_md_ext

    def generate(self) -> io.StringIO:
        def iterate(node_: FileNode) -> None:
            prefix_tabs = node_.get_depth() * '\t'
            path = node_.get_path()
            link = './' + str(path.relative_to(self.root.get_path()))
            if path.is_dir():
                if self.full_dir_link:
                    print(f"{prefix_tabs}- [{node_.get_filename()}]({link})", file=self.stringio)
                else:
                    if self.dir_link and (path / "README.md").exists():
                        print(f"{prefix_tabs}- [{node_.get_filename()}]({link})", file=self.stringio)
                    else:
                        print(f"{prefix_tabs}- {node_.get_filename()}", file=self.stringio)
            elif path.is_file():
                display_name = node_.get_filename().replace(".md", "") \
                    if node_.get_filename()[-3:] == ".md" and self.remove_md_ext else node_.get_filename()
                if not (self.no_readme_link and path.name == "README.md"):
                    print(f"{prefix_tabs}- [{display_name}]({link})", file=self.stringio)
            else:
                raise ValueError("Unhandled Error")
            children = node_.get_children()
            for child_node in children:
                iterate(child_node)

        iterate(self.root)
        return self.stringio

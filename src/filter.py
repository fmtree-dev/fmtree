from abc import ABC, abstractmethod

import re
from typing import List, Union

import pathlib2


class Filter(ABC):
    """
    Path filter abstract class
    """

    def __init__(self, root: pathlib2.Path = None,
                 whitelist: Union[List[Union[str, pathlib2.Path]], None] = None,
                 blacklist: Union[List[Union[str, pathlib2.Path]], None] = None):
        """
        allow and ignore list must be lists of absolute paths
        if root is specified, then allow and ignore are both relative paths
        else allow and ignore are absolute paths
        :param root: root path
        :param whitelist: List of allowed paths (either absolute or relative paths)
        :param blacklist: List of ignored paths (either absolute or relative paths)
        """
        self.root = root
        self.whitelist = whitelist if whitelist else []
        self.blacklist = blacklist if blacklist else []
        self._update()

    def _update(self):
        if self.root:
            self.whitelist = [(self.root / path).resolve().absolute() for path in self.whitelist]
            self.blacklist = [(self.root / path).resolve().absolute() for path in self.blacklist]

    def set_root(self, root: pathlib2.Path):
        self.root = root
        # self.

    @abstractmethod
    def __call__(self, path: pathlib2.Path):
        """
        taking a path and decide whether it agrees with the filter
        :param path: pathlib2.Path: file path
        :return: bool: whether agree with the filter
        """
        raise NotImplementedError


class MarkdownFilter(Filter):
    """
    A filter that keeps only markdown files and intermediate directories (non-files)
    """

    def __call__(self, path: pathlib2.Path):
        """
        Take a path and decide whether it's a markdown file
        :param path: pathlib2.Path: file path
        :return: bool: true if path is a markdown file or a directory/link, false otherwise
        """
        return path.name.endswith(".md") and path.is_file() if path.is_file() else True


class ExtensionFilter(Filter):
    """
    A filter that only keeps files with given extensions and intermediate directories (non-files)
    """

    def __init__(self, extensions: List[str]):
        """
        Initialize Extension Filter
        :param extensions: list of allowed file extensions
        """
        self._extensions = extensions

    def __call__(self, path: pathlib2.Path):
        """
        Decide if the given path has one of the allowed extensions (self._extensions)
        :param path: a pathlib2.Path file path
        :return: true if the given path has one of the allowed extensions, false otherwise
        """
        return sum(
            [path.name.endswith(ext) and path.is_file() if path.is_file() else True for ext in self._extensions]) > 0


class RegexFilter(Filter):
    """
    Filter with Regular Expression
    """

    def __init__(self, regex_pattern: str):
        """
        Initialize a Regular Expression Filter with a regex pattern
        :param regex_pattern: regular expression string
        """
        self._pattern = re.compile(regex_pattern)

    def __call__(self, path: pathlib2.Path):
        """
        Take a path and decide whether it matches the regular expression self._pattern
        :param path: pathlib2.Path: file path
        :return: bool: true if path matches regular expression, false otherwise
        """
        return self._pattern.match(str(path)) is not None


def markdown_filter(path: pathlib2.Path):
    """
    A function form markdown file filter
    :param path: a pathlib2.Path path
    :return: true if path is a markdown file or directory/link, false otherwise
    """
    return path.name.endswith(".md") if path.is_file() else True

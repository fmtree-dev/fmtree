from abc import ABC, abstractmethod

import re
from typing import List, Iterable


class BaseFilter(ABC):
    """
    Path filter abstract class
    """

    @abstractmethod
    def filter(self, items: Iterable) -> Iterable:
        """
        taking a path and decide whether it agrees with the filter
        :param items: items to be filtered
        :return: Iterable: result after filtering
        """
        raise NotImplementedError

    def __call__(self, items: Iterable) -> Iterable:
        """
        taking a path and decide whether it agrees with the filter
        :param path: items to be filtered
        :return: Iterable: result after filtering, only markdown and directory are kept
        """
        return self.filter(items)


class MarkdownFilter(BaseFilter):
    """
    A filter that keeps only markdown files and intermediate directories (non-files)
    """

    def filter(self, items: Iterable) -> Iterable:
        return list(
            filter(lambda path: path.name.endswith(".md") and path.is_file() if path.is_file() else True, items))


class ExtensionFilter(BaseFilter):
    """
    A filter that only keeps files with given extensions and intermediate directories (non-files)
    """

    def __init__(self, extensions: List[str]):
        """
        Initialize Extension Filter
        :param extensions: list of allowed file extensions
        """
        self._extensions = extensions

    def filter(self, items: Iterable) -> Iterable:
        """
        Decide if the given path has one of the allowed extensions (self._extensions)
        :param items: Iterable, files to be filtered
        :return: filtered files with either directory or allowed extensions
        """
        return list(
            filter(lambda filepath: sum(
                map(lambda ext: filepath.name.endswith(ext) or filepath.is_dir(), self._extensions)) > 0, items))


class RegexFilter(BaseFilter):
    """
    Filter with Regular Expression
    """

    def __init__(self, regex_patterns: List) -> None:
        """
        Initialize a Regular Expression Filter with a regex pattern
        :param regex_patterns: regular expression list
        """
        self._patterns = [re.compile(pattern) for pattern in regex_patterns]

    def filter(self, items: Iterable) -> Iterable:
        """
        Take a path and decide whether it matches the regular expression self._pattern
        :param items: Iterable, files to be filtered
        :return: Iterable: filter out file paths that don't match regular expression
        """

        return list(
            filter(lambda filepath: sum(
                map(lambda pattern: pattern.match(str(filepath)) is not None or filepath.is_dir(), self._patterns)) > 0,
                   items))
        # return self._pattern.match(str(path)) is not None


def markdown_filter(items: Iterable) -> Iterable:
    """
    A function form markdown file filter
    :param items: files to be filtered
    :return: Iterable, filtered files (only markdown and directory are kept)
    """
    return list(filter(lambda path: path.name.endswith(".md") and path.is_file() if path.is_file() else True, items))

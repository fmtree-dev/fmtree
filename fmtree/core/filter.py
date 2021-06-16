import pathlib2
from abc import ABC, abstractmethod

import re
from typing import List, Iterable, TypeVar

from .constants import HTML_IMAGE_EXTENSIONS

T = TypeVar('T')
ACCEPT_MODE = 0
IGNORE_MODE = 1


class BaseFilter(ABC):
    """
    Path filter abstract class
    """

    @abstractmethod
    def filter(self, items: Iterable) -> Iterable:
        """apply filter to iterable

        :param items: items to be filtered
        :type items: Iterable
        :raises NotImplementedError: Abstract method has to be implemented
        :return: items to keep
        :rtype: Iterable
        """
        raise NotImplementedError

    def __call__(self, items: Iterable) -> Iterable:
        """__call__ function to apply filter
        :param items: items to be filtered
        :type items: Iterable
        :return: result after filtering
        :rtype: Iterable
        """
        return self.filter(items)


class BaseFileFilter(BaseFilter):

    def __init__(self, ignore_list: Iterable = None, root_path: pathlib2.Path = None, mode: int = IGNORE_MODE) -> None:
        """BaseFilter Initializer

        :param ignore_list: list of regex to ignore, defaults to None
        :type ignore_list: Iterable, optional
        :param root_path: path to scrape, used to obtain relative path, defaults to None
        :type root_path: pathlib2.Path, optional
        :param mode: whether the filter is for keeping files or filtering out files, defaults to IGNORE_MODE
        :type mode: int, optional
        """

        self.ignore_list = list(map(re.compile, ignore_list)) if ignore_list else []
        self.root_path = root_path
        assert mode == ACCEPT_MODE or mode == IGNORE_MODE
        self.mode = mode

    def set_root_path(self, root_path: pathlib2.Path) -> None:
        """root_path setter

        :param root_path: path to scrape, used to obtain relative path
        :type root_path: pathlib2.Path
        """
        self.root_path = root_path.resolve().absolute()

    # @abstractmethod
    def filter(self, items: Iterable) -> Iterable:
        """apply filter to iterable

        :param items: items to be filtered
        :type items: Iterable
        :raises NotImplementedError: Abstract method has to be implemented
        :return: items to keep
        :rtype: Iterable
        """
        raise NotImplementedError

    def __call__(self, paths: Iterable[pathlib2.Path]) -> Iterable[pathlib2.Path]:
        """__call__ function to apply filter
        A wrapper for self.filter, pre-filter based on ignore_list first, then pass the result into self.filter
        :param paths: paths to be filtered
        :type paths: Iterable
        :return: result after filtering
        :rtype: Iterable
        """

        def make_decision(path: pathlib2.Path):
            match_sum = sum(
                map(lambda ignore: ignore.match(str(path.relative_to(self.root_path))) is not None,
                    self.ignore_list))
            return match_sum == 0 if self.mode == IGNORE_MODE else match_sum > 0

        paths = list(filter(lambda path: make_decision(path), paths))
        return self.filter(paths)


class IdentityFilter(BaseFileFilter):
    """Useless filter, return what it receives"""

    def filter(self, items: Iterable) -> Iterable:
        """return what it gets directly, does no filtering

        :param items: paths to be filtered
        :type items: Iterable
        :return: filtered paths (same as what's passed in)
        :rtype: Iterable
        """
        return items


class MarkdownFilter(BaseFileFilter):
    """
    A filter that keeps only markdown files and intermediate directories (non-files)
    """

    def filter(self, items: Iterable) -> Iterable:
        return list(
            filter(lambda path: path.name.endswith(".md") and path.is_file() if path.is_file() else True, items))


class ExtensionFilter(BaseFileFilter):
    """
    A filter that only keeps files with given extensions and intermediate directories (non-files)
    """

    def __init__(self, extensions: List[str], ignore_list: Iterable = None, root_path: pathlib2.Path = None,
                 mode: int = IGNORE_MODE) -> None:
        """Initialize Extension Filter

        :param extensions: list of allowed file extensions
        :type extensions: List[str]
        :param ignore_list: [description], defaults to None
        :type ignore_list: Iterable, optional
        :param root_path: [description], defaults to None
        :type root_path: pathlib2.Path, optional
        :param mode: [description], defaults to IGNORE_MODE
        :type mode: int, optional
        """
        super(ExtensionFilter, self).__init__(ignore_list=ignore_list, root_path=root_path, mode=mode)
        self._extensions = extensions

    def filter(self, items: List[T]) -> List[T]:
        """
        Decide if the given path has one of the allowed extensions (self._extensions)
        :param items: Iterable, files to be filtered
        :return: filtered files with either directory or allowed extensions
        """
        return list(
            filter(lambda filepath: sum(
                map(lambda ext: filepath.name.endswith(ext) or filepath.is_dir(), self._extensions)) > 0, items))


class RegexFilter(BaseFileFilter):
    """
    Filter with Regular Expression
    """

    def __init__(self, regex_patterns: List[str], ignore_list: Iterable = None, root_path: pathlib2.Path = None,
                 mode: int = IGNORE_MODE) -> None:
        """
        Initialize a Regular Expression Filter with a regex pattern
        :param regex_patterns: regular expression list
        """
        super(RegexFilter, self).__init__(ignore_list=ignore_list, root_path=root_path, mode=mode)
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


class ImageFilter(ExtensionFilter):
    """A variant/wrapper of ExtensionFilter
    Filter based on commonly-seen image extensions (can be customized)
    """

    def __init__(self, image_extensions: List[str] = HTML_IMAGE_EXTENSIONS, ignore_list: Iterable = None,
                 root_path: pathlib2.Path = None, mode: int = IGNORE_MODE):
        """ImageFilter Initializer

        :param image_extensions: target extensions, defaults to HTML_IMAGE_EXTENSIONS
        :type image_extensions: List[str], optional
        :param ignore_list: paths to ignore, defaults to None
        :type ignore_list: Iterable, optional
        :param root_path: path to scrape, defaults to None
        :type root_path: pathlib2.Path, optional
        :param mode: whether the filter is IGNORE_MODE or ACCEPT_MODE, defaults to IGNORE_MODE
        :type mode: int, optional
        """

        super(ImageFilter, self).__init__(image_extensions, ignore_list=ignore_list, root_path=root_path, mode=mode)

    def filter(self, items: List[T]) -> List[T]:
        return super().filter(items)

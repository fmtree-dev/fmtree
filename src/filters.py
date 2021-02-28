from abc import ABC, abstractmethod

import re

import pathlib2


class Filter(ABC):
    @abstractmethod
    def __call__(self, path: pathlib2.Path):
        raise NotImplementedError


class MarkdownFilter(Filter):
    def __call__(self, path: pathlib2.Path):
        return path.name.endswith(".md") and path.is_file() if path.is_file() else True


class RegexFilter(Filter):
    def __init__(self, regex_pattern: str):
        self.pattern = re.compile(regex_pattern)

    def __call__(self, path: pathlib2.Path):
        return self.pattern.match(str(path)) is not None


def markdown_filter(path: pathlib2.Path):
    return path.name.endswith(".md") if path.is_file() else True


if __name__ == '__main__':
    f = MarkdownFilter()
    p = pathlib2.Path("asdq.md")
    print(f(p))
    print(markdown_filter(p))
    regex_f = RegexFilter("^.+\.md$")
    print(regex_f(p))

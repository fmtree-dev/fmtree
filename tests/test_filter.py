import fmtree.core.filter as filter_

import pathlib2

paths = [
    pathlib2.Path("/p/a.md"),
    pathlib2.Path("/p/b.java"),
    pathlib2.Path("/p/c.py"),
    pathlib2.Path("/p/d.cpp"),
    pathlib2.Path("/p/e.c"),
    pathlib2.Path("/p/f.ini"),
]


class TestExtensionFilter:
    def test_filter(self):
        extensions = [".md", ".py"]
        ext_filter = filter_.ExtensionFilter(extensions=extensions)
        result = set(ext_filter(paths))
        target = {pathlib2.Path("/p/a.md"), pathlib2.Path("/p/c.py")}
        assert result == target


class TestRegexFilter:
    def test_filter(self):
        regex_patterns = [".+\\.md", ".+\\.py"]
        regex_filter = filter_.RegexFilter(regex_patterns=regex_patterns)
        result = set(regex_filter(paths))
        target = {pathlib2.Path("/p/a.md"), pathlib2.Path("/p/c.py")}
        assert result == target

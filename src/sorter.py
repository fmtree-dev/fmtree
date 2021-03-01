from typing import Iterable
from abc import ABC, abstractmethod


class BaseSorter(ABC):
    @abstractmethod
    def sorted(self, iterable: Iterable) -> Iterable:
        raise NotImplementedError

    def __call__(self, iterable: Iterable) -> Iterable:
        return self.sorted(iterable)


class Sorter(BaseSorter):
    def sorted(self, iterable: Iterable) -> Iterable:
        return sorted(iterable)

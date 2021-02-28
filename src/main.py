import os
import re
import io
import sys
import pathlib2
import scraper

path = pathlib2.Path('/Users/huakunshen/Local/Dev/OSCP')


class Filter:
    def __init__(self):
        pass

    def __call__(self, x):
        print(x)


if __name__ == '__main__':
    f = Filter()
    f(1)

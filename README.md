# FileTree

[![Build Documentation](https://github.com/fmtree-dev/fmtree/actions/workflows/build-docs.yml/badge.svg)](https://github.com/fmtree-dev/fmtree/actions/workflows/build-docs.yml)
[![Pytest](https://github.com/fmtree-dev/fmtree/actions/workflows/python-package.yml/badge.svg)](https://github.com/fmtree-dev/fmtree/actions/workflows/python-package.yml)
![Publish Package](https://github.com/fmtree-dev/fmtree/actions/workflows/python-publish.yml/badge.svg)
[![CircleCI](https://circleci.com/gh/fmtree-dev/fmtree.svg?style=shield)](https://circleci.com/gh/fmtree-dev/fmtree)
## Documentation

https://fmtree-dev.github.io/fmtree/


## Sample Output

### GithubMarkdownContentFormatter

```
- OSCP
- [Notes](./Notes)
  - Tools
    - [Python](./Notes/Tools/Python.md)
    - [nmap](./Notes/Tools/nmap.md)
    - [Netcat](./Notes/Tools/Netcat.md)
    - [Metasploit](./Notes/Tools/Metasploit.md)
  - [common](./Notes/common.md)
  - [FileTransfer](./Notes/FileTransfer.md)
  - [Service](./Notes/Service.md)
  - [Bash](./Notes/Bash.md)
```
#### Render in MarkDown
- OSCP
  - [Notes](./Notes)
    - Tools
      - [Python](./Notes/Tools/Python.md)
      - [nmap](./Notes/Tools/nmap.md)
      - [Netcat](./Notes/Tools/Netcat.md)
      - [Metasploit](./Notes/Tools/Metasploit.md)
    - [common](./Notes/common.md)
    - [FileTransfer](./Notes/FileTransfer.md)
    - [Service](./Notes/Service.md)
    - [Bash](./Notes/Bash.md)

### TreeCommandFormatter

```
OSCP
└── Notes
    ├── Tools
    │   ├── Python.md
    │   ├── nmap.md
    │   ├── Netcat.md
    │   └── Metasploit.md
    ├── common.md
    ├── FileTransfer.md
    ├── README.md
    ├── Service.md
    └── Bash.md
```

## Sample Code

```python
import sys
import pathlib2
from fmtree.core.scraper import Scraper
from fmtree.core.format import TreeCommandFormatter, GithubMarkdownContentFormatter
from fmtree.core.filter import MarkdownFilter
from fmtree.core.sorter import Sorter


path_ = pathlib2.Path('/OSCP')
scraper = Scraper(path_, scrape_now=False, keep_empty_dir=False)

# add filter
scraper.add_filter(filter_=MarkdownFilter())

# run scraper
scraper.run()

# GNU Tree Format
formatter = TreeCommandFormatter(scraper.get_tree())
stringio = formatter.generate()
print(stringio.getvalue())

# sort
sorter_ = Sorter()
tree = sorter_(scraper.get_tree())

# GitHub Content Format
formatter = GithubMarkdownContentFormatter(tree)
stringio = formatter.generate()
print(stringio.getvalue())
formatter.to_stream(sys.stdout)
```


## Visualizer

### fmtree.visualizer.visualize

A command line one-liner to visualize a directory like gnu tree

```
python -m fmtree.visualizer.visualize -h                                                      
usage: fmtree visualizer argument parser [-h] [--debug] [-i INPUT] [--stdout] [--stderr]
                                         [-o OUTPUT] [--tree] [--markdown] [--html]
                                         [--ext EXT [EXT ...]] [-d DEPTH]

optional arguments:
  -h, --help            show this help message and exit
  --debug               debug mode
  -i INPUT, --input INPUT
                        input path (path to format)
  --stdout              output to stdout
  --stderr              output to stderr
  -o OUTPUT, --output OUTPUT
                        output file path
  --tree                nu tree style output
  --markdown            markdown style output
  --html                html list style output
  --ext EXT [EXT ...]
  -d DEPTH, --depth DEPTH
                        Directory depth to parse
```

#### Sample Usage
```bash
python -m visualizer.visualize  -i '/home/user/images' --depth 5 --ext .jpg .png --stdout --debug --html
```

### fmtree.visualizer.image_dir

A command line one-liner that produce a html for visualizing an image directory.

It produces a html file that display all images in a nested image directory.

Just open the html file in a browser.

```
python -m visualizer.image_dir --help          
usage: Fmtree Visualizer Parser [-h] [-o OUTPUT] [-q]
                                [-d DEPTH] [--cdn]
                                [--show_all]
                                input

positional arguments:
  input                 input path

optional arguments:
  -h, --help            show this help message and exit
  -o OUTPUT, --output OUTPUT
                        output directory to save html
  -q, --quiet           whether to print out the
                        directory
  -d DEPTH, --depth DEPTH
                        Directory depth to parse
  --cdn                 Use CDN for libraries, requires
                        internet access, minimize html
                        size
  --show_all            Show All Images By Default
```

#### Sample Usage
```bash
python -m visualizer.image_dir --cdn /home/user/images
```










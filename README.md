# FileTree

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
path_ = pathlib2.Path('/OSCP')
scraper = Scraper(path_, scrape_now=False, keep_empty_dir=False)
scraper.add_filter(filter_=MarkdownFilter())
scraper.run()

# GNU Tree Format
formatter = TreeCommandFormatter(scraper.get_tree())
stringio = formatter.generate()
print(stringio.getvalue())

# GitHub Content Format
formatter = GithubMarkdownContentFormatter(scraper.get_tree())
stringio = formatter.generate()
print(stringio.getvalue())
formatter.to_stream(sys.stdout)
```

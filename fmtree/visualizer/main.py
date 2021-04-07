from fmtree.core.scraper import Scraper
from fmtree.core.filter import ImageFilter
from fmtree.core.format import TreeCommandFormatter
import argparse
import sys

import pathlib2
from jinja2 import Environment, FileSystemLoader

print(sys.path)

current_directory = pathlib2.Path(__file__).parent.absolute()


def main(args):
    print(args)
    scraper = Scraper(pathlib2.Path(args['input']), scrape_now=False, keep_empty_dir=False)
    scraper.add_filter(ImageFilter())
    scraper.run()
    tree = scraper.get_tree()
    formatter = TreeCommandFormatter(tree)
    stringio = formatter.generate()
    formatter.to_stream(sys.stdout)
    json_content = tree.to_json(indent=2)
    file_loader = FileSystemLoader(str(current_directory / 'template'))
    env = Environment(loader=file_loader)
    template = env.get_template('index.html')
    output = template.render(data=json_content)
    with open(str(pathlib2.Path(args['input']) / 'fmtree-image-visualizer.html'), 'w') as f:
        f.write(output)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Fmtree Visualizer Parser")
    parser.add_argument('--input', required=True, help='input path')
    parser.add_argument('--silent', type=bool, default=False, help="whether to print out the directory")
    args = parser.parse_args()
    main(dict(args.__dict__))

from fmtree.core.scraper import Scraper
from fmtree.core.filter import ImageFilter
from fmtree.core.format import TreeCommandFormatter
import argparse
import sys

import pathlib2
from jinja2 import Environment, FileSystemLoader

current_directory = pathlib2.Path(__file__).parent.absolute()


def main(args):
    print(args)
    scraper = Scraper(pathlib2.Path(args['input']), scrape_now=False, keep_empty_dir=False)
    scraper.add_filter(ImageFilter())
    scraper.run()
    tree = scraper.get_tree()
    formatter = TreeCommandFormatter(tree)
    if not args['silent']:
        formatter.to_stream(sys.stdout)
    json_content = tree.to_json(indent=2)
    file_loader = FileSystemLoader(str(current_directory / 'template'))
    env = Environment(loader=file_loader)
    template = env.get_template('index.html')
    with open(str(current_directory / 'template' / 'assets' / 'bootstrap.min.css'), 'r') as f:
        bootstrap_min_css = f.read()
    with open(str(current_directory / 'template' / 'assets' / 'bootstrap.bundle.min.js'), 'r') as f:
        bootstrap_min_js = f.read()
    with open(str(current_directory / 'template' / 'assets' / 'jquery-3.6.0.min.js'), 'r') as f:
        jquery_min_js = f.read()
    output = template.render(data=json_content, bootstrap_css=bootstrap_min_css, bootstrap_js=bootstrap_min_js,
                             jquery_js=jquery_min_js)
    with open(str(pathlib2.Path(args['input']) / 'fmtree-image-visualizer.html'), 'w') as f:
        f.write(output)
    print("finished")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Fmtree Visualizer Parser")
    parser.add_argument('input', help='input path')
    parser.add_argument('--silent', type=bool, default=False, help="whether to print out the directory")
    args = parser.parse_args()
    main(dict(args.__dict__))

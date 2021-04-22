from fmtree.core.scraper import Scraper
from fmtree.core.filter import ImageFilter
from fmtree.core.format import TreeCommandFormatter
import argparse
import sys

import pathlib2
from jinja2 import Environment, FileSystemLoader

current_directory = pathlib2.Path(__file__).parent.absolute()

bootstrap_css_cdn = """
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-eOJMYsd53ii+scO/bJGFsiCZc+5NDVN2yr8+0RDqr0Ql0h+rP48ckxlpbzKgwra6" crossorigin="anonymous">
"""
bootstrap_js_cdn = """
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta3/dist/js/bootstrap.bundle.min.js" integrity="sha384-JEW9xMcG8R+pH31jmWH6WWP0WintQrMb4s7ZOdauHnUtxwoG2vI5DkLtS3qm9Ekf" crossorigin="anonymous"></script>
"""
jquery_cdn = """
<script src="https://code.jquery.com/jquery-3.6.0.min.js" integrity="sha256-/xUj+3OJU5yExlq6GSYGSHk7tPXikynS7ogEvDej/m4=" crossorigin="anonymous"></script>
"""


def main(args):
    if not args['quiet']:
        print("Arguments")
        for key, value in args.items():
            print(f"\t{key}: {value}")
    scraper = Scraper(pathlib2.Path(args['input']), scrape_now=False, keep_empty_dir=False, depth=args['depth'])
    scraper.add_filter(ImageFilter())
    scraper.run()
    tree = scraper.get_tree()
    formatter = TreeCommandFormatter(tree)
    if not args['quiet']:
        formatter.generate()
        formatter.to_stream(sys.stdout)
    json_content = tree.to_json(indent=None)
    file_loader = FileSystemLoader(str(current_directory / 'template'))
    env = Environment(loader=file_loader)
    template = env.get_template('index.html')
    if args['cdn']:
        bootstrap_css, bootstrap_js, jquery_js = bootstrap_css_cdn, bootstrap_js_cdn, jquery_cdn
    else:
        with open(str(current_directory / 'template' / 'assets' / 'bootstrap.min.css'), 'r') as f:
            bootstrap_css = "<style>" + f.read() + "</style>"
        with open(str(current_directory / 'template' / 'assets' / 'bootstrap.bundle.min.js'), 'r') as f:
            bootstrap_js = "<script>" + f.read() + "</script>"
        with open(str(current_directory / 'template' / 'assets' / 'jquery-3.6.0.min.js'), 'r') as f:
            jquery_js = "<script>" + f.read() + "</script>"
    output = template.render(data=json_content, bootstrap_css=bootstrap_css, bootstrap_js=bootstrap_js,
                             jquery_js=jquery_js, show_all=args['show_all'])
    output_path = args['output'] if args['output'] else str(
        pathlib2.Path(args['input']) / 'fmtree-image-visualizer.html')
    with open(output_path, 'w') as f:
        f.write(output)
    if not args['quiet']:
        print("finished")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Fmtree Visualizer Parser")
    parser.add_argument('input', help='input path')
    parser.add_argument('-o', '--output', help='output directory to save html')
    parser.add_argument('-q', '--quiet', action='store_true', help="whether to print out the directory")
    parser.add_argument('-d', '--depth', type=int, default=10, help="Directory depth to parse")
    parser.add_argument('--cdn', action='store_true',
                        help="Use CDN for libraries, requires internet access, minimize html size")
    parser.add_argument('--show_all', action='store_true', help="Show All Images By Default")
    args = parser.parse_args()
    main(dict(args.__dict__))

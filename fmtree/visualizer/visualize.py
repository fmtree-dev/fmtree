import os
import sys
import argparse
import pathlib2
from fmtree.core.scraper import Scraper
from fmtree.core.format import TreeCommandFormatter, HTMLFormatter, MarkdownContentFormatter
from fmtree.core.filter import ExtensionFilter
from fmtree.core.sorter import Sorter


def validate_args(args_dict):
    def count_args(keys):
        count = 0
        for key in keys:
            count += 1 if args_dict[key] else 0
        return count
    keys = ['tree', 'markdown', 'html']
    if count_args(keys) != 1:
        raise ValueError(f"There can be only one style argument, choose from: {', '.join(keys)}")


def main(args_dict: dict):
    validate_args(args_dict)
    path = pathlib2.Path(args_dict['input']).absolute()
    scraper = Scraper(path, scrape_now=False, keep_empty_dir=False, depth=args_dict['depth'])
    scraper.add_filter(ExtensionFilter(extensions=['.md']))
    scraper.run()
    sorter = Sorter()
    tree = sorter(scraper.get_tree())
    if args_dict['html']:
        formatter = HTMLFormatter(tree)
    elif args_dict['tree']:
        formatter = TreeCommandFormatter(tree)
    elif args_dict['markdown']:
        formatter = MarkdownContentFormatter(tree)
    else:
        raise ValueError('No Valida output format is set')
    stringio = formatter.generate()
    if args_dict['stdout']:
        formatter.to_stream(sys.stdout)
    if args_dict['stderr']:
        formatter.to_stream(sys.stderr)
    if args_dict['output']:
        with open(args_dict['output'], 'w') as f:
            f.write(stringio.getvalue())


if __name__ == '__main__':
    parser = argparse.ArgumentParser("fmtree visualizer argument parser")
    parser.add_argument('--debug', action='store_true', help='debug mode')
    parser.add_argument('-i', '--input', default=os.getcwd(), help='input path (path to format)')
    # output location, there can be multiple output
    parser.add_argument('--stdout', action='store_true', help='output to stdout')
    parser.add_argument('--stderr', action='store_true', help='output to stderr')
    parser.add_argument('-o', '--output', help='output file path')
    # output style
    parser.add_argument('--tree', action='store_true', help='nu tree style output')
    parser.add_argument('--markdown', action='store_true', help='markdown style output')
    parser.add_argument('--html', action='store_true', help='html list style output')

    # filter
    parser.add_argument("--ext", nargs="+", default=["md"])
    parser.add_argument('-d', '--depth', type=int, default=10, help="Directory depth to parse")
    args = parser.parse_args()
    if args.debug:
        print("Begin")
        print("arguments:")
        for key, value in args.__dict__.items():
            print(f"\t{key}: {value}")
    main(args.__dict__)
    if args.debug:
        print("Finished")

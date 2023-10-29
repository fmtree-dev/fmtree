import argparse
import json
import os
from pathlib2 import Path
from PIL import Image
import imagehash
from fmtree.core.scraper import Scraper
from fmtree.core.filter import ImageFilter
from fmtree.core.node import FileNode
from fmtree.core.format import TreeCommandFormatter
from dataclasses import dataclass, asdict
from tqdm import tqdm
from typing import Callable, Union
import numpy as np
import multiprocessing as mp
from collections import defaultdict
import shutil
from enum import Enum

DEFAULT_NUM_WORKERS = max(mp.cpu_count() - 1, 1)


class HashMethod(Enum):
    AverageHashing = 'avg-hash'
    PerceptualHashing = 'perceptual-hash'
    DifferenceHashing = 'difference-hash'
    WaveletHashing = 'wavelet-hash'
    CropResistantHashing = 'crop-resistant-hash'
    ColorHashing = 'color-hash'


@dataclass
class ArgsConfig:
    recursive: bool
    path: Path
    output_json: None | Path
    remove_inplace: bool
    out_dir: None | Path
    dont_print_stats: bool
    num_workers: int
    hash_method: HashMethod


@dataclass
class ImageHash:
    hash_: np.ndarray
    file_node: FileNode


def compute_hash_diff(
        hash_func: Callable[[Image], np.ndarray], img1: Image, img2: Image
):
    return hash_func(img1) - hash_func(img2)


hash_function_method_union = Union[
    imagehash.average_hash,
    imagehash.phash,
    imagehash.dhash,
    imagehash.colorhash,
    imagehash.whash,
    imagehash.crop_resistant_hash
]


@dataclass
class HashComputer:
    hash_func: hash_function_method_union

    def __call__(self, file_node: FileNode):
        img = Image.open(str(file_node.get_path()))
        hash_ = self.hash_func(img)
        img.close()
        return file_node, hash_


def verify_args(args: ArgsConfig):
    if not args.path.exists():
        raise FileNotFoundError("Target Directory Not Found", args.path)
    if args.path.is_file():
        raise ValueError("Target Path is a File, Expect Directory", args.path)
    if args.out_dir and args.out_dir.exists():
        if args.out_dir.is_file():
            raise ValueError(
                f"Output path: {args.out_dir} exists and is a file, it should be either a directory or non-existing."
            )
        if args.out_dir.is_dir():
            is_empty = len(list(args.out_dir.iterdir())) == 0
            if not is_empty:
                clear_dir = input(
                    f"Target output directory is not empty, clear it? [Y/n]"
                )
                clear = len(clear_dir) == 0 or clear_dir.lower() == "y"
                if clear:
                    shutil.rmtree(str(args.out_dir))


def get_hash_function(hash_method: HashMethod) -> hash_function_method_union:
    if hash_method == HashMethod.AverageHashing:
        return imagehash.average_hash
    elif hash_method == HashMethod.PerceptualHashing:
        return imagehash.phash
    elif hash_method == HashMethod.DifferenceHashing:
        return imagehash.dhash
    elif hash_method == HashMethod.WaveletHashing:
        return imagehash.whash
    elif hash_method == HashMethod.CropResistantHashing:
        return imagehash.crop_resistant_hash
    elif hash_method == HashMethod.ColorHashing:
        return imagehash.colorhash
    else:
        raise ValueError("Invalid Hash Method: ", hash_method)


class DuplicateImageSearcher:
    def __init__(self, path: Path, hash_func: hash_function_method_union, num_workers: int = DEFAULT_NUM_WORKERS):
        self.path = path
        self.image_hash_dict: defaultdict[np.ndarray, list[Path]] = defaultdict(list)
        self.hash_func = hash_func
        self.num_workers = num_workers

    def run(self):
        scraper = Scraper(args.path, scrape_now=False, keep_empty_dir=False)
        # add filter
        scraper.add_filter(filter_=ImageFilter())
        # run scraper
        scraper.run()
        with mp.Pool(self.num_workers) as p:
            nodes = list(scraper.get_tree().walk(recursive=True, no_dir=True))
            hasher = HashComputer(self.hash_func)
            for file_node, hash_ in tqdm(p.imap_unordered(hasher, nodes), total=len(nodes)):
                self.image_hash_dict[hash_].append(file_node.get_path())


def main(args: ArgsConfig):
    print(f"Searching Duplicate Images in Directory: {args.path}; with hash function: {args.hash_method}")
    print(f"Number of Worker: {args.num_workers}")
    hash_func = get_hash_function(args.hash_method)
    searcher = DuplicateImageSearcher(args.path, hash_func, args.num_workers)
    searcher.run()
    image_hash_dict = searcher.image_hash_dict
    # now each path in image_hash_dict value array are duplicates, what to do with them?
    paths = [[str(p) for p in path_list] for path_list in image_hash_dict.values()]
    num_unique_images = len(paths)
    if not args.dont_print_stats:
        print(f"Number of Unique Images: {num_unique_images}")
        duplicate_arr_lengths = [len(lst) for lst in paths]
        print(f"Max Number of Duplicates: {max(duplicate_arr_lengths)}")
    if args.output_json:
        with open(str(args.output_json), "w") as f:
            # convert 2D array of pathlib2.Path into 2D array of str
            json.dump(paths, f, indent=4)
    if args.out_dir:
        print(f"Save unique images to {args.out_dir}")
        args.out_dir.mkdir(parents=True, exist_ok=True)
        for dup_image_paths in tqdm(image_hash_dict.values()):
            shutil.copyfile(dup_image_paths[0], args.out_dir / dup_image_paths[0].name)
        print(f"Images subset without duplicates saved to ({args.out_dir})")
    if args.remove_inplace:
        total_image_count = sum([len(p) for p in paths])
        paths_to_remove: list[Path] = []
        for dup_image_paths in image_hash_dict.values():
            paths_to_remove.extend(dup_image_paths[1:])
        print("Removing Duplicate Images Inplace")

        with mp.Pool(args.num_workers) as p:
            for _ in tqdm(
                    p.imap_unordered(os.remove, paths_to_remove), total=len(paths_to_remove)
            ):
                pass
        print(f"{len(paths_to_remove)} images removed, {num_unique_images} unique images left")


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Duplicate Image Locator and Remover")
    parser.add_argument("path", help="Directory to Search")
    parser.add_argument(
        "-r", "--recursive", action="store_true", help="Search Recursively"
    )
    parser.add_argument("--output_json", help="Output Search Results to Json File")
    parser.add_argument(
        "--remove_inplace",
        action="store_true",
        help="Remove duplicate images inplace, keep only one from the duplicates",
    )
    parser.add_argument(
        "--no_print_stats",
        action="store_true",
        help="Print Quick Status (Print by Default)",
    )
    parser.add_argument(
        "-o",
        "--output_dir",
        help="Output a subset of images to a directory without any duplicates",
    )
    parser.add_argument(
        "-w",
        "--num_worker",
        type=int,
        default=-1,
        help="Number of Worker (CPU), use (all cpus - 1) by default",
    )
    methods = [m.value for m in HashMethod]
    parser.add_argument('-m', '--hash_method', type=HashMethod,
                        default=HashMethod.PerceptualHashing,
                        help=f'Choose hash method from {methods}, default: Perceptual Hashing')
    args = parser.parse_args()
    output_json_path = Path(args.output_json).absolute() if args.output_json else None
    out_dir = Path(args.output_dir).absolute() if args.output_dir else None
    if args.num_worker == -1:
        num_worker = DEFAULT_NUM_WORKERS
    else:
        num_worker = max(min(args.num_worker, mp.cpu_count()), 1)

    args_conf = ArgsConfig(
        args.recursive,
        Path(args.path).absolute(),
        output_json_path,
        args.remove_inplace,
        out_dir,
        args.no_print_stats,
        num_worker,
        args.hash_method
    )
    verify_args(args_conf)
    main(args_conf)

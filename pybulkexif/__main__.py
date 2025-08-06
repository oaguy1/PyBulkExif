import argparse
import logging
import os
import sys

from typing import Any, Dict, List

import piexif
import yaml


SUPPORTED_FILE_EXT = ('.jpg', '.jpeg', '.tif', '.tiff', '.webp')
IFD = ("0th", "Exif", "GPS", "1st")
IFD_MAP = {"0th": piexif.ImageIFD, "Exif": piexif.ExifIFD, "GPS": piexif.GPSIFD}


def write_exif_data(image_path: str, target_exif_data: Dict[str, Any]) -> None:
    """
    Write the Exif data to the image file
    """
    try:
        exif_dict = piexif.load(image_path)
        for tag, data in target_exif_data['exif'].items():
            for ifd_name, ifd_class in IFD_MAP.items():
                if hasattr(ifd_class, tag):
                    exif_dict[ifd_name][getattr(ifd_class, tag)] = data
        exif_bytes = piexif.dump(exif_dict)
        piexif.insert(exif_bytes, image_path)
        logging.info(f"Updated Exif data for {image_path}")
    except Exception as e:
        logging.error(f"Failed to write Exif data for {image_path}: {e}")

def read_exif_data(image_path: str) -> None:
    """
    Read and print the Exif data from the image file
    """
    try:
        print(os.path.basename(image_path))
        print("-" * len(os.path.basename(image_path)))
        exif_dict = piexif.load(image_path)
        for ifd in IFD:
            for tag in exif_dict[ifd]:
                print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])
        print()
    except Exception as e:
        logging.error(f"Failed to read Exif data for {image_path}: {e}")

def iter_images(images_dir: str):
    """
    Yield supported image file paths in images_dir
    """
    for root, _, files in os.walk(images_dir):
        for file in files:
            _, file_ext = os.path.splitext(file)
            file_ext = file_ext.lower()
            if file_ext in SUPPORTED_FILE_EXT:
                yield os.path.join(root, file)

def handle_read(args) -> None:
    for image_path in iter_images(args.images_dir):
        read_exif_data(image_path)

def handle_edit(args) -> None:
    try:
        with open(args.exif_data) as f:
            exif_from_yaml = yaml.safe_load(f)
    except Exception as e:
        logging.error(f"Failed to load YAML file {args.exif_data}: {e}")
        return
    for image_path in iter_images(args.images_dir):
        write_exif_data(image_path, exif_from_yaml)

def main(argv: List[str]) -> None:
    """
    Main function, parses args and orchestrates all other function calls
    """
    parser = argparse.ArgumentParser(
        prog="PyBulkExif",
        description="A TUI Python tool to bulk edit Exif photo data",
        epilog="Please file all bugs on GitHub"
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Read command
    read_parser = subparsers.add_parser("read", help="Read Exif metadata and print to STDOUT")
    read_parser.add_argument(
        "images_dir",
        help="Path to the directory containing the images to read Exif data from"
    )
    read_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output (log info statements)"
    )

    # Edit command
    edit_parser = subparsers.add_parser("edit", help="Bulk edit Exif data on images")
    edit_parser.add_argument(
        "images_dir",
        help="Path to the directory containing the images to have their Exif data set"
    )
    edit_parser.add_argument(
        "-E", "--exif_data",
        required=True,
        help="Path to the YAML file containing the Exif data to be written",
    )
    edit_parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output (log info statements)"
    )

    args = parser.parse_args(argv)

    log_level = logging.INFO if getattr(args, "verbose", False) else logging.WARNING
    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')

    if args.command == "read":
        handle_read(args)
    elif args.command == "edit":
        handle_edit(args)


if __name__ == "__main__":
    """
    Call main function with all args except the first, which is the
    name of the script file
    """
    main(sys.argv[1:])
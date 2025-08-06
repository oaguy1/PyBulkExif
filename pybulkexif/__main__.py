import argparse
import os
import sys

from typing import Any, Dict, List

import piexif
import yaml


SUPPORTED_FILE_EXT = ('.jpg', '.jpeg', '.tif', '.tiff', '.webp')
IFD = ("0th", "Exif", "GPS", "1st")
IFD_MAP = {"0th": piexif.ImageIFD, "Exif": piexif.ExifIFD, "GPS": piexif.GPSIFD}


def write_exif_data(image_path: str, target_exif_data: Dict[str, Any]):
    """
    Actually write the Exif data to the image file
    """
    exif_dict = piexif.load(image_path)
    for tag, data in target_exif_data['exif'].items():
        for ifd_name, ifd_class in IFD_MAP.items():
            if hasattr(ifd_class, tag):
                exif_dict[ifd_name][getattr(ifd_class, tag)] = data

    exif_bytes = piexif.dump(exif_dict)
    piexif.insert(exif_bytes, image_path)

def read_exif_data(image_path: str):
    """
    Actually write the Exif data to the image file
    """
    print(os.path.basename(image_path))
    print("-" * len(os.path.basename(image_path)))

    exif_dict = piexif.load(image_path)
    for ifd in IFD:
        for tag in exif_dict[ifd]:
            print(piexif.TAGS[ifd][tag]["name"], exif_dict[ifd][tag])
            
    print()

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

    args = parser.parse_args(argv)

    for root, _, files in os.walk(args.images_dir):
        for file in files:
            _, file_ext = os.path.splitext(file)
            file_ext = file_ext.lower()

            if file_ext in SUPPORTED_FILE_EXT:
                image_path = os.path.join(root, file)
                if args.command == "read":
                    read_exif_data(image_path)
                elif args.command == "edit":
                    with open(args.exif_data) as f:
                        exif_from_yaml = yaml.safe_load(f)
                    write_exif_data(image_path, exif_from_yaml)


if __name__ == "__main__":
    """
    Call main function with all args except the first, which is the
    name of the script file
    """
    main(sys.argv[1:])
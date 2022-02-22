#!/usr/bin/env python
"""
This script appends CRC-32s to the end of the files in a directory.
This is intended for anime fansubbing releases.
You can change what it checks by modifying the 'ext' (extension) on L47.
Can be run both from the command line, and imported.
"""
import argparse
import binascii
import glob
import mimetypes
import os
import re
from typing import Literal

__author__ = "LightArrowsEXE"
__license__ = 'MIT'
__version__ = '1.3'


crc32_hash: Literal = r'\s?\[[0-9a-fA-F]{8}\]'


def calculate_crc(f) -> str:
    with open(f, 'rb') as file:
        calc = file.read()
    return "%08X" % (binascii.crc32(calc) & 0xFFFFFFFF)


def strip_crc(f) -> None:
    if re.search(crc32_hash, f):
        os.rename(f, re.sub(crc32_hash, '', f))
        print(f"[-] {f} wrong CRC stripped")


def main() -> None:
    files = glob.glob('**/*' if args.recursive else '*', recursive=True)

    for f in files:
        mime = mimetypes.types_map.get(os.path.splitext(f)[-1], "")
        if mime.startswith("video/") or f.endswith('.mkv'):
            if args.strip:
                strip_crc(f)
            else:
                crc = calculate_crc(f)
                if re.search(crc, f):
                    print(f"[*] {f}, correct CRC already present in filename")
                else:
                    strip_crc(f)
                    str_f = re.sub(crc32_hash, '', f)
                    os.rename(str_f, f'{os.path.splitext(str_f)[0]} [{crc}]{os.path.splitext(str_f)[1]}')
                    print(f"[+] {f}, CRC: [{crc}]")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-R", "--recursive",
                        action="store_true", default=False,
                        help="check recursively (default: %(default)s)")
    parser.add_argument("-S", "--strip",
                        action="store_true", default=False,
                        help="strip CRCs from filenames (default: %(default)s)")
    parser.parse_args()
    args = parser.parse_args()

    main()

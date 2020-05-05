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

__author__ = "LightArrowsEXE"
__license__ = 'MIT'
__version__ = '1.0'


def calculateCRC(f):
    with open(f, 'rb') as file:
        calc = file.read()
    return "%08X" % (binascii.crc32(calc) & 0xFFFFFFFF)


def strip_crc(f):
    if re.search(r'\[[0-9a-fA-F]{8}\]', f):
        strip = re.sub(r'\[[0-9a-fA-F]{8}\]', '', f)

        # Hate how re.sub leaves some whitespace
        filename = os.path.splitext(strip)[0]
        filename = filename[:-1] + os.path.splitext(strip)[1]

        os.rename(f, filename)
        print(f"[-] {f} stripped")


def main(recursive=False):
    if args.recursive:
        filelist = glob.glob('**/*', recursive=True)
    else:
        filelist = glob.glob('*')

    for f in filelist:
        mime = mimetypes.types_map.get(os.path.splitext(f)[-1], "")
        if mime.startswith("video/") or f.endswith('.m2ts') or f.endswith('.mkv'):
            if args.strip:
                strip_crc(f)
            else:
                crc = calculateCRC(f)
                if re.search(crc, f):
                    print(f"[*] {f}, correct CRC already present in filename")
                else:
                    filename = f'{os.path.splitext(f)[0]} [{crc}]{os.path.splitext(f)[1]}'
                    os.rename(f, filename)
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

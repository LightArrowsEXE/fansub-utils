#!/usr/bin/env python
"""
This script appends CRC-32s to the end of the files in a directory.
This is intended for anime fansubbing releases.
You can change what it checks by modifying the 'ext' (extension) on L22.
"""
import argparse
import binascii
import glob
import os.path
import re


def calculateCRC(filename):
    calc = open(filename, 'rb').read()
    calc = (binascii.crc32(calc) & 0xFFFFFFFF)
    return "%08X" % calc


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-R", "--recursive", help="check recursively",
                        action="store_true")
    parser.parse_args()
    args = parser.parse_args()
    ext = '*.mkv'

    if args.recursive:
        filelist = glob.glob('**/*.mkv', recursive=True)
    else:
        filelist = glob.glob(ext)

    for f in filelist:
        if re.search(r'\[[0-9a-fA-F]{8}\]', f):
            print(f"Filename already has a CRC.\n{f} is unchanged.\n")
        else:
            crc = str(calculateCRC(f))
            removeExt = os.path.splitext(f)[0]
            filename = f'{removeExt}' + f' [{crc}]' + f'{ext[1:]}'
            os.rename(f, filename)
            print(f"Old Name: {f} \nNew Name: {filename}\n")

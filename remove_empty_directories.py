#! /usr/bin/env python

"""
    Removes all empty directories located in the current directory.

    Huge parts were taken from a comment on this gist;
      https://gist.github.com/jacobtomlinson/9031697#gistcomment-3130652
    As well as this stackoverflow post:
      https://stackoverflow.com/a/40347279
"""

import argparse
import glob
import os

__author__  = 'LightArrowsEXE'
__license__ = 'MIT'
__version__ = '1.0'


def fast_scandir(dirname):
    subfolders = [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders


def main():
    L = sorted(
        fast_scandir(os.getcwd()),
        key=lambda p: len(str(p)),
        reverse=True,
    )

    for pdir in L:
        try: # remove directory if empty
            os.rmdir(pdir)
            print(f"[-] Deleted \"{pdir}\"")
        except OSError: # catch and continue if non-empty
            print(f"[*] Retained \"{pdir}\"")
            continue


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-R", "--recursive",
                        action="store_false", default=True,
                        help="Encode files recursively (default: %(default)s)")
    parser.parse_args()
    args = parser.parse_args()

    main()
    input("\nDone (Press \"Enter\" to close this window)")

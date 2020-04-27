#!/usr/bin/env python
"""
    A script to automate my audio-encoding setup.

    Dependencies:
     - eac3to       (https://www.videohelp.com/software/eac3to)
     - flac         (https://xiph.org/flac/index.html)
     - qaac         (https://github.com/nu774/qaac)
     - ffmpeg       (https://www.ffmpeg.org/download.html)

"""
import argparse
import glob
import mimetypes
import os
import re
import subprocess
import tempfile

__author__ = "LightArrowsEXE"
__license__ = 'MIT'
__version__ = '1.0.2'


ignored_formats = ["audio/opus", "audio/aac"]


def main():
    filelist = glob.glob('**/*', recursive=True) if args.recursive else glob.glob('*')

    for f in filelist:
        mime = mimetypes.types_map.get(os.path.splitext(f)[-1], "")
        if mime.startswith("audio/") or mime.startswith("video/") or f.endswith('.m2ts'):
            if mime not in ignored_formats:
                encode(f)


def encode(f):
    print(f"\n{f}\n")
    if args.wav_only:
        if args.track:
            if args.core:
                subprocess.run(["eac3to", f, "-log=NUL", f"{args.track}:", f"{os.path.splitext(f)[0]}_Track0{args.track}.wav", "-core"])
            else:
                subprocess.run(["eac3to", f, "-log=NUL", f"{args.track}:", f"{os.path.splitext(f)[0]}_Track0{args.track}.wav"])
        else:
            if args.core:
                subprocess.run(["eac3to", f, "-log=NUL", f"{os.path.splitext(f)[0]}.wav", "-core"])
            else:
                subprocess.run(["eac3to", f, "-log=NUL", f"{os.path.splitext(f)[0]}.wav"])
    else:
        temp = tempfile.mkstemp(prefix=f"{os.path.splitext(f)[0]}_")
        subprocess.run(["ffmpeg", "-i", f, "-loglevel", "panic", "-stats", f"{temp[1]}.wav"])
        if not args.noflac:
            subprocess.run(["flac", f"{temp[1]}.wav", "-8", "-o", f"{os.path.splitext(f)[0]}.flac"])
        if not args.noaac:
            subprocess.run(["qaac", f"{temp[1]}.wav", "-V 127", "--no-delay", "-o", f"{os.path.splitext(f)[0]}.m4a"])
        os.remove(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-R", "--recursive",
                        action="store_true", default=False,
                        help="Encode files recursively (default: %(default)s)")
    parser.add_argument("-W", "--wav_only",
                        action="store_true", default=False,
                        help="Encode just a PCM file (default: %(default)s)")
    parser.add_argument("-C", "--core",
                        action="store_true", default=False,
                        help="Decodes DTS core. Only select if you're dealing with DTS audio (default: %(default)s)")
    parser.add_argument("-T", "--track",
                        action="store", type=int, default=None,
                        help="Track to trim using eac3to (default: %(default)s)")
    parser.add_argument("--noflac",
                        action="store_true", default=False,
                        help="Disable FLAC encoding (default: %(default)s)")
    parser.add_argument("--noaac",
                        action="store_true", default=False,
                        help="Disable AAC encoding (default: %(default)s)")
    parser.parse_args()
    args = parser.parse_args()
    main()

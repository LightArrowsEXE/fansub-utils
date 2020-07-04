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
import subprocess
import tempfile

__author__ = "LightArrowsEXE"
__license__ = 'MIT'
__version__ = '1.0.8'


ignored_formats = ["audio/opus", "audio/aac"]


def main():
    filelist = (glob.glob('**/*', recursive=True)
                if args.recursive else glob.glob('*'))

    for f in filelist:
        mime = mimetypes.types_map.get(os.path.splitext(f)[-1], "")
        if f.endswith('.m2ts'):
            encode_main(f, wav_only=True)
        elif mime.startswith("audio/") or mime.startswith("video/"):
            if mime not in ignored_formats:
                encode_main(f)


def encode_flac(f):
    subprocess.run(["eac3to", f, "-log=NUL", f"{os.path.splitext(f)[0]}.flac"])


def encode_aac(f):
    temp = tempfile.mkstemp(prefix=f"{os.path.splitext(f)[0]}_")
    subprocess.run(["ffmpeg", "-i", f, "-loglevel", "panic", "-stats",
                    f"{temp[1]}.wav"])
    subprocess.run(["qaac", f"{temp[1]}.wav", "-V 127", "--no-delay",
                    "-o", f"{os.path.splitext(f)[0]}.m4a"])


def encode_opus(f):
    subprocess.run(["ffmpeg", "-i", f, "-stats",
                    "-c:a", "libopus", "-b:a", f"{args.bitrate}",
                    f"{os.path.splitext(f)[0]}.opus"])


def encode_main(f, wav_only: bool = False):
    print(f"\n{f}\n")
    if wav_only:
        if args.track:
            subprocess.run(["eac3to", f, "-log=NUL", f"{args.track}:",
                            f"{os.path.splitext(f)[0]}_Track0{args.track}.wav"])
        else:
            subprocess.run(["eac3to", f, "-log=NUL",
                            f"{os.path.splitext(f)[0]}.wav"])
    else:
        if not args.noflac:
            encode_flac(f)
        if not args.nolossy:
            codec = args.codec.lower()
            if codec in ['aac']:
                encode_aac(f)
            elif codec in ['opus']:
                encode_opus(f)
        if not args.keep:
            os.remove(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-R", "--recursive",
                        action="store_true", default=False,
                        help="Encode files recursively (default: %(default)s)")
    parser.add_argument("-C", "--codec",
                        action="store", type=str, default="opus",
                        choices=('aac', 'opus'),
                        help="Pick lossy codec to encode with (default: %(default)s)")
    parser.add_argument("-B", "--bitrate",
                        action="store", type=int, default=192000,
                        help="Bitrate for opus encoding (default: %(default)s)")
    parser.add_argument("-K", "--keep",
                        action="store_true", default=False,
                        help="Do not delete source file after re-encoding (default: %(default)s)")
    parser.add_argument("-T", "--track",
                        action="store", type=int, default=None,
                        help="Track to encode using eac3to. If none; autoselects first audio track (default: %(default)s)")
    parser.add_argument("--noflac",
                        action="store_true", default=False,
                        help="Disable FLAC encoding (default: %(default)s)")
    parser.add_argument("-N", "--nolossy",
                        action="store_true", default=False,
                        help="Disable lossy encoding (default: %(default)s)")
    parser.parse_args()
    args = parser.parse_args()

    main()

#!/usr/bin/env python
"""
    Attempts to encode audio from every video file in a directory.
    If the file is incompatible with ffmpeg or has no audio, it will be ignored.
    wav, m4a, opus, and flac files will also be ignored.

    Intended usage is for encoding BDMV audio to a target codec.

    Dependencies (in PATH):
        * ffmpeg
        * qaac
"""

import subprocess
import argparse
import glob
import os
import re


def main():
    filelist = glob.glob('**/*', recursive=True) if args.recursive else glob.glob('*')

    for f in filelist:
        # TO-DO: Figure out a reliable way to only loop through audio files, but ignore the following three. Maybe messing with MIME recognition?
        if not re.search(r'\.(wav|m4a|opus|flac)$', f):
            print(f)
            if args.codec in ["aac"]:
                subprocess.call(["ffmpeg", "-loglevel", "panic", "-stats", "-i", f,"-vn", f"{os.path.splitext(f)[0]}.wav"])
                subprocess.call(["qaac", f"{os.path.splitext(f)[0]}.wav", "-V 127", "--no-delay"])
            elif args.codec in ["flac"]:
                subprocess.call(["ffmpeg", "-hide_banner", "-i", f,"-vn", "-c:a", "flac", "-sample_fmt", "s16", "-compression_level", "12",  f"{os.path.splitext(f)[0]}.flac"])
            elif args.codec in ["opus"]:
                subprocess.call(["ffmpeg", "-hide_banner", "-i", f, "-c:a", "libopus", "-b:a", f"{args.bitrate}", f"{os.path.splitext(f)[0]}.opus"])
            print(f"Done encoding {os.path.splitext(f)[0]}\n")
        else:
            pass

    try:
        os.remove(f"{os.path.splitext(f)[0]}.wav")
    except OSError:
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-R", "--recursive",
                        help="check recursively", action="store_true")
    parser.add_argument("-C", "--codec",
                        default="aac",
                        choices=('aac', 'flac', 'opus'),
                        metavar='',
                        help="encode using a specific codec (default: %(default)s)")
    parser.add_argument("-B", "--bitrate",
                        action="store", type=int, default=64000,
                        metavar='',
                        help="set bitrate for the opus encoder in bps (default: %(default)s)")
    parser.parse_args()
    args = parser.parse_args()
    main()
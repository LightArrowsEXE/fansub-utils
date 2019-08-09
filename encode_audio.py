#!/usr/bin/env python
"""
    Encodes audio from m2ts sources

    Dependencies (in PATH):
        * mkvmerge
        * mkvextract
        * ffmpeg
        * qaac
"""

import subprocess
import argparse
import glob
import os
import shutil
import re

parser = argparse.ArgumentParser()
parser.add_argument("-R", "--recursive",
                    help="check recursively", action="store_true")
parser.add_argument("-F", "--flac",
                    help="enables FLAC encoding")
args = parser.parse_args()

if args.recursive:
    filelist = glob.glob('**/*', recursive=True)
else:
    filelist = glob.glob('*')

for f in filelist:
    # TO-DO: Figure out a reliable way to only loop through audio files, but ignore the following three. Maybe messing with MIME recognition?
    if not re.search(r'\.(wav|m4a|flac)$', f):
        print(f)
        subprocess.call(["ffmpeg", "-loglevel", "panic", "-stats", "-i", f,"-vn", f"{os.path.splitext(f)[0]}.wav"])
        if not os.path.exists(f'{f[0]}.m4a') or os.path.exists(f'{f[0]}.flac'):
            if args.flac:
                subprocess.call(["ffmpeg", "-i", f"{os.path.splitext(f)[0]}.wav", "-vn", "-c:a flac", "-sample_fmt s16","compression_level 12", f"{os.path.splitext(f)[0]}.flac"])
            else:
                subprocess.call(["qaac", f"{os.path.splitext(f)[0]}.wav", "-V 127", "--no-delay"])
        else:
            pass
    else:
        pass

    try:
        os.remove(f"{os.path.splitext(f)[0]}.wav")
    except OSError:
        pass

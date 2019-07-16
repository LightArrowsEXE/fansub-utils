#!/usr/bin/env python
"""
    Generic script for remuxing files from a certain filetype into another.

    Flags:
    -R - Check recursively
    -i - change input extension
    -o - change output extension

    TO-DO: clean up
"""
import os
import glob
import argparse
import subprocess
import time

parser = argparse.ArgumentParser()
parser.add_argument("-R", "--recursive",
                    help="check recursively", action="store_true")
parser.add_argument("-i", "--input_ext",
                    help="set input's extension (default: mkv)")
parser.add_argument("-o", "--output_ext",
                    help="set output's extension (default: mp4)")
args = parser.parse_args()

if args.recursive:
    filelist = glob.glob('**/*', recursive=True)
else:
    filelist = glob.glob('*')

if args.input_ext:
    ext_in = args.input_ext
    if ext_in.startswith("."):
        ext_in = ext_in[1:]
else:
    ext_in = "mkv"

if args.output_ext:
    ext_out = args.output_ext
    if ext_out.startswith("."):
        ext_out = ext_out[1:]
else:
    ext_out = "mp4"

print(f"Remuxing all {ext_in} to {ext_out}\n")
time.sleep(1)

for f in filelist:
    if f.endswith(ext_in):
        subprocess.call(["ffmpeg", "-hide_banner", "-loglevel", "panic", "-i", f"{os.path.splitext(f)[0]}.{ext_in}", "-c", "copy", f"{os.path.splitext(f)[0]}.{ext_out}"])
        print(f"Remuxing:\n{f} ->\n{os.path.splitext(f)[0]}.{ext_out}\n")
    else:
        pass


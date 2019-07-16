#!/usr/bin/env python
"""
    Generic script to generate keyframes for all files of a given extension using kagefunc's generate_keyframes function.
"""
import glob
import argparse
import os
import vapoursynth as vs
import kagefunc as kgf
import fvsfunc as fvf
core = vs.core


def generate_keyframes():
    if args.recursive:
        files = glob.glob('**/*', recursive=True)
    else:
        files = glob.glob('*')

    if args.extension:
        ext_in = args.extension
    else:
        ext_in = "mkv"

    for f in files:
        if f.endswith(ext_in):
            print(f"Generating keyframes for {f}:")
            if f.endswith(".m2ts"):
                src = core.lsmas.LWLibavSource(f)
            else:
                src = core.ffms2.Source(f)
            src = fvf.Depth(src, 8)
            kgf.generate_keyframes(src, os.path.abspath(f"{f}_keyframes.txt"))
            if f.endswith(".m2ts"):
                try:
                    os.remove(f"{f}.lwi")
                except OSError:
                    pass
            else:
                try:
                    os.remove(f"{f}.ffindex")
                except OSError:
                    pass
        else:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-R", "--recursive",
                        help="check recursively", action="store_true")
    parser.add_argument("-E", "--extension", help="pick extension to generate keyframes for")
    args = parser.parse_args()
    generate_keyframes()

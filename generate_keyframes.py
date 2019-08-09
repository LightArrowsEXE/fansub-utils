#!/usr/bin/env python
"""
    Generic script to generate keyframes for all files of a given extension using kagefunc's generate_keyframes function.

    Dependencies:
    * VapourSynth                                                           (http://vapoursynth.com/doc/installation.html)
    * ffms2                                                                 (https://github.com/FFMS/ffms2)
    * L-SMASH (when generating keyframes from BDs)                          (https://www.dropbox.com/sh/3i81ttxf028m1eh/AAABkQn4Y5w1k-toVhYLasmwa?dl=0)
    * wwxd                                                                  (https://github.com/dubhater/vapoursynth-wwxd)
"""
import glob
import argparse
import os
import vapoursynth as vs
core = vs.core


# Slightly modified from kagefunc to remove some dependencies
def generate_keyframes(clip: vs.VideoNode, out_path=None) -> None:
    """
    probably only useful for fansubbing
    generates qp-filename for keyframes to simplify timing
    """
    clip = core.resize.Bilinear(clip, 640, 360)  # speed up the analysis by resizing first
    clip = core.wwxd.WWXD(clip)
    out_txt = "# WWXD log file, using qpfile format\n\n"
    for i in range(clip.num_frames):
        if clip.get_frame(i).props.Scenechange == 1:
            out_txt += "%d I -1\n" % i
        if i % 500 == 0:
            print(f"{i} frames")
    if out_path is None:
        out_path = os.path.expanduser("~") + "/Desktop/keyframes.txt"
    text_file = open(out_path, "w")
    text_file.write(out_txt)
    text_file.close()


def main():
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
            src = core.resize.Point(src, format=vs.YUV420P8, dither_type='error_diffusion')
            generate_keyframes(src, os.path.abspath(f"{f}_keyframes.txt"))
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
    main()

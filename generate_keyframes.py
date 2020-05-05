#!/usr/bin/env python
"""
    Generic script to generate keyframes for all files of a given extension
    using kagefunc's generate_keyframes function.

    Dependencies:
    * VapourSynth
    * wwxd (https://github.com/dubhater/vapoursynth-wwxd)
"""
import argparse
import glob
import mimetypes
import os
from ast import literal_eval

import vapoursynth as vs

core = vs.core

__author__ = "LightArrowsEXE"
__license__ = 'MIT'
__version__ = '1.0'


# Slightly modified from kagefunc to remove some dependencies
def generate_keyframes(clip: vs.VideoNode, out_path=None, no_header=False) -> None:
    """
    probably only useful for fansubbing
    generates qp-filename for keyframes to simplify timing
    """
    clip = core.resize.Bilinear(clip, 640, 360, format=vs.YUV420P8)
    clip = core.wwxd.WWXD(clip) # speed up the analysis by resizing first

    out_txt = '' if no_header else "# WWXD log file, using qpfile format\n# Please do not modify this file\n\n"

    for i in range(clip.num_frames):
        if clip.get_frame(i).props.Scenechange == 1:
            out_txt += "%d I -1\n" % i
        if i % 1 == 0:
            print(f"Progress: {i}/{clip.num_frames} frames", end="\r")
    text_file = open(out_path, "w")
    text_file.write(out_txt)
    text_file.close()


def main():
    if args.outfile and not args.file:
        print("Warning: Please set --file (-F) when using --outfile (-O)!")
        return

    if args.file:
        files = [args.file]
    else:
        files = glob.glob('**/*', recursive=True) if args.recursive else glob.glob('*')

    for f in files:
        mime = mimetypes.types_map.get(os.path.splitext(f)[-1], "")
        # Not entirely sure why mkv's fail, as they have a mimetype of "video/x-matroska"
        if mime.startswith("video/") or f.endswith('.m2ts') or f.endswith('.mkv'):
            if args.check_exists:
                if os.path.exists(f"{os.path.splitext(f)[0]}_keyframes.txt"):
                    print(f"\nKeyframes already exist for {f}. Skipping.")
                    continue

            src = core.lsmas.LWLibavSource(f) if f.endswith(".m2ts") else core.ffms2.Source(f)

            mime = mimetypes.types_map.get(os.path.splitext(f)[-1]) or "Unknown"
            print(f"\nVideo info\nFilename: {f}\nDimensions: {src.width}x{src.height}\nFramerate: {src.fps}\nFormat: {src.format.name}\nMimetype: {mime}\n")

            if args.trims:
                trims = literal_eval(args.trims)
                if type(trims) is not tuple:
                    trims = (trims,)
                try:
                    src = core.std.Splice([src[slice(*trim)] for trim in trims])
                except:
                    print("TypeError: Please make sure you’re using a list for this function.\nExample: -T \"[24,-24]\" , -T \"[None,30000],[None,-24]\", -T \"[None,16000],[16100,16200],[16300,None]\"")
                    return

            if args.outfile and args.file:
                generate_keyframes(src, os.path.join(os.path.dirname(f),args.outfile), args.noheader)
            else:
                generate_keyframes(src, os.path.abspath(f"{os.path.splitext(f)[0]}_keyframes.txt"), args.noheader)
            print(f"Progress: {src.num_frames}/{src.num_frames} frames")

            try:
                os.remove(f"{f}.lwi") if f.endswith(".m2ts") else os.remove(f"{f}.ffindex")
            except FileNotFoundError:
                pass

            print(f"Output: {args.outfile}") if args.outfile and args.file else print(f"Output: {os.path.splitext(f)[0]}_keyframes.txt")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-F", "--file",
                        help="generate keyframes for a specific file",
                        action="store")
    parser.add_argument("-R", "--recursive",
                        action="store_true", default=False,
                        help="search files recursively (default: %(default)s)")
    parser.add_argument("-N", "--noheader",
                        action="store_true", default=False,
                        help="do not include header line for aegisub (default: %(default)s)")
    parser.add_argument("-O", "--outfile",
                        action="store", default=None,
                        help="name for keyframes file output (Note: requires --file (-F) to be set)")
    parser.add_argument("-T", "--trims",
                        action="store",
                        help="string of trims to source file. " \
                             "format: \"[inclusive,exclusive],[inclusive,exclusive],[None,exclusive],[inclusive,None]\"")
    parser.add_argument("-C", "--check_exists",
                        action="store_true", default=False,
                        help="Check if keyframe file already exists (default: %(default)s)")
    # TO-DO: Add a SCXvid mode for those where the WWXD format
    # doesn't appear to work properly.
    args = parser.parse_args()
    main()
    print(f"\nDone generating keyframes.")

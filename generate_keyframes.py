#!/usr/bin/env python
"""
    Generic script to generate keyframes for all files of a given extension
    using kagefunc's generate_keyframes function.

    Dependencies:
    * VapourSynth
    * wwxd (https://github.com/dubhater/vapoursynth-wwxd)
"""
import vapoursynth as vs
import glob
import argparse
import os
from ast import literal_eval
core = vs.core

# Slightly modified from kagefunc to remove some dependencies
def generate_keyframes(clip: vs.VideoNode, out_path=None, no_header=False) -> None:
    """
    probably only useful for fansubbing
    generates qp-filename for keyframes to simplify timing
    """
    clip = core.resize.Bilinear(clip, 640, 360, format=vs.YUV420P8)  # speed up the analysis by resizing first
    clip = core.wwxd.WWXD(clip)

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
        ext_in = os.path.splitext(files[0])[1]
    else:
        files = glob.glob('**/*', recursive=True) if args.recursive else glob.glob('*')
        ext_in = args.extension if args.extension else "mkv"

    for f in files:
        if f.endswith(ext_in):
            print(f"\nGenerating keyframes for {f}:")

            src = core.lsmas.LWLibavSource(f) if f.endswith("m2ts") else core.ffms2.Source(f)

            print(f"Video info: {src.width}x{src.height}, {src.fps} fps, {src.format.name}")

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
                generate_keyframes(src, os.path.abspath(f"{f[:-len(ext_in)]}_keyframes.txt"), args.noheader)
            print(f"Progress: {src.num_frames}/{src.num_frames} frames")

            if f.endswith(".m2ts"):
                try:
                    os.remove(f"{f}.lwi")
                except FileNotFoundError:
                    pass
            else:
                try:
                    os.remove(f"{f}.ffindex")
                except FileNotFoundError:
                    pass

            print(f"Output: {args.outfile}\nDone.") if args.outfile and args.file else print(f"Output: {f[:-len(ext_in)]}_keyframes.txt\nDone.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-F", "--file",
                        help="generate keyframes for a specific file",
                        action="store")
    parser.add_argument("-R", "--recursive",
                        help="search files recursively",
                        action="store_true")
    parser.add_argument("-E", "--extension",
                        default="mkv",
                        help="pick extension to generate keyframes for (default: %(default)s)",
                        action="store")
    # TO-DO: Add mimetype recognition, add drag-and-drop functionality
    # -E only exists so it automatically looks for a common video file type.
    # If I can have it recognize video using mimetypes instead, there is no real need for this.
    parser.add_argument("-N", "--noheader",
                        help="do not include header line for aegisub",
                        action="store_true")
    parser.add_argument("-O", "--outfile",
                        default=None,
                        help="name for keyframes file output (Note: requires --file (-F) to be set)", action="store")
    parser.add_argument("-T", "--trims",
                        help="string of trims to source file. " \
                             "format: \"[inclusive,exclusive],[inclusive,exclusive],[None,exclusive],[inclusive,None]\"",
                        action="store")
    # TO-DO: Add a SCXvid mode for those where the WWXD format
    # doesn't appear to work properly.
    args = parser.parse_args()
    main()

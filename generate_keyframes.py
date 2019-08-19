#!/usr/bin/env python
"""
    Generic script to generate keyframes for all files of a given extension using kagefunc's generate_keyframes function.

    Dependencies:
    * VapourSynth
    * wwxd (https://github.com/dubhater/vapoursynth-wwxd)
"""
import glob
import argparse
import os
import vapoursynth as vs
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
    if no_header:
        out_txt = ''
    else:
        out_txt = "# WWXD log file, using qpfile format\n\n"
    for i in range(clip.num_frames):
        if clip.get_frame(i).props.Scenechange == 1:
            out_txt += "%d I -1\n" % i
        if i % 1000 == 0:
            print(f"Progress: {i}/{clip.num_frames} frames")
    text_file = open(out_path, "w")
    text_file.write(out_txt)
    text_file.close()


def main():
    if args.file:
        file_name = args.file
        files = [file_name]
        ext_in = os.path.splitext(files[0])[1]

    else:
        if args.recursive:
            files = glob.glob('**/*', recursive=True)
        else:
            files = glob.glob('*')

        if args.extension:
            ext_in = args.extension
        else:
            ext_in = "mkv"

    if args.noheader:
        no_header = True
    else:
        no_header = False

    if args.outfile:
        out_file = args.outfile
    else:
        out_file = None

    for f in files:
        if f.endswith(ext_in):
            print(f"\nGenerating keyframes for {f}:")
            if f.endswith("m2ts"):
                src = core.lsmas.LWLibavSource(f)
            else:
                src = core.ffms2.Source(f)

            if args.trims:
                trims = literal_eval(args.trims)
                if type(trims) is not tuple:
                    trims = (trims,)
                try:
                    src = core.std.Splice([src[slice(*trim)] for trim in trims])
                except:
                    print("TypeError: Please make sure you’re using a list for this function.\nFor example: -T \"[24,-24]\" , -T \"[None,30000],[None,-24]\", -T \"[None,16000],[16100,16200],[16300,None]\"")
                    return

            if args.outfile:
                generate_keyframes(src, os.path.join(os.path.dirname(f),out_file), no_header)
            else:
                generate_keyframes(src, os.path.abspath(f"{f[:-len(ext_in)]}_keyframes.txt"), no_header)

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
            print(f"Progress: {src.num_frames}/{src.num_frames} frames")
            if args.outfile:
                print(f"Output: {out_file}\nDone.")
            else:
                print(f"Output: {f[:-len(ext_in)]}_keyframes.txt\nDone.")
        else:
            pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-F", "--file",
                        help="specific file", action="store")
    parser.add_argument("-R", "--recursive",
                        help="check recursively", action="store_true")
    parser.add_argument("-E", "--extension", help="pick extension to generate keyframes for")
    # TO-DO: Add mimetype recognition, add drag-and-drop functionality
    # -E only exists so it automatically looks for a common video file type.
    # If I can have it recognize video using mimetypes instead, there is no real need for this.
    parser.add_argument("-N", "--noheader",
                        help="do not include header line for aegisub", action="store_true")
    parser.add_argument("-O", "--outfile",
                        help="name for keyframes file output", action="store")
    parser.add_argument("-T", "--trims",
                        help="string of trims to source file. format: \"[inclusive,exclusive],[inclusive,exclusive],[None,exclusive],[inclusive,None]\"", action="store")
    args = parser.parse_args()
    main()

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


# Functions for every supported codec
def wav(f):
    subprocess.call(["ffmpeg", "-loglevel", "panic", "-stats", "-i", f,"-vn", f"{os.path.splitext(f)[0]}.wav"])


def aac(f, cut=False):
    if cut:
        subprocess.call(["ffmpeg", "-loglevel", "panic", "-stats", "-i", f,"-vn", f"{os.path.splitext(f)[0]}_temp.wav"])
        subprocess.call(["qaac", f"{os.path.splitext(f)[0]}_temp.wav", "-V 127", "--no-delay"])
        try:
            os.rename(f"{os.path.splitext(f)[0]}_temp.m4a", f"{os.path.splitext(f)[0]}.m4a")
        except:
            pass
        try:
            os.remove(f"{os.path.splitext(f)[0]}_temp.wav")
        except OSError:
            pass
    else:
        subprocess.call(["ffmpeg", "-loglevel", "panic", "-stats", "-i", f,"-vn", f"{os.path.splitext(f)[0]}.wav"])
        subprocess.call(["qaac", f"{os.path.splitext(f)[0]}.wav", "-V 127", "--no-delay"])


def flac(f):
    subprocess.call(["ffmpeg", "-loglevel", "panic", "-stats", "-i", f,"-vn", "-c:a", "flac", "-sample_fmt", "s16", "-compression_level", "12",  f"{os.path.splitext(f)[0]}.flac"])


def opus(f):
    subprocess.call(["ffmpeg", "-loglevel", "panic", "-stats", "-i", f, "-c:a", "libopus", "-b:a", f"{args.bitrate}", f"{os.path.splitext(f)[0]}.opus"])


# audio encoding and Main functions
def encode_audio(f):
    if args.cut_only:
        if f.endswith("wav") and re.search(r"_cut.", f):
            if args.encode_all:
                aac(f, True)
                flac(f)
                opus(f)
            elif args.codec in ["aac"]:
                aac(f, True)
            elif args.codec in ["flac"]:
                flac(f)
            elif args.codec in ["opus"]:
                opus(f)
    else:
        if args.encode_all:
            aac(f, False)
            flac(f)
            opus(f)
        elif args.wav_only:
            subprocess.call(["ffmpeg", "-loglevel", "panic", "-stats", "-i", f,"-vn", f"{os.path.splitext(f)[0]}.wav"])
        elif args.codec in ["aac"]:
            aac(f, False)
        elif args.codec in ["flac"]:
            flac(f)
        elif args.codec in ["opus"]:
            opus(f)


def main():
    filelist = glob.glob('**/*', recursive=True) if args.recursive else glob.glob('*')

    for f in filelist:
        # TO-DO: Figure out a reliable way to only loop through audio files, but ignore the following three. Maybe messing with MIME recognition?
        if not re.search(r'\.(m4a|opus|flac|lwi|ffindex|py)$', f):
            if args.cut_only and not re.search(r"_cut", f):
                print(f)
            elif args.cut_only is False:
                print(f)
            encode_audio(f)
            if args.encode_all:
                print(f"Done encoding {os.path.splitext(f)[0]}.wav in AAC, FLAC, and opus\n")
            else:
                print(f"Done encoding {os.path.splitext(f)[0]}.{args.codec}\n")


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
    parser.add_argument("-W", "--wav_only",
                        action="store_true",
                        help="Encode just a PCM file (default: False)")
    parser.add_argument("-c", "--cut_only",
                        action="store_true",
                        help="Only encode wav files with \"_cut\" at the end. For use with ocsuite and .wav files")
    parser.add_argument("-e", "--encode_all",
                        action="store_true",
                        help="Encodes target files in aac, flac, and opus")
    parser.parse_args()
    args = parser.parse_args()
    main()
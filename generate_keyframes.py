#!/usr/bin/env python
"""
Generic script to generate keyframes for all files of a given extension.

Dependencies:

    * VapourSynth
    * vs-jetpack (https://github.com/Jaded-Encoding-Thaumaturgy/vs-jetpack?tab=readme-ov-file#how-to-install)
    * wwxd (https://github.com/dubhater/vapoursynth-wwxd) (depending on the scene-mode)
    * scxvid (https://github.com/dubhater/vapoursynth-scxvid) (depending on the scene-mode)
    * colorlog (https://github.com/borntyping/python-colorlog) (optional for colored logging)
"""

import argparse
import logging
from ast import literal_eval
import pprint

from vssource import BestSource, FFMS2
from vstools import FileType, Keyframes, SceneChangeMode, SPath, core, vs

import sys

try:
    from colorlog import ColoredFormatter

    _colorlog_available = True
except ImportError:
    _colorlog_available = False

__author__ = "LightArrowsEXE"
__license__ = "MIT"
__version__ = "2.0"

logger = logging.getLogger("generate_keyframes")

if _colorlog_available:
    handler = logging.StreamHandler(sys.stdout)
    formatter = ColoredFormatter(
        "%(log_color)s%(asctime)s %(levelname)s %(name)s: %(message)s",
        log_colors={
            "DEBUG": "cyan",
            "INFO": "green",
            "WARNING": "yellow",
            "ERROR": "red",
            "CRITICAL": "bold_red",
        },
    )
    handler.setFormatter(formatter)
    logger.handlers = []
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)
else:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(name)s: %(message)s",
    )


def generate_keyframes(clip: vs.VideoNode, out_path: SPath, header: bool) -> None:
    """Generate keyframes for a given clip."""

    logger.debug(f"Generating keyframes: out_path={out_path}, header={header}")

    scenes = Keyframes.from_clip(clip, mode=SceneChangeMode(args.scene_mode))
    scenes.to_file(out_path, header=header, force=args.force)

    logger.debug(f"Keyframes written to {out_path}")


def clean_index_files(file: SPath) -> None:
    """Clean index files from a given file."""

    logger.debug(f"Cleaning index files: {file}")

    idx_file = "ffindex" if args.fast else "[0-9].bsindex"

    for f in file.glob(f"*.{idx_file}"):
        logger.debug(f"Removing index file: {f}")

        f.unlink(missing_ok=True)


def get_files(args: argparse.Namespace) -> list:
    """Get list of files to process based on args."""

    if args.file:
        return [SPath(args.file)]

    return list(SPath.cwd().glob("**/*" if args.recursive else "*"))


def is_video_file(f: SPath) -> bool:
    """Check if file is a video file."""

    return FileType.parse(f).file_type is FileType.VIDEO


def keyframes_exist(f: SPath) -> bool:
    """Check if keyframe file already exists and should be skipped."""

    logger.debug(f"Checking if keyframe file exists: {f}")

    return f.exists()


def get_source_and_info(f: SPath, ftype) -> tuple:
    """Get video source and info lines."""

    if args.fast:
        src = FFMS2.source(f, bits=0)
    else:
        src = BestSource.source(f, bits=0)

    info_lines = [
        "Video info",
        f"Filename: {f}",
        f"Dimensions: {src.width}x{src.height} ({src.format.name if src.format else 'Unknown'}) @ {src.fps} fps",
        f"Mimetype: {ftype.mime}",
        "",
    ]
    logger.debug("\n" + "\n".join(info_lines))
    return src, info_lines


def apply_trims(src: vs.VideoNode, trims_arg: str) -> vs.VideoNode:
    """Apply trims to the source if specified."""

    logger.debug(f"Trims argument: {trims_arg}")
    trims = literal_eval(trims_arg)

    if type(trims) is not tuple:
        trims = (trims,)

    try:
        logger.debug(f"Applying trims: {trims}")
        src = core.std.Splice([src[slice(*trim)] for trim in trims])
    except (vs.Error, TypeError) as e:
        logger.error(
            "TypeError: Please make sure you're using a list for this function.\n"
            'Example: -T "[24,-24]" , -T "[None,30000],[None,-24]", -T "[None,16000],[16100,16200],[16300,None]"'
        )

        logger.debug(f"Error: {e}")

        return  # type: ignore

    return src


def get_output_path(f: SPath, args: argparse.Namespace) -> SPath:
    """Determine output path for keyframes file."""

    if args.outfile:
        return f.parent / args.outfile

    return f.with_name(f.stem + "_keyframes.txt")


def process_file(f: SPath, args: argparse.Namespace):
    logger.debug(f"Processing file: {f}")

    if (ftype := FileType.parse(f)).file_type is not FileType.VIDEO:
        logger.info(f"{f} is not a video file. Skipping.")
        return

    out_path = get_output_path(f, args)

    if args.check_exists and not args.force:
        if keyframes_exist(out_path):
            logger.info(f"Keyframes already exist for {f}. Skipping.")
            return

    logger.debug(f"Indexing video: {f}")
    src, _ = get_source_and_info(f, ftype)

    if args.trims:
        if (src := apply_trims(src, args.trims)) is None:
            return

    logger.debug(f"Output path: {out_path}")

    generate_keyframes(src, out_path, args.header)
    logger.info(f"Output: {out_path}")


def set_fast_scene_change_detection(args: argparse.Namespace) -> argparse.Namespace:
    """Set fast scene change detection mode."""

    if not args.fast:
        return args

    args.scene_mode = 1
    return args


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-F", "--file", help="generate keyframes for a specific file", action="store"
    )
    parser.add_argument(
        "--scene-mode",
        type=int,
        default=0,
        choices=[0, 1, 2, 3],
        metavar="MODE",
        help=(
            "Scene change detection mode (integer):\n"
            "  0 = WWXD_SCXVID_INTERSECTION (default, both detectors must agree)\n"
            "  1 = WWXD (use only WWXD)\n"
            "  2 = SCXVID (use only SCXVID)\n"
            "  3 = WWXD_SCXVID_UNION (either detector triggers)\n"
            "Example: --scene-mode 2\n"
            "Default: %(default)s"
        ),
    )
    parser.add_argument(
        "-R",
        "--recursive",
        action="store_true",
        default=False,
        help="search files recursively (default: %(default)s)",
    )
    parser.add_argument(
        "--fast",
        action="store_true",
        default=False,
        help="use fast scene change detection mode (note that this will override other options) (default: %(default)s)",
    )
    parser.add_argument(
        "-N",
        "--header",
        action="store_true",
        default=True,
        help="include header line in keyframes file (default: %(default)s)",
    )
    parser.add_argument(
        "-O",
        "--outfile",
        action="store",
        default=None,
        help="name for keyframes file output (Note: requires --file (-F) to be set)",
    )
    parser.add_argument(
        "-T",
        "--trims",
        action="store",
        help="string of trims to source file. "
        'format: "[inclusive,exclusive],[inclusive,exclusive],[None,exclusive],[inclusive,None]"',
    )
    parser.add_argument(
        "-C",
        "--check-exists",
        action="store_true",
        default=False,
        help="Check if keyframe file already exists before generating (default: %(default)s)",
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        default=False,
        help="Force overwrite keyframes file if it already exists (default: %(default)s)",
    )
    parser.add_argument(
        "-L",
        "--log-level",
        action="store",
        default="INFO",
        choices=["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"],
        help=(
            "set logging level:\n"
            "  DEBUG = print debug messages\n"
            "  INFO = print info messages (default)\n"
            "  WARNING = print warning messages\n"
            "  ERROR = print error messages\n"
            "  CRITICAL = print critical messages\n"
            "Example: --log-level DEBUG\nDefault: %(default)s"
        ),
    )

    args = parser.parse_args()

    logging.getLogger().setLevel(getattr(logging, args.log_level))
    logger.debug("Debug mode enabled.")

    logger.debug(f"Arguments: {args}")

    if args.outfile and not args.file:
        logger.error("Please set --file (-F) when using --outfile (-O)!")
        exit(1)

    files = get_files(args)
    logger.debug(
        f"Files to process: {pprint.pformat([f.name for f in files], width=120)}"
    )

    for f in files:
        process_file(f, args)

    logger.info("Done generating keyframes.")

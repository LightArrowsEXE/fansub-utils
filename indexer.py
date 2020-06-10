"""
    A util script that simply indexes every video file it can find.
    This way you don't have to when loading new videos into VapourSynth.

    l-smash is used for m2ts files, ffms2 for everything else.
    l-smash can also be forced.
"""
import argparse
import mimetypes
from glob import glob
from os import path

try:
    from lvsfunc import src
except ModuleNotFoundError:
        raise ModuleNotFoundError("Cannot find lvsfunc: Please install it here <https://github.com/Irrational-Encoding-Wizardry/lvsfunc/>")


__author__ = "LightArrowsEXE"
__license__ = 'MIT'
__version__ = '1.1.2'


def index():
    print(f"Indexing files:\n")
    files = glob('**/*', recursive=True) if args.recursive else glob('*')

    for f in files:
        mime = mimetypes.types_map.get(path.splitext(f)[-1], "")
        if mime.startswith("video/") or f.endswith('.m2ts') or f.endswith('.mkv'):
            print(f"[+] Generating index file for {f}")
            print(src(f, force_lsmas=args.force))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-R", "--recursive",
                        action="store_true", default=False,
                        help="search files recursively (default: %(default)s)")
    parser.add_argument("-F", "--force",
                        action="store_true", default=False,
                        help="force l-smash for indexing (default: %(default)s)")
    args = parser.parse_args()
    index()
    input("\nDone generating index files. \n(press Enter to close this window...)")

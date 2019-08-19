A collection of utilities for fansubbing
that I've written.
Improvements and ideas are always welcome.

## Requirements:
- Python 3.6 or higher

## Usage:
    $ python [script].py [--args]

# Utilities:

## auto-CRC
A small script that
appends CRC-32's to every mkv
in the current directory.

### Arguments:
| Argument | Arg | Description |
| -------- | --- | ----------- |
| --help | -h |show this help message and exit |
| --recursive | -R | check recursively |

## encode-audio
Automatically encodes audio
in the current directory
to AAC (using qaac -V 127)
or FLAC.

### Arguments:
| Argument | Arg | Description |
| -------- | --- |------------ |
| --help | -h | show this help message and exit |
| --recursive | -R | check recursively |
| --flac | -F | enable FLAC encoding |

## generate_keyframes
Generic script to generate keyframes
for all files of a given extension.
Heavily inspired by kagefunc's `generate_keyframes`,
but made to work as a standalone script
for timers.
Special thanks to begna
for helping me with writing
big parts
of this.


### Arguments:
| Argument | Arg | Description |
| -------- | --- |------------ |
| --help | -h | show this help message and exit |
| --recursive | -R | check recursively |
| --extension | -E | pick extension to generate keyframes for |
| --noheader | -N | do not include header line for aegisub |
| --outfile | -O | name for keyframes file output |
| --trims | -T | string of trims to source file. format: "[inclusive,exclusive],[inclusive,exclusive],[None,exclusive],[inclusive,None]\" |

## remux
Generic script for remuxing videos
from a certain filetype into another.
Remuxes mkv's into mp4's by default.


### Arguments:
| Argument | Arg | Description |
| -------- | --- | ----------- |
| --recursive | -R | check recursively |
| --input_ext | -i | set input's extension (default: mkv) |
| --output_ext | -o | set output's extension (default: mp4) |
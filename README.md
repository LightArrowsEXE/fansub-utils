A collection of utilities for fansubbing that I've written. Improvements and ideas are always welcome.

## Requirements:
- Python 3.6 or higher

## Usage:
    $ python [script].py [--args]

# Utilities:

## auto-CRC
A small script that appends CRC-32's to every mkv in the current directory.

### Arguments:
| Argument | Description | 
| -------- | --------------------------------- |
| --help | show this help message and exit
| --recursive | check recursively |

## clean-dir
Cleans a directory of everything but mkv's or a given *ext*.<br>
Please make sure it doesn't accidently wipe everything else you *need* to include in there.
*Ext* is intended to be used for other video extensions, like mp4, webm, etc.

### Arguments:
| Argument |  |Description | 
| -------- | --------------------------------- |
| --help | -h | show this help message and exit
| --recursive | -R | check recursively |
| --extension | -E | change extension |
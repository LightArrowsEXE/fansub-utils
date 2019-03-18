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
Cleans a directory of everything but mkv's and py's (to ensure my scripts don't get wiped).<br>
Please make sure it doesn't accidently wipe everything else you *need* to include in there.

### Arguments:
| Argument | Description | 
| -------- | --------------------------------- |
| --help | show this help message and exit
| --recursive | check recursively |
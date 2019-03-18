"""
    Cleaning final release folder.
    This will only keep the mkv files and move the other files to the upper directory.

    Please note that this NOT remove empty directories and does not have ANY exceptions. It will only keep mkv's.
"""

import argparse
import glob
import shutil
import os
import time

parser = argparse.ArgumentParser()
parser.add_argument("-R", "--recursive", help="check recursively", action="store_true")
parser.parse_args()
args = parser.parse_args()

if args.recursive:
    filelist = glob.glob('**\*.*', recursive=True)
else:
    filelist = glob.glob('*.*')

ext = '.mkv'

for f in filelist:
    if f.endswith('.py'): # Will not remove my other cleaning scripts
        pass  
        print("Python file ignored.")
    elif f.endswith(ext) is False:
        os.remove(f)
        print(f"Cleaned {f}")
    else:
        pass

print('-------------------------------------------------\nPrinting remaining files in directory...')
time.sleep(3)
print('-------------------------------------------------\nRemaining files:\n\n')
for f in filelist:
    print(f)
print('\n\nPlease ensure that all the relevant files are included')
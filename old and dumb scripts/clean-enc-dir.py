"""
    Cleaning encoding directory of everything but vpy's and py's.

    Please note that this does NOT remove empty directories and does not have ANY exceptions. It will only keep mkv's.
"""
import argparse
import glob
import shutil
import os
import time

parser = argparse.ArgumentParser()
parser.add_argument("-R", "--recursive",
                    help="check recursively", action="store_true")
parser.parse_args()
args = parser.parse_args()

if args.recursive:
    filelist = glob.glob('**\*.*', recursive=True)
else:
    filelist = glob.glob('*.*')

for f in filelist:
    if f.endswith('.py') or f.endswith('.vpy'):
        if os.path.isfile(f):
            try:
                shutil.copy(f, os.getcwd())
                os.remove(f)
                print(f"Moving '{f}' to current directory.")
            except Exception:
                pass
    else:
        os.remove(f)
        print(f"Cleaned '{f}'")

print('-------------------------------------------------\nPrinting remaining files in directory...')
time.sleep(3)
print('-------------------------------------------------\nRemaining files:\n\n')
for f in filelist:
    print(f"'{f}'")
print('\n\nPlease ensure that all the relevant files are included.')

"""
    Cleaning final release folder.
    This will only keep the mkv files and move the other files to the upper directory.

    Please note that this does NOT remove empty directories and does not have ANY exceptions. It will only keep mkv's.
"""
import argparse
import glob
import shutil
import os
import time

parser = argparse.ArgumentParser()
parser.add_argument("-R", "--recursive", help="check recursively", action="store_true")
parser.add_argument("-E", "--extension", help="change extension")
args = parser.parse_args()

if args.recursive:
    filelist = glob.glob('**/*', recursive=True)
else:
    filelist = glob.glob('*')

if args.extension:
    ext = f'.{args.extension}'
else:
    ext = '.mkv'
print(f"Cleaning up everything without the {ext} extension\n")

new_directory = '!_Cleaned Files'

for f in filelist:
    if f.startswith(new_directory):
        pass
    elif not f.endswith(ext):
        if os.path.isfile(f):
            try:
                cleaned_directory = os.path.join(os.getcwd(), new_directory)
                if not os.path.exists(cleaned_directory):
                    os.makedirs(new_directory)
                    print(f"Created a new directory. Moving cleaned files into {cleaned_directory}")
                shutil.copy(f, cleaned_directory)
                os.remove(f)
            except Exception:
                pass
        print(f"Cleaned '{f}'")
    else:
        pass

print('-------------------------------------------------\nRemaining files:\n')

if args.recursive:
    filelist = glob.glob('**/*', recursive=True)
else:
    filelist = glob.glob('*')
    

for f in filelist:
    try:
        os.rmdir(f)
    except Exception:
        pass
    print(f"'{f}'")
    
print('\n\nPlease ensure that all the relevant files are included')
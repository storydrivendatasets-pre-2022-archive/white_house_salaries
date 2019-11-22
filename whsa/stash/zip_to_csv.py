#!/usr/bin/env python

"""
Years 2013-2016 come as zip files. The zips each contain a single CSV text file, with
  an unpredictable filename.

This script basically unzips and extracts that single file into a more simpler named
  file, e.g. stashed/processed/2014.csv
"""

from zipfile import ZipFile
from pathlib import Path

SRC_DIR = Path('data', 'stashed', 'originals')
DEST_DIR = Path('data', 'stashed', 'processed')


def extract_bytes_from_zip(fpath):
    """returns bytes, even though the only file in each zip archive is technically just
       a text file"""
    z = ZipFile(fpath)
    if len(z.filelist) != 1:
        raise IOError(f"Expected exactly 1 file in zip archive but found {len(z.filelist)}")

    f = z.filelist[0]
    print("Reading from", f.filename)
    return z.read(f)

def main():
    files = sorted(SRC_DIR.glob('*.zip'))
    for fn in files:
        year = fn.stem
        destpath = DEST_DIR.joinpath(f'{year}.csv')
        d = extract_bytes_from_zip(fn)
        destpath.write_bytes(d)
        print(f"Unzipped {len(d)} bytes to {destpath}")


if __name__ == '__main__':
    main()

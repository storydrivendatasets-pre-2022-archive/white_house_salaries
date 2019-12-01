#!/usr/bin/env python

"""
zip2csv.py

Years 2013-2016 come as zip files. The zips each contain a single CSV text file, with
  an unpredictable filename.

This script basically unzips and extracts that single file into a more simpler named
  file, e.g. collected/processed/2014.csv
"""

from pathlib import Path
from sys import stderr
from zipfile import ZipFile


SRC_DIR = Path('data', 'collected',)
DEST_DIR = Path('data', 'converted',)


def extract_bytes_from_zip(fpath):
    """returns bytes, even though the only file in each zip archive is technically just
       a text file"""
    z = ZipFile(fpath)
    if len(z.filelist) != 1:
        raise IOError(f"Expected exactly 1 file in zip archive but found {len(z.filelist)}")

    f = z.filelist[0]
    stderr.write(f"Reading from: {f.filename}\n")
    return z.read(f)

def main():
    DEST_DIR.mkdir(exist_ok=True, parents=True)

    files = sorted(SRC_DIR.glob('*.zip'))
    for fn in files:
        year = fn.stem
        destpath = DEST_DIR.joinpath(f'{year}.csv')
        content = extract_bytes_from_zip(fn)
        destpath.write_bytes(content)

        stderr.write(f"\tUnzipped {len(content)} bytes to: {destpath}\n")


if __name__ == '__main__':
    main()


"""
Expected output:
Reading from: 2013-Report-White-House_Staff.csv
    Unzipped 44172 bytes to: data/converted/2013.csv
Reading from: 2014-report-white-house_staff.csv
    Unzipped 44359 bytes to: data/converted/2014.csv
Reading from: 2015-Report-White-House-Staff.csv
    Unzipped 45716 bytes to: data/converted/2015.csv
Reading from: 2016-Report-White-House-Staff.csv
    Unzipped 44685 bytes to: data/converted/2016.csv
"""

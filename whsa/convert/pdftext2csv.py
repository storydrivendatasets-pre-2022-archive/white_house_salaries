#!/usr/bin/env python

"""
pdftext2csv.py

Years 2017-2019 come as PDF. They were converted to text via pdftotext -layout

This script uses the magic of regex to delimit the data so we can get a CSV out of it.

This script also adds headers to the parsed CSV
"""

import csv
from pathlib import Path
import re
from sys import stderr

SRC_DIR = Path('data', 'collected', 'handcleaned')
DEST_DIR = Path('data', 'converted',)

HEADERS = ('name', 'status', 'salary', 'pay_basis', 'position_title')
META_STRINGS = ('SALARY', 'PAY BASIS', 'TITLE', 'Total Count')


def process_line(line):
    """
    line is a plaintext string, straight from the pdftotext -layout formatted text file

    Returns:
        - None if the line is perceived to be a non-data line, such as a header
        - a list of strings if it is a data line
    """


    if not re.match(r'^\w', line):
        # we assume all data lines have text at the very beginning
        # title and footer text do not, e.g. "For Official Use Only"
        return None

    if any(h in line for h in META_STRINGS):
        # skip lines that contain meta info, like headers or totals
        return None

    record = re.split(r'\s{3,}', line)

    # Sometimes the job field can be broken into several lines:
    if len(record) != 5:
        print(f"Record found with {len(record)} fields")
        print(line)
        # import code; code.interact(local=locals())

        return None
    else:
        return record


def process_textfile(srcpath):
    """srcpath is a path to a text file, presumably from pdftotext"""

    data = []
    for line in srcpath.open():
        record = process_line(line)
        if record:
            data.append(record)
    return data



def main():
    DEST_DIR.mkdir(exist_ok=True, parents=True)
    files = sorted(SRC_DIR.glob('*.txt'))
    for fn in files:
        stderr.write(f"Opening {fn}\n")
        data = process_textfile(fn)
        destpath = DEST_DIR.joinpath(f'{fn.stem}.csv')
        with open(destpath, 'w') as w:
            outs = csv.writer(w)
            outs.writerow(HEADERS)
            outs.writerows(data)

            stderr.write(f"\t{len(data)} records written to: {destpath}\n")


if __name__ == '__main__':
    main()


"""
Expected output

./whsa/convert/pdftext2csv.py
Opening data/collected/handcleaned/2017.txt
    377 records written to: data/converted/2017.csv
Opening data/collected/handcleaned/2018.txt
    374 records written to: data/converted/2018.csv
Opening data/collected/handcleaned/2019.txt
    418 records written to: data/converted/2019.csv
"""

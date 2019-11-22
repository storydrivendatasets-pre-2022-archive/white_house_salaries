#!/usr/bin/env python

"""
Years 2017-2019 come as PDF. They were converted to text via pdftotext -layout

This script uses the magic of regex to delimit the data so we can get a CSV out of it.

This script also adds headers to the parsed CSV
"""

import csv
from pathlib import Path
import re

SRC_DIR = Path('data', 'stashed', 'handcleaned')
DEST_DIR = Path('data', 'stashed', 'processed')

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
    files = sorted(SRC_DIR.glob('*.txt'))
    for fn in files:
        print("Opening", fn)
        data = process_textfile(fn)
        destpath = DEST_DIR.joinpath(f'{fn.stem}.csv')
        with open(destpath, 'w') as w:
            outs = csv.writer(w)
            outs.writerow(HEADERS)
            outs.writerows(data)
            print(len(data), "records written to:", destpath)


if __name__ == '__main__':
    main()

    """stdout
    Opening data/stashed/processed/handcleaned/2017.txt
    377 records written to: data/stashed/processed/2017.csv
    Opening data/stashed/processed/handcleaned/2018.txt
    374 records written to: data/stashed/processed/2018.csv
    Opening data/stashed/processed/handcleaned/2019.txt
    418 records written to: data/stashed/processed/2019.csv

    This is the exact number of total records for each file as
        specified in their respective PDFs
    """



# Killed this code because I ended up handcleaning the data. Turns out I could've automated it
# but oh well
#
# def clean_text(txt):
#     """
#     txt is a string containing the entire contents of a text file, newlines intact
#     Returns: string, with newlines intact

#     Sometimes the job titles for records span several lines:


#     Einhorn, Charles A.                Employee    $58,200.00   Per Annum   SPECIAL ASSISTANT
#                                                                             DEPUTY COUNSEL TO THE PRESIDENT FOR NATIONAL SECURITY AFFAIRS AND LEGAL ADVISOR TO THE NATIONAL
#     Eisenberg, John A.                 Employee   $183,000.00   Per Annum
#                                                                             SECURITY COUNCIL

#     """
#     ctext = []
#     for line in txt.splitlines():
#         prevline = "" if not ctext else ctext[-1]
#         if line.strip() and re.match(r'^\w', prevline) \
#                         and re.match(r'\s{55,}(\w+.*)$', line):
#             orphan = re.match(r'\s{55,}(\w+.*)$', line).group().strip()

#             print("Orphan:", orphan)

#             if re.search(r'Annum$', prevline):
#                 # sometimes, the previous line did not have a job title, as in the case
#                 #   of Eisenberg, John A. in 2019

#                 # In this special case, we have to append 3+ leading whitespaces, then the
#                 #  text, so that the line is considered a job field
#                 ctext[-1] = prevline + "     " + orphan
#             else:
#                 # otherwise, assume it's a continuation of a job title
#                 ctext[-1] = prevline + " " + orphan
#             print("\t", ctext[-1])
#         else:
#             # append the line as normal
#             ctext.append(line)

#     return "\n".join(ctext)

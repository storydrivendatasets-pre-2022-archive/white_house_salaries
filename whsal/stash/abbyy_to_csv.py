#!/usr/bin/env python

"""DEPRECATED SINCE WE DONT USE ABBYY ANYMORE"""

import csv
from openpyxl import load_workbook
from pathlib import Path

SRC_DIR = Path('data', 'stashed', 'originals', 'abbyy')
DEST_DIR = Path('data', 'stashed', 'extracts')


def extract_csv(xlspath):
    book = load_workbook(xlspath)
    return [[cell.value for cell in row] for row in book.active.rows]



def main():
    files = sorted(SRC_DIR.glob('*.xlsx'))
    for fn in files:
        print("Opening", fn)
        data = extract_csv(fn)
        destpath = DEST_DIR.joinpath(f'{fn.stem}.csv')
        print("Writing to:", destpath)
        with open(destpath, 'w') as w:
            outs = csv.writer(w)
            outs.writerows(data)
        import code; code.interact(local=locals())

if __name__ == '__main__':
    main()

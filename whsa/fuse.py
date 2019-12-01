#!/usr/bin/env python

"""
fuse.py

gather files from data/collected/processed.csv

- Remove ,$ from salary column
- collapse and strip whitespace
- unite them as data/fused/white_house_salaries.csv
"""
import csv
from pathlib import Path
import re




SRC_DIR = Path('data', 'collected', 'processed')
DEST_PATH = Path('data', 'fused', 'white_house_salaries.csv')

SALARY_COL_IDX = 2
# note: a couple of Obama year files have a 6th column called, "White House Review"
HEADERS = ('year', 'full_name', 'status', 'salary',
           'pay_basis', 'position_title',
           'white_house_review')



def cleanspace(txt):
    return re.sub(r'\s{2,}', ' ', txt).strip()

def process_file(srcpath):
    """
    yields a clean data row
    """
    year = srcpath.stem

    try:
        with open(srcpath, encoding='utf-8') as src:
            # skip header, since layout is always the same
            records = list(csv.reader(src))[1:]
    except UnicodeDecodeError:
        with open(srcpath, encoding='cp1252') as src:
            records = list(csv.reader(src))[1:]


    for row in records:
        d = [year]
        for idx, col in enumerate(row):
            val = cleanspace(col)
            if idx == SALARY_COL_IDX:
                val = re.sub(r'\$|,', '', val)
            d.append(val)
        yield d



def main():
    DEST_PATH.parent.mkdir(exist_ok=True, parents=True)
    destfile = DEST_PATH.open('w')
    outs = csv.writer(destfile)
    outs.writerow(HEADERS)
    for fn in sorted(SRC_DIR.glob('*.csv')):
        for row in process_file(fn):
            outs.writerow(row)
    destfile.close()
    print("Wrote", DEST_PATH.stat().st_size, 'bytes to', DEST_PATH)

if __name__ == '__main__':
    main()

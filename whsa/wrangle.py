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
from whsa.utils import parse_name


SRC_PATH = Path('data', 'fused', 'white_house_salaries.csv')
DEST_PATH = Path('data', 'wrangled', 'white_house_salaries.csv')

SALARY_COL_IDX = 2
PRES_TERMS = (
    (('2012', '2013', '2014', '2015', '2016',), 'Obama'),
    (('2017', '2018', '2019',), 'Trump')
)

HEADERS = ('year', 'president' ,'last_name', 'first_name',
            'middle_name', 'suffix', 'full_name',
            'status', 'salary', 'pay_basis', 'position_title', 'white_house_review')
# shared between fused and wrangled
SHARED_HEADERS = ('year', 'full_name', 'status', 'salary', 'pay_basis',
                  'position_title', 'white_house_review')


def get_president(year):
    yr = str(year)
    return next(pres for yrs, pres in PRES_TERMS if yr in yrs)

def process_record(row):
    """
    row is a dict

    Returns: a dict
    """
    d = {h: row[h] for h in SHARED_HEADERS}
    d['president'] = get_president(d['year'])
    d.update(parse_name(row['full_name']))

    return d




def main():
    with open(SRC_PATH) as f:
        data = [process_record(row) for row in csv.DictReader(f)]

    DEST_PATH.parent.mkdir(exist_ok=True, parents=True)

    with open(DEST_PATH, 'w') as f:
        outs = csv.DictWriter(f, fieldnames=HEADERS, restval=None)
        outs.writeheader()
        outs.writerows(data)

    print("Wrote", DEST_PATH.stat().st_size, 'bytes to', DEST_PATH)

if __name__ == '__main__':
    main()

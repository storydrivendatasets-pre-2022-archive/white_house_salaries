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

NAME_RX = r'(?P<last_name>.+?), (?:(?P<suffix>[^,]+),)? *(?P<first_name>.+?) *(?P<middle_name>[A-Z]\.)?$'


def parse_name(name):
    """
    name is a string

    returns dict: {'last_name': 'x', 'first_name': , 'middle_name', 'suffix'}

    Examples:
        Trump, Ivanka M.
        Hsu, Irene
        Johnston, Jr., Robert O.
    """
    mx = re.match(NAME_RX, name)
    if mx:
        return mx.groupdict()
    else:
        # import code; code.interact(local=locals())
        return {}

def process_record(row):
    """
    row is a dict

    returns a dict
    """
    d = {}
    for h in SHARED_HEADERS:
        d[h] = row[h]

    nameparts = parse_name(row['full_name'])
    d.update(nameparts)
    d['president'] = next(pres for yrs, pres in PRES_TERMS if d['year'] in yrs)

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

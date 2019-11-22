#!/usr/bin/env python

"""
Downloads files from original remote sources, as found in data/stashed/filelist.csv
"""

import csv
from pathlib import Path
import requests

SRC_PATH = Path('data', 'stashed', 'filelist.csv')
DEST_DIR = Path('data', 'stashed', 'originals')



def main():
    DEST_DIR.mkdir(exist_ok=True, parents=True)
    with open(SRC_PATH) as o:
        records = list(csv.DictReader(o))

    for row in records:
        print(f"Downloading {row['url']}")
        resp = requests.get(row['url'])
        if resp.status_code == 200:
            fileext = row['url'].split('.')[-1]
            destpath = DEST_DIR.joinpath(f'{row["year"]}.{fileext}')
            print('Writing to:', destpath)
            destpath.write_bytes(resp.content)

if __name__ == '__main__':
    main()

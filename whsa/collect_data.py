#!/usr/bin/env python

"""
Downloads files from original remote sources, as found in data_inventory.csv
"""

import csv
from pathlib import Path
import requests
from sys import stderr

INVENTORY_PATH = Path('data_inventory.csv')
DEST_DIR = Path('data', 'collected',)


def get_inventory():
    with open(INVENTORY_PATH) as o:
        records = list(csv.DictReader(o))
        return records

def fetch_file(url):
    """
    returns bytes of a successfully fetched file
    """
    resp = requests.get(url)
    if resp.status_code != 200:
        raise ValueError(f"Got status code {resp.status_code} when trying to get {url}")
    else:
        return resp.content

def main():
    DEST_DIR.mkdir(exist_ok=True, parents=True)

    for row in get_inventory():
        # figure out what the destination path will be
        fileext = row['url'].split('.')[-1]
        destpath = DEST_DIR.joinpath(f'{row["year"]}.{fileext}')
        # then see if it already exists; if so, skip it
        if destpath.exists():
            stderr.write(f'{destpath} ({destpath.stat().st_size} bytes) already exists; skipping\n')
        else:
            stderr.write(f"Downloading:\n\t{row['url']}\n")
            content = fetch_file(row['url'])
            destpath.write_bytes(content)

            stderr.write(f'\tWrote {len(content)} bytes to {destpath}\n\n')


if __name__ == '__main__':
    main()

# download_data.py
# author: Jenny Zhang
# date: 2024-12-03

# Usage:
# python scripts/download_data.py \
#     --url="https://www.kaggle.com/api/v1/datasets/download/uciml/pima-indians-diabetes-database" \
#     --write-to=data/raw

import click
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from src.read_zip import read_zip

@click.command()
@click.option('--url', type=str, help="URL of dataset to be downloaded")
@click.option('--write-to', type=str, help="Path to directory where raw data will be written to")
def main(url, write_to):
    """Downloads data zip data from the web to a local filepath and extracts it."""
    try:
        read_zip(url, write_to)
    except:
        os.makedirs(write_to)
        read_zip(url, write_to)

if __name__ == '__main__':
    main()
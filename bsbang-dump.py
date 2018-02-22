#!/usr/bin/env python3

import argparse
import contextlib
import json
import logging
import os

import sqlite3

import bioschemas
import bsbang


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# FUNCTIONS
def save_crawl_data(jsonld_data, filename):
    """
    Save jsonlds to sae directory where the db is

    :param _jsonld_data: str(jsonld)
    :param _filename: <path_to_db/name_of_db.json>
    :return:
    """

    with open(filename, 'a') as f:
        f.write(jsonld_data + '\n')


# MAIN
parser = argparse.ArgumentParser('Dump Bioschemas JSONLD from extracted database.')
parser.add_argument('path_to_crawl_db', help='Path to the database used to store extracted jsonld information.')

args = parser.parse_args()

if not os.path.exists(args.path_to_crawl_db):
    logger.error('Crawl database %s does not exist', args.path_to_crawl_db)
    exit(1)

urls_to_exclude = set()

dbpath, dbname = os.path.split(args.path_to_crawl_db)
filepath = str(dbpath) + '/' + dbname[:-3] + '.json'
logger.info('Saving at %s', filepath)

with sqlite3.connect(args.path_to_crawl_db) as conn:
    conn.execute("PRAGMA busy_timeout = 30000")
    conn.row_factory = sqlite3.Row

    with contextlib.closing(conn.cursor()) as curs:

        curs.execute('SELECT COUNT(*) from jsonld')
        count = int(curs.fetchone()[0])
        i = 1
        for row in curs.execute('SELECT jsonld FROM jsonld'):
            jld = row['jsonld']
            logger.info('Processing %s (%d of %d)', jld, i, count)
            save_crawl_data(jld, filepath)
            i += 1

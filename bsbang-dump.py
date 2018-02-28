#!/usr/bin/env python3

import argparse
import contextlib
import logging
import os

import sqlite3


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# MAIN
parser = argparse.ArgumentParser('Dump Bioschemas JSONLD from extracted database.')
parser.add_argument('path_to_crawl_db', help='Path to the database used to store extracted jsonld information.')
parser.add_argument('path_to_save_jsonld', nargs='?', help='Path to the jsonld file where the data is to be dumped')
parser.add_argument(
    '--force-dump',
    action='store_true',
    help='If true then the data will be dumped to the existing location by re-writing the file')

args = parser.parse_args()

if not os.path.exists(args.path_to_crawl_db):
    logger.error('Crawl database %s does not exist', args.path_to_crawl_db)
    exit(1)

if args.path_to_save_jsonld is None:
    dbpath, _ =  os.path.splitext(args.path_to_crawl_db)
    filepath = str(dbpath) + '.json'
else:
   filepath = args.path_to_save_jsonld

logger.info('Saving at %s', filepath)

with sqlite3.connect(args.path_to_crawl_db) as conn:
    conn.execute("PRAGMA busy_timeout = 30000")
    conn.row_factory = sqlite3.Row

    with contextlib.closing(conn.cursor()) as curs:

        curs.execute('SELECT COUNT(*) from jsonld')
        count = int(curs.fetchone()[0])
        i = 1
        if os.path.exists(filepath) and args.force_dump==False:
            logger.error(
                'File already exists. Please choose a custom file name or add --force-dump to re-write this file',
                filepath)
            exit(1)
        else:
            with open(filepath, 'a') as f:
                for row in curs.execute('SELECT jsonld FROM jsonld'):
                    jsonld_data = row['jsonld']
                    logger.info('Processing %s (%d of %d)', jsonld_data, i, count)
                    f.write(jsonld_data + '\n')
                    i += 1

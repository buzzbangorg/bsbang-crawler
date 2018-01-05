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
def insert_into_db(_conn, _url, jsonlds):
    """
    Insert jsonlds into the database

    :param _conn:
    :param _url:
    :param jsonlds: [<jsonld>]
    :return:
    """

    with contextlib.closing(_conn.cursor()) as _curs:
        for jsonld in jsonlds:
            _curs.execute('INSERT INTO jsonld (url, jsonld) VALUES (?, ?)', (_url, json.dumps(jsonld)))
        _curs.execute('DELETE FROM extract_queue WHERE url=?', (_url,))

    _conn.commit()


# MAIN
parser = argparse.ArgumentParser('Extract Bioschemas JSONLD from URLs on the crawl DB extract queue.')
parser.add_argument('path_to_crawl_db', help='Path to the database used to store crawl information.')
args = parser.parse_args()

if not os.path.exists(args.path_to_crawl_db):
    logger.error('Crawl database %s does not exist', args.path_to_crawl_db)
    exit(1)

config = bioschemas.DEFAULT_CONFIG.copy()

urls_to_exclude = set()

with sqlite3.connect(args.path_to_crawl_db) as conn:
    conn.execute("PRAGMA busy_timeout = 30000")
    conn.row_factory = sqlite3.Row

    with contextlib.closing(conn.cursor()) as curs:
        curs.execute('SELECT COUNT(*) from extract_queue')
        count = int(curs.fetchone()[0])
        i = 1

        for row in curs.execute('SELECT url FROM extract_queue'):
            url = row['url']
            logger.info('Processing %s (%d of %d)', url, i, count)
            insert_into_db(conn, url, bsbang.load_bioschemas_jsonld_from_html(url, config))
            i += 1

#!/usr/bin/env python3

import argparse
import contextlib
import json
import logging

import sqlite3

import bioschemas
import bsbang

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# FUNCTIONS
def insert_into_db(_conn, url, jsonlds):
    """
    Insert jsonlds into the database

    :param _conn:
    :param url:
    :param jsonlds_by_url: [<jsonld>]
    :return:
    """

    with contextlib.closing(_conn.cursor()) as curs:
        for jsonld in jsonlds:
            curs.execute('INSERT INTO jsonld (url, jsonld) VALUES (?, ?)', (url, json.dumps(jsonld)))
        curs.execute('DELETE FROM extract_queue WHERE url=?', (url,))

    _conn.commit()


# MAIN
parser = argparse.ArgumentParser('Process URLs on the crawl DB extract queue and extract Bioschemas for indexing.')
args = parser.parse_args()

config = bioschemas.DEFAULT_CONFIG.copy()

urls_to_exclude = set()

with sqlite3.connect('data/crawl.db') as conn:
    conn.execute("PRAGMA busy_timeout = 30000")
    conn.row_factory = sqlite3.Row

    with contextlib.closing(conn.cursor()) as curs:
        for row in curs.execute('SELECT url FROM extract_queue'):
            url = row['url']
            logger.info('Processing %s', url)
            insert_into_db(conn, url, bsbang.load_bioschemas_jsonld_from_html(url, config))

#!/usr/bin/env python3

import argparse
import json
import logging
import os

import sqlite3

import bioschemas
import bsbang

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# FUNCTIONS
def init_db(path):
    """
    Initialize the database

    :param path:
    :return: the open database connection
    """

    _conn = sqlite3.connect(path)

    curs = _conn.cursor()
    curs.execute(
        "CREATE TABLE IF NOT EXISTS jsonld "
            + "(url TEXT NOT NULL, when_crawled INT DEFAULT (strftime('%s', CURRENT_TIMESTAMP)), jsonld TEXT NOT NULL)")
    _conn.commit()
    curs.close()

    return _conn


def insert_into_db(_conn, jsonlds_by_url):
    """
    Insert jsonlds into the database

    :param _conn:
    :param jsonlds_by_url: {<url>:[<jsonld>]}
    :return:
    """
    curs = _conn.cursor()

    for url, jsonlds in jsonlds_by_url.items():
        # FIXME: Yes, this currently doesn't add new jsonld or update on changes
        curs.execute("SELECT COUNT(*) FROM jsonld WHERE url=?", (url,))
        count_row = curs.fetchone()
        if count_row[0] <= 0:
            for jsonld in jsonlds:
                curs.execute('INSERT INTO jsonld (url, jsonld) VALUES (?, ?)', (url, json.dumps(jsonld)))

    _conn.commit()
    curs.close()


# MAIN
parser = argparse.ArgumentParser('Crawl a sitemap XML or webpage and insert the bioschemas information into Solr.')
parser.add_argument('location',
                    help='''Location to crawl. 
If given a sitemap XML URL (e.g. http://beta.synbiomine.org/synbiomine/sitemap.xml) then crawls all the pages referenced
 by the sitemap.
If given a webpage URL (e.g. http://identifiers.org, file://test/examples/FAIRsharing.html) then crawls that webpage.
If given a path (e.g. conf/default-targets.txt) then crawl all the newline-separated URLs in that file.''')
args = parser.parse_args()

config = bioschemas.DEFAULT_CONFIG.copy()
conn = init_db('data/crawl.db')

if os.path.exists(args.location):
    with open(args.location) as f:
        for line in f:
            line = line.strip()
            if not line.startswith('#'):
                insert_into_db(conn, bsbang.load_bioschemas_jsonld_from_url(line, config))
else:
    insert_into_db(conn, bsbang.load_bioschemas_jsonld_from_url(args.location, config))

conn.close()

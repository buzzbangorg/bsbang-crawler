#!/usr/bin/env python3

import argparse
import contextlib
import json
import logging
import os
import sqlite3

import bioschemas.indexers


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# FUNCTIONS
def index_row(_row):
    indexer.index(_row['url'], json.loads(_row['jsonld']))


# MAIN
parser = argparse.ArgumentParser('Index extracted JSONLD into Solr.')
parser.add_argument('path_to_crawl_db', help='Path to the database used to store crawl information.')
parser.add_argument('url_to_index', nargs='?', help='URL to index using only data from the crawl DB')
parser.add_argument('-s', '--solr-core-url', nargs='?', help='URL to solr endpoint')
args = parser.parse_args()

if args.solr_core_url is None:
	endpoint = 'http://localhost:8983/solr/bsbang/'
else:
	endpoint = str(args.solr_core_url)
	logger.info('Indexing at Solr core %s', args.solr_core_url)

if not os.path.exists(args.path_to_crawl_db):
    logger.error('Crawl database %s does not exist', args.path_to_crawl_db)
    exit(1)

config = bioschemas.DEFAULT_CONFIG.copy()
config.update({
    'post_to_solr': True,
    'solr_json_doc_update_url': endpoint + 'update/json/docs',
    'solr_query_url': endpoint +'select'
})

indexer = bioschemas.indexers.SolrIndexer(config)

with sqlite3.connect(args.path_to_crawl_db) as conn:
    conn.execute("PRAGMA busy_timeout = 30000")
    conn.row_factory = sqlite3.Row

    with contextlib.closing(conn.cursor()) as curs:
        if args.url_to_index is not None:
            curs.execute('SELECT jsonld, url FROM jsonld where url=?', (args.url_to_index,))
            index_row(curs.fetchone())
        else:
            curs.execute('SELECT COUNT(*) from jsonld')
            count = int(curs.fetchone()[0])
            i = 1

            for row in curs.execute('SELECT jsonld, url FROM jsonld'):
                logger.info('Indexing %s (%d of %d)', row['url'], i, count)
                index_row(row)
                i += 1

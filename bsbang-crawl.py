#!/usr/bin/env python3

import argparse
import contextlib
import logging
import os

import sqlite3

import bioschemas.crawler

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# MAIN
parser = argparse.ArgumentParser('Add a set of URLs for JSONLD extraction to the crawl database.')

parser.add_argument('path_to_crawl_db', help='Path to the database used to store crawl information.')

parser.add_argument(
    'location',
    help='''Location to process. 
If given a sitemap XML URL (e.g. http://beta.synbiomine.org/synbiomine/sitemap.xml) then adds all the pages referenced
 by the sitemap.
If given a webpage URL (e.g. http://identifiers.org, file://test/examples/FAIRsharing.html) then adds that webpage.
If given a path (e.g. conf/default-targets.txt) then processes all the locations in that file.''')

parser.add_argument(
    '--force-add',
    action='store_true',
    help='If true then URLs are added even if they have already had their JSON-LD extracted')

parser.add_argument(
    '--force-sitemap',
    action='store_true',
    help='If true then the location is always processed as a sitemap.'
         + 'Normally this happens automatically when the URL ends with sitemap.xml'
         + ', but sometimes we need to force this for debugging purposes')

args = parser.parse_args()

if not os.path.exists(args.path_to_crawl_db):
    logger.error('Crawl database %s does not exist', args.path_to_crawl_db)
    exit(1)

config = bioschemas.DEFAULT_CONFIG.copy()
urls_to_crawl = set()

if os.path.exists(args.location):
    with open(args.location) as f:
        for line in f:
            line = line.strip()
            if not line.startswith('#'):
                urls_to_crawl.add(line)
else:
    urls_to_crawl = [args.location]

urls_for_extractor = set()

for url in urls_to_crawl:
    if url.endswith('/sitemap.xml') or args.force_sitemap:
        logger.info('Crawling sitemap %s', url)
        try:
            urls_for_extractor.update(bioschemas.crawler.get_urls_from_sitemap(url))
        except:
            logger.warning('Skipping sitemap %s because it is not valid XML')
    else:
        urls_for_extractor.add(url)

added = 0

with sqlite3.connect(args.path_to_crawl_db) as conn:
    conn.execute("PRAGMA busy_timeout = 30000")
    conn.row_factory = sqlite3.Row
    urls_to_exclude = set()

    with contextlib.closing(conn.cursor()) as curs:
        if not args.force_add:
            for row in curs.execute('SELECT DISTINCT url FROM jsonld'):
                urls_to_exclude.add(row['url'])

        for url in urls_for_extractor:
            # FIXME: Yes, this currently doesn't add new jsonld or update on changes
            if url not in urls_to_exclude:
                curs.execute("INSERT INTO extract_queue VALUES (?)", (url,))
                added += 1

logger.info('Refreshed %d urls', added)

#!/usr/bin/env python3

import contextlib
import sqlite3
import argparse

#MAIN
parser = argparse.ArgumentParser('Setup a database to store crawl data')
parser.add_argument('path_to_crawl_db', help='Path to the database used to store crawl information, e.g data/crawl.db')

args = parser.parse_args()

with sqlite3.connect(args.path_to_crawl_db) as conn:
    with contextlib.closing(conn.cursor()) as curs:
        curs.execute("CREATE TABLE IF NOT EXISTS extract_queue (url TEXT PRIMARY KEY ON CONFLICT IGNORE)")
        curs.execute(
            "CREATE TABLE IF NOT EXISTS jsonld "
            "(url TEXT NOT NULL, when_crawled INT DEFAULT (strftime('%s', CURRENT_TIMESTAMP)), jsonld TEXT NOT NULL)")
        conn.commit()

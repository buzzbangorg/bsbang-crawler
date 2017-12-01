#!/usr/bin/env python3

import contextlib
import sqlite3


with sqlite3.connect('../data/crawl.db') as conn:
    with contextlib.closing(conn.cursor()) as curs:
        curs.execute("CREATE TABLE IF NOT EXISTS extract_queue (url TEXT PRIMARY KEY ON CONFLICT IGNORE)")
        curs.execute(
            "CREATE TABLE IF NOT EXISTS jsonld "
                + "(url TEXT NOT NULL, when_crawled INT DEFAULT (strftime('%s', CURRENT_TIMESTAMP)), jsonld TEXT NOT NULL)")
        conn.commit()

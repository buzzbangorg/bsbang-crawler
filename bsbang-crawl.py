#!/usr/bin/env python3

import argparse
import logging
import os

import bioschemas
import bsbang

logging.basicConfig(level=logging.DEBUG)

# MAIN
parser = argparse.ArgumentParser('Crawl a sitemap XML or webpage and insert the bioschemas information into Solr.')
parser.add_argument('location',
                    help='''Location to crawl. 
If given a sitemap XML URL (e.g. http://beta.synbiomine.org/synbiomine/sitemap.xml) then crawls all the pages referenced
 by the sitemap.
If given a webpage URL (e.g. http://identifiers.org, file://test/examples/FAIRsharing.html) then crawls that webpage.
If given a path (e.g. conf/default-targets.txt) then crawl all the newline-separated URLs in that file.''')
parser.add_argument('--nosolr', action='store_true', help='Don''t actually load anything into Solr, just fetch')
args = parser.parse_args()

config = {
    'jsonld_to_solr_map': bioschemas.JSONLD_TO_SOLR_MAP,
    'mandatory_properties': bioschemas.MANDATORY_PROPERTIES,
    'schema_inheritance_graph': bioschemas.SCHEMA_INHERITANCE_GRAPH,
    'schemas_to_parse': bioschemas.SCHEMAS_TO_PARSE,

    'post_to_solr': not args.nosolr,
    'solr_json_doc_update_path': 'http://localhost:8983/solr/bsbang/update/json/docs'
}

if os.path.exists(args.location):
    with open(args.location) as f:
        for line in f:
            line = line.strip()
            if not line.startswith('#'):
                bsbang.load_bioschemas_jsonld_from_url(line, config)
else:
    bsbang.load_bioschemas_jsonld_from_url(args.location, config)

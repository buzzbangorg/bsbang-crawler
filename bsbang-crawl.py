#!/usr/bin/env python3

import argparse
import canonicaljson
import hashlib
import requests

import bioschemas_lib
import bioschemas_lib.crawler
import bioschemas_lib.parser
import bioschemas_lib.translator


def load_bioschemas_jsonld(url):
    parser = bioschemas_lib.parser.BioschemasParser()
    jsonlds = parser.parse_bioschemas_jsonld_from_url(url)

    headers = {'Content-type': 'application/json'}

    for jsonld in jsonlds:
        schema = jsonld['@type']
        solr_json = bioschemas_lib.translator.create_solr_json_with_mandatory_properties(schema, jsonld)

        # TODO: Use solr de-dupe for this
        # jsonld['id'] = str(uuid.uuid5(namespaceUuid, json.dumps(jsonld)))
        solr_json['id'] = hashlib.sha256(canonicaljson.encode_canonical_json(solr_json)).hexdigest()

        print(solr_json)

        if config['post_to_solr']:
            r = requests.post(config['solr_json_doc_update_path'] + '?commit=true', json=solr_json, headers=headers)
            print(r.text)


# MAIN
parser = argparse.ArgumentParser('Crawl a sitemap XML or webpage and insert the bioschemas information into Solr.')
parser.add_argument('url',
                    help='''URL to crawl. If given a sitemap XML URL (e.g. http://beta.synbiomine.org/synbiomine/sitemap.xml) then crawls
all the pages referenced by the sitemap.
If given a webpage URL (e.g. http://identifiers.org) then currently crawls only that webpage''')
parser.add_argument('--nosolr', action='store_true', help='Don''t actually load anything into Solr, just fetch')
args = parser.parse_args()

config = {
    'post_to_solr': not args.nosolr,
    'solr_json_doc_update_path': 'http://localhost:8983/solr/bsbang/update/json/docs'
}

if args.url.endswith('/sitemap.xml'):
    urls = bioschemas_lib.crawler.get_urls_from_sitemap(args.url)
    urlsLen = len(urls)
    i = 1
    for url in urls:
        print('Crawling %d of %d pages' % (i, urlsLen))
        load_bioschemas_jsonld(url)
        i += 1
else:
    load_bioschemas_jsonld(args.url)

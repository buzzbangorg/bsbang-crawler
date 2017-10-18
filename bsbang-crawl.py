#!/usr/bin/env python3

import argparse
import canonicaljson
import hashlib
import os
import requests

import bioschemas
import bioschemas.crawler
import bioschemas.parser
import bioschemas.translator


def load_bioschemas_jsonld_from_url(url):
    """
    Load Bioschemas JSON-LD from an url.  This may be a webpage or a sitemap pointing to webpages'''

    :param url:
    :return:
    """

    if url.endswith('/sitemap.xml'):
        urls = bioschemas.crawler.get_urls_from_sitemap(url)
        urlsLen = len(urls)
        i = 1
        for url in urls:
            print('Crawling %d of %d pages' % (i, urlsLen))
            load_bioschemas_jsonld_from_html(url)
            i += 1
    else:
        load_bioschemas_jsonld_from_html(url)


def load_bioschemas_jsonld_from_html(url):
    """
    Load Bioschemas JSON-LD from a webpage.

    :param url:
    :return:
    """

    try:
        parser = bioschemas.parser.BioschemasParser()
        jsonlds = parser.parse_bioschemas_jsonld_from_url(url)

        headers = {'Content-type': 'application/json'}

        for jsonld in jsonlds:
            schema = jsonld['@type']
            solr_json = bioschemas.translator.create_solr_json_with_mandatory_properties(schema, jsonld)

            # TODO: Use solr de-dupe for this
            # jsonld['id'] = str(uuid.uuid5(namespaceUuid, json.dumps(jsonld)))
            solr_json['id'] = hashlib.sha256(canonicaljson.encode_canonical_json(solr_json)).hexdigest()

            print(solr_json)

            if config['post_to_solr']:
                r = requests.post(config['solr_json_doc_update_path'] + '?commit=true', json=solr_json, headers=headers)
                print(r.text)
    except Exception as e:
        print('Ignoring failure with %s' % str(e))

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
    'post_to_solr': not args.nosolr,
    'solr_json_doc_update_path': 'http://localhost:8983/solr/bsbang/update/json/docs'
}

if os.path.exists(args.location):
    with open(args.location) as f:
        for line in f:
            line = line.strip()
            if not line.startswith('#'):
                load_bioschemas_jsonld_from_url(line)
else:
    load_bioschemas_jsonld_from_url(args.location)

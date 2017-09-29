#!/usr/bin/env python3

import argparse
import canonicaljson
import hashlib
import lxml.etree as etree
import requests

from bioschemas_lib import MANDATORY_PROPS
from bioschemas_lib.parser import BioschemasParser


def create_solr_json_with_mandatory_properties(jsonld):
    solr_json = {}
    for prop in MANDATORY_PROPS:
        solr_json[prop] = jsonld[prop]

    return solr_json


def load_bioschemas_jsonld(url):
    jsonlds = bsParser.parse_bioschemas_jsonld_from_url(url)

    headers = {'Content-type': 'application/json'}

    for jsonld in jsonlds:
        solr_json = create_solr_json_with_mandatory_properties(jsonld)

        # TODO: Use solr de-dupe for this
        # jsonld['id'] = str(uuid.uuid5(namespaceUuid, json.dumps(jsonld)))
        solr_json['id'] = hashlib.sha256(canonicaljson.encode_canonical_json(solr_json)).hexdigest()

        print(solr_json)

        if config['post_to_solr']:
            r = requests.post(config['solr_json_doc_update_path'] + '?commit=true', json=solr_json, headers=headers)
            print(r.text)


def load_from_sitemap(sitemap):
    loc_elems = sitemap.findall('//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
    loc_elems_len = len(loc_elems)
    print('Found %d pages to crawl' % loc_elems_len)
    i = 1
    for loc_elem in loc_elems:
        print('Crawling %d of %d pages' % (i, loc_elems_len))
        load_bioschemas_jsonld(loc_elem.text)
        i += 1


def load_from_sitemapindex(sitemapindex):
    # for loc_elem in sitemapindex_elem.findall('/sitemap/loc'):
    for loc_elem in sitemapindex.findall('//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        load_sitemap(loc_elem.text)


def load_sitemap(url):
    sitemap = etree.parse(url)
    root_tag = sitemap.getroot().tag

    if root_tag == '{http://www.sitemaps.org/schemas/sitemap/0.9}sitemapindex':
        print('Loading sitemap index %s' % url)
        load_from_sitemapindex(sitemap)
    elif root_tag == '{http://www.sitemaps.org/schemas/sitemap/0.9}urlset':
        print('Loading sitemap %s' % url)
        load_from_sitemap(sitemap)
    else:
        print('Unrecognized root tag %s in sitemap from %s. Ignoring' % (root_tag, url))


# MAIN
parser = argparse.ArgumentParser('Crawl a site and insert the bioschemas information into Solr.')
parser.add_argument('siteUrl', help='Site to crawl. For example, http://www.synbiomine.org')
parser.add_argument('--nosolr', action='store_true', help='Don''t actually load anything into Solr, just fetch')
args = parser.parse_args()

config = {
    'post_to_solr': not args.nosolr,
    'solr_json_doc_update_path': 'http://localhost:8983/solr/bsbang/update/json/docs'
}

bsParser = BioschemasParser()

load_sitemap(args.siteUrl + '/sitemap.xml')

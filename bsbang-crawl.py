#!/usr/bin/env python3

import argparse
import hashlib
import json
import requests
import lxml.etree as etree

import bs4
import canonicaljson
# import uuid

context = {'mandatory_props': ['identifier', 'name', 'additionalType', 'url']}


def assert_mandatory_jsonld_properties(jsonld):
    """Assert that the property exists in the jsonld"""
    for prop in context['mandatory_props']:
        if prop not in jsonld:
            raise KeyError('Mandatory property %s not present' % (prop))


def create_solr_json_with_mandatory_properties(jsonld):
    solr_json = {}
    for prop in context['mandatory_props']:
        solr_json[prop] = jsonld[prop]

    return solr_json


def load_bioschemas_jsonld_from_url(url, post_to_solr=True):
    print('Loading page %s' % url)
    r = requests.get(url)
    load_bioschemas_jsonld_from_html(r.text)


def load_bioschemas_jsonld_from_html(html, post_to_solr=True):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    tags = soup.find_all('script', type='application/ld+json')
    print('Found %d ld+json sections' % len(tags))

    jsonlds = []

    for tag in tags:
        jsonlds.append(json.loads(tag.string))

    headers = {'Content-type': 'application/json'}

    for jsonld in jsonlds:
        try:
            assert_mandatory_jsonld_properties(jsonld)
        except KeyError as err:
            print('Ignoring %s as %s' % (jsonld, err))
            continue

        solr_json = create_solr_json_with_mandatory_properties(jsonld)

        # TODO: Use solr de-dupe for this
        # jsonld['id'] = str(uuid.uuid5(namespaceUuid, json.dumps(jsonld)))
        solr_json['id'] = hashlib.sha256(canonicaljson.encode_canonical_json(solr_json)).hexdigest()

        print(solr_json)

        if post_to_solr:
            r = requests.post(solrJsonDocUpdatePath + '?commit=true', json=solr_json, headers=headers)
            print(r.text)


def load_from_sitemap(sitemap, post_to_solr=True):
    loc_elems = sitemap.findall('//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
    loc_elems_len = len(loc_elems)
    print('Found %d pages to crawl' % loc_elems_len)
    i = 1
    for loc_elem in loc_elems:
        print('Crawling %d of %d pages' % (i, loc_elems_len))
        load_bioschemas_jsonld_from_url(loc_elem.text, post_to_solr=post_to_solr)
        i += 1


def load_from_sitemapindex(sitemapindex, post_to_solr=True):
    # for loc_elem in sitemapindex_elem.findall('/sitemap/loc'):
    for loc_elem in sitemapindex.findall('//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        load_sitemap(loc_elem.text, post_to_solr=post_to_solr)


def load_sitemap(url, post_to_solr=True):
    sitemap = etree.parse(url)
    root_tag = sitemap.getroot().tag

    if root_tag == '{http://www.sitemaps.org/schemas/sitemap/0.9}sitemapindex':
        print('Loading sitemap index %s' % url)
        load_from_sitemapindex(sitemap, post_to_solr=post_to_solr)
    elif root_tag == '{http://www.sitemaps.org/schemas/sitemap/0.9}urlset':
        print('Loading sitemap %s' % url)
        load_from_sitemap(sitemap, post_to_solr=post_to_solr)
    else:
        print('Unrecognized root tag %s in sitemap from %s. Ignoring' % (root_tag, url))


# MAIN
# namespaceUuid = uuid.UUID('734bf6c4-c123-412e-981f-b867570a369f')
solrPath = 'http://localhost:8983/solr/bsbang/'
solrJsonDocUpdatePath = solrPath + 'update/json/docs'

parser = argparse.ArgumentParser('Crawl a site and insert the bioschemas information into Solr.')
parser.add_argument('siteUrl', help='Site to crawl. For example, http://www.synbiomine.org')
parser.add_argument('--nosolr', action='store_true', help='Don''t actually load anything into Solr, just fetch')
args = parser.parse_args()

load_sitemap(args.siteUrl + '/sitemap.xml', post_to_solr=not args.nosolr)

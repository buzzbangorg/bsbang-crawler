#!/usr/bin/env python3

import argparse
import lxml.etree as etree

from bioschemas_lib.parser import BioschemasParser


def load_from_sitemap(sitemap):
    loc_elems = sitemap.findall('//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
    loc_elems_len = len(loc_elems)
    print('Found %d pages to crawl' % loc_elems_len)
    i = 1
    for loc_elem in loc_elems:
        print('Crawling %d of %d pages' % (i, loc_elems_len))
        bsParser.load_bioschemas_jsonld_from_url(loc_elem.text)
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

bsParser = BioschemasParser(post_to_solr=not args.nosolr)

load_sitemap(args.siteUrl + '/sitemap.xml')

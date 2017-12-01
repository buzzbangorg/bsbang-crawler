import logging

import io
import lxml.etree as etree
import requests

logger = logging.getLogger(__name__)


def get_urls_from_sitemap(sitemap_url):
    """
    Get all the webpage urls we can reach from a sitemap, whether this is a sitemap XML or a sitemap index XML

    :param sitemap_url:
    :return: set(<url>)
    """

    r = requests.get(sitemap_url)
    sitemap = etree.parse(io.BytesIO(r.content))
    root_tag = sitemap.getroot().tag

    if root_tag == '{http://www.sitemaps.org/schemas/sitemap/0.9}sitemapindex' or root_tag == 'sitemapindex':
        logger.info('Loading sitemap index %s' % sitemap_url)
        return get_urls_from_loaded_sitemapindex(sitemap)
    elif root_tag == '{http://www.sitemaps.org/schemas/sitemap/0.9}urlset' or root_tag == 'urlset':
        logger.info('Loading sitemap %s' % sitemap_url)
        return get_urls_from_loaded_sitemap(sitemap)
    else:
        logger.debug('Unrecognized root tag %s in sitemap from %s. Ignoring' % (root_tag, sitemap_url))


def get_urls_from_loaded_sitemap(sitemap):
    urls = set()
    loc_elems = sitemap.findall('//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')
    loc_elems += sitemap.findall('//loc')

    loc_elems_len = len(loc_elems)
    logger.info('Found %d pages to crawl' % loc_elems_len)
    for loc_elem in loc_elems:
        urls.add(loc_elem.text)

    return urls


def get_urls_from_loaded_sitemapindex(sitemapindex):
    """Get all the webpage urls in a retrieved sitemap index XML"""
    urls = set()
    # for loc_elem in sitemapindex_elem.findall('/sitemap/loc'):
    for loc_elem in sitemapindex.findall('//{http://www.sitemaps.org/schemas/sitemap/0.9}loc'):
        urls.update(get_urls_from_sitemap(loc_elem.text))
    for loc_elem in sitemapindex.findall('//loc'):
        urls.update(get_urls_from_sitemap(loc_elem.text))

    return urls

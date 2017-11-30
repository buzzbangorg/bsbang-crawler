import logging

import bioschemas
import bioschemas.crawler
import bioschemas.extractors
import bioschemas.indexers

logger = logging.getLogger(__name__)


def load_bioschemas_jsonld_from_url(url, config, urls_to_exclude = set(), force_sitemap=False):
    """
    Load Bioschemas JSON-LD from an url.  This may be a webpage or a sitemap pointing to webpages'''

    :param url:
    :param config:
    :param urls_to_exclude:
    :return: {<url>:[<jsonlds>+]}
    """

    jsonlds = {}

    if url.endswith('/sitemap.xml') or force_sitemap:
        urls = bioschemas.crawler.get_urls_from_sitemap(url)
    else:
        urls = [url]

    urls_len = len(urls)
    i = 1
    for url in urls:
        if url in urls_to_exclude:
            logger.info('Ignoring %s (%d of %d) since it''s on the exclude list', url, i, urls_len)
        else:
            logger.info('Crawling %s (%d of %d)', url, i, urls_len)
            jsonlds[url] = load_bioschemas_jsonld_from_html(url, config)

        i += 1

    return jsonlds


def load_bioschemas_jsonld_from_html(url, config):
    """
    Load Bioschemas JSON-LD from a webpage.

    :param url:
    :param config:
    :return: array of extracted jsonld
    """

    try:
        extractor = bioschemas.extractors.ExtractorFromHtml(config)
        jsonlds = extractor.parse_bioschemas_jsonld_from_url(url)
        logger.info('Got %d jsonld sections', len(jsonlds))
        return jsonlds
    except Exception as e:
        logging.exception('Ignoring failure')

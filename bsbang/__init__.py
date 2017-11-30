import logging

import bioschemas
import bioschemas.crawler
import bioschemas.parser
import bioschemas.indexers


def load_bioschemas_jsonld_from_url(url, config, urls_to_exclude = set()):
    """
    Load Bioschemas JSON-LD from an url.  This may be a webpage or a sitemap pointing to webpages'''

    :param url:
    :param config:
    :param urls_to_exclude:
    :return: {<url>:[<jsonlds>+]}
    """

    jsonlds = {}

    if url.endswith('/sitemap.xml'):
        urls = bioschemas.crawler.get_urls_from_sitemap(url)
    else:
        urls = [url]

    urls_len = len(urls)
    i = 1
    for url in urls:
        if url in urls_to_exclude:
            logging.info('Ignoring %s (%d of %d) since it''s on the exclude list', url, i, urls_len)
        else:
            logging.info('Crawling %s (%d of %d)', url, i, urls_len)
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
        parser = bioschemas.parser.Parser(config)
        return parser.parse_bioschemas_jsonld_from_url(url)
    except Exception as e:
        logging.exception('Ignoring failure')

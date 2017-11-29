import bioschemas
import bioschemas.crawler
import bioschemas.parser
import bioschemas.inserters


def load_bioschemas_jsonld_from_url(url, config):
    """
    Load Bioschemas JSON-LD from an url.  This may be a webpage or a sitemap pointing to webpages'''

    :param url:
    :param config:
    :return:
    """

    if url.endswith('/sitemap.xml'):
        urls = bioschemas.crawler.get_urls_from_sitemap(url)
        urls_len = len(urls)
        i = 1
        for url in urls:
            print('Crawling %d of %d pages' % (i, urls_len))
            load_bioschemas_jsonld_from_html(url, config)
            i += 1
    else:
        load_bioschemas_jsonld_from_html(url, config)


def load_bioschemas_jsonld_from_html(url, config):
    """
    Load Bioschemas JSON-LD from a webpage.

    :param url:
    :param config:
    :return:
    """

    try:
        parser = bioschemas.parser.Parser(config)
        jsonlds = parser.parse_bioschemas_jsonld_from_url(url)
        inserter = bioschemas.inserters.SolrInserter(config)
        inserter.insert(jsonlds)
    except Exception as e:
        print('Ignoring failure with %s' % str(e))

import logging

import bioschemas
import bioschemas.crawler
import bioschemas.extractors
import bioschemas.indexers

logger = logging.getLogger(__name__)


def load_bioschemas_jsonld_from_html(url, config):
    """
    Load Bioschemas JSON-LD from a webpage.

    :param url:
    :param config:
    :return: array of extracted jsonld
    """

    try:
        extractor = bioschemas.extractors.ExtractorFromHtml(config)
        jsonlds = extractor.extract_bioschemas_jsonld_from_url(url)
        logger.info('Got %d jsonld sections', len(jsonlds))
        return jsonlds
    except Exception as e:
        logging.exception('Ignoring failure')

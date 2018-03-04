import logging

import bioschemas
import bioschemas.crawler
import bioschemas.extractors
import bioschemas.filters
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
        filt = bioschemas.filters.BioschemasFilter(config)
        jsonlds = extractor.extract_jsonld_from_url(url)
        jsonlds = filt.filter(jsonlds)
        logger.info('Got %d jsonld sections', len(jsonlds))
        return jsonlds
    except Exception as e:
        logging.exception('Ignoring failure')

import logging
import os

from requests_html import HTMLSession
import bs4
import json

logger = logging.getLogger(__name__)


class ExtractorFromHtml:
    def __init__(self, config):
        self.config = config

    def extract_jsonld_from_url(self, url):
        """
        Extract jsonld from the given url
        :param url:
        :return: [<jsonld>+]
        """
        session = HTMLSession()
        response = session.get(url)
        if self.config.get('dynamic', None):
            response.html.render()
        return self._extract_jsonld_from_html(response.text)

    def _extract_jsonld_from_html(self, html):
        """
        Extract jsonld from html

        :param html:
        :return: [<jsonld>]
        """
        soup = bs4.BeautifulSoup(html, 'html.parser')
        ldjson_script_sections = soup.find_all('script', type='application/ld+json')
        logger.debug('Found %d ld+json sections', len(ldjson_script_sections))

        jsonlds = []

        for ldjson_script_section in ldjson_script_sections:
            jsonlds.append(json.loads(ldjson_script_section.string))

        return jsonlds

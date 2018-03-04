import logging

from requests_html import HTMLSession
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
        html_response = self.get_html_from_url(url)
        return self.extract_jsonld_from_html(html_response)

    @staticmethod
    def get_html_from_url(url, is_dynamic=False):
        with HTMLSession() as session:
            response = session.get(url)
            if is_dynamic:
                response.html.render()
            return response.html

    @staticmethod
    def extract_jsonld_from_html(html):
        """
        Extract jsonld from html

        :param html: request-html HTML object
        :return: [<jsonld>]
        """
        ldjson_script_sections = html.find("script[type='application/ld+json']")  # use css selector to find the tag
        logger.debug('Found %d ld+json sections', len(ldjson_script_sections))

        return [json.loads(section.text.replace('\\n', ''), strict=False) for section in ldjson_script_sections]

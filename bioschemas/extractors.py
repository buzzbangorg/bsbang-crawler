import logging
import os

import bs4
import json
import requests
from requests_testadapter import Resp

logger = logging.getLogger(__name__)


class LocalFileAdapter(requests.adapters.HTTPAdapter):
    def build_response_from_file(self, request):
        file_path = request.url[7:]
        with open(file_path, 'rb') as file:
            buff = bytearray(os.path.getsize(file_path))
            file.readinto(buff)
            resp = Resp(buff)
            r = self.build_response(request, resp)

            return r

    def send(self, request, stream=False, timeout=None,
             verify=True, cert=None, proxies=None):
        return self.build_response_from_file(request)


class ExtractorFromHtml:
    def __init__(self, config):
        self.config = config

    def extract_jsonld_from_url(self, url):
        """
        Extract jsonld from the given url

        :param url:
        :return: [<jsonld>+]
        """
        requests_session = requests.session()
        requests_session.mount('file://', LocalFileAdapter())
        r = requests_session.get(url)
        return self._extract_jsonld_from_html(r.text)

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

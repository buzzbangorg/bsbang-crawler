import json
import requests

import bs4

from bioschemas_lib import MANDATORY_PROPS


class BioschemasParser:
    def __init__(self):
        self.config = {'mandatory_props': MANDATORY_PROPS}

    def assert_mandatory_jsonld_properties(self, jsonld):
        """Assert that the property exists in the jsonld"""
        for prop in self.config['mandatory_props']:
            if prop not in jsonld:
                raise KeyError('Mandatory property %s not present' % prop)

    def parse_bioschemas_jsonld_from_url(self, url):
        print('Loading page %s' % url)
        r = requests.get(url)
        return self.parse_bioschemas_jsonld_from_html(r.text)

    def parse_bioschemas_jsonld_from_html(self, html):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        tags = soup.find_all('script', type='application/ld+json')
        print('Found %d ld+json sections' % len(tags))

        jsonlds = []

        for tag in tags:
            jsonlds.append(json.loads(tag.string))

        final_jsonlds = []

        for jsonld in jsonlds:
            try:
                self.assert_mandatory_jsonld_properties(jsonld)
                final_jsonlds.append(jsonld)
            except KeyError as err:
                print('Ignoring %s as %s' % (jsonld, err))
                continue

        return final_jsonlds

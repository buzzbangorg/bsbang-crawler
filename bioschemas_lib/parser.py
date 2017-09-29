import hashlib
import json
import requests

import bs4
import canonicaljson


class BioschemasParser:
    def __init__(self, post_to_solr=True):
        self.config = {'post_to_solr': post_to_solr}
        self.solr_path = 'http://localhost:8983/solr/bsbang/'
        self.solr_json_doc_update_path = self.solr_path + 'update/json/docs'

    def assert_mandatory_jsonld_properties(self, jsonld):
        """Assert that the property exists in the jsonld"""
        for prop in self.config['mandatory_props']:
            if prop not in jsonld:
                raise KeyError('Mandatory property %s not present' % prop)

    def create_solr_json_with_mandatory_properties(self, jsonld):
        solr_json = {}
        for prop in self.config['mandatory_props']:
            solr_json[prop] = jsonld[prop]

        return solr_json

    def load_bioschemas_jsonld_from_url(self, url):
        print('Loading page %s' % url)
        r = requests.get(url)
        self.load_bioschemas_jsonld_from_html(r.text)

    def load_bioschemas_jsonld_from_html(self, html):
        soup = bs4.BeautifulSoup(html, 'html.parser')
        tags = soup.find_all('script', type='application/ld+json')
        print('Found %d ld+json sections' % len(tags))

        jsonlds = []

        for tag in tags:
            jsonlds.append(json.loads(tag.string))

        headers = {'Content-type': 'application/json'}

        for jsonld in jsonlds:
            try:
                self.assert_mandatory_jsonld_properties(jsonld)
            except KeyError as err:
                print('Ignoring %s as %s' % (jsonld, err))
                continue

            solr_json = self.create_solr_json_with_mandatory_properties(jsonld)

            # TODO: Use solr de-dupe for this
            # jsonld['id'] = str(uuid.uuid5(namespaceUuid, json.dumps(jsonld)))
            solr_json['id'] = hashlib.sha256(canonicaljson.encode_canonical_json(solr_json)).hexdigest()

            print(solr_json)

            if self.config['post_to_solr']:
                r = requests.post(self.solr_json_doc_update_path + '?commit=true', json=solr_json, headers=headers)
                print(r.text)

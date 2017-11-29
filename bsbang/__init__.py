import canonicaljson
import hashlib
import requests

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
        translator = bioschemas.inserters.SolrInserter(config)

        headers = {'Content-type': 'application/json'}

        for jsonld in jsonlds:
            schema = jsonld['@type']
            solr_json = translator.create_solr_json_with_mandatory_properties(schema, jsonld)

            # TODO: Use solr de-dupe for this
            # jsonld['id'] = str(uuid.uuid5(namespaceUuid, json.dumps(jsonld)))
            solr_json['id'] = hashlib.sha256(canonicaljson.encode_canonical_json(solr_json)).hexdigest()

            print(solr_json)

            if config['post_to_solr']:
                r = requests.post(config['solr_json_doc_update_path'] + '?commit=true', json=solr_json, headers=headers)
                print(r.text)
    except Exception as e:
        print('Ignoring failure with %s' % str(e))

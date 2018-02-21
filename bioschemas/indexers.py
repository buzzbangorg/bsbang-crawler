import logging

import canonicaljson
import hashlib
import json
import requests

import bioschemas.utils

logger = logging.getLogger(__name__)
# logger.level = logging.DEBUG


class SolrIndexer:
    def __init__(self, config):
        self.config = config
        self.utils = bioschemas.utils.Utils(config)

    def index(self, url, jsonld):
        headers = {'Content-type': 'application/json'}
        schema = jsonld['@type']
        solr_json = self._create_solr_json(schema, jsonld)

        # TODO: Use solr de-dupe for this
        # jsonld['id'] = str(uuid.uuid5(namespaceUuid, json.dumps(jsonld)))
        solr_json['id'] = hashlib.sha256(canonicaljson.encode_canonical_json(solr_json)).hexdigest()

        if self.config['post_to_solr']:
            r = requests.get(self.config['solr_query_url'] + '?q=id:' + solr_json['id'])
            if r.status_code != 200:
                logger.error('Could not post to Solr: %s', r.text)

            r_json = json.loads(r.text)
            num_found = int(r_json['response']['numFound'])
            if num_found > 0:
                logger.info('Skipping %s as already indexed', url)

                if num_found > 1:
                    logger.warning('%s has %d instances which should be impossible', url, num_found)

                return

            logger.debug('Posting %s', solr_json)

            r = requests.post(
                self.config['solr_json_doc_update_url'] + '?commit=true', json=solr_json, headers=headers)
            if r.status_code != 200:
                logger.error('Could not post to Solr: %s', r.text)

    def _create_solr_json(self, schema, jsonld):
        """
        Create JSON we can put into Solr from the Bioschemas JSON-LD

        :param schema:
        :param jsonld:
        :return:
        """
        schema = self.utils.map_schema_if_necessary(schema)
        jsonld['@type'] = schema

        return self._create_solr_json_properties(schema, jsonld)

    def _create_solr_json_properties(self, schema, jsonld):
        """
        Create JSON properties we can put into Solr from the Bioschemas JSON-LD

        :param schema: The name of the schema (e.g. 'DataCatalog')
        :param jsonld: The schema JSON-LD
        :return:
        """

        # print('Inspecting schema %s with jsonld size %d' % (schema, len(jsonld)))
        solr_json = {}

        if 'mandatory_properties' in self.config:
            self._process_configured_properties(schema, jsonld, self.config['mandatory_properties'], solr_json)

        if 'optional_properties' in self.config:
            self._process_configured_properties(schema, jsonld, self.config['optional_properties'], solr_json)

        schema_graph = self.config['schema_inheritance_graph']
        parent_schema = schema_graph[schema]

        if parent_schema is not None:
            solr_json.update(self._create_solr_json_properties(parent_schema, jsonld))

        return solr_json

    def _process_configured_properties(self, schema, jsonld, configured_props, solr_json):
        """
        Process the configured properties, taking them out of jsonld, transforming them where appropriate, and inserting
        into the solr_json

        :param schema:
        :param jsonld:
        :param configured_props:
        :param solr_json:
        :return:
        """

        json_to_solr_map = self.config['jsonld_to_solr_map']

        if schema in configured_props:
            for prop_name in configured_props[schema]:
                # Mandatory checking is done by the parser
                if prop_name not in jsonld:
                    continue

                if prop_name in json_to_solr_map:
                    solr_prop_name = json_to_solr_map[prop_name]
                else:
                    solr_prop_name = prop_name

                prop_value = self.utils.get_value_from_jsonld_value(jsonld[prop_name])

                logger.debug(
                    'Adding key "%s" -> "%s" for %s, value "%s"',
                    prop_name, solr_prop_name, prop_value, schema)

                solr_json[solr_prop_name] = prop_value

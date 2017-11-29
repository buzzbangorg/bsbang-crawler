import logging

logger = logging.getLogger(__name__)


class SolrInserter:
    def __init__(self, config):
        self.config = config

    def create_solr_json(self, schema, jsonld):
        """
        Create JSON we can put into Solr from the Bioschemas JsonLD

        :param schema:
        :param jsonld:
        :return:
        """

        # print('Inspecting schema %s with jsonld size %d' % (schema, len(jsonld)))
        solr_json = {}

        self._process_configured_properties(schema, jsonld, self.config['mandatory_properties'], solr_json)
        self._process_configured_properties(schema, jsonld, self.config['optional_properties'], solr_json)

        schema_graph = self.config['schema_inheritance_graph']
        parent_schema = schema_graph[schema]

        if parent_schema is not None:
            solr_json.update(self.create_solr_json(parent_schema, jsonld))

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
                if prop_name in json_to_solr_map:
                    solr_prop_name = json_to_solr_map[prop_name]
                else:
                    solr_prop_name = prop_name

                logger.debug(
                    'Adding key "%s" -> "%s" for %s, value "%s"',
                    prop_name, solr_prop_name, jsonld[prop_name], schema)

                solr_json[solr_prop_name] = jsonld[prop_name]

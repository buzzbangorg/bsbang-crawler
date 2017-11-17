import logging

logger = logging.getLogger(__name__)


class Translator:
    def __init__(self, config):
        self.config = config

    def create_solr_json_with_mandatory_properties(self, schema, jsonld):
        """
        Create JSON we can put into Solr from the Bioschemas JsonLD

        :param schema:
        :param jsonld:
        :return:
        """

        # print('Inspecting schema %s with jsonld size %d' % (schema, len(jsonld)))
        solr_json = {}

        props = self.config['mandatory_properties']
        map = self.config['jsonld_to_solr_map']
        schema_graph = self.config['schema_inheritance_graph']

        if schema in props:
            for prop_name in props[schema]:
                if prop_name in map:
                    solr_prop_name = map[prop_name]
                else:
                    solr_prop_name = prop_name

                logger.debug(
                    'Adding key "%s" -> "%s" for %s, value "%s"',
                    prop_name, solr_prop_name, jsonld[prop_name], schema)

                solr_json[solr_prop_name] = jsonld[prop_name]

        parent_schema = schema_graph[schema]
        if parent_schema is not None:
            solr_json.update(self.create_solr_json_with_mandatory_properties(parent_schema, jsonld))

        return solr_json

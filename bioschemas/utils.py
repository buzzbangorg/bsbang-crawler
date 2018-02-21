import logging

logger = logging.getLogger(__name__)


class Utils:
    def __init__(self, config):
        self.config = config

    @staticmethod
    def get_value_from_jsonld_value(jsonld_value):
        """
        Return the value for the given jsonld_value object.

        If jsonld_value is a primitive value, return that directly
        Else, if it is a value object then return the associated value

        :param jsonld_value:
        :return:
        """
        if not isinstance(jsonld_value, dict):
            return str(jsonld_value)
        elif '@value' in jsonld_value:
            return str(jsonld_value['@value'])
        else:
            return None

    def map_schema_if_necessary(self, schema):
        """
        Get the mapped schema if there is one for this schema

        :param schema:
        :return:
        """
        if 'schema_map' in self.config:
            schema_map = self.config['schema_map']

            if schema in schema_map:
                logger.debug('Mapping schema %s to %s', schema, schema_map[schema])
                schema = schema_map[schema]

        return schema

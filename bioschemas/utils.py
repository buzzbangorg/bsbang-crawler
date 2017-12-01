import logging

logger = logging.getLogger(__name__)


class Utils:
    def __init__(self, config):
        self.config = config

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

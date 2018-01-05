import logging
import unittest

import bioschemas.filters


logging.basicConfig(level=logging.ERROR)


class TestFilters(unittest.TestCase):
    def test_type(self):
        config = {
            'schemas_to_parse': ['atype'],
            'schema_inheritance_graph': {'atype': None}
        }

        jsonld = {
            '@type': 'atype',
        }

        f = bioschemas.filters.BioschemasFilter(config)
        jsonlds = f.filter([jsonld])
        self.assertEqual(len(jsonlds), 1)

    def test_mapped_type(self):
        config = {
            'schemas_to_parse': ['atype'],
            'schema_map': {'mappedtype': 'atype'},
            'schema_inheritance_graph': {'atype': None}
        }

        jsonld = {
            '@type': 'mappedtype',
        }

        f = bioschemas.filters.BioschemasFilter(config)
        jsonlds = f.filter([jsonld])
        self.assertEqual(len(jsonlds), 1)

    def test_ignored_type(self):
        config = {
            'schemas_to_parse': ['atype'],
            'schema_inheritance_graph': {'atype': None}
        }

        jsonld = {
            '@type': 'btype',
        }

        f = bioschemas.filters.BioschemasFilter(config)
        jsonlds = f.filter([jsonld])
        self.assertEqual(len(jsonlds), 0)

    def test_mandatory_prop_missing(self):
        config = {
            'schemas_to_parse': ['atype'],
            'mandatory_properties': {'atype': ['mandatory_prop']},
            'schema_inheritance_graph': {'atype': None}
        }

        jsonld = {
            '@type': 'atype',
            'some_other_prop': 'cheese'
        }

        f = bioschemas.filters.BioschemasFilter(config)
        jsonlds = f.filter([jsonld])
        self.assertEqual(len(jsonlds), 0)

    def test_mapped_property(self):
        config = {
            'schemas_to_parse': ['a_type'],
            'schema_inheritance_graph': {'a_type': None},
            'properties_map': {'a_type': { 'a_property': 'b_property' }}
        }

        jsonld = {
            '@type': 'a_type',
            'a_property': 'a_value'
        }

        f = bioschemas.filters.BioschemasFilter(config)
        jsonlds = f.filter([jsonld])
        self.assertEqual(jsonlds[0]['b_property'], 'a_value')

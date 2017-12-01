import unittest

import bioschemas.filters


class TestFilters(unittest.TestCase):
    def test_bs_mandatory_prop_missing(self):
        config = {
            'mandatory_properties': {'atype', 'mandatory_prop'},
            'schema_inheritance_graph': {'atype': None}
        }

        jsonld = {
            '@type': 'atype',
            'some_other_prop': 'cheese'
        }

        f = bioschemas.filters.BioschemasFilter(config)
        jsonlds = f.filter([jsonld])
        self.assertEqual(len(jsonlds), 0)

    def test_non_bs_type(self):
        config = {
            'mandatory_properties': {'atype', 'mandatory_prop'},
            'schema_inheritance_graph': {'atype': None}
        }

        jsonld = {
            '@type': 'btype',
        }

        f = bioschemas.filters.BioschemasFilter(config)
        jsonlds = f.filter([jsonld])
        self.assertEqual(len(jsonlds), 0)

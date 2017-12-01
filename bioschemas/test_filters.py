import unittest

import bioschemas.filters


class TestFilters(unittest.TestCase):
    def test_bs_mandatory_prop_missing(self):
        config = {
            'mandatory_properties': {'type', 'mandatory_prop'},
            'schema_inheritance_graph': {'type': None}
        }

        # "name": "Gene arcA E. coli str. K-12 substr. MG1655 b4401",
        jsonld = {
            '@type': 'type',
            'some_other_prop': 'cheese'
        }

        f = bioschemas.filters.BioschemasFilter(config)
        jsonlds = f.filter([jsonld])
        self.assertEqual(len(jsonlds), 0)

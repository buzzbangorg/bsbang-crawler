import unittest

import bioschemas.filters


config = bioschemas.DEFAULT_CONFIG


class TestFilters(unittest.TestCase):
    def test_bs_mandatory_prop_missing(self):
        # "name": "Gene arcA E. coli str. K-12 substr. MG1655 b4401",
        jsonld = {
            '@type': 'PhysicalEntity',
            'additionalType': 'http://www.ebi.ac.uk/ols/ontologies/so/terms?obo_id=SO:0000704',
            'identifier': 'b4401',
            'url': 'http://localhost:8080/synbiomine/report.do?id=2026346'
        }

        f = bioschemas.filters.BioschemasFilter(config)
        jsonlds = f.filter([jsonld])
        self.assertEqual(len(jsonlds), 0)
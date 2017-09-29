#!/usr/bin/env python3

import unittest

from bioschemas_lib.parser import BioschemasParser


class TestBioschemasParserMethods(unittest.TestCase):
    def test_load_bioschemas_jsonld_from_html_mandatory_prop_missing(self):
        # "name": "Gene arcA E. coli str. K-12 substr. MG1655 b4401",
        html = '''<script type="application/ld+json">
        {
          "@context": "http://bioschemas.org",
          "@type": "PhysicalEntity",
          "additionalType": "http://www.ebi.ac.uk/ols/ontologies/so/terms?obo_id=SO:0000704",
          "identifier": "b4401",  
          "url": "http://localhost:8080/synbiomine/report.do?id=2026346"
        }
        </script>
        '''

        bs_parser = BioschemasParser()
        jsonlds = bs_parser.parse_bioschemas_jsonld_from_html(html)
        self.assertEqual(len(jsonlds), 0)

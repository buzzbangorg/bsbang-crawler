import unittest

import bioschemas
from bioschemas.parser import Parser

config = {
    'jsonld_to_solr_map': bioschemas.JSONLD_TO_SOLR_MAP,
    'mandatory_properties': bioschemas.MANDATORY_PROPERTIES,
    'schema_inheritance_graph': bioschemas.SCHEMA_INHERITANCE_GRAPH,
    'schemas_to_parse': bioschemas.SCHEMAS_TO_PARSE
}


class TestParser(unittest.TestCase):
    def test_load_bioschemas_jsonld_from_html(self):
        html = '''<script type="application/ld+json">
        {
          "@context": "http://bioschemas.org",
          "@type": "PhysicalEntity",
          "name": "Gene arcA E. coli str. K-12 substr. MG1655 b4401",
          "additionalType": "http://www.ebi.ac.uk/ols/ontologies/so/terms?obo_id=SO:0000704",
          "identifier": "b4401",
          "url": "http://localhost:8080/synbiomine/report.do?id=2026346"
        }
        </script>
        '''

        bs_parser = Parser(config)
        jsonlds = bs_parser.parse_bioschemas_jsonld_from_html(html)
        self.assertEqual(len(jsonlds), 1)

        jsonld = jsonlds[0]
        self.assertEqual(jsonld['name'], 'Gene arcA E. coli str. K-12 substr. MG1655 b4401')
        self.assertEqual(jsonld['additionalType'], 'http://www.ebi.ac.uk/ols/ontologies/so/terms?obo_id=SO:0000704')
        self.assertEqual(jsonld['identifier'], 'b4401')
        self.assertEqual(jsonld['url'], 'http://localhost:8080/synbiomine/report.do?id=2026346')

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

        bs_parser = Parser(config)
        jsonlds = bs_parser.parse_bioschemas_jsonld_from_html(html)
        self.assertEqual(len(jsonlds), 0)

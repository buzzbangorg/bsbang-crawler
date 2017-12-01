import unittest

import bioschemas
from bioschemas.extractors import ExtractorFromHtml

config = bioschemas.DEFAULT_CONFIG


class TestExtractors(unittest.TestCase):
    def test_jsonld_extraction_from_html(self):
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

        e = ExtractorFromHtml(config)
        jsonlds = e._extract_jsonld_from_html(html)
        self.assertEqual(len(jsonlds), 1)

        jsonld = jsonlds[0]
        self.assertEqual(jsonld['name'], 'Gene arcA E. coli str. K-12 substr. MG1655 b4401')
        self.assertEqual(jsonld['additionalType'], 'http://www.ebi.ac.uk/ols/ontologies/so/terms?obo_id=SO:0000704')
        self.assertEqual(jsonld['identifier'], 'b4401')
        self.assertEqual(jsonld['url'], 'http://localhost:8080/synbiomine/report.do?id=2026346')

import logging
import unittest

import bioschemas
import bioschemas.translator

logging.basicConfig(level=logging.DEBUG)


class TestTranslatorMethods(unittest.TestCase):
    def test_translate(self):
        config = {
            'jsonld_to_solr_map': bioschemas.JSONLD_TO_SOLR_MAP,
            'mandatory_properties': bioschemas.MANDATORY_PROPERTIES,
            'schema_inheritance_graph': bioschemas.SCHEMA_INHERITANCE_GRAPH,
            'schemas_to_parse': bioschemas.SCHEMAS_TO_PARSE
        }

        translator = bioschemas.translator.Translator(config)

        jsonld = {
            'context': 'http://bioschemas.org',
            '@type': 'PhysicalEntity',
            'identifier': 'b4401',
            'additionalType': 'http://www.ebi.ac.uk/ols/ontologies/so/terms?obo_id=SO:0000704',
            'name': 'Gene arcA E. coli str. K-12 substr. MG1655 b4401',
            'url': 'http://localhost:8080/synbiomine/report.do?id=2026346'
        }

        solr_json = translator.create_solr_json_with_mandatory_properties(jsonld['@type'], jsonld)
        self.assertEqual(solr_json['name'], 'Gene arcA E. coli str. K-12 substr. MG1655 b4401')
        self.assertEqual(solr_json['AT_type'], 'PhysicalEntity')
        self.assertEqual(solr_json['additionalType'], 'http://www.ebi.ac.uk/ols/ontologies/so/terms?obo_id=SO:0000704')
        self.assertEqual(solr_json['url'], 'http://localhost:8080/synbiomine/report.do?id=2026346')
        self.assertFalse('context' in solr_json)

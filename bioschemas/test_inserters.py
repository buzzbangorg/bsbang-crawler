import logging
import unittest

import bioschemas
import bioschemas.inserters

logging.basicConfig(level=logging.ERROR)


class TestTranslator(unittest.TestCase):
    def test_translate(self):
        config = {
            'jsonld_to_solr_map': {'@type': 'AT_type'},

            'mandatory_properties': {
                'Parent_Type': ['@type', 'parent_prop'],
                'Child_type': ['child_prop']
            },

            'schema_inheritance_graph': {
                'Child_type': 'Parent_Type',
                'Parent_Type': None
            }
        }

        translator = bioschemas.inserters.SolrInserter(config)

        jsonld = {
            '@type': 'Child_type',
            'parent_prop': 'pp_val',
            'child_prop': 'cp_val'
        }

        solr_json = translator.create_solr_json_with_mandatory_properties(jsonld['@type'], jsonld)
        self.assertEqual(solr_json['parent_prop'], 'pp_val')
        self.assertEqual(solr_json['child_prop'], 'cp_val')
        self.assertEqual(solr_json['AT_type'], 'Child_type')

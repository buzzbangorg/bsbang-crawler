import logging
import unittest

import bioschemas
import bioschemas.indexers

logging.basicConfig(level=logging.DEBUG)


class TestIndexers(unittest.TestCase):
    def test_solr_indexer(self):
        config = {
            'jsonld_to_solr_map': {'@type': 'AT_type'},

            'mandatory_properties': {
                'Parent_type': ['@type', 'parent_prop'],
                'Child_type': ['child_prop']
            },

            'optional_properties': {
                'Parent_type': ['optional_parent_prop'],
                'Child_type': ['optional_child_prop']
            },

            'schema_inheritance_graph': {
                'Child_type': 'Parent_type',
                'Parent_type': None
            }
        }

        inserter = bioschemas.indexers.SolrIndexer(config)

        jsonld = {
            '@type': 'Child_type',
            'parent_prop': 'pp_val',
            'child_prop': 'cp_val',
            'optional_parent_prop': 'opp_val',
            'ignored_parent_prop': 'ipp_val',
            'ignored_child_prop': 'icp_val'
        }

        solr_json = inserter._create_solr_json(jsonld['@type'], jsonld)

        self.assertEqual(solr_json['AT_type'], 'Child_type')
        self.assertEqual(solr_json['parent_prop'], 'pp_val')
        self.assertEqual(solr_json['child_prop'], 'cp_val')
        self.assertEqual(solr_json['optional_parent_prop'], 'opp_val')
        self.assertFalse('optional_child_prop' in solr_json)
        self.assertFalse('ignored_parent_prop' in solr_json)
        self.assertFalse('ignored_child_prop' in solr_json)

    def test_solr_indexer_mapped_type(self):
        config = {
            'jsonld_to_solr_map': {'@type': 'AT_type'},
            'mandatory_properties': {'atype': ['@type']},
            'schema_map': {'mappedtype': 'atype'},
            'schema_inheritance_graph': {'atype': None}
        }

        jsonld = {
            '@type': 'mappedtype',
        }

        inserter = bioschemas.indexers.SolrIndexer(config)
        solr_json = inserter._create_solr_json(jsonld['@type'], jsonld)
        self.assertEqual(solr_json['AT_type'], 'atype')

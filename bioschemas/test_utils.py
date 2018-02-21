import logging
import unittest

import bioschemas.utils as bsutils

logging.basicConfig(level=logging.DEBUG)


class TestUtils(unittest.TestCase):
    def test_get_value_from_jsonld_value_simple(self):
        value = bsutils.Utils.get_value_from_jsonld_value('foo')

        self.assertEqual(value, 'foo')

    def test_get_value_from_jsonld_value_object(self):
        value = bsutils.Utils.get_value_from_jsonld_value({'@value': 'foo'})

        self.assertEqual(value, 'foo')

    def test_get_value_from_jsonld_value_object(self):
        value = bsutils.Utils.get_value_from_jsonld_value({})

        self.assertEqual(value, None)

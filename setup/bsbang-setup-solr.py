#!/usr/bin/env python3

import argparse
from lxml import etree
import requests
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# FUNCTIONS
def post_to_solr(json):
    headers = {'Content-type': 'application/json'}

    logger.info('Posting json - [%s]', json)
    r = requests.post(solrSchemaPath, json=json, headers=headers)
    logger.info('Response json - [%s]', r.text)


# MAIN
parser = argparse.ArgumentParser('Setup a Solr schema for Buzzbang')
parser.add_argument('config', help='Config file location, e.g. conf/bsbang-solr-setup.xml')
parser.add_argument('-s', '--solr-core-url', nargs='?', help='Solr core URL to be configured')
args = parser.parse_args()

if args.solr_core_url is None:
    solrPath = 'http://localhost:8983/solr/bsbang/'
else:
    solrPath = str(args.solr_core_url)
    logger.info('Setting up Solr core at %s', args.solr_core_url)

solrSchemaPath = solrPath + 'schema'

configXml = etree.parse(args.config)

for fieldElem in configXml.findall('./field'):
    logger.info(fieldElem.attrib['name'] + ' ' + fieldElem.attrib['type'])
    addFieldConfigJson = {
        'add-field': {
            'name': fieldElem.attrib['name'],
            'type': fieldElem.attrib['type'],
            'multiValued': fieldElem.get('multiValued', default='false')
        }
    }

    post_to_solr(addFieldConfigJson)

    addCopyFieldConfigJson = {
        'add-copy-field': {'source': fieldElem.attrib['name'], 'dest': '_text_'}
    }

    post_to_solr(addCopyFieldConfigJson)

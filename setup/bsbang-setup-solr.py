#!/usr/bin/env python3

import argparse
from lxml import etree
import requests



def post_to_solr(json):
    headers = {'Content-type': 'application/json'}

    # print('posting [%s]' % json)
    r = requests.post(solrSchemaPath, json=json, headers=headers)
    # print('response [%s]' % r.text)


# MAIN
parser = argparse.ArgumentParser('Setup a Solr schema for Buzzbang')
parser.add_argument('config', help='Config file location, e.g. conf/bsbang-solr-setup.xml')
parser.add_argument('--core-name', default=['bsbang'], nargs='*', help='core-name to be configured')
args = parser.parse_args()

solrPath = 'http://localhost:8983/solr/' + str(args.core_name[0]) + '/'
solrSchemaPath = solrPath + 'schema'
print(solrSchemaPath)
configXml = etree.parse(args.config)

for fieldElem in configXml.findall('./field'):
    print(fieldElem.attrib['name'] + ' ' + fieldElem.attrib['type'])
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
    print()
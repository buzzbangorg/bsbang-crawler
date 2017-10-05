#!/usr/bin/env python3

import argparse
from lxml import etree
import requests

solrPath = 'http://localhost:8983/solr/bsbang/'
solrSchemaPath = solrPath + 'schema'

# MAIN
parser = argparse.ArgumentParser('Setup a Solr schema for Buzzbang')
parser.add_argument('config', help='Config file location, e.g. conf/bsbang-solr-setup.xml')
args = parser.parse_args()

configXml = etree.parse(args.config)

for fieldElem in configXml.findall('./field'):
    print(fieldElem.attrib['name'] + ' ' + fieldElem.attrib['type'])
    addFieldConfigJson = {
        'add-field': {'name': fieldElem.attrib['name'], 'type': fieldElem.attrib['type']}
    }

    headers = {'Content-type': 'application/json'}

    r = requests.post(solrSchemaPath, json=addFieldConfigJson, headers=headers)
    print('response [%s]' % r.text)

    addCopyFieldConfigJson = {
        'add-copy-field': {'source': fieldElem.attrib['name'], 'dest': '_text_'}
    }

    r = requests.post(solrSchemaPath, json=addCopyFieldConfigJson, headers=headers)
    print('response [%s]' % r.text)
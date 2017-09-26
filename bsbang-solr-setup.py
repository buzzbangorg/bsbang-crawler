#!/usr/bin/env python3

import requests

solrPath = 'http://localhost:8983/solr/bsbang/'
solrSchemaPath = solrPath + 'schema'

addFieldConfigJson = {
    'add-field': [
        {'name': 'identifier', 'type': 'string'},
        {'name': 'name', 'type': 'text_en'},
        {'name': 'additionalType', 'type': 'string'},
        {'name': 'url', 'type': 'text_en'}
    ]
}

addCopyFieldConfigJson = {
    'add-copy-field': [
        {'source': 'identifier', 'dest': '_text_'},
        {'source': 'name', 'dest': '_text_'},
        {'source': 'additionalType', 'dest': '_text_'},
        {'source': 'url', 'dest': '_text_'},
    ]
}

headers = {'Content-type': 'application/json'}

r = requests.post(solrSchemaPath, json=addFieldConfigJson, headers=headers)
print('response [%s]' % r.text)

r = requests.post(solrSchemaPath, json=addCopyFieldConfigJson, headers=headers)
print('response [%s]' % r.text)

#!/usr/bin/env python3

import json
import requests

solrPath = 'http://localhost:8983/solr/bsbang-dev-core/'
solrSchemaPath = solrPath + 'schema'

idFieldAddJson = {'add-field': {'name': 'bioId', 'type': 'string'}}
headers = {'Content-type': 'application/json'}

r = requests.post(solrSchemaPath, data=json.dumps(idFieldAddJson), headers=headers)
print('response [%s]' % r.text)

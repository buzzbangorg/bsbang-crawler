#!/usr/bin/env python3

import bs4
import json
import requests

solrPath = 'http://localhost:8983/solr'
solrJsonDocUpdatePath = solrPath + '/update/json/doc'

# MAIN
r = requests.get('http://localhost:8080/synbiomine/report.do?id=2026346')
soup = bs4.BeautifulSoup(r.text, 'html.parser')
tags = soup.find_all('script', type='application/ld+json')
print('Found %d ld+json sections' % len(tags))

jsonlds = []

for tag in tags:
    jsonlds.append(json.loads(tag.string))

for jsonld in jsonlds:
    print(jsonld)
    r = requests.post(solrPath, jsonld)

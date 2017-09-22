#!/usr/bin/env python3

import bs4
import requests

r = requests.get('http://localhost:8080/synbiomine/report.do?id=2026346')
soup = bs4.BeautifulSoup(r.text, 'html.parser')
tags = soup.find_all('script', type='application/ld+json')
print('Found %d ld+json sections' % len(tags))
for tag in tags:
    print(tag)

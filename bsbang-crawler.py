#!/usr/bin/env python3

import requests

r = requests.get('http://localhost:8080/synbiomine/report.do?id=2026346')
print(r.text)
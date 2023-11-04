#!/usr/bin/env python
import json

json_file_path = 'webPages.json'  
with open(json_file_path, 'r') as json_file:
    web_pages = json.load(json_file)

for page in web_pages:
    print(page)

#!/usr/bin/env python

import subprocess

def createFileToParse(url, i):
    filename = str(i) + ".html"
    subprocess.run(["curl", "-o", filename, url])

url_array = []
url_array.append("https://www.nrk.no/")
url_array.append("https://www.dn.no/")
url_array.append("https://www.e24.no/")

def createContentFiles(listOfUrls):
    iterator = 1
    for i in listOfUrls:
        createFileToParse(i, iterator)
        iterator += 1

createContentFiles(url_array)
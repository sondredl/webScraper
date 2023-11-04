#!/usr/bin/env python

import subprocess

url_array = []

def createFileToParse(url, i):
    filename = str(i) + ".html"
    path = "htmlFiles/" 
    path += filename
    subprocess.run(["curl", "-o", path, url])

def createContentFiles(listOfUrls):
    subprocess.run(["mkdir", "htmlFiles"])
    iterator = 1
    for i in listOfUrls:
        createFileToParse(i, iterator)
        iterator += 1

url_array.append("https://www.nrk.no/")
url_array.append("https://www.dn.no/")
url_array.append("https://www.e24.no/")

createContentFiles(url_array)
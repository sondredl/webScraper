#!/usr/bin/env python
import jsonParser
import htmlParser

import subprocess
import time

def createFileToParse(name, url):
    filename = name + ".html"
    path = "htmlFiles/" 
    path += filename
    subprocess.run(["curl", "-L", "-o", path, url])

def createContentFiles():
    subprocess.run(["mkdir", "htmlFiles"])
    pageList = jsonParser.webPages()
    for page in pageList:
        createFileToParse(page[0], page[1])


def main():
    createContentFiles()
    htmlParser.updateDatabase()

if __name__ == "__main__":
    main()



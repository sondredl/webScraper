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
    while True:
        createContentFiles()
        htmlParser.updateDatabase()
        htmlParser.WordAndUrl()
        subprocess.run(["rm", "-rf", "htmlFiles/"])
        time.sleep(300)


if __name__ == "__main__":
    main()



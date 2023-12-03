#!/usr/bin/env python

import jsonParser
import htmlParser
import dbCleaner

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

database_path = 'your_database.db'
table_name = 'WordAndUrl'
column_name = 'href'

def main():
    while True:
        createContentFiles()
        htmlParser.updateDatabase()
        htmlParser.getWordAndUrl()
        subprocess.run(["rm", "-rf", "htmlFiles/"])
        time.sleep(3600) # 3 hours sleep
        dbCleaner.remove_duplicates(database_path, table_name, column_name)


if __name__ == "__main__":
    main()



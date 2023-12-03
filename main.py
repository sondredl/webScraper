#!/usr/bin/env python

import jsonParser
import htmlParser
import dbCleaner

import subprocess
import time
import multiprocessing


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
date_column = 'timestamp'  # Replace with the actual date column name

def main():
    while True:
        subprocess.run(["rm", "-rf", "htmlFiles/"])
        createContentFiles()
        htmlParser.updateDatabase()
        htmlParser.getWordAndUrl()
        htmlParser.getCompanyAndUrl()
        subprocess.run(["rm", "-rf", "htmlFiles/"])
        # dbCleaner.remove_duplicates_on_date(database_path, table_name, column_name, date_column)
        # dbCleaner.remove_duplicates_on_date(database_path, table_name, column_name, date_column)
        cleanDuplicates = multiprocessing.Process(target= dbCleaner.remove_duplicates_on_date(database_path, table_name, column_name, date_column))
        cleanDuplicates.start()
        cleanDuplicates.join()
        dbCleaner.reorganize_ids(database_path)
        # dbCleaner.clean_last_update()
        print("sleep for 3 hours")
        time.sleep(3600) # 3 hours sleep


if __name__ == "__main__":
    main()



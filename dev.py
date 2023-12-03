#!/usr/bin/env python

import jsonParser
import htmlParser

import subprocess
import dbCleaner

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


# Call the function to remove duplicates

# Replace 'your_database.db' with the actual path to your SQLite database file
database_path = 'your_database.db'
table_name = 'WordAndUrl'
column_name = 'href'
date_column = 'timestamp'  # Replace with the actual date column name

def main():
    createContentFiles()
    htmlParser.updateDatabase()
    htmlParser.getWordAndUrl()
    # dbCleaner.remove_duplicates(database_path, table_name, column_name)
    dbCleaner.remove_duplicates_on_date(database_path, table_name, column_name, date_column)


if __name__ == "__main__":
    main()



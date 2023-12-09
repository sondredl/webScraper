#!/usr/bin/env python

import sys

print("system path: ")
print(sys.path)
print("end")
import jsonParser
import subprocess
import dbCleaner
import multiprocessing
import download_page
import htmlParser

import sqlite3


def createArticlesTable():
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            subtitle TEXT,
            text TEXT NOT NULL
        )
                """
    )

    conn.commit()
    conn.close()


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


database_path = "your_database.db"
table_name = "WordAndUrl"
column_name = "href"
date_column = "timestamp"


def main():
    createContentFiles()
    htmlParser.updateDatabase()
    htmlParser.getWordAndUrl()
    htmlParser.getCompanyAndUrl()

    cleanDuplicates = multiprocessing.Process(
        target=dbCleaner.remove_duplicates_on_date(
            database_path, table_name, column_name, date_column
        )
    )
    cleanDuplicates.start()
    cleanDuplicates.join()
    print("done cleaning duplicates")

    dbCleaner.reorganize_ids(database_path)
    dbCleaner.clean_last_update()

    createArticlesTable()
    download_page.download_all_article_pages()


if __name__ == "__main__":
    main()

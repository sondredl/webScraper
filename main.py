#!/usr/bin/env python

import subprocess
import sqlite3
import multiprocessing
from src import jsonParser
from src import dbCleaner
from src import download_page
from src import htmlParser
from src import extractArticle
import createMarkdown
import time
from datetime import datetime


def createArticlesTable():
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()

    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
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


def main():
    database_path = "your_database.db"
    table_name = "WordAndUrl"
    column_name = "href"
    date_column = "timestamp"

    last_time_run : str
    last_time_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    while True:
        createContentFiles()
        htmlParser.updateDatabase()
        htmlParser.updateDatabaseCompany()
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

        extractArticle.loop_all_articles()

        # createMarkdown.create_markdown_overview("your_database.db", "articles.md")
        dbCleaner.evaluateArticlesTable(last_time_run)
        createMarkdown.create_markdown_overview("your_database.db", "markdown", last_time_run)
        last_time_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sleep_time = 7200 # seconds
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()

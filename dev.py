#!/usr/bin/env python

import subprocess
import sqlite3
import multiprocessing
from src import jsonParser
from src import dbCleaner
from src import download_page
from src import htmlParser
from src import extractArticle
from datetime import datetime
from src.databaseHandler  import DbHandler


def createArticlesTable():
    conn = sqlite3.connect("temp.db")
    cursor = conn.cursor()

    # create_articles_table(connection)
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sentences_id INTEGER,
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


def compareTimestamps(db_handler):
    conn = sqlite3.connect("temp.db")
    cursor = conn.cursor()

    cursor.execute("SELECT href FROM WordAndUrl")
    urls = cursor.fetchall()

    cursor.execute("SELECT id FROM WordAndUrl")
    ids = cursor.fetchall()

    cursor.execute("SELECT timestamp FROM WordAndUrl")
    timestamp = cursor.fetchall()
    word_and_url_rows = 0
    new_word_and_url_rows = 0
    last_time_run : datetime.datetime

    database_path = 'temp.db'
    table_name = 'WordAndUrl'
    column_name = 'timestamp_int'
    column_type = 'INTEGER'  
    db_handler.add_column_if_not_exists(database_path, table_name, column_name, column_type)

    for row in timestamp:
        # Each row is a tuple, so extract the first element
        word_and_url_rows += 1
        timestamp_str = row[0]
    
        # Now pass the individual timestamp string to getTimeType
        timestamp = db_handler.get_time_type(timestamp_str)
        # print(f"{timestamp} type: {type(timestamp)}")
        # print(f'timestamp: {url} , \nlast_time_run: {url[0]}\n')
        # if timestamp > last_time_run:
        #     # downloadArticlePage(url[0], cursor)
        #     # cursor.execute("INSERT INTO WordAndUrl (local_article_file) VALUES (?)", ("int.html",))
        #     new_word_and_url_rows += 1
        #     # print(f"{row[0]} \n{last_time_run}\n")
    # timestamp = db_handler.getTimeType(timestamp)
    print(f"all rows: {word_and_url_rows}")
    print(f"new rows: {new_word_and_url_rows}")

    # print(f"{last_time_run} type: {type(last_time_run)}\n")

    # if timestamp  > last_time_run:
    #     for url in urls and timestamp > last_time_run:
    #         # downloadArticlePage(url[0], cursor)
    #         # cursor.execute("INSERT INTO WordAndUrl (local_article_file) VALUES (?)", ("int.html",))
    #         # print(f'timestamp: {url} , \nlast_time_run: {url[0]}\n')
    #         iterator += 1
    conn.close()

def main():
    db_handler = DbHandler()
    compareTimestamps(db_handler)
    # database_path = "your_database.db"
    # table_name = "WordAndUrl"
    # column_name = "href"
    # date_column = "timestamp"

    # articlesTable_name = "Articles"
    # title_column_name = "title"

    #createContentFiles()
    #htmlParser.updateDatabase()
    #htmlParser.updateDatabaseCompany()
    #htmlParser.getWordAndUrl()
    #htmlParser.getCompanyAndUrl()

    # cleanDuplicates = multiprocessing.Process(
    #     target=dbCleaner.remove_duplicates_on_date(
    #         database_path, table_name, column_name, date_column
    #     )
    # )
    # cleanDuplicates.start()
    # cleanDuplicates.join()

    # cleanDuplicateArticles = multiprocessing.Process(
    #     target=dbCleaner.remove_duplicates_on_date(
    #         database_path, articlesTable_name, title_column_name, date_column
    #     )
    # )
    # cleanDuplicateArticles.start()
    # cleanDuplicateArticles.join()
    # print("done cleaning duplicates")

    # dbCleaner.reorganize_ids(database_path)
    # dbCleaner.clean_last_update()

    # createArticlesTable()
    # download_page.download_all_article_pages()

    # extractArticle.loop_all_articles()

    # last_time_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # createMarkdown.create_markdown_overview("your_database.db", "markdown", last_time_run)
    # dbCleaner.evaluateArticlesTable(last_time_run)


if __name__ == "__main__":
    main()

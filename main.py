
import multiprocessing
from src import dbCleaner
from src import download_page
from src import htmlParser
from src import extractArticle
from src import databaseHandler
from src import contentCreator
import createMarkdown
import time
from datetime import datetime

table_name = "WordAndUrl"
column_name = "href"
date_column = "timestamp"

articlesTable_name = "Articles"
title_column_name = "title"

def main():


    while True:
        contentCreator.createContentFiles()

        htmlParser.updateDatabase()
        htmlParser.updateDatabaseCompany()
        htmlParser.getWordAndUrl()
        htmlParser.getCompanyAndUrl()

        databaseHandler.cleanDuplicatesh("WordAndUrlh", "href",  "timestamp")
        databaseHandler.cleanDuplicatesh("Articles",    "title", "timestamp")
        
        dbCleaner.reorganize_ids(databaseHandler.database_path)
        dbCleaner.clean_last_update()

        databaseHandler.createArticlesTable()
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

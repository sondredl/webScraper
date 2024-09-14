
from src import dbCleaner
from src import download_page
from src import htmlParser
from src import extractArticle
from src.databaseHandler  import DbHandler
from src import contentCreator
import createMarkdown
import time
# from datetime import datetime

table_name = "WordAndUrl"
column_name = "href"
date_column = "timestamp"

articlesTable_name = "Articles"
title_column_name = "title"

def main():

    db_handler = DbHandler()
    db_handler.set_last_time_run()

    while True:

        contentCreator.createContentFiles()

        db_handler.createArticlesTable()
        db_handler.createSentencesTable()
        db_handler.createWordAndUrlTable()

        htmlParser.updateDatabase()
        htmlParser.updateDatabaseCompany()
        htmlParser.getWordAndUrl()
        htmlParser.getCompanyAndUrl()

        db_handler.cleanDuplicates("WordAndUrl", "href",  "timestamp")
        db_handler.cleanDuplicates("Articles",    "title", "timestamp")
        
        dbCleaner.reorganize_ids(db_handler.database_path)
        db_handler.clean_last_update()

        download_page.download_all_article_pages(db_handler)

        extractArticle.loop_all_articles()

        dbCleaner.evaluateArticlesTable(db_handler.get_last_time_run())
        last_run_int = db_handler.get_last_time_run_int()
        date_time = db_handler.get_last_time_run()
        createMarkdown.create_markdown_overview("your_database.db", "markdown", date_time, last_run_int)

        db_handler.set_last_time_run()
        sleep_time = 7200 # seconds
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()

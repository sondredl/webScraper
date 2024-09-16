import os
import shutil
from src import dbCleaner
from src import download_page
from src import htmlParser
from src import extractArticle
from src.databaseHandler  import DbHandler
from src import contentCreator
from src.dataExtractor import dataExtractor
import createMarkdown
import time
# from datetime import datetime

table_name = "WordAndUrl"
column_name = "href"
date_column = "timestamp"

articlesTable_name = "Articles"
title_column_name = "title"

def delete_folder_contents(folder_path):
    # Check if the folder exists
    if os.path.exists(folder_path):
        # Loop through each item in the directory
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            # Check if it is a file or directory
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # Remove the file or symlink
                print(f"File {file_path} deleted.")
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)  # Remove the directory and all its contents
                print(f"Directory {file_path} deleted.")
    else:
        print(f"The folder {folder_path} does not exist.")


def main():

    db_handler = DbHandler()
    data_Extractor = dataExtractor()

    db_handler.set_last_time_run()

    while True:

        contentCreator.createContentFiles()

        db_handler.createArticlesTable()
        db_handler.createSentencesTable()
        db_handler.createWordAndUrlTable()

        # htmlParser.updateDatabase()
        # htmlParser.updateDatabaseCompany()
        # htmlParser.getWordAndUrl()
        # htmlParser.getCompanyAndUrl()
        # data_Extractor.updateDatabase()
        data_Extractor.updateDatabaseCompany()
        # data_Extractor.getWordAndUrl()
        data_Extractor.getCompanyAndUrl()
        

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

        delete_folder_contents("articles")
        delete_folder_contents("htmlFiles")
        db_handler.set_last_time_run()
        sleep_time = 7200 # seconds
        time.sleep(sleep_time)

if __name__ == "__main__":
    main()

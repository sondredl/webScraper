#!/usr/bin/env python

from src import jsonParser
from src import dbCleaner
from src import download_page
from src import htmlParser
from src import extractArticle
from datetime import datetime
from src import articleEvaluation


database_path = "your_database.db"

def main():

    dbCleaner.reorganize_ids(database_path)
    dbCleaner.clean_last_update()
    last_time_run = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    # dbCleaner.evaluateArticlesTable(last_time_run)

    articleEvaluation.evaluateArticles(database_path)


if __name__ == "__main__":
    main()

#!/usr/bin/env python

import sqlite3
from datetime import datetime

class DatabaseHandler:

    def __ini__():
        self.last_time_run = datetime.min
        self.database_path = "database.db"

    def createArticlesTable():
        conn = sqlite3.connect(__database_path)
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

    def set_last_time_run(newest_run_time):
        self.last_time_run = getTimeType(newest_run_time)

    def get_last_time_run():
        return datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # Convert the strings to datetime objects using strptime
    
    def getTimeType(time_str : str):
        return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')

    # def cleanDuplicates(database, table, column1, column2):
    def cleanDuplicates(table, column1, column2):
        cleanDuplicates = multiprocessing.Process(
            target=dbCleaner.remove_duplicates_on_date(
                this.database_path, table, column1, column2
            )
        )
        cleanDuplicates.start()
        cleanDuplicates.join()
        print(f"removed duplicates in {table}")

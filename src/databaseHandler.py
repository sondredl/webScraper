#!/usr/bin/env python

import sqlite3
from datetime import datetime
import multiprocessing
from src import dbCleaner
import time

class DbHandler:

    def __init__(self):
        self.last_time_run = datetime.min
        self.last_time_run_int : int
        self.last_time_run_int = int(time.time())
        self.database_path = "your_database.db"
    
    def createDatabaseTables(self):
        self.create_database_if_not_exists(self.database_path)

        self.create_articles_table()
        self.create_sentences_table()
        self.create_word_and_url_table()
        self.create_last_checked_table()

    def create_sentences_table(self):
        tableName = "Sentences"

        column_0 = "id"
        primary_key = "INTEGER PRIMARY KEY AUTOINCREMENT"

        column_1 = "filename"
        column_2 = "pagename"
        column_3 = "tag_name"
        column_4 = "sentence"
        column_5 = "href"
        column_6 = "timestamp"
        column_7 = "timestamp_int"

        integer_type = "INTEGER"
        text_type = "TEXT"

        self.add_table_if_not_exists(self.database_path, tableName, column_0, primary_key)

        self.add_column_if_not_exists(self.database_path, tableName, column_1, text_type)
        self.add_column_if_not_exists(self.database_path, tableName, column_2, text_type)
        self.add_column_if_not_exists(self.database_path, tableName, column_3, text_type)
        self.add_column_if_not_exists(self.database_path, tableName, column_4, text_type)
        self.add_column_if_not_exists(self.database_path, tableName, column_5, text_type)
        self.add_column_if_not_exists(self.database_path, tableName, column_6, text_type)
        self.add_column_if_not_exists(self.database_path, tableName, column_7, integer_type)
    def create_articles_table(self):
        table_name = "Articles"

        column_0 = "id"
        primary_key = "INTEGER PRIMARY KEY AUTOINCREMENT"

        column_1 = "timestamp"
        column_2 = "timestamp_int"
        column_3 = "title"
        column_4 = "subtitle"
        column_5 = "content"
        column_6 = "search_words"

        integer_type = "INTEGER"
        text_type = "TEXT"
        text_type_not_null = "TEXT NOT NULL"

        self.add_table_if_not_exists(self.database_path, table_name, column_0, primary_key)

        self.add_column_if_not_exists(self.database_path, table_name, column_1, text_type)
        self.add_column_if_not_exists(self.database_path, table_name, column_2, integer_type)
        self.add_column_if_not_exists(self.database_path, table_name, column_3, text_type_not_null)
        self.add_column_if_not_exists(self.database_path, table_name, column_4, text_type)
        self.add_column_if_not_exists(self.database_path, table_name, column_5, text_type_not_null)
        self.add_column_if_not_exists(self.database_path, table_name, column_6, text_type)
    def create_last_checked_table(self):
        connection = sqlite3.connect(self.database_path)
        cursor = connection.cursor()
        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS LastCheckedEntry (
                id INTEGER PRIMARY KEY,
                table_name TEXT,
                last_entry_id INTEGER,
                last_checked_timestamp DATETIME
            )
        """
        )
        connection.commit()
    def create_word_and_url_table(self):
        conn = sqlite3.connect("your_database.db")
        cursor = conn.cursor()

        cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS WordAndUrl
                (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    local_article_file TEXT,
                    pagename TEXT,
                    tag_name TEXT,
                    search_word TEXT,
                    href TEXT,
                    timestamp TEXT,
                    timestamp_int INTEGER)
            """
    )
        conn.commit()
        conn.close()

    def set_last_time_run(self):
        newest_run_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.last_time_run = self.get_time_type(newest_run_time)
    def set_last_time_run_int(self):
        self.last_time_run_int = int(time.time())

    def get_highest_id(self, database_path, table_name="WordAndUrl"):
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        try:
            cursor.execute(f"SELECT MAX(id) FROM {table_name}")
            result = cursor.fetchone()

            return result[0] if result[0] is not None else None

        except sqlite3.Error as e:
            print(f"Error: {e}")
            return None

        finally:
            connection.close()
    def get_last_time_run(self):
        return self.last_time_run
    def get_last_time_run_int(self):
        return self.last_time_run_int
    def get_time_type(self, time_str):
        return datetime.strptime(time_str, '%Y-%m-%d %H:%M:%S')
    def get_current_time(self):
        return datetime.strptime('%Y-%m-%d %H:%M:%S')

    def cleanDuplicates(self, table, column1, column2):
        _cleanDuplicates = multiprocessing.Process(
            target=self.remove_duplicates_on_date(
                self.database_path, table, column1, column2
            )
        )
        _cleanDuplicates.start()
        _cleanDuplicates.join()
        print(f"removed duplicates in {table}")
    def remove_duplicates_on_date(self, database_path, table_name, column_name, date_column):
        last_entry_id = self.get_highest_id(database_path)
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        try:
            cursor.execute(
                f"""SELECT {column_name}, date({date_column}), 
                COUNT(*) FROM {table_name} 
                WHERE id > ? 
                GROUP BY {column_name}, date({date_column}) 
                HAVING COUNT(*) > 1""",
                (last_entry_id,),
            )
            duplicates = cursor.fetchall()

            for duplicate in duplicates:
                href_value, date_value, count = duplicate
                print(
                    f"Removing duplicates for {column_name}: {href_value} on {date_value}, {count} rows removed."
                )

            cursor.execute(
                f"CREATE TABLE temp_table AS SELECT * FROM {table_name} WHERE id <= ? GROUP BY {column_name}, date({date_column})",
                (last_entry_id,),
            )
            cursor.execute(f"DROP TABLE {table_name}")
            cursor.execute(f"ALTER TABLE temp_table RENAME TO {table_name}")
            connection.commit()

            print(
                f"Duplicates removed successfully from {column_name} column in {table_name} table after id {last_entry_id}."
            )
        except Exception as e:
            print(f"Error: {e}")
            connection.rollback()
        finally:
            connection.close()
    def clean_last_update(self):
        database_path = "your_database.db"
        table_name = "WordAndUrl"

        connection = sqlite3.connect(database_path)

        self.insert_initial_record(connection, table_name)

        last_entry_id_checked = self.get_highest_id(database_path)

        self.update_last_checked_record(connection, table_name, last_entry_id_checked)

        connection.close()

        if last_entry_id_checked is not None:
            print(f"The highest id in the WordAndUrl table is: {last_entry_id_checked}")
        else:
            print("Failed to retrieve the highest id.")
    def insert_initial_record(self, connection, table_name):
        cursor = connection.cursor()
        cursor.execute(
            """
            INSERT INTO LastCheckedEntry (table_name, last_entry_id, last_checked_timestamp)
            VALUES (?, 0, ?)
        """,
            (table_name, datetime.now()),
        )
        connection.commit()
    def update_last_checked_record(self, connection, table_name, last_entry_id):
        cursor = connection.cursor()
        cursor.execute(
            """
            UPDATE LastCheckedEntry
            SET last_entry_id = ?, last_checked_timestamp = ?
            WHERE id = (SELECT id FROM LastCheckedEntry WHERE table_name = ? ORDER BY last_checked_timestamp DESC LIMIT 1)
        """,
            (last_entry_id, datetime.now(), table_name),
        )
        connection.commit()

    def create_database_if_not_exists(self, database_path):
        # Connect to the database (this will create the database if it doesn't exist)
        conn = sqlite3.connect(database_path)
        print(f"Database '{database_path}' has been created or already exists.")
        
        # Close the connection
        conn.close()
    def add_table_if_not_exists(self, database_path, table_name, column_0, primary_key):
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}';")

        if not cursor.fetchone():
            cursor.execute(f''' CREATE TABLE {table_name} ( {column_0} {primary_key}); ''')
            print(f"Table '{table_name}' created.")
        else:
            print(f"Table '{table_name}' already exists.")

        conn.commit()
        conn.close()
    def add_column_if_not_exists(self, database_path, table_name, column_name, column_type):
        conn = sqlite3.connect(database_path)
        cursor = conn.cursor()

        # Ensure table exists
        cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if cursor.fetchone() is None:
            print(f"Table '{table_name}' does not exist.")
            return

        # Check if the column exists using PRAGMA table_info
        cursor.execute(f"PRAGMA table_info({table_name})")
        columns_info = cursor.fetchall()

        # Extract the existing column names
        existing_columns = [column[1] for column in columns_info]  # Column names are in the second index

        # Check if the column exists
        if column_name not in existing_columns:
            # Column does not exist, so add it
            try:
                cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} {column_type}")
                print(f"Column '{column_name}' added to table '{table_name}'.")
            except sqlite3.OperationalError as e:
                print(f"Error adding column '{column_name}': {e}")
        else:
            print(f"Column '{column_name}' already exists in table '{table_name}'.")

        conn.commit()
        conn.close()

#!/usr/bin/env python

import jsonParser
import htmlParser

import subprocess
import sqlite3

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

def remove_duplicates(database_path, table_name, column_name):
    # Connect to the SQLite database
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    try:
        # Create a temporary table with distinct values
        cursor.execute(f"CREATE TABLE temp_table AS SELECT DISTINCT * FROM {table_name}")

        # Drop the original table
        cursor.execute(f"DROP TABLE {table_name}")

        # Rename the temporary table to the original table name
        cursor.execute(f"ALTER TABLE temp_table RENAME TO {table_name}")

        # Commit the changes
        connection.commit()

        print(f"Duplicates removed successfully from {column_name} column in {table_name} table.")
    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        # Close the connection
        connection.close()

# Replace 'your_database.db' with the actual path to your SQLite database file
database_path = 'your_database.db'
table_name = 'WordAndUrl'
column_name = 'href'

# Call the function to remove duplicates


def main():
    createContentFiles()
    htmlParser.updateDatabase()
    htmlParser.getWordAndUrl()
    remove_duplicates(database_path, table_name, column_name)


if __name__ == "__main__":
    main()



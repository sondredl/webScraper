#!/usr/bin/env python

import jsonParser
import subprocess
import os
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

def updateDatabase():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Sentences
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT,
                    tag_name TEXT,
                    sentence TEXT,
                    href TEXT,
                    timestamp TEXT)''')

    folder_path = "htmlFiles/"

    selected_words = jsonParser.searchWords()
    html_tags = jsonParser.htmlTags()
    previousInsertion = ""
    previousHrefLink = ""

    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')

            for tag_name in html_tags:
                for tag in soup.find_all(tag_name):
                    content = tag.text
                    if any(word in content for word in selected_words):
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        link_tag = tag.find_parent('a')
                        if link_tag:
                            href_link = link_tag.get('href')
                        if (href_link == previousHrefLink):
                            href_link = "" 
                        else:
                            previousHrefLink = href_link

                        if not (content == previousInsertion):
                            cursor.execute("INSERT INTO Sentences (filename, tag_name, sentence, href, timestamp) VALUES (?, ?, ?, ?, ?)", 
                                                                    (filename, tag_name, content, href_link, timestamp))
                            previousInsertion = content

                            


    conn.commit()
    conn.close()

def createNewColumn(cursor, table_name, column_name):
    # table_name = 'Sentences'
    # new_column_name = 'new_column'
    if not doesColumnExist(cursor, table_name, column_name):
        # Step 3: If the column doesn't exist, add it
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} TEXT")
        print(f"The column {column_name} has been added.")
        return
    print("FAILED TO ADD COLUMN TO TABLE")

def doesColumnExist(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    
    columns = cursor.fetchall()
    # print(column_name, " in ", table_name, "DOES NOT EXIST")
    
    return any(column[1] == column_name for column in columns)

updateDatabase()
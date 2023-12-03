#!/usr/bin/env python

import jsonParser
import json
import subprocess
import os
from bs4 import BeautifulSoup
import sqlite3
from datetime import datetime

def getWordAndUrl():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS WordAndUrl
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pagename TEXT,
                    tag_name TEXT,
                    search_word,
                    href TEXT,
                    timestamp TEXT)''')

    with open('inputData/searchWords.json') as json_file:
        search_words = json.load(json_file)

    for search_word in search_words:
        cursor.execute('''SELECT filename, tag_name, sentence, href, timestamp
                        FROM Sentences
                        WHERE sentence LIKE ?''', ('%' + search_word + '%',))

        matching_rows = cursor.fetchall()

        for row in matching_rows:
            pagename, tag_name, search_word, href, timestamp = row
            cursor.execute('''INSERT INTO WordAndUrl (pagename, tag_name, search_word, href, timestamp)
                            VALUES (?, ?, ?, ?, ?)''', (pagename, tag_name, search_word, href, timestamp))
    
    conn.commit()
    conn.close()

def getCompanyAndUrl():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS WordAndUrl
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pagename TEXT,
                    tag_name TEXT,
                    search_word,
                    href TEXT,
                    timestamp TEXT)''')

    with open('inputData/companies.json') as json_file:
        search_words = json.load(json_file)

    for search_word in search_words:
        cursor.execute('''SELECT filename, tag_name, sentence, href, timestamp
                        FROM Sentences
                        WHERE sentence LIKE ?''', ('%' + search_word + '%',))

        matching_rows = cursor.fetchall()

        for row in matching_rows:
            pagename, tag_name, search_word, href, timestamp = row
            cursor.execute('''INSERT INTO WordAndUrl (pagename, tag_name, search_word, href, timestamp)
                            VALUES (?, ?, ?, ?, ?)''', (pagename, tag_name, search_word, href, timestamp))
    
    conn.commit()
    conn.close()


def updateDatabase():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS Sentences
                    (id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT,
                    pagename TEXT,
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

                        link_tag = tag.find_parent('a')
                        if link_tag:
                            href_link = link_tag.get('href')
                            dot_index = filename.find(".")
                            pageName = filename[:dot_index]
                            if not href_link.startswith("https"):
                                href_link = getUrl(pageName, link_tag.get('href'))

                        if (href_link == previousHrefLink):
                            href_link = "" 
                        else:
                            previousHrefLink = href_link
                        
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        

                        if not (content == previousInsertion) and href_link != "":
                            cursor.execute("INSERT INTO Sentences (filename, tag_name, sentence, href, timestamp) VALUES (?, ?, ?, ?, ?)", 
                                                                    (filename, tag_name, content, href_link, timestamp))
                            previousInsertion = content

    conn.commit()
    conn.close()


def createNewColumn(cursor, table_name, column_name):
    if not doesColumnExist(cursor, table_name, column_name):
        cursor.execute(f"ALTER TABLE {table_name} ADD COLUMN {column_name} TEXT")
        print(f"The column {column_name} has been added.")
        return
    print("FAILED TO ADD COLUMN TO TABLE")

def doesColumnExist(cursor, table_name, column_name):
    cursor.execute(f"PRAGMA table_info({table_name})")
    
    columns = cursor.fetchall()
    
    return any(column[1] == column_name for column in columns)

def fixHrfLinks():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    tableName = 'Sentences'
    cursor.execute(f"select * from {tableName}")
    rows = cursor.fetchall()

    web_pages = jsonParser.webPages()
    web_pages += jsonParser.companyNames()

    for row in rows:
        if not row[4].startswith("https"):
            for page in web_pages:
                href_link = page[1] + row[4]
                cursor.execute("INSERT INTO Sentences ( href) VALUES ( ?)", (href_link))

    conn.commit()
    conn.close()

def getUrl(pageName, href):
    web_pages = jsonParser.webPages()

    if not href.startswith("https"):
        for page in web_pages:
            if (pageName == page[0]):
                href_link = page[1] + href
                return href_link
    else:
        return


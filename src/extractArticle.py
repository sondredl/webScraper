#!/usr/bin/env python

import os
import sqlite3
from bs4 import BeautifulSoup
from datetime import datetime


def create_articles_table(connection):
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sentences_id INTEGER,
            timestamp TEXT,
            timestamp TEXT,
            title TEXT,
            subtitle TEXT,
            text TEXT
        )
    """
    )
    connection.commit()

def insert_article(connection, title, subtitle, text):
    cursor = connection.cursor()
    # sentences_id = 42
        # sentences_id, timestamp, title, subtitle, text = row
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        """
        INSERT INTO articles (
            timestamp,
            title, 
            subtitle, 
            text)
        VALUES (?, ?, ?, ?)
    """,
        ( timestamp, title, subtitle, text),
    )
    connection.commit()


def loop_all_articles():
    # directory_path = "../articles/"
    directory_path = "articles/"

    # db_path = "../your_database.db"
    db_path = "your_database.db"
    connection = sqlite3.connect(db_path)

    create_articles_table(connection)

    file_list = os.listdir(directory_path)

    for file_name in file_list:
        file_name_path = os.path.join(directory_path, file_name)
        get_article_from_file(file_name_path, connection)

    connection.close()


def get_article_from_file(filename, connection):
    with open(filename, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    title_tag = soup.title
    subtitle_tag = soup.find(["h2", "h3", "h4", "h5", "h6", "p"])

    title = title_tag.text.strip() if title_tag else "No Title Found"
    subtitle = subtitle_tag.text.strip() if subtitle_tag else "No Subtitle Found"

    text = "\n".join([p.text.strip() for p in soup.find_all("p")])

    insert_article(connection, title, subtitle, text)

    print(f"Article '{title}' inserted into the database.")


# loop_all_articles()

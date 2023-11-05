#!/usr/bin/env python

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
                    timestamp TEXT)''')

    folder_path = "htmlFiles/"

    for filename in os.listdir(folder_path):
        if filename.endswith('.html'):
            file_path = os.path.join(folder_path, filename)

            # Step 4: Parse HTML file
            with open(file_path, 'r', encoding='utf-8') as file:
                soup = BeautifulSoup(file, 'html.parser')

            selected_words = ['konflikt', 'krig', 'topp', 'seafood', 'euronext', 'performers']

            for tag_name in ['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6']:
                for tag in soup.find_all(tag_name):
                    content = tag.text
                    if any(word in content for word in selected_words):
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        cursor.execute("INSERT INTO Sentences (filename, tag_name, sentence, timestamp) VALUES (?, ?, ?, ?)",
                                    (filename, tag_name, content, timestamp))

    conn.commit()
    conn.close()

# subprocess.run(["rm -rf", "htmlFiles"])

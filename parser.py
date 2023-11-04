#!/usr/bin/env python

import os
from bs4 import BeautifulSoup
import sqlite3

# Step 1: Connect to SQLite database
conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Adjust the table structure based on your needs
cursor.execute('''CREATE TABLE IF NOT EXISTS Sentences
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, sentence TEXT)''')

# Step 2: Specify the folder containing HTML files
folder_path = "htmlFiles/"

# Step 3: Loop through HTML files in the folder
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
                    # Step 6: Store in SQLite Database
                    cursor.execute("INSERT INTO Sentences (sentence) VALUES (?)", (content,))

# Step 7: Commit changes and close the connection
conn.commit()
conn.close()

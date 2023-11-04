#!/usr/bin/env python

import os
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

folder_path = "htmlFiles/"

for filename in os.listdir(folder_path):
      if filename.endswith('.html'):
        # print(filename)
        file_path = os.path.join(folder_path, filename)

        # Step 4: Parse HTML file
        with open(file_path, 'r', encoding='utf-8') as file:
            soup = BeautifulSoup(file, 'html.parser')

        selected_words = ['konflikt', 'krig', 'topp', 'seafood', 'euronext', 'performers']

        for tag in soup.select('tbody, div, h1, h2, h3, p, tbody, td, kur-newsfeed, a'):
            sentences = tag.text.split('.')
            selected_sentences = [sentence.strip() for sentence in sentences if any(word in sentence for word in selected_words)]

        cursor.execute('''CREATE TABLE IF NOT EXISTS Sentences
                        (id INTEGER PRIMARY KEY AUTOINCREMENT, sentence TEXT)''')

        for sentence in selected_sentences:
            cursor.execute("INSERT INTO Sentences (sentence) VALUES (?)", (sentence,))

conn.commit()
conn.close()

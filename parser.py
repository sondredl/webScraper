#!/usr/bin/env python

from bs4 import BeautifulSoup
import sqlite3

# with open('1.html', 'r', encoding='utf-8') as file:
with open('htmlFiles/2.html', 'r', encoding='utf-8') as file:
    soup = BeautifulSoup(file, 'html.parser')

selected_words = ['konflikt', 'krig', 'topp', 'seafood']

# for paragraph in soup.find_all('tbody, h1, h2, h3, p, tbody, td, kur-newsfeed'):  # Adjust the tag based on your HTML structure
for paragraph in soup.find_all('tbody, h1, h2, h3, p, tbody, td, tr, kur-newsfeed'):  # Adjust the tag based on your HTML structure
    sentences = paragraph.text.split('.')
    selected_sentences = [sentence.strip() for sentence in sentences if any(word in sentence for word in selected_words)]
# for paragraph in soup.find_all('div'):  # Adjust the tag based on your HTML structure
#     sentences = paragraph.text.split('.')
#     selected_sentences = [sentence.strip() for sentence in sentences if any(word in sentence for word in selected_words)]
# for paragraph in soup.find_all('span'):  # Adjust the tag based on your HTML structure
#     sentences = paragraph.text.split('.')
#     selected_sentences = [sentence.strip() for sentence in sentences if any(word in sentence for word in selected_words)]


conn = sqlite3.connect('your_database.db')
cursor = conn.cursor()

# Adjust the table structure based on your needs
cursor.execute('''CREATE TABLE IF NOT EXISTS Sentences
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, sentence TEXT)''')

for sentence in selected_sentences:
    cursor.execute("INSERT INTO Sentences (sentence) VALUES (?)", (sentence,))

conn.commit()
conn.close()

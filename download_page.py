#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import sqlite3

def downloadArticlePage(url):
    path = "articles/"
    output_file = path + url

    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        print(f"Webpage content saved to {output_file}")
    else:
        print(f"Failed to retrieve webpage. Status code: {response.status_code}")


def download_all_article_pages():
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    try:
        cursor.execute('SELECT href FROM WordAndUrl')
        urls = cursor.fetchall()

        for url in urls:
            downloadArticlePage(url[0])  

    except Exception as e:
        print(f"Error: {e}")

    finally:
        conn.close()

download_all_article_pages()

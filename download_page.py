#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import sqlite3


def downloadArticlePage(url):
    path = "articles/"
    output_file = path + str(increment_counter()) + ".html"

    response = requests.get(url)
    print(response)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        with open(output_file, "w", encoding="utf-8") as file:
            file.write(str(soup))

        print(f"Webpage content saved to {output_file}")
    else:
        print(f"Failed to retrieve webpage. Status code: {response.status_code}")


def download_all_article_pages():
    conn = sqlite3.connect("your_database.db")
    cursor = conn.cursor()

    # try:
    cursor.execute("SELECT href FROM WordAndUrl")
    urls = cursor.fetchall()

    cursor.execute("SELECT id FROM WordAndUrl")
    ids = cursor.fetchall()

    for url in urls:
        downloadArticlePage(url[0])

    conn.close()


def increment_counter(counter=[0]):
    counter[0] += 1
    return counter[0]


download_all_article_pages()

#!/usr/bin/env python

import requests
from bs4 import BeautifulSoup
import sqlite3

def downloadArticlePage(url):
    path = "articles/"
    output_file = path + url

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page
        soup = BeautifulSoup(response.text, 'html.parser')

        # Save the HTML content to a file
        with open(output_file, 'w', encoding='utf-8') as file:
            file.write(str(soup))

        print(f"Webpage content saved to {output_file}")
    else:
        print(f"Failed to retrieve webpage. Status code: {response.status_code}")


# url = "https://www.finansavisen.no/energi/2023/12/02/8066756/exxonmobil-pa-klimatoppmote-fokusert-for-mye-pa-fornybar-energi"
# downloadArticlePage(url)

def download_all_article_pages():
    # Connect to the database
    conn = sqlite3.connect('your_database.db')
    cursor = conn.cursor()

    try:
        # Select all URLs from the WordAndUrl table
        cursor.execute('SELECT href FROM WordAndUrl')
        urls = cursor.fetchall()

        # ids.execute('SELECT id FROM WordAndUrl')
        # ids = cursor.fetchall()

        # Loop through the URLs and call downloadArticlePage function
        for url in urls:
            downloadArticlePage(url[0])  # Assuming that the URL is in the first column (index 0)

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the connection
        conn.close()

# Replace this function with your actual download implementation
# def downloadArticlePage(url):
#     print(f"Downloading article page from URL: {url}")

# Call the function to download all article pages
download_all_article_pages()

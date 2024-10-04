#!/usr/bin/env python

import json
from src.jsonParser         import JsonParser
import sqlite3
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

# Sample word list
word_list = ['python', 'data', 'analysis', 'science', 'machine']

# Step 1: Connect to SQLite database and fetch articles
def get_articles_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Assuming your articles are stored in a table called 'articles' with a 'content' column
    cursor.execute("SELECT content FROM Articles")
    articles = cursor.fetchall()
    
    conn.close()
    
    # Flatten the list of tuples into a list of strings
    return [article[0] for article in articles]

# Step 2: Count occurrences of each word in the articles
def count_word_occurrences(word_list, articles):
    word_count = Counter()
    
    for article in articles:
        # Split article into words and count occurrences
        words = article.lower().split()  # Simple tokenization, can be improved with nltk or other libraries
        word_count.update([word for word in words if word in word_list])
    
    return word_count

# Step 3: Plot the occurrences of words
def plot_word_occurrences(word_count):
    words, counts = zip(*word_count.items())
    
    plt.figure(figsize=(10, 6))
    plt.bar(words, counts, color='blue')
    plt.xlabel('Words')
    plt.ylabel('Occurrences')
    plt.title('Occurrences of Words in Articles')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("occurances.svg")
    # plt.show()


def print_unique_company_names(db_name, table_name, column_name):
    # Connect to the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    # Query to get unique company names
    cursor.execute(f"""SELECT DISTINCT {column_name} 
                   FROM {table_name}""")  # Replace 'your_table_name' with the actual table name

    # Fetch all unique values
    unique_companies = cursor.fetchall()

    # Print each unique company name
    for company in unique_companies:
        print(company[0])

    # Close the connection
    conn.close()

# Usage

# Main function
def main():
    db_path = 'temp.db'  # Change this to your actual database path
    articles = get_articles_from_db(db_path)
    
    with open("inputData/companies.json") as json_file:
        search_words = json.load(json_file)
    word_count = count_word_occurrences(search_words, articles)
    
    # Plot the results
    plot_word_occurrences(word_count)
    print_unique_company_names('temp.db', 'Stock_index', 'company_name')

if __name__ == "__main__":
    main()

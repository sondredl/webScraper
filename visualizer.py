#!/usr/bin/env python

import json
from src.jsonParser         import JsonParser
import sqlite3
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt


def get_articles_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Assuming your articles are stored in a table called 'articles' with a 'content' column
    cursor.execute("SELECT content FROM Articles")
    articles = cursor.fetchall()
    
    conn.close()
    
    # Flatten the list of tuples into a list of strings
    return [article[0] for article in articles]

def count_word_occurrences(word_list, articles):
    word_count = Counter()
    
    for article in articles:
        # Split article into words and count occurrences
        words = article.lower().split()  # Simple tokenization, can be improved with nltk or other libraries
        word_count.update([word for word in words if word in word_list])
    
    return word_count

# Step 3: Plot the occurrences of words
def plot_word_occurrences(word_count : dict) -> dict: 
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
    return words

def plot_word_correlations(word_count : dict, company_names: dict):
    # Convert company names to lowercase
    if isinstance(word_count, dict):
        # Extract words and counts from the dictionary
        words, counts = zip(*word_count.items())
    # elif isinstance(word_count, tuple):
        # If word_count is already a tuple, assign it directly (e.g., if the input was (words, counts))
        # words, counts = word_count
    else:
        raise TypeError("word_count should be either a dictionary or a tuple of (words, counts)")
    
    company_names = [company.lower() for company in company_names]
    
    # Separate the words and counts
    words, counts = zip(*word_count.items())
    
    # Convert words to lowercase
    # words_lower = words
    # words_lower = word_count
    words_lower = [word.lower() for word in words]
    
    # Create the bar plot
    plt.figure(figsize=(12, 7))
    
    # Color the bars differently if the word is a company name
    bar_colors = ['red' if word in company_names else 'blue' for word in words_lower]
    
    plt.bar(words, counts, color=bar_colors)
    
    plt.xlabel('Words')
    plt.ylabel('Occurrences')
    plt.title('Occurrences of Words in Articles')
    plt.xticks(rotation=45)
    
    # Adding a legend to distinguish company names from other words
    red_patch = plt.Line2D([0], [0], color='red', lw=4, label='Company Name')
    blue_patch = plt.Line2D([0], [0], color='blue', lw=4, label='Other Words')
    plt.legend(handles=[red_patch, blue_patch])
    
    plt.tight_layout()
    plt.savefig("correlations.svg")
    # plt.show()

def print_unique_company_names(db_name, table_name, column_name) -> dict :
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute(f"""SELECT DISTINCT {column_name} 
                   FROM {table_name}""")  

    unique_companies = cursor.fetchall()

    for company in unique_companies:
        print(company[0])

    conn.close()
    return unique_companies

def main():
    db_path = 'temp.db'  
    articles = get_articles_from_db(db_path)
    
    with open("inputData/companies.json") as json_file:
        search_words = json.load(json_file)
    word_count = count_word_occurrences(search_words, articles)
    
    # Plot the results
    words : dict = plot_word_occurrences(word_count)
    companies : dict = print_unique_company_names('temp.db', 'Stock_index', 'company_name')
    plot_word_correlations(words, companies)

if __name__ == "__main__":
    main()

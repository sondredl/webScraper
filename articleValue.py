import sqlite3
from collections import Counter
from src import jsonParser

# Connect to the SQLite database
conn = sqlite3.connect('temp.db')
cursor = conn.cursor()

# Fetch all text content from the articles table
cursor.execute("SELECT content FROM articles")
texts = cursor.fetchall()

# List of words to check for
# words_to_check = ["word1", "word2", "word3"]  # Replace with your actual list of words
words_to_check = jsonParser.companyNames()

# Function to count word instances in a text
def count_word_instances(text, words):
    # Convert text to lowercase for case-insensitive matching
    text = text.lower()
    # Initialize a counter
    word_count = Counter()
    
    # Count occurrences of each word in the text
    for word in words:
        word_count[word] = text.count(word.lower())
    
    return word_count

# Initialize an overall counter for all articles
overall_word_count = Counter()

# Process each text and update the overall counter
for article in texts:
    text_content = article[0]  # Get the text column from the row
    word_count = count_word_instances(text_content, words_to_check)
    overall_word_count.update(word_count)

# Close the database connection
conn.close()

# Display the results
for word, count in overall_word_count.items():
    print(f"The word '{word}' appears {count} times.")

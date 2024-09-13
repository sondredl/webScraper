#!/usr/bin/env python

import json
import sqlite3

def evaluateArticles(db_path):
    article_id = 2
    getArticle(db_path, article_id)

def getArticle(db_path, article_id):

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    query = """ SELECT id, timestamp, title, subtitle, text, search_words
                FROM articles
                WHERE id = ? """
    cursor.execute(query, (article_id,))
    # articles = cursor.fetchall()
    article = cursor.fetchone()
    text = ""
    if article:
        article_data = {
            "id": article[0],
            "timestamp": article[1],
            "title": article[2],
            "subtitle": article[3],
            "text": article[4],
            "search_words": article[5]
        }
        text = article_data["text"]
        # return article_data
    # else:
    #     return None

    conn.close()
    analyzeArticle(text)

def analyzeArticle(article):
    # Split the article into sentences using punctuation markers like '.', '!', and '?'
    sentences = article.split('. ')
    sentences = [sentence.strip() for sentence in sentences if sentence]  # Remove extra spaces and empty strings
    topicList = []
    with open("inputData/searchWords.json") as json_file:
        topicList += json.load(json_file)
    with open("inputData/companies.json") as json_file:
        topicList += json.load(json_file)

    for sentence in sentences:
        # words = article.split(' ')
        # if words.index():
        #     print(sentence)
        # for word in words:
        #     print(word)
        contains_any_word(sentence, topicList)
        # if contains_any_word(sentence, topicList):
        #     print(sentence)

def contains_any_word(sentence, word_list):
    # Convert the sentence to lowercase for case-insensitive comparison
    sentence = sentence.lower()
    
    # Check if any word from the word_list is in the sentence
    containsTopic = any(word.lower() in sentence for word in word_list)
    for word in word_list:
        if word.lower() in sentence :
            print(word, sentence)

    # if(containsTopic):
    return containsTopic
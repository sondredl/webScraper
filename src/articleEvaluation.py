#!/usr/bin/env python

import json
import sqlite3

def evaluateArticles(db_path):
    article_id = 2
    getArticle(db_path, article_id)

def getArticle(db_path, article_id):
    topicList = []
    with open("inputData/searchWords.json") as json_file:
        topicList += json.load(json_file)
    with open("inputData/companies.json") as json_file:
        topicList += json.load(json_file)

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

    for sentence in sentences:
        words = article.split(' ')
        if words.index():
            print(sentence)
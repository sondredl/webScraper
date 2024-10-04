#!/usr/bin/env python

import re
import sqlite3
import json
from gensim.models import Word2Vec
from bs4                    import BeautifulSoup

class vectorizeText:
    # def __init__(self):
        # self.m_data_Extractor = dataExtractor()

    def get_sentences_in_article(self, database_name, table_name):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        
        rows = cursor.fetchall()
        conn.close()
        
        # Print or return the rows
        for row in rows:
            self._get_article_from_db(database_name, table_name, row, row[0] )
            # return

        try:
            # self.m_dbCleaner.delete_all_content_in_table(database_name, table_name)
            print(f"deleted content in {table_name}")
        except:
            print(f"failed to delete content in {table_name}")
        finally:
            print("successfull insertion in Articles table")
            return rows  # Optionally return the rows if needed

    def _get_article_from_db(self,database_name, table_name, table_row_content, index):
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor = connection.cursor()

        cursor.execute(f"""
            SELECT  title, subtitle, content
            FROM {table_name}
            WHERE id = ?
            """,
            (index, ) )
        row = cursor.fetchone()
        if row:
            title, subtitle, text = row
            sentences = [sentence.strip().split() for sentence in text.split('.') if sentence.strip()]
            all_words = [word for sentence in sentences for word in sentence]


            w2v = Word2Vec(vector_size=100, window=5, workers=4, min_count=1)
            w2v.build_vocab([all_words])
            w2v.train(sentences, total_examples=w2v.corpus_count, epochs=10)
            for word in w2v.wv.index_to_key:
                print(f"word: {word}\nVector: \n{w2v.wv[word]}\n")

            print(title)

        connection.commit()
        connection.close()

    def get_sentences_from_articles(self, database_name, table_name):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            self._extract_sentences_from_article(database_name, table_name, row, row[0])

    def _extract_sentences_from_article(self, database_name, table_name, row_content, index):
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor = connection.cursor()

        cursor.execute(f"""
            SELECT  title, subtitle, content
            FROM {table_name}
            WHERE id = ?
            """,
            (index, ) )
        row = cursor.fetchone()
        if row:
            article_id = row_content[0]
            text = row_content[5]
            sentences = text
            sentences = [sentence.strip() for sentence in text.split('.') if sentence.strip()]

            for sentence in sentences:
                cursor.execute(f"""
                    INSERT INTO Sentences_in_article(article_id, sentence)
                    VALUES (?, ?) """,
                                        (article_id, sentence),
                )
        connection.commit()
        connection.close()

    def get_word_from_sentences(self, database_name, table_name):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        
        rows = cursor.fetchall()
        conn.close()
        for row in rows:
            self._extract_word_from_sentence(database_name, table_name, row, row[0])

    def _extract_word_from_sentence(self, database_name, table_name, row_content, index):
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor = connection.cursor()

        cursor.execute(f"""
            SELECT  id, sentence
            FROM {table_name}
            WHERE id = ?
            """,
            (index, ) )
        row = cursor.fetchone()
        if row:
            sentence_id = row_content[0]
            article_id = row_content[1]
            sentence = row_content[2]

            words = re.findall(r'\b\w+\b', sentence)

            w2v = Word2Vec(vector_size=100, 
                           window=5, 
                           workers=4, 
                           min_count=1)
            w2v.build_vocab([words])
            w2v.train(sentence, total_examples=w2v.corpus_count, epochs=10)

            for word in words:
                word_vector : str = w2v.wv[word]
                vector = json.dumps(word_vector.tolist())
                cursor.execute(f"""
                    INSERT INTO Word_in_sentences(sentence_id, article_id, word, vector)
                    VALUES (?, ?, ?, ?) """,
                                        (sentence_id, article_id, word, vector),
                )
        connection.commit()
        connection.close()



wordToVector = vectorizeText()
# wordToVector.get_sentences_in_article("temp.db", "Articles")
# wordToVector.get_sentences_from_articles("temp.db", "Articles")
wordToVector.get_word_from_sentences("temp.db", "Sentences_in_article")
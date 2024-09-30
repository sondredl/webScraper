#!/usr/bin/env python

import sqlite3
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
            # sentences = [line.split() for line in text]
            sentences = [sentence.strip().split() for sentence in text.split('.') if sentence.strip()]
            all_words = [word for sentence in sentences for word in sentence]


            # w2v = Word2Vec(sentences, vector_size=100, window=5, workers=4, min_count=5)
            w2v = Word2Vec(vector_size=100, window=5, workers=4, min_count=1)
            w2v.build_vocab([all_words])
            # w2v.build_vocab(sentences)
            w2v.train(sentences, total_examples=w2v.corpus_count, epochs=10)
            # for sentence in sentences:
            #     print(f"\n\nsentence {sentence}")
            for word in w2v.wv.index_to_key:
                print(f"word: {word}\nVector: \n{w2v.wv[word]}\n")

            print(title)

        connection.commit()
        connection.close()

    def get_sentences_from_articles(self, database_name, table_name, column_name):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        
        rows = cursor.fetchall()
        conn.close()
        for row in rows:


wordToVector = vectorizeText()
wordToVector.get_sentences_in_article("temp.db", "Articles")
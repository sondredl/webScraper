#!/usr/bin/env python

import sqlite3
from gensim.models import word2vec
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
            print(title)

        connection.commit()
        connection.close()

word2vec = vectorizeText()
word2vec.get_sentences_in_article("temp.db", "Articles")
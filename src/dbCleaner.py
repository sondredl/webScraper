import sqlite3
import json
import os
import shutil

class databaseCleaner:
    def reorganize_ids(self, database_path, table_name):
        # database_path = "your_database.db"
        connection = sqlite3.connect(database_path)
        cursor = connection.cursor()

        try:
            cursor.execute(
                f"""
                CREATE TABLE IF NOT EXISTS temp_table AS
                SELECT *, ROW_NUMBER() OVER (ORDER BY id) AS new_id
                FROM {table_name}
            """
            )

            cursor.execute(f"DELETE FROM {table_name}")
            cursor.execute(
                f"""
                INSERT INTO {table_name} (id, pagename, tag_name, search_word, href, timestamp)
                SELECT new_id, pagename, tag_name, search_word, href, timestamp
                FROM temp_table
            """
            )

            cursor.execute("DROP TABLE temp_table")
            connection.commit()

            print(f"IDs in {table_name} table have been reorganized.")

        except sqlite3.Error as e:
            print(f"Error: {e}")
            connection.rollback()

        finally:
            connection.close()

    def evaluateArticlesTable(self, last_date_time):
        db_path = "temp.db"
        connection = sqlite3.connect(db_path)

        cursor = connection.cursor()
        # cursor.execute("PRAGMA table_info(articles)")
        # columns = cursor.fetchall()

        # # Extract column names
        # column_names = [column[1] for column in columns]

        # If 'search_words' column doesn't exist, add it
        # if 'search_words' not in column_names:
        #     cursor.execute("ALTER TABLE articles ADD COLUMN search_words TEXT")
        #     print("Column 'search_words' added.")
        # else:
        #     print("Column 'search_words' already exists.")


        with open("inputData/searchWords.json") as json_file:
            search_words = json.load(json_file)
        with open("inputData/companies.json") as json_file:
            search_words += json.load(json_file)
        print(f'search_words: {search_words}')

        # for article in articles:
        cursor.execute("""SELECT id, timestamp, title, subtitle, content 
                    FROM articles
                    WHERE timestamp > ?
                    """, (last_date_time,))
        articles = cursor.fetchall()
        for article in articles:
            article_id = article[0]
            text = article[4]
            searchWordsInArticle = []
            for word in search_words:
                if word.lower() in text.lower():
                    searchWordsInArticle.append(word)
            print(f'article_id {article_id} contains: {searchWordsInArticle} ')

            if isinstance(searchWordsInArticle, list) and searchWordsInArticle:
                searchWordsInArticle = ','.join(searchWordsInArticle)
            else:
                searchWordsInArticle = "empty"

            cursor.execute(
                """
                UPDATE articles
                SET search_words = ?
                WHERE id > ?
                """, (searchWordsInArticle, article_id)
            )

    def delete_folder_contents(self, folder_path):
        # Check if the folder exists
        if os.path.exists(folder_path):
            # Loop through each item in the directory
            for filename in os.listdir(folder_path):
                file_path = os.path.join(folder_path, filename)

                # Check if it is a file or directory
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)  # Remove the file or symlink
                    print(f"File {file_path} deleted.")
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)  # Remove the directory and all its contents
                    print(f"Directory {file_path} deleted.")
        else:
            print(f"The folder {folder_path} does not exist.")


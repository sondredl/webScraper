import json
import subprocess
import os
import sqlite3
import textwrap
import time
import requests
from datetime       import datetime
from bs4            import BeautifulSoup
from src.jsonParser import JsonParser
from src.databaseHandler    import DbHandler
from src.dbCleaner          import databaseCleaner

class dataExtractor:
    def __init__(self):
        self.m_jsonParser = JsonParser()
        self.m_dbHandler = DbHandler()
        self.m_dbCleaner = databaseCleaner()
        self.create_folder_if_none_exists("htmlFiles")
        self.create_folder_if_none_exists("markdown")
        self.create_folder_if_none_exists("articles")
    
    def create_folder_if_none_exists(self, folderName):
        subprocess.run(["mkdir", "folderName"])

    def download_web_pages(self):
        pageList = self.m_jsonParser.webPages()
        for page in pageList:
            self._download_web_pages(page[0], page[1])

    def download_all_article_pages(self, database_name):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT href 
            FROM WordAndUrl""")
        urls = cursor.fetchall()

        cursor.execute("""
            SELECT id 
            FROM WordAndUrl""")
        ids = cursor.fetchall()

        cursor.execute("""
            SELECT timestamp 
            FROM WordAndUrl""")
        timestamp = cursor.fetchall()

        for row in timestamp:
            # Each row is a tuple, so extract the first element
            timestamp_str = row[0]
        
            # Now pass the individual timestamp string to getTimeType
            timestamp = self.m_dbHandler.get_time_type(timestamp_str)
        conn.close()

        for url in urls:
            self._downloadArticlePage(database_name, url[0])


    def getWordAndUrl(self, database_name):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        with open("inputData/searchWords.json") as json_file:
            search_words = json.load(json_file)

        for search_word in search_words:
            cursor.execute( """
                SELECT filename, tag_name, sentence, href, timestamp
                FROM Sentences
                WHERE sentence LIKE ?""",
                ("%" + search_word + "%",),
            )

            matching_rows = cursor.fetchall()
            # print(matching_rows)

            for row in matching_rows:
                # pagename = row
                pagename, tag_name, search_word, href, timestamp = row
                cursor.execute( """
                    INSERT INTO WordAndUrl (pagename, tag_name, search_word, href, timestamp)
                    VALUES (?, ?, ?, ?, ?)""",
                    (pagename, tag_name, search_word, href,  timestamp),
                )
                # print(f"added {pagename}, {tag_name}, {search_word}, {href}, {timestamp}")

        conn.commit()
        conn.close()

    def getCompanyAndUrl(self, database_name):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        with open("inputData/companies.json") as json_file:
            search_words = json.load(json_file)

        for search_word in search_words:
            cursor.execute( """
                SELECT filename, tag_name, sentence, href, timestamp
                FROM Sentences
                WHERE sentence LIKE ?""",
                ("%" + search_word + "%",),
            )

            matching_rows = cursor.fetchall()

            for row in matching_rows:
                pagename, tag_name, search_word, href, timestamp = row
                cursor.execute("""
                    INSERT INTO WordAndUrl ( pagename, tag_name, search_word, href, timestamp)
                    VALUES (?, ?, ?, ?, ?)""",
                    (pagename, tag_name, search_word, href, timestamp),
                )

        conn.commit()
        conn.close()

    def updateDatabase(self, database_name):
        # search_words = self.m_jsonParser.searchWords()
        # self._update_database_with_relevant_articles( search_words)

        search_words = self.m_jsonParser.companyNames()
        self._update_database_with_relevant_articles(database_name, search_words)

    def loop_all_articles(self, database_name, table_name):
        # try:
        # Step 1: Select all rows from the table
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        
        # Step 2: Fetch all results
        rows = cursor.fetchall()
        conn.close()
        
        # Print or return the rows
        for row in rows:
            # print(row)
            self._get_article_from_db(database_name, table_name, row , row[0])

        try:
            self.m_dbCleaner.delete_all_content_in_table(database_name, table_name)
            print(f"deleted content in {table_name}")
        except:
            print(f"failed to delete content in {table_name}")
        finally:
            print("successfull insertion in Articles table")
            return rows  # Optionally return the rows if needed

        # except sqlite3.Error as e:
        #     print(f"An error occurred: {e}")
        #     return None
        # finally:

    def create_markdown_overview(self, db_path, output_dir):
        last_time_run = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_time_run_int = int(time.time())
        # last_time_run = self.m_dbHandler.get_last_time_run()
        # last_time_run_int = self.m_dbHandler.get_last_time_run_int()
        
        output_file = os.path.join(output_dir, f"articles_overview_{last_time_run}.md")
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT timestamp, timestamp_int, title, subtitle, content
            FROM articles
            WHERE timestamp_int > ? """, 
            (last_time_run_int,))
        articles = cursor.fetchall()
        print(f"last_date_time {last_time_run_int}")
        print(f"number of articles to be used {len(articles)}")

        # Determine the file mode ('a' for append, 'w' for write if new file)
        file_mode = 'a' if os.path.exists(output_file) else 'w'
        
        with open(output_file, file_mode) as md_file:
            if file_mode == 'w': 
                md_file.write("# Articles Overview\n\n")

            for index, article in enumerate(articles):
                timestamp, title, subtitle, text, timestamp_int = article
                if len(text) > 10 and timestamp_int > last_time_run_int:
                    md_file.write(f"## Article {index + 1}: {title}\n")
                    if subtitle:
                        md_file.write(f"### {subtitle}\n")
                    else:
                        md_file.write("### No subtitle\n")
                    
                    md_file.write(f"{text}...\n\n") 
                    md_file.write("---\n\n")
                else:
                    print("no new articles, will not make new file")

        conn.commit()
        conn.close()
        print(f"Markdown overview saved to {output_file}")
        self._format_markdown_file(output_file)

    def cleanDuplicates(self, database_name):
        # self.m_dbHandler.cleanDuplicates(database_name, "WordAndUrl", "href",  "timestamp")
        self.m_dbHandler.clean_duplicates_in_column(database_name, "WordAndUrl", "href")
        self.m_dbHandler.clean_duplicates_in_column(database_name, "Sentences", "href")
        # self.m_dbHandler.cleanDuplicates(database_name, "Articles",    "title", "timestamp")
        self.m_dbHandler.clean_duplicates_in_column(database_name, "raw_articles", "url")
        # self.m_dbHandler.clean_duplicates_in_column(database_name, "articles", "href")
        self.m_dbCleaner.reorganize_ids(database_name, "WordAndUrl")
        self.m_dbHandler.clean_last_update(database_name, "WordAndUrl")

    def _update_database_with_relevant_articles(self, database_name, search_words):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        folder_path = "htmlFiles/" # set to table name after downloading to database instead of file

        search_words = self.m_jsonParser.searchWords()
        html_tags = self.m_jsonParser.htmlTags()
        previousInsertion = ""
        previousHrefLink = ""

        for filename in os.listdir(folder_path):
            if filename.endswith(".html"):
                file_path = os.path.join(folder_path, filename)

                with open(file_path, "r", encoding="utf-8") as file:
                    soup = BeautifulSoup(file, "html.parser")

                for tag_name in html_tags:
                    for tag in soup.find_all(tag_name):
                        content = tag.text
                        if any(word in content for word in search_words):
                            link_tag = tag.find_parent("a")
                            href_link = ""
                            if link_tag:
                                href_link = link_tag.get("href")
                                dot_index = filename.find(".")
                                pageName = filename[:dot_index]
                                if not href_link.startswith("https"):
                                    href_link = self._getUrl(pageName, link_tag.get("href"))

                            if href_link == previousHrefLink:
                                href_link = ""
                            else:
                                previousHrefLink = href_link

                            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                            if not (content == previousInsertion) and href_link != "":
                                cursor.execute("""
                                    INSERT INTO Sentences ( filename, tag_name, sentence, href, timestamp) 
                                    VALUES (?, ?, ?, ?, ?)
                                """,
                                (pageName, tag_name, content, href_link,   timestamp),
                                )
                                previousInsertion = content
        conn.commit()
        conn.close()

    def _download_web_pages(self,name, url):
        filename = name + ".html"
        path = "htmlFiles/"
        path += filename
        print(f"\n downloading {url} to {path}")
        subprocess.run(["curl", "-L", "-o", path, url])

    def _format_markdown_file(self, file_path, max_width=120):
        with open(file_path, 'r') as md_file:
            content = md_file.read()

        lines = content.splitlines()

        formatted_lines = []
        for line in lines:
            if line.__contains__('###') :
                if len(formatted_lines) > 0 and not formatted_lines[-1].startswith('#'):
                    formatted_lines.append('\n')  # Add a blank line

            formatted_lines.append(line)

        content = '\n'.join(formatted_lines)
        paragraphs = content.split('\n\n')

        formatted_paragraphs = []
        for paragraph in paragraphs:
            # Handle code blocks and lists 
            if paragraph.startswith("```") or paragraph.startswith("- ") or paragraph.startswith("* "):
                formatted_paragraphs.append(paragraph)
            else:
                wrapped = textwrap.fill(paragraph, width=max_width)
                formatted_paragraphs.append(wrapped)

        formatted_content = '\n\n'.join(formatted_paragraphs)

        with open(file_path, 'w') as md_file:
            md_file.write(formatted_content)

        print(f"File '{file_path}' has been formatted with a max width of {max_width} characters.")

    def _get_article_from_db(self,database_name, table_name, table_row_content, index):
        raw_html = table_row_content[3] # index of column with raw html
        
        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(raw_html, "html.parser")

        # Extract title and subtitle
        title_tag = soup.title
        subtitle_tag = soup.find(["h2", "h3", "h4", "h5", "h6", "p"])

        title = title_tag.text.strip() if title_tag else "No Title Found"
        subtitle = subtitle_tag.text.strip() if subtitle_tag else "No Subtitle Found"

        # Extract the article's text
        text = "\n".join([p.text.strip() for p in soup.find_all("p")])

        # Insert article data into the relevant table
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor = connection.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_int = int(time.time())
        cursor.execute( """
            INSERT INTO Articles(timestamp, timestamp_int, title, subtitle, content)
            VALUES (?, ?, ?, ?, ?) """,
                                (timestamp, timestamp_int, title, subtitle, text),
        )
        connection.commit()
        connection.close()
        # self._insert_article(database_name , table_name, table_row_content,  title, subtitle, text)
        print(f"Article {index} '{title}' inserted into the database.")

        # Commit the changes
        # connection.commit()
        # else:
        #     print(f"No article found for URL: {url}")
        
        # Close the connection
        # connection.close()


    def _get_article_from_file(self, filename, connection, index):
        with open(filename, "r", encoding="utf-8") as file:
            html_content = file.read()

        cursor = connection.cursor()

        matching_rows = cursor.fetchall()
        
        soup = BeautifulSoup(html_content, "html.parser")

        for row in matching_rows:
            pagename, tag_name, search_word, href, timestamp = row
            cursor.execute("""
                INSERT INTO WordAndUrl ( pagename, tag_name, search_word, href, timestamp)
                VALUES (?, ?, ?, ?, ?)""",
                (pagename, tag_name, search_word, href, timestamp),
            )


        title_tag = soup.title
        subtitle_tag = soup.find(["h2", "h3", "h4", "h5", "h6", "p"])

        title = title_tag.text.strip() if title_tag else "No Title Found"
        subtitle = subtitle_tag.text.strip() if subtitle_tag else "No Subtitle Found"

        text = "\n".join([p.text.strip() for p in soup.find_all("p")])
        self._insert_article(connection, title, subtitle, text)
        print(f"Article  {index} {title}' inserted into the database.")

        connection.commit()
        connection.close()

    def _insert_article(self, database_name, title, subtitle, text):
        connection = sqlite3.connect(database_name)
        cursor = connection.cursor()
        cursor = connection.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_int = int(time.time())
        cursor.execute( """
            INSERT INTO Articles(timestamp, title, subtitle, content, timestamp_int)
            VALUES (?, ?, ?, ?, ?) """,
                                (timestamp, title, subtitle, text, timestamp_int),
        )
        connection.commit()
        connection.close()

    def _getUrl(self, pageName, href):
        web_pages = self.m_jsonParser.webPages()

        if not href.startswith("https"):
            for page in web_pages:
                if pageName == page[0]:
                    href_link = page[1] + href
                    return href_link
        else:
            return

    def _increment_counter(self, counter=[0]):
        counter[0] += 1
        return counter[0]

    def _downloadArticlePage(self, database_name, url):
        # Fetch the article page content
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()
        response = requests.get(url)

        if response.status_code == 200:
            # Parse the HTML using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Convert BeautifulSoup object to a string (raw HTML)
            raw_html = str(soup)

            # Get the current timestamp in two formats: human-readable and integer (Unix timestamp)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Human-readable timestamp
            timestamp_int = int(time.time())  # Unix timestamp

            # Assume search_words is some text or keywords extracted from the URL or HTML
            search_words = self._extract_search_words(soup)  # You should define this method for extracting search words

            # Insert the raw HTML into the 'raw_articles' table
            cursor.execute("""
                INSERT INTO raw_articles (timestamp, timestamp_int, raw_html, search_words, url) 
                VALUES (?, ?, ?, ?, ?)
            """, (timestamp, timestamp_int, raw_html, search_words, url))

            print(f"'raw_articles' inserted : {url}")
        else:
            print(f"Failed to retrieve webpage. Status code: {response.status_code}")
        conn.commit()
        conn.close()

    def _extract_search_words(self, soup):
        # Example: extract text from <title> and <meta name="keywords">
        title = soup.title.string if soup.title else ""
        meta_keywords = soup.find("meta", {"name": "keywords"})
        keywords = meta_keywords["content"] if meta_keywords else ""

        # Combine title and keywords or any other search words logic
        search_words = title + " " + keywords
        return search_words
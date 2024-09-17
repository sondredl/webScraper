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

    def download_all_article_pages(self):
        conn = sqlite3.connect("your_database.db")
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

        for url in urls:
            self._downloadArticlePage(url[0], cursor)

        conn.close()

    def getWordAndUrl(self):
        conn = sqlite3.connect("your_database.db")
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

            for row in matching_rows:
                pagename, tag_name, search_word, href, timestamp = row
                cursor.execute( """
                    INSERT INTO WordAndUrl ( pagename, tag_name, search_word, href, timestamp)
                    VALUES (?, ?, ?, ?, ?)""",
                                            (pagename, tag_name, search_word, href,  timestamp),
                )

        conn.commit()
        conn.close()

    def getCompanyAndUrl(self):
        conn = sqlite3.connect("your_database.db")
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

    def updateDatabase(self):
        search_words = self.m_jsonParser.searchWords()
        self._update_database_with_relevant_articles( search_words)

        search_words = self.m_jsonParser.companyNames()
        self._update_database_with_relevant_articles( search_words)

    def loop_all_articles(self, db_path, table):
        directory_path = table                  # change when writing to database instad of file

        connection = sqlite3.connect(db_path)

        file_list = os.listdir(directory_path)

        for file_name in file_list:
            file_name_path = os.path.join(directory_path, file_name)
            self._get_article_from_file(file_name_path, connection, file_name[0])

        connection.close()

    def create_markdown_overview(self, db_path, output_dir):
        last_time_run = self.m_dbHandler.get_last_time_run()
        last_time_run_int = self.m_dbHandler.get_last_time_run_int()
        
        # Construct the markdown file path
        output_file = os.path.join(output_dir, f"articles_overview_{last_time_run}.md")
        
        # Connect to the SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Query the articles table
        cursor.execute("""
            SELECT timestamp, title, subtitle, content, timestamp_int 
            FROM articles
            WHERE timestamp_int > ? """, 
            (last_time_run_int,))
        articles = cursor.fetchall()
        print(f"last_date_time {last_time_run_int}")
        # print(f"last_time_run {last_date_time}")
        print(f"number of articles to be used {len(articles)}")

        # Determine the file mode ('a' for append, 'w' for write if new file)
        file_mode = 'a' if os.path.exists(output_file) else 'w'
        
        # Open the markdown file in the appropriate mode
        with open(output_file, file_mode) as md_file:
            # If appending, check if we need to add a header for a new file
            if file_mode == 'w':
                md_file.write("# Articles Overview\n\n")

            # Loop through the articles and write each one to the markdown file
            for index, article in enumerate(articles):
                timestamp, title, subtitle, text, timestamp_int = article
                # if len(text) > 10 :
                if len(text) > 10 and timestamp_int > last_time_run_int:
                    # Write the article title and subtitle in markdown
                    md_file.write(f"## Article {index + 1}: {title}\n")
                    if subtitle:
                        md_file.write(f"### {subtitle}\n")
                    else:
                        md_file.write("### No subtitle\n")
                    
                    # Write the article text (truncated if necessary)
                    md_file.write(f"{text}...\n\n")  # Limit to first 500 characters
                    md_file.write("---\n\n")
                else:
                    print("no new articles, will not make new file")

        # Close the database connection
        conn.close()
        print(f"Markdown overview saved to {output_file}")
        self._format_markdown_file(output_file)

    def cleanDuplicates(self):
        self.m_dbHandler.cleanDuplicates("WordAndUrl", "href",  "timestamp")
        self.m_dbHandler.cleanDuplicates("Articles",    "title", "timestamp")
        self.m_dbCleaner.reorganize_ids(self.m_dbHandler.database_path, "WordAndUrl")
        self.m_dbHandler.clean_last_update("WordAndUrl")

    def _update_database_with_relevant_articles(self, search_words):
        conn = sqlite3.connect("your_database.db")
        cursor = conn.cursor()

        folder_path = "htmlFiles/"

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
                                    VALUES (?, ?, ?, ?, ?)""",
                                                            (pageName, tag_name, content, href_link,   timestamp),
                                )
                                previousInsertion = content
        conn.commit()
        conn.close()

    def _download_web_pages(self,name, url):
        filename = name + ".html"
        path = "htmlFiles/"
        path += filename
        subprocess.run(["curl", "-L", "-o", path, url])

    def _format_markdown_file(self, file_path, max_width=120):
        # Open the input markdown file and read its content
        with open(file_path, 'r') as md_file:
            content = md_file.read()

        # Split the content into lines for more granular control
        lines = content.splitlines()

        formatted_lines = []
        for line in lines:
            # Add a newline before `###` headers and list items that don't start with a `#`
            if line.__contains__('###') :
                # Ensure the previous line isn't a header or list
                if len(formatted_lines) > 0 and not formatted_lines[-1].startswith('#'):
                    formatted_lines.append('\n')  # Add a blank line

            # Add the line itself to the formatted list
            formatted_lines.append(line)

        # Join the lines back into paragraphs for wrapping
        content = '\n'.join(formatted_lines)

        # Split the content into paragraphs by double newlines
        paragraphs = content.split('\n\n')

        # Wrap each paragraph to the specified width
        formatted_paragraphs = []
        for paragraph in paragraphs:
            # Handle code blocks and lists (you may want to skip wrapping these)
            if paragraph.startswith("```") or paragraph.startswith("- ") or paragraph.startswith("* "):
                formatted_paragraphs.append(paragraph)
            else:
                # Wrap lines to the max_width
                wrapped = textwrap.fill(paragraph, width=max_width)
                formatted_paragraphs.append(wrapped)

        # Join the formatted paragraphs back with double newlines
        formatted_content = '\n\n'.join(formatted_paragraphs)

        # Write the formatted content back to the same file or a new file
        with open(file_path, 'w') as md_file:
            md_file.write(formatted_content)

        print(f"File '{file_path}' has been formatted with a max width of {max_width} characters.")

    def _get_article_from_file(self, filename, connection, index):
        with open(filename, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        title_tag = soup.title
        subtitle_tag = soup.find(["h2", "h3", "h4", "h5", "h6", "p"])

        title = title_tag.text.strip() if title_tag else "No Title Found"
        subtitle = subtitle_tag.text.strip() if subtitle_tag else "No Subtitle Found"

        text = "\n".join([p.text.strip() for p in soup.find_all("p")])

        self._insert_article(connection, title, subtitle, text)

        print(f"Article  {index} {title}' inserted into the database.")

    def _insert_article(self, connection, title, subtitle, text):
        cursor = connection.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_int = int(time.time())
        cursor.execute( """
            INSERT INTO articles(timestamp, title, subtitle, content, timestamp_int)
            VALUES (?, ?, ?, ?, ?) """,
                                (timestamp, title, subtitle, text, timestamp_int),
        )
        connection.commit()

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

    def _downloadArticlePage(self, url, cursor):
        path = "articles/"
        os.makedirs(path, exist_ok=True)
        output_file = path + str(self._increment_counter()) + ".html"

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            with open(output_file, "w", encoding="utf-8") as file_url:
                file_url.write(str(soup))

                print(f"Webpage content saved to {output_file}")
            cursor.execute("""
                INSERT INTO WordAndUrl (local_article_file) 
                VALUES (?)""", 
                ("int.html",))
        else:
            print(f"Failed to retrieve webpage. Status code: {response.status_code}")

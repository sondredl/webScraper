import json
import subprocess
import os
import sqlite3
from datetime import datetime
from bs4 import BeautifulSoup
from src import jsonParser
import time
import requests

class dataExtractor:
    def createFileToParse(self,name, url):
        filename = name + ".html"
        path = "htmlFiles/"
        path += filename
        subprocess.run(["curl", "-L", "-o", path, url])

    def createContentFiles(self):
        subprocess.run(["mkdir", "htmlFiles"])
        pageList = jsonParser.webPages()
        for page in pageList:
            self.createFileToParse(page[0], page[1])

    def downloadArticlePage(self, url, cursor):
        path = "articles/"
        os.makedirs(path, exist_ok=True)
        output_file = path + str(self.increment_counter()) + ".html"

        response = requests.get(url)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")

            with open(output_file, "w", encoding="utf-8") as file_url:
                file_url.write(str(soup))

                print(f"Webpage content saved to {output_file}")
            cursor.execute("INSERT INTO WordAndUrl (local_article_file) VALUES (?)", ("int.html",))
        else:
            print(f"Failed to retrieve webpage. Status code: {response.status_code}")

    def download_all_article_pages(self, db_handler):
        conn = sqlite3.connect("your_database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT href FROM WordAndUrl")
        urls = cursor.fetchall()

        cursor.execute("SELECT id FROM WordAndUrl")
        ids = cursor.fetchall()

        cursor.execute("SELECT timestamp FROM WordAndUrl")
        timestamp = cursor.fetchall()
        for row in timestamp:
            # Each row is a tuple, so extract the first element
            timestamp_str = row[0]
        
            # Now pass the individual timestamp string to getTimeType
            timestamp = db_handler.get_time_type(timestamp_str)
        # timestamp = db_handler.getTimeType(timestamp)

        last_time_run = db_handler.get_last_time_run()
        # current_time = db_handler.getCurrentTime()

        # if timestamp  > last_time_run:
        for url in urls:
            self.downloadArticlePage(url[0], cursor)
            # cursor.execute("INSERT INTO WordAndUrl (local_article_file) VALUES (?)", ("int.html",))
            # print(f'url: {url} , {url[0]}')
        # else:
        #     print(f"    timestamp: {timestamp} \n last_time_run: {last_time_run}")

        conn.close()

    def increment_counter(self, counter=[0]):
        counter[0] += 1
        return counter[0]

    def getWordAndUrl(self):
        conn = sqlite3.connect("your_database.db")
        cursor = conn.cursor()

        with open("inputData/searchWords.json") as json_file:
            search_words = json.load(json_file)

        for search_word in search_words:
            cursor.execute(
                """SELECT 
                        filename, 
                        tag_name, 
                        sentence, 
                        href, 
                        timestamp
                            FROM Sentences
                            WHERE sentence LIKE ?""",
                ("%" + search_word + "%",),
            )

            matching_rows = cursor.fetchall()

            for row in matching_rows:
                pagename, tag_name, search_word, href, timestamp = row
                cursor.execute(
                    """INSERT INTO WordAndUrl (
                                            pagename, 
                                            tag_name, 
                                            search_word, 
                                            href, 
                                            timestamp)
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
            cursor.execute(
                """SELECT 
                    filename, 
                    tag_name, 
                    sentence, 
                    href, 
                    timestamp
                            FROM Sentences
                            WHERE sentence LIKE ?""",
                ("%" + search_word + "%",),
            )

            matching_rows = cursor.fetchall()

            for row in matching_rows:
                pagename, tag_name, search_word, href, timestamp = row
                cursor.execute(
                    """INSERT INTO WordAndUrl (
                            pagename, 
                            tag_name, 
                            search_word, 
                            href, 
                            timestamp)
                                VALUES (?, ?, ?, ?, ?)""",
                    (pagename, tag_name, search_word, href, timestamp),
                )

        conn.commit()
        conn.close()

    def updateDatabaseCompany(self):
        conn = sqlite3.connect("your_database.db")
        cursor = conn.cursor()

        folder_path = "htmlFiles/"

        html_tags = jsonParser.htmlTags()
        selected_words = jsonParser.companyNames()
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
                        if any(word in content for word in selected_words):
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
                                cursor.execute(
                                    "INSERT INTO Sentences (filename, tag_name, sentence, href,  timestamp) VALUES (?, ?, ?, ?, ?)",
                                    (filename, tag_name, content, href_link, timestamp),
                                )
                                previousInsertion = content
        conn.commit()
        conn.close()

    def updateDatabase(self):
        conn = sqlite3.connect("your_database.db")
        cursor = conn.cursor()

        folder_path = "htmlFiles/"

        selected_words = jsonParser.searchWords()
        html_tags = jsonParser.htmlTags()
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
                        if any(word in content for word in selected_words):
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
                                cursor.execute(
                                    """INSERT INTO Sentences (
                                        filename, 
                                        tag_name, 
                                        sentence, 
                                        href, 
                                        timestamp) 
                                        VALUES (?, ?, ?, ?, ?)""",
                                    (pageName, tag_name, content, href_link,   timestamp),
                                )
                                previousInsertion = content
        conn.commit()
        conn.close()

    # def fixHrfLinks(self):
    #     conn = sqlite3.connect("your_database.db")
    #     cursor = conn.cursor()

    #     tableName = "Sentences"
    #     cursor.execute(f"select * from {tableName}")
    #     rows = cursor.fetchall()

    #     web_pages = jsonParser.webPages()
    #     web_pages += jsonParser.companyNames()

    #     for row in rows:
    #         if not row[4].startswith("https"):
    #             for page in web_pages:
    #                 href_link = page[1] + row[4]
    #                 cursor.execute("INSERT INTO Sentences ( href) VALUES ( ?)", (href_link))

    #     conn.commit()
    #     conn.close()

    def _getUrl(self, pageName, href):
        web_pages = jsonParser.webPages()

        if not href.startswith("https"):
            for page in web_pages:
                if pageName == page[0]:
                    href_link = page[1] + href
                    return href_link
        else:
            return

    def insert_article(self, connection, title, subtitle, text):
        cursor = connection.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_int = int(time.time())
        cursor.execute(
            """
            INSERT INTO articles (
                timestamp,
                title, 
                subtitle, 
                content,
                timestamp_int)
            VALUES (?, ?, ?, ?, ?)
        """,
            ( timestamp, title, subtitle, text, timestamp_int),
        )
        connection.commit()

    def loop_all_articles(self):
        # directory_path = "../articles/"
        directory_path = "articles/"

        # db_path = "../your_database.db"
        db_path = "your_database.db"
        connection = sqlite3.connect(db_path)

        file_list = os.listdir(directory_path)

        for file_name in file_list:
            file_name_path = os.path.join(directory_path, file_name)
            self.get_article_from_file(file_name_path, connection, file_name[0])

        connection.close()

    def get_article_from_file(self, filename, connection, index):
        with open(filename, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "html.parser")

        title_tag = soup.title
        subtitle_tag = soup.find(["h2", "h3", "h4", "h5", "h6", "p"])

        title = title_tag.text.strip() if title_tag else "No Title Found"
        subtitle = subtitle_tag.text.strip() if subtitle_tag else "No Subtitle Found"

        text = "\n".join([p.text.strip() for p in soup.find_all("p")])

        self.insert_article(connection, title, subtitle, text)

        print(f"Article  {index} {title}' inserted into the database.")

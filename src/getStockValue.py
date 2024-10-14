#!/usr/bin/env python

import time
import subprocess
import os
import sqlite3
from bs4            import BeautifulSoup
from datetime       import datetime
import re
# import dataExtractor

# subprocess.run(["make"])


class aksjer24:
    def __init__(self):
        self.subtitle : str

    def download_web_pages(self, name, url):
        filename = name + ".html"
        path = "htmlFiles/"
        path += filename
        print(f"\n downloading {url} to {path}")
        subprocess.run(["curl", "-L", "-o", path, url])

    def get_content_element_from_file(self, 
                                      file_name, 
                                      parent_class, 
                                      element_class, 
                                      nested_element_class):
        with open(file_name, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "lxml")
        parent_section = soup.find_all(True, class_= parent_class)

        if parent_section:
            element_section = soup.find_all(True, class_= element_class)
            for section in element_section:
                nested_elements = section.find_all(True, class_=nested_element_class)
                if nested_elements:
                    for i, element in enumerate(nested_elements, 1):
                        element_content = element.get_text(strip=True) 
                        self._add_stock_to_database("temp.db", "Stock_index", element_content)
        else:
            print(f"No element with class '{parent_class}' found.")

    def _add_stock_to_database(self, database_name, table_name, element_content):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        url = ""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_int = int(time.time())
        market = "oslo bors"
        title = ""

        company_name ,value = self.extract_company_and_value(element_content)
        print(f"{company_name} {value}")

        percent_change = ""

        cursor.execute(f"""
            INSERT INTO {table_name} ( url, timestamp, timestamp_int, market, title, company_name, value, percent_change) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ( url, timestamp, timestamp_int, market, title, company_name, value, percent_change),
            )

        conn.commit()
        conn.close()

    def extract_company_and_value(self, element_content):
        match = re.search(r'(\d+(\.\d+)?)', element_content)
        
        if match:
            company_name = element_content[:match.start()].strip()
            remaining_content = element_content[match.start():].strip()
            decimal_matches = re.findall(r'\d+,\d+', remaining_content)
        
            # Get the first valid decimal number
            value = decimal_matches[0] if decimal_matches else None

            return company_name, value
        else:
            return element_content.strip(), None

    def get_content(self):
    
        fileName = "htmlFiles/e24aksjer.html"

        parent_class = "styles_root__RKp5p"
        elementClass = "styles_table__eqU36 styles_shadowDisabled__HJU_w styles_bordered__WSE4Q"
        nested_element_class = "styles_row__Hy84e"
        self.get_content_element_from_file(fileName, parent_class, elementClass, nested_element_class)

    def get_content_2(self):
    
        fileName = "htmlFiles/e24aksjer.html"

        parent_class = "styles_table__eqU36"
        elementClass = "styles_row__Hy84e"
        nested_element_class = "styles_cell__E72Vn"
        self.get_content_element_from_file_2(fileName, parent_class, elementClass, nested_element_class)

    def get_content_element_from_file_2(self, 
                                      file_name, 
                                      parent_class, 
                                      element_class, 
                                      nested_element_class):
        with open(file_name, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "lxml")
        parent_section = soup.find_all(True, class_= parent_class)

        if parent_section:
            element_section = soup.find_all(True, class_= element_class)
            if element_section:
            # for section in element_section:
            #     nested_elements = section.find_all(True, class_=nested_element_class)
            #     if nested_elements:
                for i, element in enumerate(element_section, 1):
                    element_content = element.get_text(strip=True) 
                    self._add_stock_to_database_2("temp.db", "Stock_index", element_content)
        else:
            print(f"No element with class '{parent_class}' found.")

    def _add_stock_to_database_2(self, database_name, table_name, element_content):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        url = ""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        timestamp_int = int(time.time())
        market = "oslo bors"
        title = ""

        company_name ,value = self.extract_company_and_value_2(element_content)
        print(f"{company_name} :: {value}")

        percent_change = ""

        cursor.execute(f"""
            INSERT INTO {table_name} ( url, timestamp, timestamp_int, market, title, company_name, value, percent_change) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ( url, timestamp, timestamp_int, market, title, company_name, value, percent_change),
            )

        conn.commit()
        conn.close()

    def extract_company_and_value_2(self, element_content):
        match = re.search(r'(\d+(\.\d+)?)', element_content)
        
        if match:
            company_name = element_content[:match.start()].strip()
            remaining_content = element_content[match.start():].strip()
            decimal_matches = re.findall(r'\d+,\d+', remaining_content)
        
            # Get the first valid decimal number
            value = decimal_matches[0] if decimal_matches else None

            return company_name, value
        else:
            return element_content.strip(), None


# m_stock = aksjer24()
# m_stock.download_web_pages("e24aksjer", "https://e24.no/bors")
# m_stock.get_content()
# m_stock.update_company_name("temp.db")
# m_stock.remove_company_name_from_value("temp.db")

# m_dataExtractor = dataExtractor()
# m_dataExtractor.cleanDuplicateRows("temp.db", "Stock_index")
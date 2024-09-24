#!/usr/bin/env python
import subprocess
import os
import sqlite3
from bs4            import BeautifulSoup

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
                                      title, 
                                      element_class, 
                                      nested_element_class):
        with open(file_name, "r", encoding="utf-8") as file:
            html_content = file.read()

        soup = BeautifulSoup(html_content, "lxml")
        parent_section = soup.find_all(True, class_= parent_class)

        for section in parent_section:
            if parent_section :
                # print(f"\n\n{title}")
                # section_text = parent_section.get_text()
                section_text = section.get_text()
                if title in section_text:
                    print(f"\n\ntitle: {title}")
                    # print(f"parent_section: {parent_section}")
                    # print(f"with element with class {parent_class}")

                    section = soup.find(True, class_=element_class)
                    if section:
                        # print(f"{title} with element with class {element_class}")
                        nested_elements = section.find_all(True, class_=nested_element_class)

                        if nested_elements:
                            print(f"{title} with nested element with class {nested_element_class}")
                            for i, element in enumerate(nested_elements, 1):
                                element_content = element.get_text(strip=True) 
                                print(f"Element {i}: {element_content}")
                                self._add_stock_to_database("temp.db", "Stock_index", element_content)

            #             else:
            #                 print(f"No nested element with class '{nested_element_class}' found.")
            #         else:
            #             print(f"No element with class '{element_class}' found.")
                # else:
                #     print(f"parent_section with class {parent_class} does not contain {title}")
            else:
                print(f"No element with class '{parent_class}' found.")

    def _add_stock_to_database(self, database_name, table_name, element_content):
        conn = sqlite3.connect(database_name)
        cursor = conn.cursor()

        url = ""
        timestamp = ""
        timestamp_int = ""
        market = "oslo bors"
        title = ""
        company_name = ""
        value = element_content
        percent_change = ""

        cursor.execute(f"""
            INSERT INTO {table_name} ( url, timestamp, timestamp_int, market, title, company_name, value, percent_change) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            ( url, timestamp, timestamp_int, market, title, company_name, value, percent_change),
            )

        conn.commit()
        conn.close()

    def get_content(self):
    
        # m_stock = aksjer24()
        fileName = "htmlFiles/e24aksjer.html"

        title = "Vinnere"
        parent_class = "styles_root__RKp5p"
        elementClass = "styles_table__eqU36 styles_shadowDisabled__HJU_w styles_bordered__WSE4Q"
        nested_element_class = "styles_row__Hy84e"
        self.get_content_element_from_file(fileName, parent_class, title, elementClass, nested_element_class)

        title = "Råvarer"
        parent_class = "styles_root__e3aEm"
        elementClass ="styles_table__eqU36 styles_shadowDisabled__HJU_w styles_bordered__WSE4Q"
        nested_element_class = "styles_row__Hy84e"
        self.get_content_element_from_file(fileName, parent_class, title, elementClass, nested_element_class)

        title = "Tapere"
        parent_class = "styles_root__e3aEm"
        elementClass ="styles_table__eqU36 styles_shadowDisabled__HJU_w styles_bordered__WSE4Q"
        nested_element_class = "styles_row__Hy84e"
        self.get_content_element_from_file(fileName, parent_class, title, elementClass, nested_element_class)

        title = "Mest omsatt"
        parent_class = "styles_root__e3aEm"
        elementClass ="styles_table__eqU36 styles_shadowDisabled__HJU_w styles_bordered__WSE4Q"
        nested_element_class = "styles_row__Hy84e"
        self.get_content_element_from_file(fileName, parent_class, title, elementClass, nested_element_class)

        title = "Uvanlig høy omsetning"
        parent_class = "styles_root__e3aEm"
        elementClass ="styles_table__eqU36 styles_shadowDisabled__HJU_w styles_bordered__WSE4Q"
        nested_element_class = "styles_row__Hy84e"
        self.get_content_element_from_file(fileName, parent_class, title, elementClass, nested_element_class)

        title = "storste enhetshandel"
        parent_class = "styles_root__e3aEm"
        elementClass ="styles_table__eqU36 styles_shadowDisabled__HJU_w styles_bordered__WSE4Q"
        nested_element_class = "styles_row__Hy84e"
        self.get_content_element_from_file(fileName, parent_class, title, elementClass, nested_element_class)




m_stock = aksjer24()
m_stock.download_web_pages("e24aksjer", "https://e24.no/bors")
m_stock.get_content()
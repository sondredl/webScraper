#!/usr/bin/env python
import subprocess
import os
from bs4            import BeautifulSoup

# subprocess.run(["make"])


class aksjer24:
    def __init__(self):
        self.subtitle : str

    def download_web_pages(name, url):
        filename = name + ".html"
        path = "htmlFiles/"
        path += filename
        print(f"\n downloading {url} to {path}")
        subprocess.run(["curl", "-L", "-o", path, url])
    
    def get_most_traded(filename):
        folder_path = "htmlFiles/"
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")

    def get_winners(filename):
        folder_path = "htmlFiles/"
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")

    def get_loosers(filename):
        folder_path = "htmlFiles/"
        if filename.endswith(".html"):
            file_path = os.path.join(folder_path, filename)

            with open(file_path, "r", encoding="utf-8") as file:
                soup = BeautifulSoup(file, "html.parser")


def get_content_element_from_file(file_name,  element_class):
    with open(file_name, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "lxml")
    section = soup.find(True, class_=element_class)

    if section:
        nested_element_class = "styles_item__kyxZ3"
        nested_elements = section.find_all(True, class_=nested_element_class)

        if nested_elements:
            for i, element in enumerate(nested_elements, 1):
                element_content = element.get_text(strip=True) 
                print(f"Element {i}: {element_content}")

        else:
            print(f"No nested element with class '{nested_element_class}' found.")
    else:
        print(f"No element with class '{element_class}' found.")


dataContainerClass1 = "styles_item__kyxZ3"
dataContainerClass2 = "styles_minorPositive__2vbjs"

# download_web_pages("e24aksjer", "https://e24.no/bors")

m_stock = aksjer24()

fileName = "htmlFiles/test.html"
elementType = "section"
elementClass = "overview_section__K48df overview_main__sZ_nI"

get_content_element_from_file(fileName, elementClass)

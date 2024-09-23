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


# def get_content_element_from_file(file_name, element_type, element_class):
#     # Load the HTML file
#     with open(file_name, "r", encoding="utf-8") as file:
#         html_content = file.read()

#     # Parse the HTML content using BeautifulSoup
#     soup = BeautifulSoup(html_content, "lxml")

#     # Find the section element with the specific class
#     section = soup.find(element_type, class_=element_class)

#     # Extract the content of that section (including child elements)
#     if section:
#         section_content = section.get_text(strip=True)  # Get text content of the section
#         # print(section_content)

#         soup = BeautifulSoup(section_content, "lxml")
#         element_class = "overview_main__sZ_nI"
#         element_type = "a"
#         element = soup.find(element_type, class_=element_class)

#         print(element)

#         if element:
#             element_content = element.get_text(strip=True)  # Get text content of the section
#             print(element_content)

#         # print(section_content)
#         # dataContainerClass1 = "styles_item__kyxZ3"
#         # dataContainerClass2 = "styles_minorPositive__2vbjs"
#         # get_element_content(section_content, dataContainerClass1)
#         # get_element_content(section_content, dataContainerClass2)
#     else:
#         print(f"{element_type} not found!")

# from bs4 import BeautifulSoup

def get_content_element_from_file(file_name, element_type, element_class):
    # Load the HTML file
    with open(file_name, "r", encoding="utf-8") as file:
        html_content = file.read()

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "lxml")

    # Find the section element with the specific class
    section = soup.find(element_type, class_=element_class)

    # If the section exists, proceed to find nested elements
    if section:
        # Search for the nested 'a' element with the specific class within the section
        nested_element_class = "styles_item__kyxZ3"
        nested_element_type = "a"
        nested_element = section.find(nested_element_type, class_=nested_element_class)

        # Print the nested element if found
        if nested_element:
            nested_content = nested_element.get_text(strip=True)  # Get text content of the nested element
            print(nested_content)
        else:
            print(f"No nested element <{nested_element_type}> with class '{nested_element_class}' found.")
    else:
        print(f"No element <{element_type}> with class '{element_class}' found.")

# Example usage
# get_content_element_from_file("your_file.html", "section", "overview_section__K48df")


def get_element_content(html_content, element_class):
    # Load the HTML file
    # with open(file_name, "r", encoding="utf-8") as file:
    #     html_content = file.read()

    # Parse the HTML content using BeautifulSoup
    class_name = "overview_main__sZ_nI"
    soup = BeautifulSoup(html_content, "lxml")
    elements = soup.find_all(True, class_=class_name)

    # Loop through and print each element's content
    print(elements)
    for element in elements:
        print(element.get_text(strip=True))


    class_name = "overview_section__K48df overview_main__sZ_nI"
    element = soup.find(True, class_=class_name)
    print(element)

    # Find the section element with the specific class
    section = soup.find(True, class_=element_class)
    print(section)

    # Extract the content of that section (including child elements)
    if section:
        section_content = section.get_text(strip=True)  # Get text content of the section
        print(section_content)
    else:
        print("Section not found!")


dataContainerClass1 = "styles_item__kyxZ3"
dataContainerClass2 = "styles_minorPositive__2vbjs"

# download_web_pages("e24aksjer", "https://e24.no/bors")

m_stock = aksjer24()
# contentContainer = """<section class="overview_section__K48df overview_main__sZ_nI">"""

fileName = "htmlFiles/test.html"
elementType = "section"
elementClass = "overview_section__K48df overview_main__sZ_nI"

get_content_element_from_file(fileName, elementType, elementClass)
# get_element_content(html_content, element_class)

# section = soup.find("section", class_="overview_section__K48df overview_main__sZ_nI")
# m_stock.
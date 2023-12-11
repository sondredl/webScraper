#!/usr/bin/env python
from bs4 import BeautifulSoup


def get_article_from_url(filename):
    # with open("article.html", "r", encoding="utf-8") as file:
    with open(filename, "r", encoding="utf-8") as file:
        html_content = file.read()

    soup = BeautifulSoup(html_content, "html.parser")

    title_tag = soup.title
    subtitle_tag = soup.find(["h2", "h3", "h4", "h5", "h6", "p"])

    title = title_tag.text.strip() if title_tag else "No Title Found"
    subtitle = subtitle_tag.text.strip() if subtitle_tag else "No Subtitle Found"

    text = "\n".join([p.text.strip() for p in soup.find_all("p")])

    with open("content.txt", "w", encoding="utf-8") as output_file:
        output_file.write(f"Title: {title}\n")
        output_file.write(f"Subtitle: {subtitle}\n\n")
        output_file.write(f"Text:\n{text}")

    print("Extraction completed. Check content.txt for the result.")

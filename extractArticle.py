#!/usr/bin/env python
from bs4 import BeautifulSoup

# Read HTML from file
with open('article.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract title and subtitle
title_tag = soup.title
subtitle_tag = soup.find(['h2', 'h3', 'h4', 'h5', 'h6', 'p'])

title = title_tag.text.strip() if title_tag else 'No Title Found'
subtitle = subtitle_tag.text.strip() if subtitle_tag else 'No Subtitle Found'

# Extract text
text = '\n'.join([p.text.strip() for p in soup.find_all('p')])

# Write result to content.txt
with open('content.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(f'Title: {title}\n')
    output_file.write(f'Subtitle: {subtitle}\n\n')
    output_file.write(f'Text:\n{text}')

print('Extraction completed. Check content.txt for the result.')

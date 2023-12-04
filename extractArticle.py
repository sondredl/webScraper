from bs4 import BeautifulSoup

# Read HTML from file
with open('article.html', 'r', encoding='utf-8') as file:
    html_content = file.read()

# Parse HTML using BeautifulSoup
soup = BeautifulSoup(html_content, 'html.parser')

# Extract title and text
title = soup.title.text.strip() if soup.title else 'No Title Found'
text = '\n'.join([p.text.strip() for p in soup.find_all('p')])

# Write result to content.txt
with open('content.txt', 'w', encoding='utf-8') as output_file:
    output_file.write(f'Title: {title}\n\n')
    output_file.write(f'Text:\n{text}')

print('Extraction completed. Check content.txt for the result.')

import requests
from bs4 import BeautifulSoup

url = "https://www.finansavisen.no/energi/2023/12/02/8066756/exxonmobil-pa-klimatoppmote-fokusert-for-mye-pa-fornybar-energi"
output_file = "article.html"

# Send a GET request to the URL
response = requests.get(url)

# Check if the request was successful (status code 200)
if response.status_code == 200:
    # Parse the HTML content of the page
    soup = BeautifulSoup(response.text, 'html.parser')

    # Save the HTML content to a file
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(str(soup))

    print(f"Webpage content saved to {output_file}")
else:
    print(f"Failed to retrieve webpage. Status code: {response.status_code}")

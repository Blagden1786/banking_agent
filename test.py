import requests
from bs4 import BeautifulSoup

url = 'https://www.natwest.com/savings.html'
response = requests.get(url)

# Parse the source code using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

print(soup)

import requests
from bs4 import BeautifulSoup
page = requests.get("https://www.cs.washington.edu/education/courses/")
print (page)

soup = BeautifulSoup(page.content, 'html.parser')
rows = list(soup.find_all('div', class_='views-row'))
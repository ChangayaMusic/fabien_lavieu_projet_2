import requests
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
h3_tags = soup.find_all('h3')
product_links = []
for h3 in h3_tags:
    href = h3.a['href']
    product_link = 'http://books.toscrape.com/catalogue/' + href
    product_links.append(product_link)
    print(product_link)


















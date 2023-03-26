import requests
from bs4 import BeautifulSoup
from csv import DictWriter

url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')
product_links = []

def get_all_products_links():
    h3_tags = soup.find_all('h3')
    print(h3_tags)

    for h3 in h3_tags:
        href = h3.a['href']
        print(href)
        product_link = url + href
        product_links.append(product_link)
        print(product_link)

get_all_products_links()
print()
















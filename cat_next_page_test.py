from csv import DictWriter
from requests import get
from bs4 import BeautifulSoup

url_c = 'http://books.toscrape.com/catalogue/category/books_1/index.html'

def next():


    print(url_c)
    response_c = get(url_c)
    print(response_c)
    soup_c = BeautifulSoup(response_c.text, 'html.parser')
    quantity = soup_c.find(class_="next")
    next_page = quantity.find('a').get("href")
    print(quantity)
    print(next_page)
    next_url = url_c.replace("index.html", next_page)
    print(next_url)
next()


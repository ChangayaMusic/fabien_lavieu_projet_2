from csv import DictWriter
from requests import get
from bs4 import BeautifulSoup
from math import ceil

url_c = 'http://books.toscrape.com/catalogue/category/books_1/index.html'
print(url_c)
response_c = get(url_c)
print(response_c)
soup_c = BeautifulSoup(response_c.text, 'html.parser')
quantity = soup_c.find(class_="form-horizontal").text
print(quantity)
quantity_nb= quantity[3:5]
print(quantity_nb)
page_nb = ceil((int(quantity_nb)/20))
print(page_nb)

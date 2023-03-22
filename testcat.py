from bs4 import BeautifulSoup
import requests

url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/index.html'
print(url)
response = get(url)
print(response)
soup_mystery = BeautifulSoup(response.text, 'html.parser')
quantity = soup_mystery.find(style="display:none")
print(quantity)
    
    
   
    

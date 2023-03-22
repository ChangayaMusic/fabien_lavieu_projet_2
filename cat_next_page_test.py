import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/'

while True:

    response = requests.get(url)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")
    footer = soup.select_one('li.current')
    print(footer.text.strip())
    next_page = soup.select_one('li.next>a')
    print(next_page)
    if next_page:
        next_url = next_page.get('href')
        print(next_url)
        url = urljoin(url, next_url)
        print(url)
    else:
        break







import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/'
next_page_url = []
product_links = []
def get_book_data():

    print(url)



#if __name__ == '__main__':
def csv():
    data = get_book_data(url)
    with open('informations.csv', "w", newline="") as csvfile:
        fieldnames = data.keys()
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data)



def get_all_products_links():
    h3_tags = soup.find_all('h3')
    print(h3_tags)

    for h3 in h3_tags:
        href = h3.a['href']
        print(href)
        product_link = url + href
        product_links.append(product_link)
        print(product_link)

while True:
    next_page_url.append(url)
    response = requests.get(url)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")
    footer = soup.select_one('li.current')
    print(footer.text.strip())
    next_page = soup.select_one('li.next>a')
    if next_page:
        next_url = next_page.get('href')
        url = urljoin(url, next_url)
        print(url)
    else:
        break
print(next_page_url)

for i in next_page_url:
    url = i
    get_all_products_links()
print(product_links)

for bk in product_links:
    url = bk
    get_book_data()





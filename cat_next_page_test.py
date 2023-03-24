import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from csv import DictWriter

url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/'
next_page_url = []
product_links = []
informations_list = []

def get_book_data():

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="table table-striped")
    informations = []

    for row in table.find_all("tr"):

        type = row.find('th').text
        info = row.find('td').text
        informations.append(info)
    informations_list.append(informations)

    print(informations)

def scrap_to_csv():
    with open("v3.csv", "w", newline="") as csv_file:
        print(informations_list)
        header = ['UPC', 'Product Type', 'Price (excl. tax)', 'Price (incl. tax)', 'Tax', 'Availability',
                  'Number of reviews']
        writer = csv.writer(csv_file)  # create a DictWriter object with the header list as fieldnames
        writer.writerow(header)  # write the header to the csv file
        writer.writerows(informations_list)


def get_all_products_links():
    h3_tags = soup.find_all('h3')
    print(h3_tags)

    for h3 in h3_tags:
        href = h3.a['href']
        href = href[9:]
        print(href)
        product_link = "http://books.toscrape.com/catalogue/" + href
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
        print(next_url)
        url = urljoin(url, next_url)
        print(url)
    else:
        break
print(next_page_url)

for i in next_page_url:
    url = i
    get_all_products_links()
print(product_links)

for p in product_links:
    url = p

    get_book_data()

scrap_to_csv()


















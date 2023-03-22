from csv import DictWriter
from requests import get
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/'

def get_book_data(url):

    print(url)
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    titre = soup.find('h1').text

    informations = {titre: url}

    for row in rows:
        informations[row.find('th').text] = row.find('td').text
    print(informations)
    return informations

#if __name__ == '__main__':
def csv():
    data = get_book_data(url)
    with open('informations.csv', "w", newline="") as csvfile:
        fieldnames = data.keys()
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data)

def nextpage():
    url_a = ""
    url_c = url + url_a
    print(url_c)
    response_c = get(url_c)
    print(response_c)
    soup_c = BeautifulSoup(response_c.content, 'html.parser')
    quantity = soup_c.find(class_="next")
    print(type(quantity))
    next_page = quantity.find('a').get("href")
    print(quantity)
    print(next_page)
    url_ = next_page



nextpage()
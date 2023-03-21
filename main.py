from csv import DictWriter

from requests import get
from bs4 import BeautifulSoup

def get_book_data(url):
    response = get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    table = soup.find('table')
    rows = table.find_all('tr')
    informations = {}
    for row in rows:
        informations[row.find('th').text] = row.find('td').text
    print(informations)
    return informations

if __name__ == '__main__':
    data = get_book_data("http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html")
    with open("informations.csv", "w", newline="") as csv_file:
        fieldnames = data.keys()
        writer = DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data)
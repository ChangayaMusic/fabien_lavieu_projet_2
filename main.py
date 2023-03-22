from csv import DictWriter
from requests import get
from bs4 import BeautifulSoup

url = 'http://books.toscrape.com/catalogue/a-light-in-the-attic_1000/index.html'

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

if __name__ == '__main__':

    data = get_book_data(url)
    with open('informations.csv', "w", newline="") as csvfile:
        fieldnames = data.keys()
        writer = DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerow(data)
from csv import DictWriter
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin



def get_book_data(url):

    print(url)
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


url = 'http://books.toscrape.com/catalogue/category/books/sequential-art_5/'
cat_url = []

while True:
    cat_url.append(url)
    response = requests.get(url)
    print(response)
    soup_url = BeautifulSoup(response.content, "html.parser")
    footer = soup_url.select_one('li.current')
    print(footer.text.strip())
    next_page = soup_url.select_one('li.next>a')
    if next_page:
        next_url = next_page.get('href')
        url = urljoin(url, next_url)
        print(url)


    else:
        break


print(cat_url)
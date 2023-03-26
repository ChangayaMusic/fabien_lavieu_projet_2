import csv

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from csv import DictWriter
next_page_url = []
product_links = []
informations_list = []
links_words = []

url = "http://books.toscrape.com/catalogue/alice-in-wonderland-alices-adventures-in-wonderland-1_5/index.html"

def get_book_data():

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="table table-striped")


    links = soup.find_all("a")
    for link in links:
        links_words.append(link.string)
    #print(links_words)
    category = links_words[3]
   #print(category)

    title = soup.find('h1').text

    product_info = []
    product_page_url = url

    informations = []


    ratings = soup.find_all('article', class_='product_pod')

    for article in ratings:

        stars = article.find('p')
        review_rating = stars['class'][1]

    image = soup.find("img", class_="thumbnail")
    image_url = urljoin(url, image["src"])

    description = soup.find("div", id="product_description")
    if description is not None:  # check if description is not None
        product_description = description.find_next_sibling("p").text
    else:
        product_description = ""  # assign an empty string or some default value



    for row in table.find_all("tr"):

        type = row.find('th').text
        info = row.find('td').text

        informations.append(info)
    universal_product_code = informations[0]
    price_excluding_tax = informations[2]
    price_including_tax = informations[3]
    number_available = informations[5]

    info_list = []
    #informations_list.append(informations)
    info_list.append(product_page_url)
    info_list.append(universal_product_code)
    info_list.append(title)
    info_list.append(price_excluding_tax)
    info_list.append(price_including_tax)
    info_list.append(number_available)
    info_list.append(product_description)
    info_list.append(category)
    info_list.append(review_rating)
    info_list.append(image_url)
    informations_list.append(info_list)
    #print(informations)
    #print(review_rating)
    #print(img_url)

with open("v3.csv", "w", newline="") as csv_file:
    get_book_data()
    print(informations_list)
    header = ['Title', 'Product_page_url', 'Review_rating', 'Product_description', 'image_url', 'UPC',
              'Product Type', 'Price (excl. tax)', 'Price (incl. tax)', 'Tax', 'Availability',
              'Number of reviews']


    writer = csv.writer(csv_file)
    writer.writerow(header)
    writer.writerow(informations_list)






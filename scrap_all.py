import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
from csv import DictWriter

url = 'http://books.toscrape.com/catalogue/category/books/mystery_3/'
next_page_url = []
product_links = []

info_list = []
links_words = []
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
    product_description = description.find_next_sibling("p").text



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



with open('categories.csv', 'r') as f:
    csv_import_links = []
    reader = csv.reader(f)
    for row in reader:
        print(row)
        csv_import_links = row
for cat_link in csv_import_links:
    informations_list = []
    url = cat_link
    csv_name = url[51:].replace("/index.html","") + ".csv"
    print(url)

    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print(csv_name)
    while True:
        next_page_url.append(url)
        response = requests.get(url)
        print(response)
        soup = BeautifulSoup(response.content, "html.parser")
        footer = soup.select_one('li.current')

        next_page = soup.select_one('li.next>a')
        if next_page:
            next_url = next_page.get('href')
            print(next_url)
            url = urljoin(url, next_url)
            print(url)
        else:
            break
    print(next_page_url)
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    for i in next_page_url:
        url = i
        get_all_products_links()
    print(product_links)
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    print("------------------------------------------------------------")
    for p in product_links:
        url = p
        print(url)
        get_book_data()
        print("--------- ONE MORE BOOK ------------")

    with open(csv_name, "w", newline="", encoding="utf-8") as csv_file:




        print(informations_list)
        header = ['Title', 'Product_page_url', 'Review_rating', 'Product_description', 'image_url', 'UPC',
                  'Product Type', 'Price (excl. tax)', 'Price (incl. tax)', 'Tax', 'Availability',
                  'Number of reviews']

        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(informations_list)
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print("---------CSV CREATED----------------------------------------")
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
        print("------------------------------------------------------------")
















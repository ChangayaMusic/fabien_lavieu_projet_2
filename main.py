import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import csv
import os


categories_links = []

links_words = []
categories_links_dict = {}

links_to_scrap = []
images_urls = []
categorie_to_download = ""
categorie_selection = []
categorie_selection_all_pages = []


def get_all_categories_links():
    categories_keys = []
    category_links_list = []
    category_name_list = []
    category_dict = {}
    url = 'http://books.toscrape.com/'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    nav_tags = soup.find(class_="nav nav-list")
    nav = nav_tags.find_all('a')

    print(nav)

    for e in nav:
        # print(e)
        nav_text = e.text.replace('\n', '').strip()
        category_name_list.append(nav_text)

        # print(h_text)
        link_category = e['href']

        category_links_list.append(url + link_category)


    print(category_name_list)
    print(category_links_list)
    categories_links_dict = dict(zip(category_name_list, category_links_list))
    print(categories_links_dict)


    for index, value in enumerate(categories_links_dict):
        print(index, value)
    my_index = int(input('Please choose an index for my list: ( 0 to select all) '))
    categorie_to_download = category_links_list[my_index]

    categorie_selection.append(categorie_to_download)
    categorie_selection_all_pages.append(categorie_to_download)


    print("WE ARE SCRAPING :")
    print(categorie_to_download)




def get_all_pages():

    informations_list = []

    print(categorie_selection_all_pages)
    for cat_link in categorie_selection:
        next_page_url = []
        all_pages_categorie = []
        url = cat_link
        next_page_url.append(url)
        csv_name = url[51:].replace("/index.html", "")


        while True:



            response = requests.get(url)
            #print(response)
            soup = BeautifulSoup(response.content, "html.parser")
            footer = soup.select_one('li.current')

            next_page = soup.select_one('li.next>a')

            if next_page:
                next_url = next_page.get('href')
                #print(next_url)
                url = urljoin(url, next_url)
                print(url)
                categorie_selection_all_pages.append(url)
            else:
                categorie_name = csv_name
                categories_links_dict[categorie_name] = next_page_url
                break

    #print(categorie_selection_all_pages)
        #print(next_page_url)
        #print(categorie_name)
    #category_name_list = category_name_list[1:51]

def get_all_products_links():
    url = ""

    product_links = []
    pages_links = []

    categorie_to_download = ""

    #print(categorie_selection_all_pages)
    for p_l in categorie_selection_all_pages:

        url = p_l
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        h3_tags = []
        h3_tags = soup.find_all('h3')
        for h3 in h3_tags:
            href = h3.a['href']

            href = href.replace("../", "")
            #print(href)
            product_link = "http://books.toscrape.com/catalogue/" + href
            #print(product_link)
            product_links.append(product_link)

    for pr_l in product_links:
        links_to_scrap.append(pr_l)

    print(links_to_scrap)

def get_book_data():

    informations_list = []
    links_words = []
    counter = 1

    for u in links_to_scrap:

        url = u

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="table table-striped")
        print(counter, "book(s) scraped of", len(links_to_scrap))

        counter = counter + 1

        links = soup.find_all("a")
        for link in links:

            links_words.append(link.string)
        #print(links_words)

        if len(links_words) > 3:
            category = links_words[3]
        else:
            category = "all books"



        title = soup.find('h1').text
        print(title)
        print("###################################")

        product_info = []
        product_page_url = url

        informations = []
        review_rating = ""

        ratings = soup.find_all('article', class_='product_pod')

        for article in ratings:

            stars = article.find('p')
            review_rating = stars['class'][1]

        img_soup = BeautifulSoup(response.content, "html.parser")

        img_src = img_soup.find("img")["src"]
        img_url = "http://books.toscrape.com/"+ img_src
        #print(img_url)
        images_urls.append(img_url)

        description = soup.find("div", id="product_description")
        if description is not None:
            product_description = description.find_next_sibling("p").text
        else:
            product_description = " "



        for row in table.find_all("tr"):

            type = row.find('th').text
            info = row.find('td').text

            informations.append(info)
        universal_product_code = informations[0]
        price_excluding_tax = informations[2]
        price_including_tax = informations[3]
        number_available = informations[5]

        info_list = []

        info_list.append(title)
        info_list.append(product_page_url)
        info_list.append(review_rating)
        info_list.append(product_description)
        info_list.append(img_url)
        info_list.append(universal_product_code)
        info_list.append(price_excluding_tax)
        info_list.append(price_including_tax)
        info_list.append(number_available)
        #info_list.append(category)
        informations_list.append(info_list)
        #4print(informations)
        #print(review_rating)
        #print(img_url)

        csv_title = category + ".csv"

    with open(csv_title, "w", newline="", encoding="utf-8") as csv_file:

        #print(informations_list)

        header = ['Title', 'Product_page_url', 'Review_rating', 'Product_description', 'image_url', 'UPC',
                   'Price (excl. tax)', 'Price (incl. tax)', 'Availability']

        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(informations_list)

    print("Csv crated named:", csv_title)

def download_images():


    #print(images_urls)
    counter = 1
    answer = input('Do you want to download images? (yes/no) ')
    if answer == 'yes':

        for i_u in images_urls:
            url = i_u
            response = requests.get(url)
            folder = "images"  # create a folder name
            os.makedirs(folder, exist_ok=True)  # create the folder if it does not exist
            image_name = os.path.basename(url)  # get the image name from the url
            image_path = os.path.join(folder, image_name)  # join the folder name and image name
            with open(image_path, "wb") as img:  # open the file for writing
                img.write(response.content)  # write the image content

            print(counter, "image(s) downloaded of", len(images_urls))

            counter = counter+1
    else:
        print('See you later!')


def what_to_do():

        while True:
            answer = input('Do you want to download a single book? (yes/no) ')
            if answer == 'yes':
                url_input = input("Enter URL: ")
                links_to_scrap.append(url_input)
                get_book_data()
                download_images()
                print("Books scraped :")
                print(len(links_to_scrap))
                print("Images scraped :")
                print(len(images_urls))
            else:
                get_all_categories_links()
                print(categories_links)
                print("CATEGORIES LINKS READY")
                get_all_pages()
                print("OTHERS PAGES LINKS READY")
                print(categories_links_dict)

                get_all_products_links()
                print(links_to_scrap)
                print(len(links_to_scrap))
                print(categorie_to_download)
                print("ALL LINKS READY")
                get_book_data()
                print(links_words)
                download_images()
                print("Books scraped :")
                print(len(links_to_scrap))
                print("Images scraped :")
                print(len(images_urls))
                answer_loop()
                break
def answer_loop():
    answer = input("Do you want scrap book(s) again? (yes/no) ")
    if answer.lower() != "y":
        what_to_do()
    else:
        print("see you later")





what_to_do()













import requests # to do url requets
from bs4 import BeautifulSoup # scraping tool
from urllib.parse import urljoin # to generate clean urls with elements
import csv # to create CSV files
import os # to create folders and save img


categories_links = []
links_words = []
categories_links_dict = {}
categories_links_dict_all_pages = {}
links_to_scrap = []
categorie_to_download = {}
categorie_selection = []
categorie_selection_all_pages = []
categories_links_dict_all_pages = {}
full_dict = {}
images_dict = {}

def get_all_categories_links():
    global categories_links_dict
    categories_keys = []
    category_links_list = []
    category_name_list = []
    url = 'http://books.toscrape.com/'

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    nav_tags = soup.find(class_="nav nav-list")
    nav = nav_tags.find_all('a') # find all categories from nav bar


    for e in nav:

        nav_text = e.text.replace('\n', '').strip()
        category_name_list.append(nav_text)      # get categories names and put in a list
        link_category = e['href'] # get then the complement of base url
        category_links_list.append([url + link_category])# combine both and add cat url to a list

    categories_links_dict = dict(zip(category_name_list, category_links_list)) # add to shared dict
    print(categories_links_dict.keys())

def get_all_pages():

    informations_list = []
    key_list = []

    global categories_links_dict_all_pages
    del categories_links_dict['Books']

    for key in categories_links_dict: # get links for each category in the dict

        key_list =[]
        next_page_url = []
        all_pages_categorie = []

        url = "".join(categories_links_dict[key])
        next_page_url.append(url)

        print(url)
        key_list.append(key)

        csv_name = url[51:].replace("/index.html", "")

        while True: # while true go to next page

            response = requests.get(url)
            #print(response)
            soup = BeautifulSoup(response.content, "html.parser")
            footer = soup.select_one('li.current')

            next_page = soup.select_one('li.next>a')

            if next_page:
                next_url = next_page.get('href')
                #print(next_url)
                url = urljoin(url, next_url)
                next_page_url.append(url)
                #print(url)

            else:
                categorie_name = csv_name

                break

        categories_links_dict[key] = next_page_url
        categories_links_dict_all_pages = categories_links_dict # add result to a dict

def get_all_products_links():

    global full_dict
    global product_links


    for key in categories_links_dict_all_pages:

        product_links = []
        pages_links = []
        for l in categories_links_dict_all_pages[key]:

            url = l
            print(url)
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")

            h3_tags = []
            h3_tags = soup.find_all('h3')#h3 tags are the link container
            for h3 in h3_tags:
                href = h3.a['href']

                href = href.replace("../", "") # clean href
                print(href)
                product_link = "http://books.toscrape.com/catalogue/" + href
                # combine to get clean url
                product_links.append(product_link)
        full_dict[key]=product_links # save cleans urls to a dict
    print("######################################################")
    print(full_dict)

def get_book_data(): # get all data from a book page

    links_words = []

    print(full_dict)
    for key in full_dict : # create a folder for each category
        images_dict = {}

        informations_list = []
        images_urls = []
        links_to_scrap = full_dict[key]
        print(links_to_scrap)
        print(key)
        folder_csv = "data/" + key + "/"
        os.makedirs(folder_csv, exist_ok=True)
        csv_title = folder_csv+ key + ".csv" # csv name for each category
        counter = 1


        for u in links_to_scrap: #scrap book s datas
            url = u
            response = requests.get(url)
            soup = BeautifulSoup(response.text, "html.parser")
            table = soup.find("table", class_="table table-striped")
            print(counter, "book(s) scraped of", len(links_to_scrap))

            links = soup.find_all("a")

            for link in links:

                links_words.append(link.string)


            if len(links_words) > 3:  # all books category appear blank so we ask to correct it
                category = links_words[3]
            else:
                category = "all books"

            title = soup.find('h1').text # get title
            print(title)
            print("###################################")

            product_info = []
            product_page_url = url # get product page url


            informations = []
            review_rating = ""

            ratings = soup.find_all('article', class_='product_pod')

            for article in ratings: # looking for rating location

                stars = article.find('p')
                review_rating = stars['class'][1]

            img_soup = BeautifulSoup(response.content, "html.parser")

            img_src = img_soup.find("img")["src"] #get image url
            img_url = "http://books.toscrape.com/"+ img_src
            #print(img_url)
            images_urls.append(img_url)

            description = soup.find("div", id="product_description")

            if description is not None: # a book has no description so need to give a value
                product_description = description.find_next_sibling("p").text
            else:
                product_description = "UNAVAILABLE "

            for row in table.find_all("tr"): # look all table row

                info = row.find('td').text

                informations.append(info) #send all to list
            universal_product_code = informations[0] # define which infos
            price_excluding_tax = informations[2]
            price_including_tax = informations[3]
            number_available = informations[5]

            info_list = []

            info_list = [title, product_page_url, review_rating, product_description, img_url,
                         universal_product_code, price_excluding_tax, price_including_tax,
                         number_available, category]

            informations_list.append(info_list)
            #4print(informations)
            #print(review_rating)
            #print(img_url)
            counter = counter + 1


        #create CSV
        with open(csv_title, "w", newline="", encoding="utf-8") as csv_file:

            #print(informations_list)

            header = ['Title', 'Product_page_url', 'Review_rating', 'Product_description',
                      'image_url', 'UPC', 'Price (excl. tax)', 'Price (incl. tax)',
                      'Availability', 'Category']

            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerows(informations_list)

        counter_img = 1

        for i in images_urls: #download images

            url = i
            response = requests.get(url)
            folder = "data/" + key + "/" + "images/" #define file structure

            os.makedirs(folder, exist_ok=True)  # create the folder if it does not exist
            image_name = os.path.basename(url)  # get the image name from the url
            image_path = os.path.join(folder, image_name)  # join the folder name and image name
            with open(image_path, "wb") as img:  # open the file for writing
                img.write(response.content)  # write the image content

            print(counter_img, "image(s) downloaded of", len(images_urls))
            counter_img = counter_img + 1

        print("Csv crated named:", csv_title)


def individuals_categories(): # function to use in main scrip

    get_all_categories_links()
    print("--------------------------------")

    get_all_pages()
    print("------------------------------")

    get_all_products_links()
    get_book_data()
    print(images_dict)

individuals_categories()























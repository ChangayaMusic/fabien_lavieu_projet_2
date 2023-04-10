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
images_urls = []

def is_valid_url(url):
    try:
        response = requests.head(url)
        return response.ok
    except:
        return False
def get_all_categories_links():
    global categories_links_dict
    categories_dict = {}
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
    #######


    categories_dict = dict(zip(category_name_list, category_links_list)) # add to shared dict
    print(categories_dict.keys())
    del categories_dict['Books']

    print(categories_dict)

    for index, value in enumerate(categories_dict):
        print(index, value)
    my_index = int(input('Please choose an index for my list: ( 50 to select all) '))

    if my_index == 50:
        categories_links_dict = categories_dict
        print("We are scraping all categories")
    else:
        index = int(my_index)
        if my_index < len(categories_dict):
            key = list(categories_dict.keys())[index]
            value = categories_dict[key]
            categories_links_dict = {key: value}
            print("We are scraping:", categories_links_dict)
        else:
            print("The index is out of range.")

def get_all_pages():

    print("Looking for next pages")

    informations_list = []


    global categories_links_dict_all_pages


    for key in categories_links_dict: # get links for each category in the dict


        next_page_url = []
        all_pages_categorie = []

        url = "".join(categories_links_dict[key])
        next_page_url.append(url)




        csv_name = url[51:].replace("/index.html", "")

        while True: # while true go to next page

            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            footer = soup.select_one('li.current')

            next_page = soup.select_one('li.next>a')

            if next_page:
                next_url = next_page.get('href')
                url = urljoin(url, next_url)
                next_page_url.append(url)

            else:
                categorie_name = csv_name

                break
        print(next_page_url)

        categories_links_dict[key] = next_page_url
        categories_links_dict_all_pages = categories_links_dict # add result to a dict

def get_all_products_links():

    print("Looking for all products pages2")

    global full_dict
    global product_links


    for key in categories_links_dict_all_pages:

        product_links = []

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


def get_book_data(): # get all data from a book page

    links_words = []
    global images_dict

    for key in full_dict : # create a folder for each category
        images_dict[key] = key
        images_urls = []
        informations_list = []

        links_to_scrap = full_dict[key]
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

            counter = counter + 1

        images_dict[key] = images_urls
    #create CSV
        with open(csv_title, "w", newline="", encoding="utf-8") as csv_file:

            header = ['Title', 'Product_page_url', 'Review_rating', 'Product_description',
                      'image_url', 'UPC', 'Price (excl. tax)', 'Price (incl. tax)',
                      'Availability', 'Category']

            writer = csv.writer(csv_file)
            writer.writerow(header)
            writer.writerows(informations_list)
            print("Csv crated named:", csv_title)

    get_img()

def get_data_single_book():
    global images_dict
    images_urls = []
    informations_list = []
    url = ''

    url_input = input("Enter a URL: ")
    if is_valid_url(url_input):
        url = url_input
    else:
        print(" /!\/!\/!\/!\/!\/!\/!\ ")
        print("  /!\ Wrong URL /!\ ")
        print(" /!\/!\/!\/!\/!\/!\/!\ ")
        print(f"{url_input} is not a valid URL")
        menu()

    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    table = soup.find("table", class_="table table-striped")


    links = soup.find_all("a")

    for link in links:
        links_words.append(link.string)

    if len(links_words) > 3:  # all books category appear blank so we ask to correct it
        category = links_words[3]
    else:
        category = "all books"

    title = soup.find('h1').text  # get title
    print(title)
    print("###################################")

    product_info = []
    product_page_url = url  # get product page url

    informations = []
    review_rating = ""

    ratings = soup.find_all('article', class_='product_pod')

    for article in ratings:  # looking for rating location

        stars = article.find('p')
        review_rating = stars['class'][1]

    img_soup = BeautifulSoup(response.content, "html.parser")

    img_src = img_soup.find("img")["src"]  # get image url
    img_url = "http://books.toscrape.com/" + img_src
    images_urls.append(img_url)  # print(img_url)

    description = soup.find("div", id="product_description")

    if description is not None:  # a book has no description so need to give a value
        product_description = description.find_next_sibling("p").text
    else:
        product_description = "UNAVAILABLE "

    for row in table.find_all("tr"):  # look all table row

        info = row.find('td').text

        informations.append(info)  # send all to list
    universal_product_code = informations[0]  # define which infos
    price_excluding_tax = informations[2]
    price_including_tax = informations[3]
    number_available = informations[5]

    info_list = []

    info_list = [title, product_page_url, review_rating, product_description, img_url,
                 universal_product_code, price_excluding_tax, price_including_tax,
                 number_available, category]

    informations_list.append(info_list)

    folder_csv = "data/" + title + "/"
    os.makedirs(folder_csv, exist_ok=True)
    csv_title = folder_csv + title + ".csv"  # csv name for each category

    menu()



# create CSV
    with open(csv_title, "w", newline="", encoding="utf-8") as csv_file:

        header = ['Title', 'Product_page_url', 'Review_rating', 'Product_description',
                  'image_url', 'UPC', 'Price (excl. tax)', 'Price (incl. tax)',
                  'Availability', 'Category']

        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(informations_list)
        print("Csv crated named:", csv_title)

    images_dict = {title:images_urls}
    get_img()

def get_img():

    for key in images_dict:
        print("######################################################################")
        print(key)

        counter_img = 1

        for i in images_dict[key]: #download images

            url = i
           
            response = requests.get(url)
            folder = "data/" + key + "/" + "images/" #define file structure

            os.makedirs(folder, exist_ok=True)  # create the folder if it does not exist
            image_name = os.path.basename(url)  # get the image name from the url
            image_path = os.path.join(folder, image_name)  # join the folder name and image name
            with open(image_path, "wb") as img:  # open the file for writing
                img.write(response.content)  # write the image content

            print(counter_img, "image(s) downloaded of", len(images_dict[key]))
            counter_img = counter_img + 1




def individuals_categories(): # function to use in main scrip

    get_all_categories_links()
    print("--------------------------------")

    get_all_pages()
    print("------------------------------")

    get_all_products_links()
    print("------------------------------")
    get_book_data()
    print("------------------------------")
    menu()

def selection(): # ask what to do and return a choice
    print(
        """What do we scrap today ? :
        1: Single book scrap
        2: Category(ies) scrap
        3: Exit"""

    )
    choice = input("Your selection ? ")
    return choice

def menu(): # get the choice and run the appropriate function
    options = {
        1: lambda: get_data_single_book(),
        2: lambda: individuals_categories(),
        3: lambda: quit()
           }

    choice = selection()
    while not choice.isdigit() or int(choice) < 1 or int(choice) > 4:
        print("Invalid option")
        choice = selection()

    options[int(choice)]()


if __name__ == "__main__":

    menu()




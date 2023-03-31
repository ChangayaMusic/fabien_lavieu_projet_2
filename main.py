import requests # to do url requets
from bs4 import BeautifulSoup # scraping tool
from urllib.parse import urljoin # to generate clean urls with elements
import csv # to create CSV files
import os # to create folders and save img


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
    nav = nav_tags.find_all('a') # find all categories from nav bar

    print(nav)

    for e in nav:
        # print(e)
        nav_text = e.text.replace('\n', '').strip()
        category_name_list.append(nav_text) # get categories names and put in a list

        # print(h_text)
        link_category = e['href'] # get then the complement of base url

        category_links_list.append(url + link_category) # combine both and add cat url to a list


    print(category_name_list)
    print(category_links_list)
    categories_links_dict = dict(zip(category_name_list, category_links_list))
    # create a dict to associate name and url
    print(categories_links_dict)

    # to chose from the dict a category and get its url
    for index, value in enumerate(categories_links_dict):
        print(index, value)
    my_index = int(input('Please choose an index for my list: ( 0 to select all) '))

    if 0 <= my_index <= 50: # 50 cat so we need to choose a number btw 0 and 50
        print("Value is between 0 and 50")
        categorie_to_download = category_links_list[my_index]

        categorie_selection.append(categorie_to_download)
        categorie_selection_all_pages.append(categorie_to_download)

    else: # else tell usr its wrong
        print(" /!\/!\/!\/!\/!\/!\/!\ ")
        print("  /!\ Wrong value /!\ ")
        print(" /!\/!\/!\/!\/!\/!\/!\ ")
        menu()

    print("WE ARE SCRAPING :")
    print(categorie_to_download)

def get_all_pages():

    informations_list = []

    print(categorie_selection_all_pages)
    for cat_link in categorie_selection: # check if next page exists
        next_page_url = []
        all_pages_categorie = []
        url = cat_link
        next_page_url.append(url)
        csv_name = url[51:].replace("/index.html", "") # back up category name

        while True: # while true go to next page

            response = requests.get(url)
            soup = BeautifulSoup(response.content, "html.parser")
            next_page = soup.select_one('li.next>a')

            if next_page: # if exist save it in a list
                next_url = next_page.get('href')
                #print(next_url)
                url = urljoin(url, next_url)
                categorie_selection_all_pages.append(url)
            else: # if not save found links to the dict
                categorie_name = csv_name
                categories_links_dict[categorie_name] = next_page_url
                break


def get_all_products_links(): # get all products link of each pages
    url = ""

    product_links = []
    pages_links = []
    categorie_to_download = ""


    for p_l in categorie_selection_all_pages:

        url = p_l
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        h3_tags = [] # h3 tags are the link container
        h3_tags = soup.find_all('h3')
        for h3 in h3_tags:
            href = h3.a['href']

            href = href.replace("../", "") # clean href
            #print(href)
            product_link = "http://books.toscrape.com/catalogue/" + href # combine to get clean url
            #print(product_link)
            product_links.append(product_link)

    for pr_l in product_links:  # save cleans urls to a list
        links_to_scrap.append(pr_l)

    print(links_to_scrap)

def get_book_data(): # get all data from a book page

    informations_list = []
    links_words = []
    counter = 1

    for u in links_to_scrap:

        url = u

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        table = soup.find("table", class_="table table-striped") # special soup for table
        print(counter, "book(s) scraped of", len(links_to_scrap))

        counter = counter + 1

        links = soup.find_all("a")

        for link in links: # all books categorie appear blank so we ask to correct it
            links_words.append(link.string)

        if len(links_words) > 3:
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

        img_soup = BeautifulSoup(response.content, "html.parser") # new soup need content for img

        img_src = img_soup.find("img")["src"] #get image url
        img_url = "http://books.toscrape.com/" + img_src
        images_urls.append(img_url)

        description = soup.find("div", id="product_description")

        if description is not None: # a book has no description so need to give a value
            product_description = description.find_next_sibling("p").text
        else:
            product_description = " UNAVAILABLE "

        for row in table.find_all("tr"): # look all table row

            info = row.find('td').text
            informations.append(info) #send all to list
        # define which infos
        universal_product_code = informations[0]
        price_excluding_tax = informations[2]
        price_including_tax = informations[3]
        number_available = informations[5]

        info_list = []

        info_list = [title, product_page_url, review_rating, product_description, img_url,
                     universal_product_code, price_excluding_tax, price_including_tax,
                     number_available, category] # put all infos together

        csv_title = category + ".csv"

    with open(csv_title, "w", newline="", encoding="utf-8") as csv_file: # create csv

        header = ['Title', 'Product_page_url', 'Review_rating', 'Product_description', 'image_url', 'UPC',
                   'Price (excl. tax)', 'Price (incl. tax)', 'Availability', 'Category']

        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerows(informations_list)

    print("Csv crated named:", csv_title)

def download_images():


    counter = 0
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

            counter = counter + 1
            print(counter, "image(s) downloaded of", len(images_urls))


    else:
        print('See you later!')

def is_valid_url(url):
    try:
        response = requests.head(url)
        return response.ok
    except:
        return False


def single_book():

    url_input = input("Enter a URL: ")
    if is_valid_url(url_input):
        links_to_scrap.append(url_input)
        get_book_data()
        download_images()
        print("Books scraped :")
        print(len(links_to_scrap))
        print("Images scraped :")
        print(len(images_urls))
        menu()

    else:
        print(" /!\/!\/!\/!\/!\/!\/!\ ")
        print("  /!\ Wrong URL /!\ ")
        print(" /!\/!\/!\/!\/!\/!\/!\ ")
        print(f"{url_input} is not a valid URL")
        menu()

def single_category():

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
    menu()

def all_categries(): # use a modified version of this script
    # to get all categories but keep tree structure
    # 0 option in choose category put all in one folder
    # to dont run a heavy script if only few datas needed


    from scrap_all_individual import individuals_categories
    individuals_categories()
    menu()

def selection(): # ask what to do and return a choice
    print(
        """What do we scrap today ? :
        1: Single book scrap
        2: All books of a category scrap
        3: All books of all categories scrap
        4: Exit"""

    )
    choice = input("Your selection ? ")
    return choice

def menu(): # get the choice and run the appropriate function
    options = {
        1: lambda: single_book(),
        2: lambda: single_category(),
        3: lambda: all_categries(),
        4: lambda: quit(),
           }

    choice = selection()
    while not choice.isdigit() or int(choice) < 1 or int(choice) > 5:
        print("Invalid option")
        choice = selection()

    options[int(choice)]()


if __name__ == "__main__":

    menu()












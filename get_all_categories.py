import requests
from bs4 import BeautifulSoup
import csv


category_links_list = []
category_name_list = []
category_dict = {}

url = 'http://books.toscrape.com/'

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
nav_tags = soup.find(class_="nav nav-list")
nav = nav_tags.find_all('a')
#print(nav)

for e in nav:
    #print(e)
    nav_text = e.text.replace('\n', '').strip()
    category_name_list.append(nav_text)

    #print(h_text)
    link_category = e['href']
    category_links_list.append(url+link_category)
    #print(link_category)
category_links_list = category_links_list[1:51]
category_name_list = category_name_list[1:51]


category_dict= dict(zip(category_name_list,category_links_list))
with open("categories.csv", "w", newline="") as csv_file:


    print(category_links_list)
    writer = csv.writer(csv_file)
    writer.writerow(category_links_list)

#print(category_name_list)
#print(("------------------------------------------------------"))





    #product_link = "http://books.toscrape.com/catalogue/" + href
    #product_links.append(product_link)
    #print(product_link)


#rint(h3_tags)
#print(len(h))




        #product_link = "http://books.toscrape.com/catalogue/" + href
        #product_links.append(product_link)
        #print(product_link)


    #rint(h3_tags)
    #print(len(h))













#print(lf)
#print(len(lf))
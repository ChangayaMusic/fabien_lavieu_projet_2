import requests
from bs4 import BeautifulSoup
category_links = []
category_list = []
url = 'http://books.toscrape.com/'
category_name_list = []
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
h3_tags = soup.find(class_="nav nav-list")
h = h3_tags.find_all('a')
print(h)
for e in h:
    #print(e)
    hr = e.text.replace('\n', '').strip()
    category_list.append(hr)
    print(hr)
category_list = category_list[1:51]
print(len(category_list))
print(("------------------------------------------------------"))
print(category_list)




    #product_link = "http://books.toscrape.com/catalogue/" + href
    #product_links.append(product_link)
    #print(product_link)


#rint(h3_tags)
#print(len(h))












#print(lf)
#print(len(lf))
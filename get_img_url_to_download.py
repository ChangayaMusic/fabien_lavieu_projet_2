import requests
import os
url = "http://books.toscrape.com/media/cache/08/e9/08e94f3731d7d6b760dfbfbc02ca5c62.jpg"
def download_images():
    response = requests.get(url)
    folder = "images" # create a folder name
    os.makedirs(folder, exist_ok=True) # create the folder if it does not exist
    image_name = os.path.basename(url) # get the image name from the url
    image_path = os.path.join(folder, image_name) # join the folder name and image name
    with open(image_path, "wb") as img: # open the file for writing
      img.write(response.content) # write the image content
download_images()
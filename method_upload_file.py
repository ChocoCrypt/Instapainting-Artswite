"""
Image to art converter using the instapainting CNN because it does'nt have an
API implemented.
"""
from selenium import webdriver
import requests
from time import sleep
import os
import json


def get_art_image(img_path , art_form , output):
    """
    Method for moving an image to an artistic paint using 
    https://www.instapainting.com/ai-painter
    because there is not an API.
    Uploads a file with requests and then apply the filter with selenium and
    download the result given by instapainting.
    """
    # Driver Options
    options = webdriver.ChromeOptions()
    #options.add_argument("--headless")
    # Login stuff
    driver = webdriver.Chrome(options = options)
    driver.get("https://www.instapainting.com/assets")
    driver.implicitly_wait(10)
    # Uploading image to instapainting
    upload_photo_box = driver.find_element_by_class_name("c1kjkl90")
    upload_photo_box.send_keys(os.getcwd()+img_path)
    # Configuration of the requests session for uploading the file
    s = requests.Session()
    cookies = driver.get_cookies()
    for cookie in cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    # Uploading the file with requests
    files = {'file': open(img_path, 'rb')}
    s = requests.post("https://www.instapainting.com/updates/create-chunked/", files=files)
    # Formating recived data to get the id of the photo
    recived_data = json.loads(s.content)
    page_id = recived_data["result"]["id"]
    # Going to the page of the uploaded file
    driver.get(f"https://www.instapainting.com/assets/{page_id}")
    driver.implicitly_wait(600)
    # Updating options
    all_art_forms = driver.find_elements_by_class_name("_14xSf7HUhOgutHdGN--E87")
    options_txt = "\n".join([i.text for i in all_art_forms])
    with open("options.txt","w") as opt:
        opt.write(options_txt)
    # Select Art form in possible art forms in options.txt
    art_box = driver.find_element_by_link_text(art_form)
    art_box.click()
    # Downloading images
    resulting_image = driver.find_element_by_class_name("_3FAK3-36q_B8HP2pGt6GJG")
    resulting_image_url = resulting_image.get_attribute("src")
    result = requests.get(resulting_image_url).content
    # Saving results
    with open(output, "wb") as rs:
        rs.write(result)
    # Return result only if it's necesary
    return(result)

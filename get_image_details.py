#More scrolling:https://stackoverflow.com/questions/20986631/how-can-i-scroll-a-web-page-using-selenium-webdriver-in-python
#blocking image loading maks it quite fast
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import numpy as np
from tqdm import tqdm
from image_element_detector import get_image_elements
import time
from urllib import request






def get_image_elements(driver, n_images = 10):
    prev_img_num = 0
    while True:
        imgs =driver.find_elements_by_css_selector("img[class='rg_i Q4LuWd']")
        if prev_img_num == len(imgs):
            driver.find_element_by_class_name("mye4qd").click()
        if len(imgs) > n_images:
            break
        driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
        time.sleep(2)    
        prev_img_num = len(imgs)

    return imgs[:n_images]



def get_image_details( search_url, n_images, headless = True):
    option = webdriver.ChromeOptions()

    option.headless = False
    option.add_argument("--log-level=3")
    #option.add_argument('--no-proxy-server')
    option.add_argument("--proxy-server='direct://'")
    option.add_argument("--proxy-bypass-list=*")

    driver = webdriver.Chrome(executable_path= "chromedriver.exe", options=option )
    driver.get(search_url)

    imgs = get_image_elements(driver, n_images)

    all_image_data = []
    for i, img in enumerate(tqdm(imgs)):
        actions = ActionChains(driver)
        actions.key_down(Keys.CONTROL).click(img).send_keys(Keys.TAB ).key_up(Keys.CONTROL).perform()
        handles = driver.window_handles
        time.sleep(0.5)
        if len(handles) == 1:
            print("tried")
            actions.key_down(Keys.CONTROL).click(img).send_keys(Keys.TAB ).key_up(Keys.CONTROL).perform()
        driver.switch_to.window(handles[1])
       
        image = driver.find_element_by_tag_name('img')
        single_image_data = []
        for attribute in ['src', 'alt', 'data-w', 'data-h']:
            single_image_data.append(image.get_attribute(attribute))

        print(single_image_data[0])
        download_and_save(search_text, single_image_data[0], i+1 , save_folder = "downloaded_img")

        all_image_data.append(single_image_data)
        driver.close()
        driver.switch_to.window(handles[0])

    return np.array(all_image_data)



def get_search_url(search_text):
    url_first_part = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q='
    search_url = url_first_part + search_text.replace(' ' , '+')
    return search_url, search_text

def download_and_save(search_text, url, img_no, save_folder = "downloaded_img"):
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    #for now saving as jpg, later I will use imghdr
    path = os.path.join(save_folder, search_text.replace(' ' , '_') + str(img_no) + '.jpg')
    with request.urlopen(url) as response:
        img_data = response.read()
    with open(path, "wb") as f:
        f.write(img_data)

start_time = time.time()

#search_url = 'https://www.google.com/search?q=quantum+mechanics&rlz=1C1PRFI_enBD883BD883&sxsrf=ALeKk01LVLQTsRsl8utOmYRk1b_Rwxi-aQ:1599109012577&source=lnms&tbm=isch&sa=X&ved=2ahUKEwisg5ulmczrAhWVj-YKHQKGBb8Q_AUoAXoECBUQAw&biw=1093&bih=556'
search_url, search_text = get_search_url("dogs")
n_images = 20
output = get_image_details( search_url, n_images)
print(output)

print("--- %s seconds ---" % (time.time() - start_time))
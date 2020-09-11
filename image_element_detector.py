from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import time




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

#elements = get_image_elements(driver, n_images = 150)
#print(len(elements))

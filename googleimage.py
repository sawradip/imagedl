#vpn have to be implemented
#we have to use wait, not time sleep, for getting element
import os
import time
import selenium
import numpy as np
import pandas as pd
from tqdm import tqdm
from urllib import request
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from utils import save_base64, save_img_without_progress_bar
from utils import check_img_type
from selenium.webdriver.support.ui import WebDriverWait

class GoogleImage:
    def __init__(self, headless = False, to_csv = False, show_links = False):

        self.to_csv = to_csv
        self.show_links = show_links
        self.url_first_part = 'https://www.google.com/search?site=&tbm=isch&source=hp&biw=1873&bih=990&q='
        
        self.option = webdriver.ChromeOptions()
        self.option.headless = headless
        self.option.add_argument("--log-level=3")
        self.option.add_argument("--proxy-server='direct://'")
        self.option.add_argument("--proxy-bypass-list=*")
        self.option.add_argument('--ignore-certificate-errors')
        self.option.add_argument('--ignore-ssl-errors')



    def get_image_elements(self):
        prev_img_num = 0
        while True:
            
            imgs = self.driver.find_elements_by_css_selector("img[class='rg_i Q4LuWd']")
            if prev_img_num == len(imgs):
                try:
                    self.driver.find_element_by_class_name("mye4qd").click()
                except selenium.common.exceptions.ElementNotInteractableException:
                    break
            self.driver.execute_script("window.scrollBy(0, document.body.scrollHeight)")
            time.sleep(2)    
            prev_img_num = len(imgs)
        if len(imgs) < self.n_images:
            print(f"[Warning] Only {len(imgs)} images available at google for this search result.Downloading them.")
        return imgs

    def get_image_details(self):
        imgs = self.get_image_elements()
        
        self.all_image_data = []
        i = 0
        if len(imgs) < self.n_images:
            self.n_images = len(imgs)
        
        progress_bar = tqdm(total = self.n_images)

        imgs = iter(imgs)
        while i < self.n_images:
            img = next(imgs)
            actions = ActionChains(self.driver)
            #print(img)
            try:
                actions.key_down(Keys.CONTROL).click(img).send_keys(Keys.TAB ).key_up(Keys.CONTROL).perform()

                handles = self.driver.window_handles
                try:
                    self.driver.switch_to.window(handles[1])
                except IndexError:
                    print("[Warning] Skipping an image due to problems.")
                    continue
                image = self.driver.find_element_by_tag_name('img')
            except (selenium.common.exceptions.NoSuchElementException, selenium.common.exceptions.StaleElementReferenceException):
                self.driver.close()
                self.driver.switch_to.window(handles[0])
                continue
            single_image_data = []
            for attribute in ['src', 'alt', 'data-w', 'data-h']:
                single_image_data.append(image.get_attribute(attribute))
            
            image_name = self.search_text.replace(' ' , '_') + str(i+1) + '.jpg'
            save_path = os.path.join(self.save_folder, image_name)
            #print(single_image_data[0])
            try:
                save_base64(single_image_data[0], save_path)
            except:
                save_img_without_progress_bar(single_image_data[0], save_path)

            if  os.path.exists(save_path) and check_img_type(save_path):
                if self.show_links:
                    print(single_image_data[0])
                single_image_data[0] = image_name
            else:
                continue
            
            self.all_image_data.append(single_image_data)
            self.driver.close()
            self.driver.switch_to.window(handles[0])
            i = i+1
            progress_bar.update(1)
        progress_bar.close()

    def download (self, search_text, n_images, save_folder = "downloaded_img"):
        self.search_text = search_text
        self.n_images = n_images
        self.save_folder = save_folder

        if not os.path.exists(self.save_folder):
            os.mkdir(self.save_folder)

        self.search_url = self.url_first_part + self.search_text.replace(' ' , '+')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options = self.option )
        self.driver.get(self.search_url)

        self.get_image_details()
        self.driver.close()
        self.all_image_data = pd.DataFrame(self.all_image_data)
        if self.to_csv:
            self.all_image_data.to_csv(os.path.join(self.save_folder , "img_info.csv"), header=None, index=None, sep=' ', mode='a')
        else:
            self.all_image_data.to_csv(os.path.join(self.save_folder , "img_info.txt"), header=None, index=None, sep=' ', mode='a')



#gi = GoogleImage(headless = False, to_csv= True, show_links= False)
#gi.download(search_text = "umbrella", n_images = 8 , save_folder = "guava")
            



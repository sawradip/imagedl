import os
import re
import time
import selenium
import argparse
import requests 
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

from googleimage import GoogleImage



class GoogleReverseImage(GoogleImage):
    def __init__(self, headless = False, to_csv = False, show_links = False):

        self.to_csv = to_csv
        self.show_links = show_links
        self.url_first_part = 'http://www.google.com/searchbyimage/upload'
        
        self.option = webdriver.ChromeOptions()
        self.option.headless = headless
        self.option.add_argument("--log-level=3")
        self.option.add_argument("--proxy-server='direct://'")
        self.option.add_argument("--proxy-bypass-list=*")
        self.option.add_argument('--ignore-certificate-errors')
        self.option.add_argument('--ignore-ssl-errors')

    def get_thumbnail_images(self):
        count = 0
        self.all_image_data = []
        while count < self.n_images:
            elem = self.driver.find_elements_by_css_selector("img[class ='rISBZc M4dUYb']")

            for img in elem:
                actions = ActionChains(self.driver)
                actions.key_down(Keys.CONTROL).click(img).send_keys(Keys.TAB ).key_up(Keys.CONTROL).perform()
                handles = self.driver.window_handles
                self.driver.switch_to.window(handles[1])
                image = self.driver.find_element_by_tag_name('img')
                single_image_data = []
                for attribute in ['src', 'alt', 'data-w', 'data-h']:
                    single_image_data.append(image.get_attribute(attribute))
                image_name = self.search_text.replace(' ' , '_') + str(count+1) + '.jpg'
                save_path = os.path.join(self.save_folder, image_name)
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
                if count < self.n_images:
                    count = count + 1
                else:
                    break
            self.driver.find_element_by_xpath("//*[@id='pnnext']/span[2]").click()
            

    def download (self, search_image, n_images, save_folder = "downloaded_img"):
        self.search_image = search_image
        self.n_images = n_images
        self.save_folder = save_folder

        if not os.path.exists(self.save_folder):
            os.mkdir(self.save_folder)

        usr_agent = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
                    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                    'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
                    'Accept-Encoding': 'none',
                    'Accept-Language': 'en-US,en;q=0.8',
                    'Connection': 'keep-alive',
                    }
        first_url_part = 'http://www.google.com/searchbyimage/upload'

        multipart = {'encoded_image': (self.search_image, open(self.search_image, 'rb')), 'image_content': ''}
        first_response = requests.post(self.url_first_part, files=multipart, allow_redirects=False)
        self.search_url = first_response.headers['Location']

        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options = self.option )
        self.driver.get(self.search_url)
        time.sleep(1)

        self.search_text = self.driver.find_element_by_xpath("//*[@id='sbtc']/div[2]/div[2]/input").get_attribute("value")
        try:
            print("Getting similar images...")
            self.driver.find_element_by_xpath("//*[@id='rso']/div[*]/g-section-with-header/div[1]/h3/a").click()
            self.get_image_details() 
        
        except selenium.common.exceptions.NoSuchElementException:
            print("[Warning] Similar images to this one is not available in google search.This image in different size might be available.Getting them.")
            time.sleep(1)
            self.driver.find_element_by_xpath("//*[@id='jHnbRc']/div[2]/span[1]/a").click()
            self.get_image_details() 
            
        
        self.driver.close()
        self.all_image_data = pd.DataFrame(self.all_image_data)
        if self.to_csv:
            self.all_image_data.to_csv(os.path.join(self.save_folder , "img_info.csv"), header=None, index=None, sep=' ', mode='a')
        else:
            self.all_image_data.to_csv(os.path.join(self.save_folder , "img_info.txt"), header=None, index=None, sep=' ', mode='a')



#gi = GoogleReverseImage(headless = False, to_csv= True, show_links= False)
#search_url = "https://www.google.com/search?tbs=sbi:AMhZZiv6Cl7C37c3W_1ZpCYRjFemUaqpEhc7dPAHJAxQWDMG01ez0JNTI1o1EmVb7PMi5-xQAB95NFBfKkRj7GXpkZY1N6H-wYr7nDlYBidv3GHk9gZHhDkvNgeASty38zxRkzMKhWsLHaq9xj6vieUQipYJnvW5bRgjd2mlIsNWEbS-Yjyc8TLc16yYAsIBsQV2nDboS8lgslCcC_1bvNYQ1Nd-EApSfxYAZYtlI05oUjfDChFPelxBFjvTNje_1uf1njOoxengISh1wHh5XEeVoIMKt4PhOYq2A2gitLAOBa1Gr2CDkFBKpBUJI_1LnbJDrhoXYa7PSmg_1ZUJYQkAC1pxQ3_1f1sMPXcQ"
#gi.download(search_image = r"sd.jpg", n_images = 80 , save_folder = "umb5")


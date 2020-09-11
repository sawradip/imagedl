import os
import re
import time
import selenium
import argparse
import requests 
import pandas as pd
from tqdm import tqdm
from googleimage import GoogleImage
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

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
        #this function downloads images fron site search results
        counter = 0
        imgs = self.driver.find_elements_by_class_name("rISBZc M4dUYb")
        print(len(imgs))
        #self.driver.find_elements_by_xpath("//*[@id='dimg_13']").click()
#//a[starts-with(@href, "mylink")]

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
            self.get_thumbnail_images()
            #self.driver.find_element_by_xpath("//*[@id='rso']/div[3]/g-section-with-header/div[1]/h3/a").click()
            
        
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



gi = GoogleReverseImage(headless = False, to_csv= True, show_links= False)
#search_url = "https://www.google.com/search?tbs=sbi:AMhZZiv6Cl7C37c3W_1ZpCYRjFemUaqpEhc7dPAHJAxQWDMG01ez0JNTI1o1EmVb7PMi5-xQAB95NFBfKkRj7GXpkZY1N6H-wYr7nDlYBidv3GHk9gZHhDkvNgeASty38zxRkzMKhWsLHaq9xj6vieUQipYJnvW5bRgjd2mlIsNWEbS-Yjyc8TLc16yYAsIBsQV2nDboS8lgslCcC_1bvNYQ1Nd-EApSfxYAZYtlI05oUjfDChFPelxBFjvTNje_1uf1njOoxengISh1wHh5XEeVoIMKt4PhOYq2A2gitLAOBa1Gr2CDkFBKpBUJI_1LnbJDrhoXYa7PSmg_1ZUJYQkAC1pxQ3_1f1sMPXcQ"
gi.download(search_image = "download.jpg", n_images = 8 , save_folder = "ree")


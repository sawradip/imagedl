import os
import wget
import requests
from urllib import request
from tqdm import tqdm

def save_base64(url, save_path):

    with request.urlopen(url) as response:
        data = response.read()
    with open(save_path, "wb") as f:
        f.write(data)

def save_img_alt(url, save_path):
    wget.download(url, save_path)

def save_img_progress_bar(url, save_path):
        response = requests.get(url, stream=True)
        total_size_in_bytes= int(response.headers.get('content-length', 0))
        block_size = 1024
        progress_bar = tqdm(total=total_size_in_bytes, unit='iB', unit_scale=True)
        
        with open(save_path, 'wb') as file:
            for data in response.iter_content(block_size):
                progress_bar.update(len(data))
                file.write(data)
        progress_bar.close()

def save_img_without_progress_bar(url, save_path):
        response = requests.get(url, stream=True)
        with open(save_path, 'wb') as file:
            file.write(response.content)

#save_base64("https://www.josephfriedmanltd.com/assets/site/_large/bigbaby-large.jpg", "dl/progress.jpg")
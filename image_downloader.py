from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import os
from datetime import datetime as dt
from urllib.parse import urlparse

def writing_html_file():
    r = requests.get("http://www.origo.hu/index.html")
    data = r.text
    print(data)
    with open('origo_hu_html.html', 'w', encoding="utf-8") as file:
        file.write(data)

def parsing_url(url):
    netloc = urlparse(url).netloc.split('.')[1]
    return netloc

def create_folder():
    time_stamp = str(dt.now().year) + str(dt.now().month) + str(dt.now().day)
    if not os.path.exists(time_stamp):
        os.makedirs(time_stamp)
        os.chdir(str(os.getcwd()+ "\\" + time_stamp))
        cwd = os.getcwd()
        print("cwd: ", cwd)
        return cwd
        #TODO: mi legyen, ha van már folder? (else ág)

def get_title(pic_url):
    return (pic_url.split('/', -1))[-1].split('?')[0]

def download_picture(url):
    try:
        r = requests.get(url)
        data = r.text
        soup = bs(data, "lxml")
        folder = create_folder() + parsing_url(url)
        print("folder: ", folder)
        for link in soup.find_all('img'):
            source = link.get('src')
            print(source)
            fullfilename = os.path.join(folder, get_title(source))
            print(get_title(source))
            print("fullfilename: ", fullfilename)
            urllib.request.urlretrieve(str(source), fullfilename)
            return url
    except Exception as e:
            print(e)

download_picture('http://www.origo.hu/index.html')

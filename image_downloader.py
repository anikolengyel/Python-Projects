from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import os
from datetime import datetime as dt
from urllib.parse import urlparse
import sys

def parsing_url(url):
    netloc = urlparse(url).netloc.split('.', -1)[-2]
    return netloc

def create_folder():
    time_stamp = str(dt.now().year) + str(dt.now().month) + str(dt.now().day)
    if not os.path.exists(time_stamp):
        os.makedirs(time_stamp)
        os.chdir(str(os.getcwd()+ "\\" + time_stamp))
        cwd = os.getcwd()
        print("cwd: ", cwd)
        return cwd
        #TODO: else? if folder already exists

def get_pic_title(pic_url):
    title = (pic_url.split('/', -1))[-1].split('?')[0]
    return title

def download_picture(url):
    unknown_pictures = []
    try:
        r = requests.get(url)
        data = r.text
        soup = bs(data, "lxml")
        #todo: folder manipulating function
        os.makedirs(parsing_url(url)+ "_" + str(dt.now().year)+str(dt.now().month)+ str(dt.now().day))
        os.chdir(str(os.getcwd()+ "\\" + parsing_url(url)+ "_" + str(dt.now().year)+str(dt.now().month)+ str(dt.now().day)))
        print(os.getcwd())
        for link in soup.find_all('img'):
            # extracting the picture link
            source = link.get('src')
            #TODO: source isn't always a in a valid, downloadable url format: Unknown url type
            # concatenating the folder name and the picture title, creating a path
            fullfilename = os.path.join(os.getcwd(), get_pic_title(source))
            urllib.request.urlretrieve(str(source), str(fullfilename))
    except Exception as e:
            print(e)
            # todo: append the pictures with unknown url to a list, move to the next item

#TODO: no such file or directoty (other links)

download_picture('https://www.nytimes.com/')

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

def create_folder(url):
    time_stamp = str(dt.now().year)+str(dt.now().month)+ str(dt.now().day)
    dir_string = parsing_url(url)
    # if folder not exists, make one
    if not os.path.exists(dir_string + "_" + time_stamp):
        # creating directory with webpage name and timestamp
        os.makedirs(dir_string + "_" + time_stamp)
        # changing the working directory
        os.chdir(str(os.getcwd()+ "\\" + dir_string+ "_" + time_stamp))
        print("New folder: ", os.getcwd())
        # if folder already exists, go to the folder
        return os.getcwd()
    else:
        os.chdir(str(os.getcwd()+ "\\" + dir_string+ "_" + time_stamp))
        print("Folder already exists: ", os.getcwd())
        return os.getcwd()

def get_pic_title(pic_url):
    title = (pic_url.split('/', -1))[-1].split('?')[0]
    return title

def create_list_of_sources(url):
    sources = []
    try:
        r = requests.get(url)
        data = r.text
        soup = bs(data, "lxml")
        images = soup.find_all('img')
        for tag in images:
            source = tag.get('src')
            sources.append(source)
        return sources
    except Exception as e:
            print(e)

def download_picture(url):
    #todo: getting the webpage url from input
    # list to store the invalid picture sources
    unknown_pictures = []
    # an integer to count the pictures
    num = 0
    folder_path = create_folder(url)
    try:
        for source in create_list_of_sources(url):
            # extracting the picture link
            #source = link.get('src')
            num +=1
            print("Picture number ", num, ", ", source)
            # concatenating the folder name and the picture title, creating a path to every picture
            fullfilename = os.path.join(folder_path, get_pic_title(source))
            print(fullfilename)
            urllib.request.urlretrieve(str(source), str(fullfilename))
    except Exception:
        #catching the unknown urls, appending them to a list
        unknown_pictures.append(source)
        pass
    print(unknown_pictures)

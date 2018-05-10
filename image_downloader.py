from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import os
from datetime import datetime as dt
from urllib.parse import urlparse
from flask import Flask, request, render_template
import sys

app = Flask(__name__, template_folder='static')

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

@app.route('/download_image', methods=['GET', 'POST'])
def download_picture():
    # the user starts posting a website:
    if request.method == 'POST':
        # if the form is not empty
        if request.form['url']:
            # list to store the invalid picture sources
            unknown_pictures = []
            # an integer to count the pictures
            num = 0
            # getting the url from the form
            url = request.form['url']
            print('url: ', url)
            folder_path = create_folder(url)
            try:
                for source in create_list_of_sources(url):
                    # extracting the picture link
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
            finally:
                # change the dir back to the original working dir
                os.chdir("..")
            print('Unknown pictures: ', unknown_pictures)
            return render_template('download_ready.html')
    else:
        return render_template('start_page.html')

if __name__ == '__main__':
    # giving a key to create sessions for users
    # for development it is just super_secret_key
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


from bs4 import BeautifulSoup as bs
import requests
import urllib.request
import os
from datetime import datetime as dt
from urllib.parse import urlparse
from flask import Flask, request, render_template

# creating a Flask application
app = Flask(__name__, template_folder='static')

# get the netloc string of the url
def parsing_url(url):
    netloc = urlparse(url).netloc.split('.', -1)[-2]
    return netloc

# creating folder by using the curent date and the name of the webpage
def create_folder(url):
    # getting the date string (year, month, date)
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
    # if folder already exists, open the existing folder
    else:
        os.chdir(str(os.getcwd()+ "\\" + dir_string+ "_" + time_stamp))
        print("Folder already exists: ", os.getcwd())
        return os.getcwd()

# getting a picture title for each link
def get_pic_title(pic_url):
    title = (pic_url.split('/', -1))[-1].split('?')[0]
    return title

# creating a list of the found urls
def create_list_of_sources(url):
    sources = []
    try:
        r = requests.get(url)
        data = r.text
        soup = bs(data, "lxml")
        # find all the elements with image tag
        images = soup.find_all('img')
        for tag in images:
            source = tag.get('src')
            # append the links to the sources list
            sources.append(source)
        return sources
    except Exception as e:
            print(e)

# creating the route for the web
@app.route('/download_image', methods=['GET', 'POST'])
def download_picture():
    # if the requested method is post and the form is not empty:
    if request.method == 'POST' and request.form['url']:
        # list to store the invalid picture sources
        unknown_pictures = []
        # an integer to count the pictures
        num = 0
        # getting the url from the form
        url = request.form['url']
        print('url: ', url)
        folder_path = create_folder(url)
        url_list = create_list_of_sources(url)
        for source in url_list:
            try:
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
                # change the dir back to the original working dir to make a new session
                # TODO: find a more elegant solution
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


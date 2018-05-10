
Introduction

This project is a simple restaurant webpage connected to a database built with Flask. 
The porpuse of this project to implement a webpage with Flask and CRUD functionalities 
with sqlalchemy to maintain a database.

Setup

Clone this repository.
The repository contains:
- database_setup.py file - it sets up the tables, implement some functionalities and the necessery classes
- restaurant.py file - it implements the CRUD functionalities and runs the application
- restaurantmenu.db - contains the restaurant data
- static - contains the HTML and CSS files to the webpage
- this README.md file

The database contains the following tables with the following columns:
- restaurant: id, name
- menu_item: id, name, course, description, price, restaurant_id

If you do not have the necessary programs, you will need to install the followings:
- Python3
- Python packages: sqlalchemy, sqlalchemy.orm
- Vagrant
- Virtual Box

Running

Launch Vagrant by running vagrant up from the command line, then log with
vagrant ssh.

To access the program files, type cd /vagrant. Run the database_setup.py to setup the database.
After that, run the restaurant.py to setup the webpage. Go to http://localhost:5000/restaurants
in your web browser to get to the restaurants.

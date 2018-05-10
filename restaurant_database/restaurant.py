from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from database_setup_copy import Base, Restaurant, MenuItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# TODO: fix the CSS and HTML templates

app = Flask(__name__, template_folder='static')

# create a session to manipulate the database
def create_session():
    engine = create_engine('sqlite:///restaurantmenu.db')
    Base.metadata.bind = engine

    #binding the session with the database engine
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    return session

# creating a JSON functionality to get the raw restaurant data in JSON format
@app.route('/restaurants/JSON')
def restaurantJson():
    session = create_session()
    # query all the restaurant data
    restaurants = session.query(Restaurant).all()
    # looping through the restaurant objects, get the data for each column
    return jsonify(MenuItems= [i.serialize for i in restaurants])

# creating a JSON functionality to get the raw menu data in JSON format
@app.route('/restaurants/<int:restaurant_id>/menu/JSON')
def restaurantMenuJson(restaurant_id):
    session = create_session()
    # query all the menu data
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return jsonify(MenuItems= [i.serialize for i in items])

@app.route('/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantMenuItemJson(restaurant_id, menu_id):
    session = create_session()
    # create a restaurant object by quering the data by restaurant id
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    # selecting the item filtered by the url and the restaurant object's id
    item = session.query(MenuItem).filter_by(id=menu_id, restaurant_id = restaurant.id).one()
    return jsonify(MenuItemID= [item.serialize])

# create the possible paths for the function
@app.route('/')
@app.route('/restaurants')
# show all the restaurant names
def showRestaurants():
    session = create_session()
    restaurants = session.query(Restaurant).all()
    # return the html template
    return render_template('restaurants.html', restaurants=restaurants)

@app.route('/restaurant/new', methods=['GET', 'POST'])
# create new restaurants
def newRestaurant():
    session = create_session()
    # if the requested method is post:
    if request.method == 'POST':
        # get the new rstaurant name from the form
        newRest = Restaurant(name=request.form['name'])
        # adding the new item to the database
        session.add(newRest)
        session.commit()
        # redirect to the original page
        return redirect(url_for('showRestaurants'))
    else:
        # return an html template with the form
        return render_template('newRestaurant.html')

@app.route('/restaurant/<int:restaurant_id>/edit', methods=['GET', 'POST'])
def editRestaurant(restaurant_id):
    session = create_session()
    editedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedRestaurant.name = request.form['name']
            session.add(editedRestaurant)
            session.commit()
            return redirect(url_for('showRestaurants'))
    else:
        # befor the post activity, show the html template with the form
        return render_template('editRestaurant.html', restaurant_id=editedRestaurant.id, restaurant_name = editedRestaurant.name)

# delete a restaurant
@app.route('/restaurant/<int:restaurant_id>/delete', methods=['GET', 'POST'])
def deleteRestaurant(restaurant_id):
    session = create_session()
    deletedRestaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        session.delete(deletedRestaurant)
        session.commit()
        return redirect(url_for('showRestaurants'))
    return render_template('deleteRestaurant.html', restaurant_id=deletedRestaurant.id, restaurant_name=deletedRestaurant.name)

@app.route('/<int:restaurant_id>')
@app.route('/restaurant/<int:restaurant_id>/menu')
# show the menu for a selected restaurant
def showMenu(restaurant_id):
    session = create_session()
    # query the selected restaurant by restaurant_id on the path
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    # get all the menu items
    items = session.query(MenuItem).filter_by(restaurant_id=restaurant.id)
    return render_template('menu.html', restaurant = restaurant, restaurant_id = restaurant.id, items=items)

@app.route('/restaurant/<int:restaurant_id>/menu/new', methods=['GET', 'POST'])
# creating new menu item for a selected restaurant
def newMenuItem(restaurant_id):
    session = create_session()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    if request.method == 'POST':
        # if the form is not empty
        if request.form['name']:
            newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
            session.add(newItem)
            session.commit()
            # redirect to the webpage showing the menu items
            return redirect(url_for('showMenu', restaurant_id = restaurant_id))
    else:
        # render a template to create new menu item
        return render_template('newMenuItem.html', restaurant_id=restaurant_id, restaurant_name = restaurant.name)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/edit', methods=['GET', 'POST'])
# edit menu item for a selected restaurant
def editMenuItem(restaurant_id, menu_id):
    session = create_session()
    editedItem = session.query(MenuItem).filter_by(id=menu_id).one()
    if request.method == 'POST':
        if request.form['name']:
            editedItem.name = request.form['name']
            session.add(editedItem)
            session.commit()
            return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    else:
        return render_template('editMenuItem.html', restaurant_id = restaurant_id, menu_id = editedItem.id, edited_name = editedItem.name)

@app.route('/restaurant/<int:restaurant_id>/menu/<int:menu_id>/delete', methods=['GET', 'POST'])
# delete menu item for a selected restaurant
def deleteMenuItem(restaurant_id, menu_id):
    session = create_session()
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    deletedItem = session.query(MenuItem).filter_by(id=menu_id, restaurant_id = restaurant.id).one()
    if request.method == 'POST':
        session.delete(deletedItem)
        session.commit()
        return redirect(url_for('showMenu', restaurant_id=restaurant_id))
    return render_template('deleteMenuItem.html', restaurant = restaurant, item = deletedItem)

if __name__ == '__main__':
    # giving a key to create sessions for users
    # for development it is just super_secret_key
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=5000)


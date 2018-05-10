
from sqlalchemy import Column, ForeignKey, Integer, String

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

# making an instance of the declarative_base
Base = declarative_base()

# creating new class restaurant inherited from the class base (inherits all the functions)
class Restaurant(Base):
    # creating a table restaurant
    __tablename__ = 'restaurant'

    # creating new column called name
    # if there is no name, we cant create restaurant row
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable = False)

    @property
    def serialize(self):

        return {
            'id': self.id,
            'name': self.name,
        }


# creating menuItem inherited from Base class
class MenuItem(Base):
    # creating a table menu_item
    __tablename__ = 'menu_item'

    # creating new column - id
    id = Column(Integer, primary_key = True)
    name = Column(String(80), nullable = False)
    course = (Column(String(250)))
    description = Column(String(250))
    price = Column(String(8))
    # creating a foreign key to the restaurant, pointing to restaurant_id
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):

        return {
            'name': self.name,
            'description': self.description,
            'id': self.id,
            'price': self.price,
            'course': self.course,
        }

# creating instance of create_engine class, pointing to the database
# create a new file that we can use simiralry to a more robust database
engine = create_engine('sqlite:///restaurantmenu.db')

# goes into the db and add the classes we created as tables
Base.metadata.create_all(engine)

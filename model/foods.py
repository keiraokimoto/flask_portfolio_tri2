""" database dependencies to support sqliteDB examples """
from random import randrange
import os, base64
import json

from __init__ import app, db
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

# Define the User class to manage actions in the 'users' table
# -- Object Relational Mapping (ORM) is the key concept of SQLAlchemy
# -- a.) db.Model is like an inner layer of the onion in ORM
# -- b.) User represents data we want to store, something that is built on db.Model
# -- c.) SQLAlchemy ORM is layer on top of SQLAlchemy Core, then SQLAlchemy engine, SQL

class Ingredient(db.Model):
    __tablename__ = 'ingredients'

    id = db.Column(db.Integer, primary_key=True)
    _type = db.Column(db.String(255), unique=False, nullable=False)
    _amount = db.Column(db.Integer, unique=False, nullable=False)
    _unit = db.Column(db.String(255), unique=False, nullable=False)

    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    foodID = db.Column(db.Integer, db.ForeignKey('foods.id'))

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, id, type, amount, unit):
        self.foodID = id
        self._type = type    # variables with self prefix become part of the object, 
        self._amount = amount
        self.unit = unit

     # a name getter method, extracts name from object
    @property
    def type(self):
        return self._type
    
    # a setter function, allows name to be updated after initial object creation
    @type.setter
    def type(self, type):
        self._type = type
    
    # a getter method, extracts email from object
    @property
    def amount(self):
        return self._amount
    
    # a setter function, allows name to be updated after initial object creation
    @amount.setter
    def amount(self, amount):
        self._amount = amount
        
    # check if uid parameter matches user id in object, return boolean
    def is_amount(self, amount):
        return self._amount == amount

     # a getter method, extracts email from object
    @property
    def amount(self):
        return self._amount
    
    # a setter function, allows name to be updated after initial object creation
    @amount.setter
    def amount(self, amount):
        self._amount = amount
        
    # check if uid parameter matches user id in object, return boolean
    def is_amount(self, amount):
        return self._amount == amount

    @property
    def unit(self):
        return self._unit
    
    # a setter function, allows name to be updated after initial object creation
    @unit.setter
    def unit(self, unit):
        self._unit = unit

    def read(self):
        return {
            "id": self.foodID,
            "type": self.type,
            "amount": self.amount,
            "unit": self.unit
        }



class Food(db.Model):
    __tablename__ = 'foods'

    # Define the User schema with "vars" from object
    id = db.Column(db.Integer, primary_key=True)
    _name = db.Column(db.String(255), unique=True, nullable=False)
    _directions = db.Column(db.String(1500), unique=False, nullable=False)
    _description = db.Column(db.String(500), unique=False, nullable=True)
    # Defines a relationship between User record and Notes table, one-to-many (one user to many notes)
    ingredients = db.relationship("Ingredient", cascade='all, delete', backref='foods', lazy=True)

    # constructor of a User object, initializes the instance variables within object (self)
    def __init__(self, name, directions):
        self._name = name    # variables with self prefix become part of the object, 
        self._directions = directions

    # a name getter method, extracts name from object
    @property
    def name(self):
        return self._name
    
    # a setter function, allows name to be updated after initial object creation
    @name.setter
    def name(self, name):
        self._name = name
    
    # a getter method, extracts email from object
    @property
    def directions(self):
        return self._directions
    
    # a setter function, allows name to be updated after initial object creation
    @directions.setter
    def directions(self, directions):
        self._directions = directions
        
    # check if uid parameter matches user id in object, return boolean
    def is_directions(self, directions):
        return self._directions == directions
    
     # a getter method, extracts email from object
    @property
    def description(self):
        return self._description
    
    # a setter function, allows name to be updated after initial object creation
    @directions.setter
    def description(self, description):
        self._description = description
        
    # output content using str(object) in human readable form, uses getter
    def __str__(self):
        return f'name: "{self.name}", id: "{self.name}", directions: "{self.directions}"'

    # output command to recreate the object, uses attribute directly
    def __repr__(self):
        return f'Person(name={self._name}, name={self._name}, directions={self._directions})'
    
    # output content using str(object) in human readable form, uses getter
    # output content using json dumps, this is ready for API response
    def __str__(self):
        return json.dumps(self.read())

    # CRUD create/add a new record to the table
    # returns self or None on error
    def create(self):
        try:
            print('name in create ', self.name)
            # creates a person object from User(db.Model) class, passes initializers
            db.session.add(self)  # add prepares to persist person object to Users table
            db.session.commit()  # SqlAlchemy "unit of work pattern" requires a manual commit
            print('id in create', self.id)
            
            return self
        except IntegrityError  as e:
            print('someting wrong with adding food: ', e)
            db.session.remove()
            return None

    # CRUD read converts self to dictionary
    # returns dictionary
    def read(self):
        return {
            "id": self.id,
            "name": self.name,
            "directions": self.directions,
            "ingredients": [ingredient.read() for ingredient in self.ingredients]
        }

    # CRUD update: updates user name, password, phone
    # returns self
    def update(self):
        """only updates values with length"""
        print(self)
        print('update')
        db.session.commit()
        return self

    # CRUD delete: remove self
    # None
    def delete(self):
        db.session.delete(self)
        db.session.commit()
        return None
    @staticmethod
    def getRecipeByName(recname):
        recs = db.session.query(Food).filter(Food._name == recname)
        for r in recs:
            # Should be just 1 rec matched
            return r
        
        return None

"""Database Creation and Testing """
# Builds working data for testing
recipeList = []
def initFoods():
    """Create database and tables"""
    db.create_all()
    
    # TO DO: Load from Json docmument (this is only for testing)
    """Tester data for table"""
    # f1 = Food(name='Shoyu Ramen', directions='ajkddmsd')
    # f2 = Food(name='Tonkatsu', directions='hdasdjad')
    # f3 = Food(name='Yakisoba', directions='sadjsdasa')
    # put user objects in list for convenience
    recipes = loadRecipes()
    
    foods = recipes["Recipes"]
    print(len(foods))
    """Builds sample user/note(s) data"""
    for rec in foods:
        try:
            
            '''add a few 1 to 4 notes per user'''
            food = Food(rec["Name"] + "-othery", "need array fordirec") # rec["Directions"])
            for ing in rec["Ingredients"]:
                food.ingredients.append(Ingredient(food.id, type=ing["type"], amount=int(ing["amount"]), unit=ing["unit"]))
            '''add user/post data to table'''
            s = food.create()
        except IntegrityError:
            '''fails with bad or duplicate data'''
            db.session.remove()
            print(f"Records exist, duplicate email, or error: {food.uid}")
            
def loadRecipes():
    SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
    json_url = os.path.join(SITE_ROOT, "", "jpFood.json")
    recipeList = json.load(open(json_url))
    return recipeList


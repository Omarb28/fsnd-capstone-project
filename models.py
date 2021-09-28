import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy

database_path = os.environ['DATABASE_URL']
db = SQLAlchemy()


def setup_db(app, database_path=database_path):
    '''
    setup_db(app)
    Binds a flask application and a SQLAlchemy service
    '''
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.app = app
    db.init_app(app)
    db.create_all()

    return db


class Movie(db.Model):
    '''
    Movie Model
    Has attributes title and release year
    '''
    __tablename__ = 'Movie'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_year = Column(Integer)

    def __init__(self, title, release_year):
        self.title = title
        self.release_year = release_year

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_year': self.release_year
        }


class Actor(db.Model):
    '''
    Actor Model
    Has attributes  name, age and gender
    '''
    __tablename__ = 'Actor'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)  # TODO: Restrict column to male and female

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

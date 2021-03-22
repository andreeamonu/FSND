import os
from sqlalchemy import Column, String, Integer, Date, create_engine
from flask_sqlalchemy import SQLAlchemy
import json

database_name = "casting"
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''

def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


class BaseModel:
    '''
    insert() = post
        inserts a new model into the database
    '''
    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete() = delete
        deletes a model from the database
        the model must exist in the database
    '''
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update() = patch
        updates a model from the database
        the model must exist in the database
    '''
    def update(self):
        db.session.commit()

movie_actors = db.Table('movie_actors',
                        db.Column('movie_id',
                                  db.Integer,
                                  db.ForeignKey('movies.id'),
                                  primary_key=True),
                        db.Column('actor_id',
                                  db.Integer,
                                  db.ForeignKey('actors.id'),
                                  primary_key=True)
                        )

'''
Movies
Have title and release date
'''
class Movies(db.Model, BaseModel):  
    __tablename__ = 'movies'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(String(200), nullable=False)
    release_date = db.Column(Date, nullable=False)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date
        
    def format(self):
        return {
        'id': self.id,
        'title': self.title,
        'release_date': self.release_date
        }

    def __repr__(self):
        return json.dumps(self.format())

'''
Actors
Have name, age and gender
'''
class Actors(db.Model, BaseModel):  
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(String(200), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(String(100), nullable=False)
    movies = db.relationship('Movies', secondary=movie_actors, backref='actors', lazy=True)


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

    def __repr__(self):
        return json.dumps(self.format())
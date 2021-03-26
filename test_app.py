import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from sqlalchemy import String, Integer
from models import setup_db, Movie, Actor


#----------------------------------------------------------------------------#
# Movies tests
#----------------------------------------------------------------------------#

class MovieTestCase(unittest.TestCase):
    #This class represents the movie test cases

    def setUp(self):
        #Define test variables and initialize app.
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432',self.database_name)
        setup_db(self.app, self.database_path)


        # bind app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create tables
            self.db.create_all()
    
    #----------------------------------------------------------------------------#
    # Define tokens
    #----------------------------------------------------------------------------#

        self.casting_assistant_token = "Bearer {}".format(os.environ.get('CASTING_ASSISTANT_TOKEN'))
        self.casting_director_token = "Bearer {}".format(os.environ.get('CASTING_DIRECTOR_TOKEN'))
        self.executive_producer_token = "Bearer {}".format(os.environ.get('EXECUTIVE_PRODUCER_TOKEN'))


    def tearDown(self):
        #Executed after each test
        pass

    # Test successful request to get movies 
    def test_get_all_movies(self):
        res = self.client().get('/movies',headers={'Authorization':self.casting_assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    # Test successful request to create a movie 

    def test_create_movie(self):
        new_movie = {
            'title': 'Inception',
            'release_date': '20 July 2010'
            }
        res = self.client().post('/movies', json=new_movie, headers={'Authorization':self.executive_producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])  
        self.assertTrue(len(data['movies']))

    # Test unsuccessful request to create a movie when movie id is mentioned

    def test_405_if_movie_creation_is_not_allowed(self):
        new_movie = {
            'title': 'Inception',
            'release_date': '20 July 2010'
            }
        res = self.client().post('/movies/1', json=new_movie,headers={'Authorization':self.executive_producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')    

    # Test successful request to update a movie

    def test_update_movie(self):
        updated_movie = {
            'title': 'Inception',
            'release_date': '16 July 2010'
            }
        res = self.client().patch('/movies/3', json=updated_movie, headers={'Authorization':self.casting_director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))    

    # Test unsuccessful request to update a movie when no data is mentioned

    def test_405_if_data_is_missing_from_movies_update_request(self): 
        res = self.client().patch('/movies', headers={'Authorization': self.executive_producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Test successful request to delete a movie
    def test_delete_movie(self):
        res = self.client().delete('/movies/2', headers={'Authorization': self.executive_producer_token})
        data = json.loads(res.data)

        movie = Movie.query.filter(Movie.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    # Test unsuccessful request to delete a movie that does not exist

    def test_404_when_deleting_a_movie_that_does_not_exist(self):
        res = self.client().delete('/movies/200', headers={'Authorization': self.executive_producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    def test_401_when_no_token_is_passed(self):
        res = self.client().get('/movies')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

#----------------------------------------------------------------------------#
# Actors tests
#----------------------------------------------------------------------------#


class ActorTestCase(unittest.TestCase):
    #This class represents the actor test cases

    def setUp(self):
        #Define test variables and initialize app
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432',self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        #----------------------------------------------------------------------------#
        # Define tokens
        #----------------------------------------------------------------------------#

        self.casting_assistant_token = "Bearer {}".format(os.environ.get('CASTING_ASSISTANT_TOKEN'))
        self.casting_director_token = "Bearer {}".format(os.environ.get('CASTING_DIRECTOR_TOKEN'))
        self.executive_producer_token = "Bearer {}".format(os.environ.get('EXECUTIVE_PRODUCER_TOKEN'))

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test successful request to get actors 
    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': self.casting_assistant_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # Test successful request to create an actor 

    def test_create_actor(self):
        new_actor = {
            'name': 'Marion Cotillard',
            'age': 45,
            'gender': 'Female'
        }
        res = self.client().post('/actors', json=new_actor, headers={'Authorization': self.executive_producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
        self.assertTrue(len(data['actors']))

    # Test unsuccessful request to create an actor when actor id is mentioned

    def test_405_if_actor_creation_is_not_allowed(self):
        new_actor = {
            'name': 'Marion Cotillard',
            'age': 45,
            'gender': 'Female'
        }
        res = self.client().post('/actors/1', json=new_actor, headers={'Authorization': self.executive_producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')    

    # Test successful request to update an actor

    def test_update_actor(self):
        updated_actor = {
            'name': 'Anne Hathaway',
            'age': 38,
            'gender': 'Female'        
            }
        res = self.client().patch('/actors/3', json=updated_actor, headers={'Authorization': self.casting_director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)  
        self.assertTrue(len(data['actors']))    

    # Test unsuccessful request to update an actor when no data is mentioned

    def test_405_if_data_is_missing_from_actors_update_request(self): 
        res = self.client().patch('/actors', headers={'Authorization': self.executive_producer_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Test successful request to delete an actor

    def test_delete_actor(self):
        res = self.client().delete('/actors/2', headers={'Authorization': self.executive_producer_token})
        data = json.loads(res.data)

        actor = Actor.query.filter(Actor.id == 2).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor']) 

    # Test unsuccessful request to delete an actor that does not exist

    def test_404_when_deleting_an_actor_that_does_not_exist(self):
        res = self.client().delete('/actors/200', headers={'Authorization':self.casting_director_token})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')   

    def test_401_when_no_token_is_passed(self):
        res = self.client().get('/actors')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)

# Make the tests executable
if __name__ == "__main__":
    unittest.main()

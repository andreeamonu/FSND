import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import app
from models import setup_db, Movies, Actors

#----------------------------------------------------------------------------#
# Define tokens
#----------------------------------------------------------------------------#

casting_assistant_token = "Bearer {}".format(os.environ.get('CASTING_ASSISTANT_TOKEN'))
casting_director_token = "Bearer {}".format(os.environ.get('CASTING_DIRECTOR_TOKEN'))
executive_producer_token = "Bearer {}".format(os.environ.get('EXECUTIVE_PRODUCER_TOKEN'))

#----------------------------------------------------------------------------#
# Movies tests
#----------------------------------------------------------------------------#


class MovieTestCase(unittest.TestCase):
    """This class represents the movie test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_movie = {
            'name': 'Inception',
            'release_date': '20 July 2010'
        }

        self.update_movie = {
            'name': 'Inception',
            'release_date': '16 July 2010 (USA)'
        }

        self.update_bad_movie = {
            'name': 'Inception',
            'release': 'A day in July 2010'
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test successful request to get movies 
    def test_get_movies(self):
        res = self.client().get('/movies', headers={'Authorization': (casting_assistant_token)}))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']) > 0)

    # Test successful request to create a movie 

    def test_create_movie(self):
        res = self.client().post('/movies', json=self.new_movie, headers={'Authorization': (executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['name'])
        self.assertTrue(data['release_date'])
        self.assertTrue(data['number_of_movies'])    
        self.assertTrue(len(data['movies']))

    # Test unsuccessful request to create a movie when movie id is mentioned

    def test_400_if_movie_creation_is_not_allowed(self):
        res = self.client().post('/movies/1', json=self.new_movie, headers={'Authorization': (executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')    

    # Test unsuccessful request to create a movie when no data is mentioned

    def test_400_if_data_is_missing_from_movies_request(self):
        res = self.client().post('/movies', headers={'Authorization': (executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')    

    # Test successful request to update a movie

    def test_update_movie(self):
        res = self.client().patch('/movies/2', json=self.update_movie, headers={'Authorization': (casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['name'])
        self.assertTrue(data['release_date'])
        self.assertTrue(data['number_of_movies'])    
        self.assertTrue(len(data['movies']))    

    # Test unsuccessful request to update a movie when we have a bad format

    def test_422_when_bad_format_of_update_movie_passed(self):
        res = self.client().patch('/movies/2', json=self.update_bad_movie, headers={'Authorization': (casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')   

    # Test unsuccessful request to update a movie when no data is mentioned

    def test_400_if_data_is_missing_from_movies_update_request(self): 
        res = self.client().patch('/movies', headers={'Authorization': (executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # Test successful request to delete a movie

    def test_delete_movie(self):
        res = self.client().delete('/movies/2', headers={'Authorization': (executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'], 2)
        self.assertTrue(data['number_of_movies'])    
        self.assertTrue(len(data['movies']))    

    # Test unsuccessful request to delete a movie that does not exist

    def test_422_when_deleting_a_movie_that_does_not_exist(self):
        res = self.client().patch('/movies/200', headers={'Authorization': (casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')   

#----------------------------------------------------------------------------#
# Actors tests
#----------------------------------------------------------------------------#


class ActorTestCase(unittest.TestCase):
    """This class represents the actor test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'Marion Cotillard',
            'age': 45,
            'gender': 'Female'
        }

        self.update_actor = {
            'name': 'Anne Hathaway',
            'age': 38,
            'gender': 'Female'        
            }

        self.update_bad_actor = {
            'name': 'Anne Hathaway',
            'age': @45@,
            'gender': 'Female'        
            }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test successful request to get actors 
    def test_get_actors(self):
        res = self.client().get('/actors', headers={'Authorization': (casting_assistant_token)}))
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']) > 0)

    # Test successful request to create an actor 

    def test_create_movie(self):
        res = self.client().post('/actors', json=self.new_actor, headers={'Authorization': (executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['name'])
        self.assertTrue(data['age'])
        self.assertTrue(data['gender'])
        self.assertTrue(data['number_of_actors'])    
        self.assertTrue(len(data['actors']))

    # Test unsuccessful request to create an actor when actor id is mentioned

    def test_405_if_actor_creation_is_not_allowed(self):
        res = self.client().post('/actors/1', json=self.new_actor, headers={'Authorization': (executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')    

    # Test unsuccessful request to create an actor when no data is mentioned

    def test_400_if_data_is_missing_from_actors_request(self):
        res = self.client().post('/actors', headers={'Authorization': (executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')    

    # Test successful request to update an actor

    def test_update_actor(self):
        res = self.client().patch('/actors/2', json=self.update_actor, headers={'Authorization': (casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['name'])
        self.assertTrue(data['age'])
        self.assertTrue(data['gender'])
        self.assertTrue(data['number_of_actors'])    
        self.assertTrue(len(data['actors']))    

    # Test unsuccessful request to update an actor when we have a bad format

    def test_422_when_bad_format_of_update_actor_passed(self):
        res = self.client().patch('/actors/2', json=self.update_bad_actor, headers={'Authorization': (casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')   

    # Test unsuccessful request to update an actor when no data is mentioned

    def test_400_if_data_is_missing_from_actors_update_request(self): 
        res = self.client().patch('/actors', headers={'Authorization': (executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'bad request')

    # Test successful request to delete an actor

    def test_delete_actor(self):
        res = self.client().delete('/actors/2', headers={'Authorization': (executive_producer_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'], 2)
        self.assertTrue(data['number_of_actors'])    
        self.assertTrue(len(data['actors']))    

    # Test unsuccessful request to delete an actor that does not exist

    def test_422_when_deleting_an_actor_that_does_not_exist(self):
        res = self.client().patch('/actors/200', headers={'Authorization': (casting_director_token)})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')   


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
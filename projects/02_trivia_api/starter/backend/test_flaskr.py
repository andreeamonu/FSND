import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_question = {
            'question': 'How many new species continue to be discovered every year?',
            'answer': '18,000',
            'category': 1,
            'difficulty': 4
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

    # Test successful request to get categories 
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['categories'])
        self.assertEqual(data['total_categories'], 6)

    # Test successful request to get paginated questions 

    def test_get_paginated_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_paginated_questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
       
    # Test unsuccessful request with page 1000 and extra category field

    def test_404_is_sent_requesting_beyond_valid_page(self):
        res = self.client().get('/questions?page=200', json={'category': 6})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test successful request to delete a question

    def test_delete_question(self):
        res = self.client().delete('/questions/5')
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 5).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted'])
        self.assertEqual(data['deleted_id'], 5)
        self.assertTrue(len(data['questions']))
        self.assertTrue(data['total_questions'])
        self.assertEqual(question, None)

    # Test unsuccessful request to delete a question that doesn't exist

    def test_422_deletion_if_question_does_not_exist(self):
        res = self.client().delete('/questions/200')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    # Test successful request to create a question 

    def test_create_question(self):
        res = self.client().post('/questions', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['answer'])
        self.assertTrue(data['category'])
        self.assertTrue(data['difficulty'])
        self.assertTrue(data['created'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(len(data['questions']))

    # Test unsuccessful request to create a question when question id is mentioned

    def test_405_if_question_creation_is_not_allowed(self):
        res = self.client().post('/questions/10', json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')

    # Test successful request to search for a question with results

    def test_get_question_search_with_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'Gogh'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 1)
        self.assertTrue(data['questions'])
        self.assertTrue(data['search_term'])

    # Test successful request to search for a question with no results

    def test_get_question_search_without_results(self):
        res = self.client().post('/questions', json={'searchTerm': 'dog'})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['total_questions'], 0)
        self.assertTrue(data['search_term'])


    # Test successful request to get all questions for a category

    def test_get_questions_for_category(self):
        res = self.client().get('/categories/1/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['selected_category'], 'Science')

    # Test unsuccessful request to get all questions for an unknown category

    def test_404_if_category_does_not_exist(self):
        res = self.client().get('/categories/200/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'resource not found')

    # Test successful request to play the game

    def test_play_trivia_game(self):
        res = self.client().post('/quizzes', json={'previous_questions': [2, 4], 'quiz_category':{'type': 'Entertainment', 'id': '5'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        
    # Test unsuccessful request to play the game

    def test_405_if_play_trivia_game_fails(self):
        res = self.client().patch('/quizzes', json={'previous_questions': [2, 4], 'quiz_category':{'type': 'Extra', 'id': '15'}})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'method not allowed')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
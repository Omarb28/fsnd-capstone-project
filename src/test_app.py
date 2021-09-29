import os
import json
import unittest
from flask_sqlalchemy import SQLAlchemy

import app
from database.models import setup_db, Actor, Movie


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.create_app()
        self.client = self.app.test_client
        self.database_url = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_url)

        self.new_actor = {
            'name': 'Will Smith',
            'age': 53,
            'gender': 'Male'
        }

        self.new_movie = {
            'title': 'Bad Boys for Life',
            'release_year': 2020
        }

        self.new_actor_missing_fields = {
            'name': 'Dwayne Johnson',
        }

        self.new_movie_missing_fields = {
            'title': 'Jumanji: The Next Level'
        }

        self.token_auth = {
            'casting_assistant_auth':   {'Authorization': 'Bearer ' + os.environ['CASTING_ASSISTANT_TOKEN']},
            'casting_director_auth':    {'Authorization': 'Bearer ' + os.environ['CASTING_DIRECTOR_TOKEN']},
            'executive_producer_auth':  {'Authorization': 'Bearer ' + os.environ['EXECUTIVE_PRODUCER_TOKEN']}
        }

        self.default_token_auth = self.token_auth['executive_producer_auth']

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        pass

    '''
    Actor Endpoint Tests
    '''

    # Get Actor

    def test_get_list_of_actors(self):
        res = self.client().get(
            '/actors', 
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    def test_get_actor_information(self):
        res = self.client().get(
            '/actors/1', 
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
    
    def test_404_actor_not_found(self):
        res = self.client().get(
            '/actors/9999', 
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')
    
    # Post Actor

    def test_create_new_actor(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor, 
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_id'])
    
    def test_422_create_new_actor_with_missing_fields(self):
        res = self.client().post(
            '/actors',
            json=self.new_actor_missing_fields, 
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

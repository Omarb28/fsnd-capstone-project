import os
import json
import unittest
from flask_sqlalchemy import SQLAlchemy

import app
from database.models import setup_db, Actor, Movie


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents casting agency test cases"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app.create_app()
        self.client = self.app.test_client
        self.database_url = os.environ['DATABASE_URL']
        setup_db(self.app, self.database_url)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.drop_all()
            self.db.create_all()

            # initial seed data
            self.actors_list = [
                {'name': 'Leonardo DiCaprio', 'age': 46, 'gender': 'Male'},
                {'name': 'Kate Winslet', 'age': 45, 'gender': 'Female'},
                {'name': 'Cary Elwes', 'age': 58, 'gender': 'Male'}
            ]

            self.movies_list = [
                {'title': 'Titanic', 'release_year': 1997},
                {'title': 'SAW', 'release_year': 2004},
                {'title': 'Get Out', 'release_year': 2017}
            ]

            for actor in self.actors_list:
                actor_row = Actor(
                    name=actor['name'],
                    age=actor['age'],
                    gender=actor['gender'])
                actor_row.insert()

            for movie in self.movies_list:
                movie_row = Movie(
                    title=movie['title'],
                    release_year=movie['release_year'])
                movie_row.insert()

        # variables to use in the tests
        self.actor_test = {
            'name': 'Will Smith',
            'age': 53,
            'gender': 'Male'
        }

        self.movie_test = {
            'title': 'Bad Boys for Life',
            'release_year': 2020
        }

        self.actor_with_missing_attributes = {
            'name': 'Dwayne Johnson',
        }

        self.movie_with_missing_attributes = {
            'title': 'Jumanji: The Next Level'
        }

        self.actor_with_wrong_attributes = {
            'name': 'Jackie Chan',
            'age': -67
        }

        self.movie_with_wrong_attributes = {
            'title': 'Rush Hour',
            'release_year': -1998
        }

        self.token_auth = {
            'casting_assistant_auth':
                {'Authorization': 'Bearer '
                    + os.environ['CASTING_ASSISTANT_TOKEN']},
            'casting_director_auth':
                {'Authorization': 'Bearer '
                    + os.environ['CASTING_DIRECTOR_TOKEN']},
            'executive_producer_auth':
                {'Authorization': 'Bearer '
                    + os.environ['EXECUTIVE_PRODUCER_TOKEN']}
        }

        self.default_token_auth = self.token_auth['executive_producer_auth']

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
            '/actors/99999',
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # Post Actor

    def test_create_new_actor(self):
        res = self.client().post(
            '/actors',
            json=self.actor_test,
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_id'])

    def test_400_bad_request_create_new_actor_with_missing_attributes(self):
        res = self.client().post(
            '/actors',
            json=self.actor_with_missing_attributes,
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # Patch Actor

    def test_update_actor_information(self):
        res = self.client().patch(
            '/actors/1',
            json=self.actor_test,
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], self.actor_test['name'])

    def test_422_unprocessable_update_actor_with_wrong_attributes(self):
        res = self.client().patch(
            '/actors/1',
            json=self.actor_with_wrong_attributes,
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    # Delete Actor

    def test_delete_actor(self):
        res = self.client().delete(
            '/actors/2',
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_id'])

    def test_404_not_found_actor_to_delete(self):
        res = self.client().delete(
            '/actors/99999',
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    '''
    Movie Endpoint Tests
    '''

    # Get Movie

    def test_get_list_of_movies(self):
        res = self.client().get(
            '/movies',
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['movies']))

    def test_get_movie_information(self):
        res = self.client().get(
            '/movies/1',
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])

    def test_404_movie_not_found(self):
        res = self.client().get(
            '/movies/99999',
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    # Post Movie

    def test_create_new_movie(self):
        res = self.client().post(
            '/movies',
            json=self.movie_test,
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_id'])

    def test_400_bad_request_create_new_movie_with_missing_attributes(self):
        res = self.client().post(
            '/movies',
            json=self.movie_with_missing_attributes,
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 400)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Bad Request')

    # Patch Movie

    def test_update_movie_information(self):
        res = self.client().patch(
            '/movies/1',
            json=self.movie_test,
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movie'])
        self.assertEqual(data['movie']['title'], self.movie_test['title'])

    def test_422_unprocessable_update_movie_with_wrong_attributes(self):
        res = self.client().patch(
            '/movies/1',
            json=self.movie_with_wrong_attributes,
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Unprocessable Entity')

    # Delete Movie

    def test_delete_movie(self):
        res = self.client().delete(
            '/movies/2',
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_id'])

    def test_404_not_found_movie_to_delete(self):
        res = self.client().delete(
            '/movies/99999',
            headers=self.default_token_auth)
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Found')

    '''
    Role RBAC Tests
    '''

    # Casting Assistant

    # get:actors - success
    def test_casting_assistant_get_list_of_actors(self):
        res = self.client().get(
            '/actors',
            headers=self.token_auth['casting_assistant_auth'])
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['actors']))

    # post:actors - forbidden
    def test_403_forbidden_casting_assistant_create_new_actor(self):
        res = self.client().post(
            '/actors',
            json=self.actor_test,
            headers=self.token_auth['casting_assistant_auth'])
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Forbidden')

    # Casting Director

    # patch:actors - success
    def test_casting_director_update_actor_information(self):
        res = self.client().patch(
            '/actors/3',
            json=self.actor_test,
            headers=self.token_auth['casting_director_auth'])
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actor'])
        self.assertEqual(data['actor']['name'], self.actor_test['name'])

    # post:movies - forbidden
    def test_403_forbidden_casting_director_create_new_movie(self):
        res = self.client().post(
            '/movies',
            headers=self.token_auth['casting_director_auth'])
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 403)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Forbidden')

    # Executive Producer

    # post:movies - success
    def test_executive_producer_create_new_movie(self):
        res = self.client().post(
            '/movies',
            json=self.movie_test,
            headers=self.token_auth['executive_producer_auth'])
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created_id'])

    # delete:movies - success
    def test_executive_producer_delete_movie(self):
        res = self.client().delete(
            '/movies/3',
            headers=self.token_auth['executive_producer_auth'])
        data = json.loads(res.data.decode('utf-8'))

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['deleted_id'])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()

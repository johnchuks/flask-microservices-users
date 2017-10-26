# project/tests/test_users.py


import json

from project.tests.base import BaseTestCase
from project.api.models import User
from project import db


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])

    def test_add_user(self):
        """Ensure a new user is added to the database"""
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='johnchuks',
                    email='johnbosco@gmail.com'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 201)
            self.assertIn('johnbosco@gmail.com was added', data['message'])
            self.assertIn('success', data['status'])

    def test_add_invalid_json(self):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps(dict()),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())

            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Invalid request data', data['message'])

    def test_add_duplicate_user(self):
        with self.client:
            self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='johnchuks',
                    email='johnbosco@gmail.com'
                )),
                content_type='application/json'
            )
            response = self.client.post(
                '/users',
                data=json.dumps(dict(
                    username='johnchuks',
                    email='johnbosco@gmail.com'
                )),
                content_type='application/json'
            )
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 400)
            self.assertIn('fail', data['status'])
            self.assertIn('Sorry, The user already exist', data['message'])

    def test_incomplete_json_input(self):
        with self.client:
            response = self.client.post(
                '/users',
                data=json.dumps({'email': 'johnbosco@gmail.com'}),
                content_type='application/json'
            )
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid payload', data['message'])
        self.assertIn('fail', data['status'])

    def test_get_users(self):
        """Ensure get all users behaves correctly."""
        add_user('itunu', 'itunu@gmail.com')
        add_user('db', 'daniel@gmail.com')
        with self.client:
            response = self.client.get('/users')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(data['data']), 2)
            self.assertIn('itunu', data['data'][0]['username'])
            self.assertIn('itunu@gmail.com', data['data'][0]['email'])
            self.assertIn('db', data['data'][1]['username'])
            self.assertIn('daniel@gmail.com', data['data'][1]['email'])
            self.assertIn('success', data['status'])
            self.assertTrue('created_at' in data['data'][0])
            self.assertTrue('created_at' in data['data'][1])

    def test_get_single_user(self):
        """Ensure get single user behaves correctly."""
        user = add_user('itunu', 'itunu@gmail.com')
        with self.client:
            response = self.client.get('/users/{}'.format(user.id))
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 200)
            self.assertIn('itunu', data['data'][0]['username'])
            self.assertIn('itunu@gmail.com', data['data'][0]['email'])
            self.assertIn('success', data['status'])

    def test_get_single_user_no_id(self):
        with self.client:
            response = self.client.get('/users/nothing')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('user does not exist', data['message'])
            self.assertIn('fail', data['status'])

    def test_get_user_incorrect_id(self):
        with self.client:
            response = self.client.get('/users/44')
            data = json.loads(response.data.decode())
            self.assertEqual(response.status_code, 404)
            self.assertIn('No users found', data['message'])
            self.assertIn('fail', data['status'])

    def test_main_no_users(self):
        """Ensure the main route behaves correctly when no users have been
    added to the database."""
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Users</h1>', response.data)
        self.assertIn(b'<p>No users!</p>', response.data)

    def test_main_with_users(self):
        """Ensure the main route behaves correctly when users have been added to the database"""
        add_user('tonymontaro', 'tonymontaro@python.com')
        add_user('johnchuks', 'fetcher@realpython.com')
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<h1>All Users</h1>', response.data)
        self.assertIn(b'<p>No users</p>', response.data)
        self.assertIn(b'<strong>tonymontaro</strong>', response.data)
        self.assertIn(b'<strong>johnchuks</strong>', response.data)

    def test_main_add_users(self):
        """Ensure the main route behaves correctly when users have been added to the database"""
        with self.client:
            response = self.client.post(
                '/',
                data=json.dumps(dict(username='johnB', email='johnb@realpython.com')),
                follow_redirects=True
            )
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'<h1>All Users</h1>', response.data)
            self.assertIn(b'<p>No users</p>', response.data)
            self.assertIn(b'<strong>m</strong>', response.data)
            self.assertIn(b'<strong>fletcher</strong>', response.data)

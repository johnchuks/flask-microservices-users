# project/tests/test_users.py


import json

from project.tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    """Tests for the Users Service."""

    def test_users(self):
        """Ensure the /ping route behaves correctly."""
        response = self.client.get('/ping')
        data = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong!', data['message'])
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
            # self.assertIn('johnbosco@gmail.com was added', data['message'])
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
            self.assertIn('Invalid payload', data['message'])

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

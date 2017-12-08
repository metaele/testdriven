import json
import pytest

from app import db
from app.api.models import User


def add_user(username, email):
    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return user


class TestUserService:

    def test_users(self, testapp):
        '''test the /ping endpoint'''
        resp = testapp.test_client().get('/ping')
        data = json.loads(resp.data.decode())
        assert resp.status_code == 200
        assert 'pong' in data['message']
        assert 'success' in data['status']

    def test_add_user(self, app):
        with app.test_client() as client:
            payload = {'username': 'twicet', 'email': 'twicet@gmail.com'}
            resp = Post(client, '/users', payload).do
            data = json.loads(resp.data.decode())
            assert resp.status_code == 201
            assert 'twicet@gmail.com was added!' in data['message']
            assert 'success' in data['status']

    def test_add_user_invalid_json(self, app):
        with app.test_client() as client:
            resp = Post(client, '/users', {}).do
            data = json.loads(resp.data.decode())
            assert resp.status_code == 400
            assert 'Invalid payload.' in data['message']
            assert 'fail' in data['status']

    def test_add_user_invalid_keys(self, app):
        with app.test_client() as client:
            resp = Post(client, '/users', {'email': 'twicet@gmail.com'}).do
            data = json.loads(resp.data.decode())
            assert resp.status_code == 400
            assert 'Invalid payload.' in data['message']
            assert 'fail' in data['status']

    def test_add_user_duplicate_user(self, app):
        with app.test_client() as client:
            Post(
                client,
                '/users',
                {'username': 'twicet', 'email': 'twicet@got.io'}
            ).do
            resp = Post(
                client,
                '/users',
                {'username': 'twicet', 'email': 'twicet@got.io'}
            ).do
            data = json.loads(resp.data.decode())
            assert resp.status_code == 400
            assert 'Sorry. That email already exists.' in data['message']
            assert 'fail' in data['status']

    def test_single_user(self, app):
        user = add_user('twicet', 'twicet@gmail.com')
        with app.test_client() as client:
            response = client.get(f'/users/{user.id}')
            data = json.loads(response.data.decode())
            assert response.status_code == 200
            assert 'created_at' in data['data']
            assert 'twicet' in data['data']['username']
            assert 'twicet@gmail.com' in data['data']['email']
            assert 'success' in data['status']

    def test_single_user_no_id(self, app):
        with app.test_client() as client:
            response = client.get('/users/blah')
            data = json.loads(response.data.decode())
            assert response.status_code == 404
            assert 'User does not exist' in data['message']
            assert 'fail' in data['status']

    def test_single_user_incorrect_id(self, app):
        with app.test_client() as client:
            response = client.get('/users/999')
            data = json.loads(response.data.decode())
            assert response.status_code == 404
            assert 'User does not exist' in data['message']
            assert 'fail' in data['status']

    def test_all_users(self, app):
        add_user('twicet', 'twicet@gmail.com')
        add_user('gofhaone', 'gofha@got.io')
        with app.test_client() as client:
            response = client.get('/users')
            data = json.loads(response.data.decode())
            assert response.status_code == 200
            assert len(data['data']['users']) == 2
            assert 'created_at' in data['data']['users'][0]
            assert 'twicet' in data['data']['users'][0]['username']
            assert 'gofha@got.io' in data['data']['users'][1]['email']
            assert 'success' in data['status']


class Post:
    def __init__(self, client, url, data, content_type='application/json'):
        self.client = client
        self.url = url
        self.data = json.dumps(data) if content_type == 'application/json' else data
        self.content_type = content_type

    @property
    def do(self):
        return self.client.post(self.url, data=self.data, content_type=self.content_type)


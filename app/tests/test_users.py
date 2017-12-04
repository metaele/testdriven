import json
import pytest


class TestUserService:
    '''User service tests'''

    def test_users(self, http_test_client):
        '''test the /ping endpoint'''
        resp = http_test_client.get('/ping')
        data = json.loads(resp.data.decode())
        assert resp.status_code == 200
        assert 'pong' in data['message']
        assert 'success' in data['status']

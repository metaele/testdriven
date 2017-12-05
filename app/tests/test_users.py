import json
import pytest


class TestUserService:

    def test_users(self, testapp_client):
        '''test the /ping endpoint'''
        resp = testapp_client.get('/ping')
        data = json.loads(resp.data.decode())
        assert resp.status_code == 200
        assert 'pong' in data['message']
        assert 'success' in data['status']

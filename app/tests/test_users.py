import json

from app.tests.base import BaseTestCase


class TestUserService(BaseTestCase):
    '''User service tests'''

    def test_users(self):
        '''test the /ping endpoint'''
        resp = self.client.get('/ping')
        data = json.loads(resp.data.decode())
        self.assertEquals(resp.status_code, 200)
        self.assertIn('pong', data['message'])
        self.assertIn('success', data['status'])

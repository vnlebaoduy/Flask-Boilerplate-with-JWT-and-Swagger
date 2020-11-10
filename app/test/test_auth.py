import unittest

from app.main import db
import json
from app.test.base import BaseTestCase


def register_user(self):
    return self.client.post(
        '/user/',
        data=json.dumps(dict(
            email='lebaoduy1993@gmail.com',
            username='vnlebaoduy',
            password='123456',
            full_name='ADMIN'
        )),
        content_type='application/json'
    )


def login_user(self):
    return self.client.post(
        '/user/token',
        data=json.dumps(dict(
            username='admin',
            password='admin1234'
        )),
        content_type='application/json'
    )


def login_user_not_exits(self):
    return self.client.post(
        '/user/token',
        data=json.dumps(dict(
            username='admin2',
            password='admin1234'
        )),
        content_type='application/json'
    )


def get_info_me(self, access_token):
    return self.client.get(
        '/user/me/info',
        headers={
            'Authorization': 'Bearer {}'.format(access_token)
        },
        content_type='application/json'
    )


class TestAuthBlueprint(BaseTestCase):
    def test_user_registration(self):
        with self.client:
            response = register_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(data['message'] == 'Successfully registered.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_user_registered_with_already(self):
        register_user(self)
        with self.client:
            response = register_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(
                data['message'] == 'User already exists. Please Log in.')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 409)

    def test_user_registered_user_login(self):
        with self.client:
            # user registration
            resp_register = register_user(self)
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = login_user(self)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

    def test_user_get_info_me(self):
        with self.client:
            # registered user login
            response = login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)
            # get info me
            res_info = get_info_me(self, data['access_token'])
            data_info = json.loads(res_info.data.decode())
            self.assertTrue(
                data_info['username'] == 'admin'
            )
            self.assertTrue(res_info.content_type == 'application/json')
            self.assertEqual(res_info.status_code, 200)

    def test_user_non_registered_user_login(self):
        with self.client:
            response = login_user_not_exits(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'fail')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()

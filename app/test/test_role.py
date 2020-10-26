import unittest
import json
from app.test.base import BaseTestCase
import app.test.test_auth as Auth


def creat_role(self, access_token):
    return self.client.post(
        '/role/',
        headers={
            'Authorization': 'Bearer {}'.format(access_token)
        },
        data=json.dumps(dict(
            name="USER_ROLE",
            description="Quyền truy cập user cơ bản"
        )),
        content_type='application/json'
    )


def get_all_role(self, access_token):
    return self.client.get(
        '/role/',
        headers={
            'Authorization': 'Bearer {}'.format(access_token)
        },
        content_type='application/json'
    )


def delete_role(self, access_token):
    return self.client.delete(
        '/role/1',
        headers={
            'Authorization': 'Bearer {}'.format(access_token)
        },
        content_type='application/json'
    )


class TestRoleBlueprint(BaseTestCase):
    def test_create_role(self):
        with self.client:
            # user registration
            resp_register = Auth.register_user(self)
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)
            # registered user login
            response = Auth.login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # create role
            res_creat_role = creat_role(self, data['access_token'])
            data_create_role = json.loads(res_creat_role.data.decode())
            self.assertTrue(data_create_role['status'] == 'success')
            self.assertTrue(res_creat_role.content_type == 'application/json')
            self.assertEqual(res_creat_role.status_code, 201)

    def test_create_role_already(self):
        with self.client:
            # user registration
            resp_register = Auth.register_user(self)
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)

            # registered user login
            response = Auth.login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # create conflict
            creat_role(self, data['access_token'])
            res_creat_role_conflict = creat_role(self, data['access_token'])
            data_create_role = json.loads(res_creat_role_conflict.data.decode())
            self.assertTrue(data_create_role['status'] == 'conflict')
            self.assertEqual(res_creat_role_conflict.status_code, 409)

    def test_delete_role(self):
        with self.client:
            # user registration
            resp_register = Auth.register_user(self)
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)

            # registered user login
            response = Auth.login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # create role
            res_creat_role_conflict = creat_role(self, data['access_token'])
            data_create_role = json.loads(res_creat_role_conflict.data.decode())
            self.assertTrue(data_create_role['status'] == 'success')
            self.assertEqual(res_creat_role_conflict.status_code, 201)

            # delete role
            res_delete_role = delete_role(self, data['access_token'])
            data_delete_role = json.loads(res_delete_role.data.decode())
            self.assertEqual(res_delete_role.status_code, 200)
            self.assertTrue(data_delete_role['status'] == 'success')

    def test_get_role(self):
        with self.client:
            # user registration
            resp_register = Auth.register_user(self)
            data_register = json.loads(resp_register.data.decode())
            self.assertTrue(data_register['status'] == 'success')
            self.assertTrue(
                data_register['message'] == 'Successfully registered.'
            )
            self.assertTrue(resp_register.content_type == 'application/json')
            self.assertEqual(resp_register.status_code, 201)

            # registered user login
            response = Auth.login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # create role
            res_create_role = creat_role(self, data['access_token'])
            data_create_role = json.loads(res_create_role.data.decode())
            self.assertTrue(data_create_role['status'] == 'success')
            self.assertEqual(res_create_role.status_code, 201)

            # delete role
            res_delete_role = delete_role(self, data['access_token'])
            data_delete_role = json.loads(res_delete_role.data.decode())
            self.assertTrue(data_delete_role['status'] == 'success')
            self.assertTrue(res_delete_role.status_code == 200)


if __name__ == '__main__':
    unittest.main()

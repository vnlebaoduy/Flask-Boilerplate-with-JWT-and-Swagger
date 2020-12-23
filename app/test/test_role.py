import unittest
import json
from app.test.base import BaseTestCase
import app.test.test_auth as Auth


def create_role(self, access_token):
    return self.client.post(
        '/role/',
        headers={
            'Authorization': 'Bearer {}'.format(access_token)
        },
        data=json.dumps(dict(
            name="USER_ROLE_2",
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


def get_all_role_by_user_id(self, access_token, public_id):
    return self.client.get(
        '/role/user/{}'.format(public_id),
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


def set_role(self, access_token, public_id):
    return self.client.post(
        '/role/user/{}'.format(public_id),
        headers={
            'Authorization': 'Bearer {}'.format(access_token)
        },
        data=json.dumps(dict(
            role_id=2,
        )),
        content_type='application/json'
    )


def update_role(self, access_token):
    return self.client.put(
        '/role/update_role',
        headers={
            'Authorization': 'Bearer {}'.format(access_token)
        },
        data=json.dumps(dict(
            id=2,
            name='ROLE_USER',
            description='Done'
        )),
        content_type='application/json'
    )


class TestRoleBlueprint(BaseTestCase):
    def test_role_create(self):
        with self.client:
            # registered user login
            response = Auth.login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # create role
            res_create_role = create_role(self, data['access_token'])
            data_create_role = json.loads(res_create_role.data.decode())
            self.assertTrue(data_create_role['status'] == 'success')
            self.assertTrue(res_create_role.content_type == 'application/json')
            self.assertEqual(res_create_role.status_code, 201)

    def test_role_create_already(self):
        with self.client:
            # registered user login
            response = Auth.login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # create conflict
            create_role(self, data['access_token'])
            res_create_role_conflict = create_role(self, data['access_token'])
            data_create_role = json.loads(res_create_role_conflict.data.decode())
            self.assertTrue(data_create_role['status'] == 'fail')
            self.assertEqual(res_create_role_conflict.status_code, 409)

    def test_role_delete(self):
        with self.client:
            # registered user login
            response = Auth.login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # delete role
            res_delete_role = delete_role(self, data['access_token'])
            data_delete_role = json.loads(res_delete_role.data.decode())
            self.assertEqual(res_delete_role.status_code, 200)
            self.assertTrue(data_delete_role['status'] == 'success')

    def test_role_set(self):
        with self.client:
            # registered user login
            response = Auth.login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # get info me
            res_info = Auth.get_info_me(self, data['access_token'])
            data_info_me = json.loads(res_info.data.decode())
            self.assertTrue(
                data_info_me['username'] == 'admin'
            )
            self.assertTrue(res_info.content_type == 'application/json')
            self.assertEqual(res_info.status_code, 200)

            res_set_role = set_role(self, data['access_token'], data_info_me['public_id'])
            data_set_role = json.loads(res_set_role.data.decode())
            self.assertTrue(res_set_role.content_type == 'application/json')
            self.assertEqual(res_set_role.status_code, 201)

    def test_role_get(self):
        with self.client:
            # registered user login
            response = Auth.login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # get role
            res_get_role = get_all_role(self, data['access_token'])
            data_get_role = json.loads(res_get_role.data.decode())
            self.assertTrue(res_get_role.status_code == 200)

    def test_role_get_by_user_id(self):
        with self.client:
            # registered user login
            response = Auth.login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # get info me
            res_info = Auth.get_info_me(self, data['access_token'])
            data_info_me = json.loads(res_info.data.decode())
            self.assertTrue(
                data_info_me['username'] == 'admin'
            )
            self.assertTrue(res_info.content_type == 'application/json')
            self.assertEqual(res_info.status_code, 200)

            # get role
            res_get_role = get_all_role_by_user_id(self, data['access_token'], data_info_me['public_id'])
            data_get_role = json.loads(res_get_role.data.decode())
            self.assertTrue(
                data_get_role['status'] == 'success'
            )
            self.assertTrue(res_get_role.status_code == 200)

    def test_role_update(self):
        with self.client:
            # registered user login
            response = Auth.login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # update role
            res_update_role = update_role(self, data['access_token'])
            data_update_role = json.loads(res_update_role.data.decode())
            self.assertTrue(data_update_role['status'] == 'success')
            self.assertTrue(
                data_update_role['name'] == 'ROLE_USER'
            )
            self.assertTrue(
                data_update_role['description'] == 'Done'
            )
            self.assertEqual(res_update_role.status_code, 200)


if __name__ == '__main__':
    unittest.main()

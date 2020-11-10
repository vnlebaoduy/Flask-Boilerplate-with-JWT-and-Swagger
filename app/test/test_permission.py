import unittest
import json
from app.main import db
from app.test.base import BaseTestCase
import app.test.test_auth as Auth


def create_permission(self, access_token):
    return self.client.post(
        '/permission/',
        headers={
            'Authorization': 'Bearer {}'.format(access_token)
        },
        data=json.dumps(dict(
            name="CREATE_PERMISSION",
            description="Tạo quyền truy cập"
        )),
        content_type='application/json'
    )


def get_all_permission(self, access_token):
    return self.client.get(
        '/permission/',
        headers={
            'Authorization': 'Bearer {}'.format(access_token)
        },
        content_type='application/json'
    )


def update_permission(self, access_token):
    return self.client.put(
        '/permission/update_permission',
        headers={
            'Authorization': 'Bearer {}'.format(access_token)
        },
        data=json.dumps(dict(
            id=1,
            name='CREATE_PERMISSION',
            description='Done'
        )),
        content_type='application/json'
    )


def get_permission_by_id(self, access_token, public_id):
    return self.client.get(
        '/permission/getPermissionByUserId/{}'.format(public_id),
        headers={
            'Authorization': 'Bearer {}'.format(access_token)
        },
        content_type='application/json'
    )


class TestAuthBlueprint(BaseTestCase):
    def test_permission_create(self):
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

        # create permission
        res_create_permission = create_permission(self, data['access_token'])
        data_create_permission = json.loads(res_create_permission.data.decode())
        self.assertTrue(data_create_permission['status'] == 'success')
        self.assertTrue(res_create_permission.content_type == 'application/json')
        self.assertEqual(res_create_permission.status_code, 201)

    def test_permission_get(self):
        with self.client:
            # registered user login
            response = Auth.login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # create permission
            res_create_permission = create_permission(self, data['access_token'])
            data_create_permission = json.loads(res_create_permission.data.decode())
            self.assertTrue(data_create_permission['status'] == 'success')
            self.assertEqual(res_create_permission.status_code, 201)

            # delete permission
            res_get_permission = get_all_permission(self, data['access_token'])
            data_get_permission = json.loads(res_get_permission.data.decode())
            self.assertTrue(res_get_permission.status_code == 200)

    def test_permission_update(self):
        with self.client:
            # user login
            response = Auth.login_user(self)
            data = json.loads(response.data.decode())
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)

            # update permission
            res_update_permission = update_permission(self, data['access_token'])
            data_update_permission = json.loads(res_update_permission.data.decode())
            self.assertTrue(data_update_permission['status'] == 'success')
            self.assertTrue(
                data_update_permission['name'] == 'CREATE_PERMISSION'
            )
            self.assertTrue(
                data_update_permission['description'] == 'Done'
            )
            self.assertEqual(res_update_permission.status_code, 200)

    def test_permission_get_list_by_id(self):
        with self.client:
            # user login
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

            # update permission
            res_list_permission_id = get_permission_by_id(self, data['access_token'], data_info_me['public_id'])
            data_list_permission = json.loads(res_list_permission_id.data.decode())
            self.assertTrue(data_list_permission['status'] == 'success')
            self.assertEqual(res_list_permission_id.status_code, 200)


if __name__ == '__main__':
    unittest.main()

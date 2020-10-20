import unittest
import json
from app.test.base import BaseTestCase


def creat_role(self):
    return self.client.post(
        '/role/',
        data=json.dumps(dict(
            name="USER_ROLE",
            description="Quyền truy cập user cơ bản"
        )),
        content_type='application/json'
    )


def get_role(self):
    return self.client.get(
        '/role/',
        content_type='application/json'
    )


class TestRoleBlueprint(BaseTestCase):
    def test_create_role(self):
        """ Test for role create """
        with self.client:
            response = creat_role(self)
            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_get_role(self):
        """ Test for role create """
        with self.client:
            response = get_role(self)
            data = json.loads(response.data.decode())
            print('test_get_role', data['data'])
            self.assertTrue(data['data'] == list)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
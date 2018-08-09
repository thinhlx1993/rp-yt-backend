# coding=utf-8
import unittest
import json

from app.app import create_app
from app.extensions import client

access_token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1NTQxNzk5MzIsImlhdCI6MTUyMjY0MzkzMiwibmJmIjoxNTIyNjQzOTMyLCJqdGkiOiJjZWFlNThkMS1mNzljLTRhOTUtYTNjOC1mMDZkMTUzZmYyMWEiLCJpZGVudGl0eSI6IjVhYWI3MmRhYTJmYTEwOWIyOTE4YjY0NiIsImZyZXNoIjpmYWxzZSwidHlwZSI6ImFjY2VzcyJ9.AGCQ9JnKcW_YQDlVpkMl46SNT1UIW2VzyQXLn65nKNk'
refresh_token = 'Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MjUyMzU5MzIsImlhdCI6MTUyMjY0MzkzMiwibmJmIjoxNTIyNjQzOTMyLCJqdGkiOiIzNmI4ZDllYy04MzIyLTQzOWEtYWVjZS1mZmNlMzVlMmQzYWUiLCJpZGVudGl0eSI6IjVhYWI3MmRhYTJmYTEwOWIyOTE4YjY0NiIsInR5cGUiOiJyZWZyZXNoIn0.ZUdR5pHsb8Hfj_yHbuHfYN8WFmqjUbNLpIfknCLtjeg'


class TestApi(unittest.TestCase):
    def setUp(self):
        app = create_app()
        self.client = app.test_client()
        self.headers = {'Content-Type': 'application/json', 'Authorization': access_token}

        # Bug workaround
        client.app = app

    def test_no_header(self):
        """TEST Get with no header authorization"""
        rv = self.client.get('/api/v1/user/info')
        self.assertEqual(rv.status_code, 401)

    def test_get_user(self):
        """ Tests if category returns list items successfully """

        result = self.client.get('/api/v1/user?page=0&size=10', headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def test_rate_up(self):
        """ Tests if user vote up prediction successfully """

        result = self.client.get('/api/v1/user/rate_up', headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def test_rate_down(self):
        """ Tests if user vote down prediction successfully """

        result = self.client.get('/api/v1/user/rate_down', headers=self.headers)
        self.assertEqual(result.status_code, 200)

    def test_update_user_data(self):
        """ Tests if update user information successfully """
        data = json.dumps(dict(
            _id='5aaba8be80706b000920cccf',
            address='Viet Nam',
            phone=986111111,
            fullname="Le Thinh",
            user_type="admin",
            activate=True
        ))
        result = self.client.put('/api/v1/user', data=data, headers=self.headers)
        self.assertEqual(result.status_code, 200)

    # def test_get_sub_category(self):
    #     """ Test save settings, passed if return 200"""
    #     result = self.client.post('/api/v1/category/get_sub_category', data=dict(
    #         user_id='25',
    #         ids=["5a14374ee3e7b24ce5d3afb8", "5a143751e3e7b24ce5d3afb9"]
    #     ), follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'Cluster 0', result.data)
    #
    # def test_save_settings(self):
    #     """ Test save sub setting, passed if return 200"""
    #     data = {
    #         "user_id": "25",
    #         "selec_subcat": [
    #             {
    #                 "cat_id": "5a143751e3e7b24ce5d3afb9",
    #                 "selected_sub_cats": [
    #                     "Cluster 1"
    #                 ]
    #             }
    #         ],
    #         "custom_cat": [
    #             "5a1649e8a2fa10f14a0e4f6f"
    #         ]
    #     }
    #     result = self.client.post('/api/v1/user/save_setting', data=json.dumps(data),
    #                               content_type='application/json', follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'updated', result.data)
    #
    # def test_get_settings(self):
    #     """ Test get settings of user, passed if return 200"""
    #     result = self.client.get('/api/v1/user/25', follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #     # self.assertIn('You have been logged in', result.data)
    #
    # def test_get_articles_with_sub_cat(self):
    #     """ Test get article by cat_id sub_cat and user_id, passed if return 200"""
    #     result = self.client.post('/api/v1/category/article', data=dict(
    #         user_id='25',
    #         cat_id="5a143751e3e7b24ce5d3afb9",
    #         sub_cat="Sub Cluster 0"
    #     ), follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #     # self.assertIn('You have been logged in', result.data)
    #
    # def test_get_article(self):
    #     """ Test get article by article_id, user_id, cat_id, passed if return 200"""
    #     result = self.client.post('/api/v1/category/get_article', data=dict(
    #         user_id='25',
    #         cat_id="5a143751e3e7b24ce5d3afb9",
    #         article_id="5a01c5dfe3e7b2373543f9bd"
    #     ), follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #     # self.assertIn('You have been logged in', result.data)
    #
    # def test_add_favorite(self):
    #     """ Test add favorite of article, passed if return 200"""
    #     result = self.client.post('/api/v1/user/add_favourite', data=dict(
    #         user_id='25',
    #         cat_id="5a143751e3e7b24ce5d3afb9",
    #         article_id="5a01c5dfe3e7b2373543f9bd"
    #     ), follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #     # self.assertIn('You have been logged in', result.data)
    #
    # def test_get_favorite(self):
    #     """ Test get favorite of article, passed if return 200"""
    #     result = self.client.get('/api/v1/user/get_favourite/25', follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #     # self.assertIn('You have been logged in', result.data)
    #
    # def test_remove_favorite(self):
    #     """ Test remove favorite of article, passed if return 200"""
    #     result = self.client.post('/api/v1/category/get_article', data=dict(
    #         user_id='25',
    #         cat_id="5a143751e3e7b24ce5d3afb9",
    #         article_id="5a01c5dfe3e7b2373543f9bd"
    #     ), follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #
    # def test_new_comment(self):
    #     """ Test add new comment for article, passed if return 200"""
    #     result = self.client.post('/api/v1/comment/new', data=dict(
    #         user_id='25',
    #         article_id="5a03e798e3e7b23735441527",
    #         content="test123"
    #     ), follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'success', result.data)
    #
    # def test_get_comment(self):
    #     """ Test get comment of article, passed if return 200"""
    #     result = self.client.get('/api/v1/comment/5a03e798e3e7b23735441527', follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #
    # def test_reply_comment(self):
    #     """ Test add new comment for article, passed if return 200"""
    #     result = self.client.post('/api/v1/comment/new', data=dict(
    #         user_id='46',
    #         article_id="5a03e798e3e7b23735441527",
    #         content="reply12321",
    #         comment_id="5a1584afa2fa10ac9ed34e6b"
    #     ), follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #
    # def test_get_setting_cat(self):
    #     """ Test get setting category state, passed if return 200"""
    #     result = self.client.post('/api/v1/user/setting_cat', data=dict(
    #         user_id='25',
    #         cat_id="5a14374ee3e7b24ce5d3afb8",
    #     ), follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'5a14374ee3e7b24ce5d3afb8', result.data)
    #
    # def test_save_setting_cat(self):
    #     """ Test get setting category state, passed if return 200"""
    #     data = {
    #         "cat_id": "5a143751e3e7b24ce5d3afb9",
    #         "subs": [
    #             {
    #                 "name": "Sub Cluster 0",
    #                 "order": 0,
    #                 "show": True
    #             }
    #         ],
    #         "user_id": "25"
    #     }
    #     result = self.client.post('/api/v1/user/setting_cat/save', data=json.dumps(data),
    #                               content_type='application/json', follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'5a143751e3e7b24ce5d3afb9', result.data)
    #
    # def test_delete_setting_cat(self):
    #     """ Test remove setting category state, passed if return 200"""
    #     result = self.client.post('/api/v1/user/del_cat', data=dict(
    #         user_id='25',
    #         cat_id="5a0afaa9e3e7b24ce5d3af7a",
    #     ), follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'deleted', result.data)
    #
    # def test_search_category(self):
    #     """ Test search category by keyword, passed if return 200"""
    #     result = self.client.get('/api/v2/category/as', follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #
    # def test_make_sub_cat(self):
    #     """ Test make sub category, passed if return 200"""
    #     result = self.client.post('/api/v2/category/save', data=dict(
    #         keyword='lassen',
    #         user_id='25'
    #     ), follow_redirects=True)
    #
    #     self.assertEqual(result.status_code, 200)
    #     self.assertIn(b'lassen', result.data)


if __name__ == '__main__':
    unittest.main()

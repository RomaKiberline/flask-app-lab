import unittest
from app import create_app, db
from config import TestingConfig
from app.users.models import User, USERS


class PostsCRUDTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app.config.from_object(TestingConfig)
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            user = User(1, 'testuser', 'test@example.com', 'testpass')
            USERS[1] = user
            with self.client.session_transaction() as sess:
                sess['_user_id'] = str(user.id)
                sess['_fresh'] = True

    def tearDown(self):
        with self.app.app_context():
            db.drop_all()
            USERS.clear()

    def test_create_post_get_form(self):
        resp = self.client.get('/post/create')
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Add Post', resp.data)

    def test_create_and_list_post(self):
        # Create
        resp = self.client.post('/post/create', data={
            'title': 'Test Post',
            'content': 'Example content',
            'enabled': 'y',
            'category': 'tech'
        }, follow_redirects=True)
        self.assertEqual(resp.status_code, 200)
        self.assertIn(b'Post added successfully', resp.data)
        # List
        resp2 = self.client.get('/post')
        self.assertEqual(resp2.status_code, 200)
        self.assertIn(b'Test Post', resp2.data)

    def test_view_detail_update_delete(self):
        self.client.post('/post/create', data={
            'title': 'First',
            'content': 'Body',
            'enabled': 'y',
            'category': 'news'
        }, follow_redirects=True)
        resp_list = self.client.get('/post')
        self.assertIn(b'First', resp_list.data)
        resp_detail = self.client.get('/post/1')
        self.assertEqual(resp_detail.status_code, 200)
        self.assertIn(b'First', resp_detail.data)
        # Update
        resp_edit = self.client.post('/post/1/update', data={
            'title': 'First Edited',
            'content': 'Body Edited',
            'enabled': 'y',
            'category': 'publication'
        }, follow_redirects=True)
        self.assertEqual(resp_edit.status_code, 200)
        self.assertIn(b'Post updated successfully', resp_edit.data)
        self.assertIn(b'First Edited', resp_edit.data)
        resp_confirm = self.client.get('/post/1/delete')
        self.assertEqual(resp_confirm.status_code, 200)
        resp_del = self.client.post('/post/1/delete', follow_redirects=True)
        self.assertEqual(resp_del.status_code, 200)
        self.assertIn(b'Post deleted', resp_del.data)
        resp_list2 = self.client.get('/post')
        self.assertNotIn(b'First Edited', resp_list2.data)


if __name__ == '__main__':
    unittest.main()

import unittest
from app import create_app


class FlaskAppTestCase(unittest.TestCase):

    def setUp(self):
        """Налаштування клієнта тестування перед кожним тестом."""
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_greetings_page(self):
        """Тест маршруту /users/hi/<name>."""
        response = self.client.get("/users/hi/John?age=30")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"JOHN", response.data)
        self.assertIn(b"30", response.data)

    def test_admin_page(self):
        """Тест маршруту /users/admin, який перенаправляє."""
        response = self.client.get("/users/admin", follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"ADMINISTRATOR", response.data)
        self.assertIn(b"19", response.data)

    def test_home_page(self):
        """Тест головної сторінки."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Flask App", response.data)

if __name__ == "__main__":
    unittest.main()
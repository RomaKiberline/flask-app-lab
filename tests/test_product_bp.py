import unittest
from app import create_app

class ProductBlueprintTest(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.client = self.app.test_client()

    def test_product_list(self):
        response = self.client.get("/products/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Телефон", response.data.decode('utf-8'))

if __name__ == "__main__":
    unittest.main()

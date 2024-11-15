
import unittest
from app import app

class TicketingAppFrontendTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    # Test the index page
    def test_index_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    # Test the register page
    def test_register_page(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    # Test the login page
    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

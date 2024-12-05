import unittest
import json
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

    # Test the chatbot's response to collecting fullname
    def test_chatbot_fullname(self):
        response = self.app.post('/api/chat', data=json.dumps({
            "message": "John Doe"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Thank you! Can I have your email address?", response.json['response'])

    # Test the chatbot's response to collecting email
    def test_chatbot_email(self):
        # Simulate a previous step where the fullname was set
        with self.app.session_transaction() as session:
            session['fullname'] = "John Doe"
        
        response = self.app.post('/api/chat', data=json.dumps({
            "message": "john@example.com"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Thank you! Lastly, may I have your date of birth (YYYY-MM-DD)?", response.json['response'])

    # Test the chatbot's response to collecting date of birth
    def test_chatbot_dob(self):
        # Simulate previous steps for fullname and email
        with self.app.session_transaction() as session:
            session['fullname'] = "John Doe"
            session['email'] = "john@example.com"

        response = self.app.post('/api/chat', data=json.dumps({
            "message": "1990-01-01"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Thank you for the details! Type 'reset password' or 'download certificate' to proceed.", response.json['response'])

    # Test the chatbot's response to a reset password request
    def test_chatbot_reset_password(self):
        # Simulate all required steps for chatbot interaction
        with self.app.session_transaction() as session:
            session['fullname'] = "John Doe"
            session['email'] = "john@example.com"
            session['dob'] = "1990-01-01"

        response = self.app.post('/api/chat', data=json.dumps({
            "message": "reset password"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Please enter the OTP sent to your email.", response.json['response'])

    # Test the chatbot's response to invalid date format
    def test_chatbot_invalid_dob_format(self):
        # Simulate previous steps for fullname and email
        with self.app.session_transaction() as session:
            session['fullname'] = "John Doe"
            session['email'] = "john@example.com"

        response = self.app.post('/api/chat', data=json.dumps({
            "message": "01-01-1990"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Invalid date format. Please enter in YYYY-MM-DD format.", response.json['response'])

    # Test the chatbot's response to an unrecognized message
    def test_chatbot_unrecognized_message(self):
        # Simulate previous steps for fullname, email, and dob
        with self.app.session_transaction() as session:
            session['fullname'] = "John Doe"
            session['email'] = "john@example.com"
            session['dob'] = "1990-01-01"

        response = self.app.post('/api/chat', data=json.dumps({
            "message": "help me"
        }), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn("Please specify your request: 'reset password' or 'download certificate'.", response.json['response'])

if __name__ == '__main__':
    unittest.main()

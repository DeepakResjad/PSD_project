import unittest
import json,jwt
from unittest.mock import patch
from datetime import datetime
from app import app, get_db_connection, generate_token, hash_secret
import psycopg2

class TicketingAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.conn = get_db_connection()
        self.conn.autocommit = False  # Disable autocommit to use transactions
        self.create_test_data()
        self.app_context = app.app_context()
        self.app_context.push()

    def tearDown(self):
        if self.conn and not self.conn.closed:
            self.conn.rollback()  # Rollback all changes made in the test
            self.conn.close()
        self.app_context.pop()

    def create_test_data(self):
       
        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE email = %s", ('test@gmail.com',))
            cur.execute("INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)", 
                        ('testuser','test@gmail.com', hash_secret('test_secret')))
            self.conn.commit()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_register_page(self):
        response = self.app.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_login_page(self):
        response = self.app.get('/login')
        self.assertEqual(response.status_code, 200)

    # def test_request_admin(self):
    #     response = self.app.post('/api/request-admin', 
    #                              data=json.dumps({'username': 'testuser', 'secret': 'test_secret'}), 
    #                              content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('token', json.loads(response.data))

    # def test_grant_admin(self):
    #     token_response = self.app.post('/api/request-admin', 
    #                                     data=json.dumps({'username': 'testuser', 'secret': 'test_secret'}), 
    #                                     content_type='application/json')
    #     self.assertEqual(token_response.status_code, 200, f"Expected 200 OK, got {token_response.status_code} with response: {token_response.data}")
    #     token_data = json.loads(token_response.data) 
    #     token = token_data['token']

    #     if not token:
    #         self.fail(f"Token not found in response. Full response data: {token_response.data}")

    #     response = self.app.post('/api/grant-admin', 
    #                              data=json.dumps({'token': token}), 
    #                              content_type='application/json')
    #     self.assertEqual(response.status_code, 200,f"Expected 200 OK but got {token_response.status_code} with response: {token_response.data}")
    #     response_data = json.loads(response.data)
    #     self.assertIn("Admin privileges granted", response_data.get("message", ""))

    # def test_revoke_admin(self):
    #     token_response = self.app.post('/api/request-admin', 
    #                                     data=json.dumps({'username': 'testuser', 'secret': 'test_secret'}), 
    #                                     content_type='application/json')
    #     token = json.loads(token_response.data)['token']

    #     self.app.post('/api/grant-admin', 
    #                   data=json.dumps({'token': token}), 
    #                   content_type='application/json')

    #     response = self.app.post('/api/revoke-admin', 
    #                              data=json.dumps({'token': token}), 
    #                              content_type='application/json')
    #     self.assertEqual(response.status_code, 200)
    #     self.assertIn('Admin privileges revoked', json.loads(response.data)['message'])

    @patch('app.sentiment_analysis')
    def test_create_ticket_temporary(self, mock_sentiment_analysis):
        # Define test data for a temporary ticket creation
        test_data = {
            "user_id": 2,
            "software_name": "Example Software",
            "message": "Having trouble with installation",
            "request_type": "technical"
        }

        # Mock sentiment analysis response
        mock_sentiment_analysis.return_value = [{"label": "POSITIVE"}]

        with patch('app.get_db_connection', return_value=self.conn):
            response = self.app.post(
                '/api/tickets',
                data=json.dumps(test_data),
                content_type='application/json'
            )

            # Debugging output to capture server response details
            print("Status Code:", response.status_code)
            print("Response Data:", response.get_data(as_text=True))

            # Assertions
            self.assertEqual(response.status_code, 201)
            response_data = json.loads(response.data)
            self.assertEqual(response_data["message"], "Ticket submitted successfully")
            self.assertIn("ticket_id", response_data)

    @patch('app.sentiment_analysis')
    def test_create_ticket_user_not_exist_temporary(self, mock_sentiment_analysis):
        # Define test data with a non-existent user
        test_data = {
            "user_id": 999,  # Assume 999 is a non-existent user
            "software_name": "Example Software",
            "message": "This is a test ticket",
            "request_type": "general"
        }

        # Mock sentiment analysis response
        mock_sentiment_analysis.return_value = [{"label": "POSITIVE"}]

        with patch('app.get_db_connection', return_value=self.conn):
            response = self.app.post(
                '/api/tickets',
                data=json.dumps(test_data),
                content_type='application/json'
            )

            # Assertions
            self.assertEqual(response.status_code, 400)
            response_data = json.loads(response.data)
            self.assertEqual(response_data["error"], "User ID does not exist. Please provide a valid user.")

    def test_get_tickets(self):
        response = self.app.get('/api/tickets')
        self.assertEqual(response.status_code, 200)

    def test_hash_secret(self):
        secret = "mysecret"
        hashed_secret = hash_secret(secret)
        self.assertEqual(len(hashed_secret), 64)  # SHA256 produces a 64-character hash

    # Test JWT token generation
    def test_generate_token(self):
        username = "testuser"
        token = generate_token(username)
        self.assertIsNotNone(token)

        # Decode the token to ensure it has the correct payload
        decoded = jwt.decode(token, app.secret_key, algorithms=["HS256"])
        self.assertEqual(decoded['username'], username)

    # # Test protected route (example)
    # def test_protected_route_without_token(self):
    #     response = self.app.get('/protected')  # Assuming there's a protected route
    #     self.assertEqual(response.status_code, 401)  # Should return unauthorized

    # # Test protected route with token
    # def test_protected_route_with_token(self):
    #     token = generate_token('testuser')
    #     headers = {'Authorization': f'Bearer {token}'}
    #     response = self.app.get('/protected', headers=headers)
    #     self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

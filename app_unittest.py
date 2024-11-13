import unittest
import json,jwt
from app import app, get_db_connection, generate_token, hash_secret

class TicketingAppTests(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        self.conn = get_db_connection()
        self.conn.autocommit = False  # Disable autocommit to use transactions
        self.create_test_data()

    def tearDown(self):
        self.conn.rollback()  # Rollback all changes made in the test
        self.conn.close()

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

    def test_request_admin(self):
        response = self.app.post('/api/request-admin', 
                                 data=json.dumps({'username': 'testuser', 'secret': 'test_secret'}), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', json.loads(response.data))

    def test_grant_admin(self):
        token_response = self.app.post('/api/request-admin', 
                                        data=json.dumps({'username': 'testuser', 'secret': 'test_secret'}), 
                                        content_type='application/json')
        self.assertEqual(token_response.status_code, 200, f"Expected 200 OK, got {token_response.status_code} with response: {token_response.data}")
        token_data = json.loads(token_response.data) 
        token = token_data['token']

        if not token:
            self.fail(f"Token not found in response. Full response data: {token_response.data}")

        response = self.app.post('/api/grant-admin', 
                                 data=json.dumps({'token': token}), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200,f"Expected 200 OK but got {token_response.status_code} with response: {token_response.data}")
        response_data = json.loads(response.data)
        self.assertIn("Admin privileges granted", response_data.get("message", ""))

    def test_revoke_admin(self):
        token_response = self.app.post('/api/request-admin', 
                                        data=json.dumps({'username': 'testuser', 'secret': 'test_secret'}), 
                                        content_type='application/json')
        token = json.loads(token_response.data)['token']

        self.app.post('/api/grant-admin', 
                      data=json.dumps({'token': token}), 
                      content_type='application/json')

        response = self.app.post('/api/revoke-admin', 
                                 data=json.dumps({'token': token}), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Admin privileges revoked', json.loads(response.data)['message'])

    def test_submit_ticket(self):
        token_response = self.app.post('/api/request-admin', 
                                        data=json.dumps({'username': 'testuser', 'secret': 'test_secret'}), 
                                        content_type='application/json')
        token = json.loads(token_response.data)['token']

        response = self.app.post('/api/tickets', 
                                 data=json.dumps({'user_id': 1, 'software_name': 'Test Software', 'message': 'Test issue.'}), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('Ticket submitted successfully', json.loads(response.data)['message'])

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

    # Test protected route (example)
    def test_protected_route_without_token(self):
        response = self.app.get('/protected')  # Assuming there's a protected route
        self.assertEqual(response.status_code, 401)  # Should return unauthorized

    # Test protected route with token
    def test_protected_route_with_token(self):
        token = generate_token('testuser')
        headers = {'Authorization': f'Bearer {token}'}
        response = self.app.get('/protected', headers=headers)
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()

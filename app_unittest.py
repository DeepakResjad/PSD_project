import unittest
import json
from app import app, get_db_connection  

class TicketingAppTests(unittest.TestCase):

    def setUp(self):
        
        self.app = app.test_client()
        self.app.testing = True
        
        
        self.conn = get_db_connection()
        self.create_test_data()

    def tearDown(self):
       
        self.conn.close()

    def create_test_data(self):
       
        with self.conn.cursor() as cur:
            cur.execute("INSERT INTO users (username, passwordhash, role) VALUES (%s, %s, %s)", 
                        ('testuser', 'hashed_password', 'user'))
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
                                 data=json.dumps({'username': 'testuser', 'secret': 'password'}), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', json.loads(response.data))

    def test_grant_admin(self):
        token_response = self.app.post('/api/request-admin', 
                                        data=json.dumps({'username': 'testuser', 'secret': 'password'}), 
                                        content_type='application/json')
        token = json.loads(token_response.data)['token']

        response = self.app.post('/api/grant-admin', 
                                 data=json.dumps({'token': token}), 
                                 content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('Admin privileges granted', json.loads(response.data)['message'])

    def test_revoke_admin(self):
        token_response = self.app.post('/api/request-admin', 
                                        data=json.dumps({'username': 'testuser', 'secret': 'password'}), 
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
                                        data=json.dumps({'username': 'testuser', 'secret': 'password'}), 
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

if __name__ == '__main__':
    unittest.main()

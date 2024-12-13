import unittest
from app import app
import json

class TestAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def test_register_user(self):
        response = self.client.post('/api/register', json={
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com'
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('User registered successfully!', response.get_data(as_text=True))

    def test_login_user(self):
        self.client.post('/api/register', json={
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com'
        })
        response = self.client.post('/api/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('token', response.get_json())

    def test_upload_medical_record(self):
        self.client.post('/api/register', json={
            'username': 'testuser',
            'password': 'testpassword',
            'email': 'testuser@example.com'
        })
        response = self.client.post('/api/login', json={
            'username': 'testuser',
            'password': 'testpassword'
        })
        token = response.get_json()['token']
        response = self.client.post('/api/upload', data={
            'data': 'Medical record data'
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertIn('Record uploaded successfully!', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main()

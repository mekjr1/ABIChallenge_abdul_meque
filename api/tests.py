# tests.py
import unittest
from flask import Flask
from app import app
from model import RandomForestAPI
from passenger import Passenger

class FlaskAppTests(unittest.TestCase):
    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_test_route(self):
        response = self.app.get('/')
        data = response.get_json()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['message'], 'It works! Now you have to call the right endpoint')

    def test_get_predictions(self):
        response = self.app.get('/predictions')
        self.assertEqual(response.status_code, 200)
        # Add assertions for the response data
        
    def test_predict_single(self):
        data = {
            'pclass': 3,
            'sex': 1,
            'age': 25,
            'fare': 10,
            'embarked': 1,
            'title': 0,
            'isAlone': 1,
            'ageClass': 75
        }
        response = self.app.post('/predict', json=data)
        self.assertEqual(response.status_code, 200)
        # Add assertions for the response data
        
    def test_predict_batch(self):
        data = [
            {
                'pclass': 1,
                'sex': 0,
                'age': 35,
                'fare': 100,
                'embarked': 1,
                'title': 1,
                'isAlone': 0,
                'ageClass': 35
            },
            {
                'pclass': 2,
                'sex': 1,
                'age': 20,
                'fare': 20,
                'embarked': 1,
                'title': 1,
                'isAlone': 1,
                'ageClass': 40
            }
        ]
        response = self.app.post('/predict', json=data)
        self.assertEqual(response.status_code, 200)
        # Add assertions for the response data

if __name__ == '__main__':
    unittest.main()

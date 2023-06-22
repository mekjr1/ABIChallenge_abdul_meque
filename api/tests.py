import unittest
import json
from flask import Flask
from app import app, db
from model import RandomForestAPI
from passenger import Passenger
from database import Prediction

class FlaskAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.testing = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        cls.app = app.test_client()
        cls.api = RandomForestAPI('random_forest_model.pkl')

        with app.app_context():
            db.create_all()

    @classmethod
    def tearDownClass(cls):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def setUp(self):
        self.app_context = app.app_context()
        self.app_context.push()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
        self.app_context.pop()

    def test_index(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_predictions(self):
        response = self.app.get('/predictions')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

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
        prediction = json.loads(response.data)
        self.assertIn('prediction', prediction)

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
        predictions = json.loads(response.data)
        self.assertIn('predictions', predictions)
        self.assertIsInstance(predictions['predictions'], list)

    def test_invalid_data_format(self):
        data = {'invalid_key': 'value'}
        response = self.app.post('/predict', json=data)
        self.assertEqual(response.status_code, 200)
        error = json.loads(response.data)
        self.assertIn('error', error)

    def test_invalid_single_prediction_data(self):
        data = {'pclass': 1, 'sex': 0, 'age': 35}
        response = self.app.post('/predict', json=data)
        self.assertEqual(response.status_code, 200)
        error = json.loads(response.data)
        self.assertIn('error', error)

    def test_invalid_batch_prediction_data(self):
        data = [
            {'pclass': 1, 'sex': 0, 'age': 35},
            {'pclass': 2, 'sex': 1, 'age': 20}
        ]
        response = self.app.post('/predict', json=data)
        self.assertEqual(response.status_code, 200)
        error = json.loads(response.data)
        self.assertIn('error', error)

    def test_prediction_database_entry(self):
        data = {
            'pclass': 1,
            'sex': 0,
            'age': 35,
            'fare': 100,
            'embarked': 1,
            'title': 1,
            'isAlone': 0,
            'ageClass': 35
        }
        response = self.app.post('/predict', json=data)
        self.assertEqual(response.status_code, 200)
        prediction = json.loads(response.data)
        self.assertIn('prediction', prediction)

        with app.app_context():
            predictions = Prediction.query.all()
            self.assertEqual(len(predictions), 1)
            self.assertEqual(predictions[0].passenger_id, 1)
            self.assertEqual(predictions[0].prediction, prediction['prediction'])

if __name__ == '__main__':
    unittest.main()

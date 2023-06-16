from flask import Flask, jsonify, request
from sklearn.ensemble import RandomForestClassifier
import json
import numpy as np
import os

from passenger import Passenger
from apix import RandomForestAPI

app = Flask(__name__)


api = RandomForestAPI('random_forest_model.pkl')

class PassengerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Passenger):
            obj_dict = obj.__dict__
            obj_dict['Age'] = int(obj_dict['Age'])
            obj_dict['Fare'] = int(obj_dict['Fare'])
            obj_dict['Age*Class'] = int(obj_dict['Age*Class'])
            return obj_dict
        elif isinstance(obj, np.int64):
            return int(obj)  # Convert int64 to int
        return super().default(obj)


@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'It works! Now you have to call the right endpoint'})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Get the input data from the request

    if isinstance(data, dict):  # Single prediction
        if all(key in data for key in ['Pclass', 'Sex', 'Age', 'Fare', 'Embarked', 'Title', 'IsAlone', 'Age*Class']):
            passenger = Passenger(
                data['Pclass'],
                data['Sex'],
                int(data['Age']),  # Convert to int
                int(data['Fare']),  # Convert to int
                data['Embarked'],
                data['Title'],
                data['IsAlone'],
                int(data['Age*Class'])  # Convert to int
            )
            prediction = api.predict_single(passenger)
            response = {'prediction': int(prediction)}  # Convert prediction to int
        else:
            response = {'error': 'Invalid data format. Required keys: Pclass, Sex, Age, Fare, Embarked, Title, IsAlone, Age*Class'}
    elif isinstance(data, list):  # Batch prediction
        if all(isinstance(passenger_data, dict) and all(key in passenger_data for key in ['Pclass', 'Sex', 'Age', 'Fare', 'Embarked', 'Title', 'IsAlone', 'Age*Class']) for passenger_data in data):
            passengers = [
                Passenger(
                    passenger_data['Pclass'],
                    passenger_data['Sex'],
                    int(passenger_data['Age']),  # Convert to int
                    int(passenger_data['Fare']),  # Convert to int
                    passenger_data['Embarked'],
                    passenger_data['Title'],
                    passenger_data['IsAlone'],
                    int(passenger_data['Age*Class'])  # Convert to int
                )
                for passenger_data in data
            ]
            predictions = api.predict_batch(passengers)
            response = {'predictions': [int(prediction) for prediction in predictions]}  # Convert predictions to int
        else:
            response = {'error': 'Invalid data format. Required keys: Pclass, Sex, Age, Fare, Embarked, Title, IsAlone, Age*Class'}
    else:
        response = {'error': 'Invalid data format'}

    return jsonify(response)

port = int(os.environ.get('PORT', 5000))

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=port)

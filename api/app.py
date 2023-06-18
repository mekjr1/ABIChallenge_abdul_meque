# app.py
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from model import RandomForestAPI
from database import Prediction, db
from passenger import Passenger
import json

app = Flask(__name__)

api = RandomForestAPI('random_forest_model.pkl')

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///predictions.db'
db.init_app(app)

class PassengerEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Passenger):
            obj_dict = obj.__dict__
            obj_dict['age'] = int(obj_dict['age'])
            obj_dict['fare'] = int(obj_dict['fare'])
            obj_dict['ageClass'] = int(obj_dict['ageClass'])
            return obj_dict
        elif isinstance(obj, np.int64):
            return int(obj)  # Convert int64 to int
        return super().default(obj)
    
@app.route('/', methods=['GET'])
def test():
    return jsonify({'message': 'It works! Now you have to call the right endpoint'})

@app.route('/predictions', methods=['GET'])
def get_predictions():
    predictions = Prediction.query.all()
    response = [{'passenger_id': prediction.passenger_id, 'prediction': prediction.prediction} for prediction in predictions]
    return jsonify(response)

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json  # Get the input data from the request

    if isinstance(data, dict):  # Single prediction
        if all(key in data for key in ['pclass', 'sex', 'age', 'fare', 'embarked', 'title', 'isAlone', 'ageClass']):
            passenger = Passenger(
                data['pclass'],
                data['sex'],
                int(data['age']),  # Convert to int
                int(data['fare']),  # Convert to int
                data['embarked'],
                data['title'],
                data['isAlone'],
                int(data['ageClass'])  # Convert to int
            )
            prediction = api.predict_single(passenger)
            prediction = int(prediction)
            response = {'prediction': prediction}

            # Save the prediction to the database
            passenger_id = 1  # Replace with the actual passenger ID
            prediction_entry = Prediction(passenger_id=passenger_id, prediction=prediction)
            db.session.add(prediction_entry)
            db.session.commit()
        else:
            response = {'error': 'Invalid data format. Required keys: pclass, sex, age, fare, embarked, title, isAlone, ageClass'}
    elif isinstance(data, list):  # Batch prediction
        if all(isinstance(passenger_data, dict) and all(key in passenger_data for key in ['pclass', 'sex', 'age', 'fare', 'embarked', 'title', 'isAlone', 'ageClass']) for passenger_data in data):
            passengers = [
                Passenger(
                    passenger_data['pclass'],
                    passenger_data['sex'],
                    int(passenger_data['age']),  # Convert to int
                    int(passenger_data['fare']),  # Convert to int
                    passenger_data['embarked'],
                    passenger_data['title'],
                    passenger_data['isAlone'],
                    int(passenger_data['ageClass'])  # Convert to int
                )
                for passenger_data in data
            ]
            predictions = api.predict_batch(passengers)
            predictions = [int(prediction) for prediction in predictions]
            response = {'predictions': predictions}

            # Save the predictions to the database
            passenger_ids = [1, 2, 3]  # Replace with the actual passenger IDs
            prediction_entries = [
                Prediction(passenger_id=passenger_id, prediction=prediction)
                for passenger_id, prediction in zip(passenger_ids, predictions)
            ]
            db.session.add_all(prediction_entries)
            db.session.commit()
    
        else:
            response = {'error': 'Invalid data format. Required keys: pclass, sex, age, fare, embarked, title, isAlone, ageClass'}
    else:
        response = {'error': 'Invalid data format'}

    return jsonify(response)

if __name__ == '__main__':
    with app.app_context():
        db.create_all() 
    app.run(debug=True, host='0.0.0.0', port=5000)

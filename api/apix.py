import pickle

class RandomForestAPI:
    def __init__(self, model_path):
        self.model_path = model_path
        self.load_model()

    def load_model(self):
        with open(self.model_path, 'rb') as file:
            self.model = pickle.load(file)

    def preprocess_data(self, data):
        # Perform any necessary preprocessing on the input data
        # Convert the Passenger object to a feature vector or DataFrame row
        feature_vector = [
            data.pclass,
            data.sex,
            data.age,
            data.fare,
            data.embarked,
            data.title,
            data.is_alone,
            data.age_class
        ]
        return feature_vector

    def predict_single(self, data):
        preprocessed_data = self.preprocess_data(data)
        prediction = self.model.predict([preprocessed_data])
        return prediction[0]

    def predict_batch(self, data):
        preprocessed_data = [self.preprocess_data(passenger) for passenger in data]
        predictions = self.model.predict(preprocessed_data)
        return predictions.tolist()
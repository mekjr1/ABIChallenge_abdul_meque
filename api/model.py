# model.py
from sklearn.ensemble import RandomForestClassifier
import pickle

class RandomForestAPI:
    def __init__(self, model_path):
        self.model_path = model_path
        self.load_model()

    def load_model(self):
        with open(self.model_path, 'rb') as file:
            self.model = pickle.load(file)
    
    def predict_single(self, passenger):
        # Make a single prediction for a passenger
        # Use self.model to perform the prediction
        return self.model.predict([passenger.get_features()])[0]
    
    def predict_batch(self, passengers):
        # Make predictions for a batch of passengers
        # Use self.model to perform the predictions
        features = [passenger.get_features() for passenger in passengers]
        return self.model.predict(features)



# passenger.py
class Passenger:
    def __init__(self, pclass, sex, age, fare, embarked, title, is_alone, age_class):
        self.pclass = pclass
        self.sex = sex
        self.age = age
        self.fare = fare
        self.embarked = embarked
        self.title = title
        self.isAlone = is_alone
        self.ageClass = age_class
    
    def get_features(self):
        # Return the features as a list or array for prediction
        return [self.pclass, self.sex, self.age, self.fare, self.embarked, self.title, self.isAlone, self.ageClass]

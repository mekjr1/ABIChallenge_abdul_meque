# passenger.py
class Passenger:
    def __init__(self, pclass, sex, age, fare, embarked, title, is_alone, age_class):
        self.Pclass = pclass
        self.Sex = sex
        self.Age = age
        self.Fare = fare
        self.Embarked = embarked
        self.Title = title
        self.IsAlone = is_alone
        self.AgeClass = age_class
    
    def get_features(self):
        # Return the features as a list or array for prediction
        return [self.Pclass, self.Sex, self.Age, self.Fare, self.Embarked, self.Title, self.IsAlone, self.AgeClass]

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import precision_score
from sklearn.metrics import accuracy_score
import pandas as pd

def train_model(train_data, predictors):
    rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)
    rf.fit(train_data[predictors], train_data["target"])
    return rf

def make_predictions(model, test_data, predictors):
    preds = model.predict(test_data[predictors])
    combined = pd.DataFrame(dict(actual=test_data["target"], prediction=preds), index=test_data.index)
    precision = precision_score(test_data["target"], preds)
    accuracy = accuracy_score(test_data["target"], preds)
    return combined, precision, accuracy

import pandas as pd
from MachineLearning.utilities import rolling_averages

def load_and_preprocess_data(filepath):
    matches = pd.read_csv(filepath, index_col=0)
    matches["date"] = pd.to_datetime(matches["date"])
    matches["venue_code"] = matches["venue"].astype("category").cat.codes 
    matches["opp_code"] = matches["opponent"].astype("category").cat.codes
    matches["hour"] = matches["time"].str.replace(":.+", "", regex=True).astype("int")
    matches["day_code"] = matches["date"].dt.dayofweek
    matches["formation_code"] = matches["formation"].astype("category").cat.codes
    matches["target"] = (matches["result"] == "W").astype("int")
    return matches

def add_rolling_features(matches, cols, new_cols):
    return matches.groupby("team").apply(lambda x: rolling_averages(x, cols, new_cols), include_groups=True)

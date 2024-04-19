from MachineLearning.data_preprocessing import load_and_preprocess_data, add_rolling_features
from MachineLearning.model import train_model, make_predictions
from MachineLearning.utilities import rolling_averages

# Filepath to the dataset
filepath = "matches.csv"

# Load and preprocess data
match_data = load_and_preprocess_data(filepath)

# Define columns for rolling features
rolling_cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt"]
rolling_cols_new_names = [f"{c}_rolling" for c in rolling_cols]

# Add rolling features
matches_rolling_data = add_rolling_features(match_data, rolling_cols, rolling_cols_new_names)
matches_rolling_data = matches_rolling_data.droplevel('team')
matches_rolling_data.index = range(matches_rolling_data.shape[0]) ## specifies the index of each data row

## splits the data into training and testing data (training data must be chronologically before testing data)
training_data = matches_rolling_data[matches_rolling_data["date"] < '2022-01-01']
testing_data = matches_rolling_data[matches_rolling_data["date"] > "2022-01-01"]

# Specify predictors and train the model
predictors = ["venue_code", "opp_code", "hour", "day_code", "formation_code", "poss"] + rolling_cols_new_names
rf_model = train_model(training_data, predictors)

# Make predictions and evaluate the model
combined, precision, accuracy = make_predictions(rf_model, testing_data, predictors)

print(f"Precision: {precision}")
print(f"Accuracy: {accuracy}")






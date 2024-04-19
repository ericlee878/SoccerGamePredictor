import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import precision_score
from tabulate import tabulate

## reads the data from csv file
matches = pd.read_csv("matches.csv", index_col=0)

## makes data in format so ML program can read it (has to be numbers)
matches["date"] = pd.to_datetime(matches["date"])
matches["venue_code"] = matches["venue"].astype("category").cat.codes 
matches["opp_code"] = matches["opponent"].astype("category").cat.codes
matches["hour"] = matches["time"].str.replace(":.+", "", regex=True).astype("int")
matches["day_code"] = matches["date"].dt.dayofweek
matches["target"] = (matches["result"] == "W").astype("int") ## creates a target for a ML program (we want to predict if the team wins or not)

## calls the ML program (RandomForestClassifier)
rf = RandomForestClassifier(n_estimators=50, min_samples_split=10, random_state=1)

## splits the data into training and testing data (training data must be chronologically before testing data)
train = matches[matches["date"] < '2022-01-01']
test = matches[matches["date"] > "2022-01-01"]

## specifies predictors and trains the ML model on the predictors
predictors = ["venue_code", "opp_code", "hour", "day_code"]
rf.fit(train[predictors], train["target"])

## gets predictions from the trained ML model
preds = rf.predict(test[predictors])

## Evaluates the accuracy of the ML model
acc = accuracy_score(test["target"], preds)
##print(acc)

## Creates a table that represents the accuracy of ML model when teams win vs. when teams lose
combined = pd.DataFrame(dict(actual=test["target"], prediction=preds))
pd.crosstab(index=combined["actual"], columns=combined["prediction"])

## Gets precision score of ML model
precision_score(test["target"], preds)

## Groups data by teams
grouped_matches = matches.groupby("team")

## Function that gathers the average value of the past three values of a specific column
## In this case, it is used to see the average of past 3 game performances (if team won or lost in recent games) 
def rolling_averages(group, cols, new_cols):
    group = group.sort_values("date")
    rolling_stats = group[cols].rolling(3, closed='left').mean()
    group[new_cols] = rolling_stats
    group = group.dropna(subset=new_cols)
    return group

## Specifies which columns to use for prediction model
cols = ["gf", "ga", "sh", "sot", "dist", "fk", "pk", "pkatt"]
new_cols = [f"{c}_rolling" for c in cols]

## Uses the rolling_averages function to get past data for teams on the specified columns
## Adds the specified columns to the data
matches_rolling = matches.groupby("team").apply(lambda x: rolling_averages(x, cols, new_cols), include_groups=True)

## Indexes the games by a unique index instead of categorizing it by team
matches_rolling = matches_rolling.droplevel('team')
matches_rolling.index = range(matches_rolling.shape[0])

## Creates a function that: 1) splits the data into training and testing data  
##                          2) trains the ML model with the data
##                          3) gets the predictions from the data
##                          4) gets the precision scores of the model
def make_predictions(data, predictors):
    train = data[data["date"] < '2022-01-01']
    test = data[data["date"] > "2022-01-01"]
    rf.fit(train[predictors], train["target"])
    preds = rf.predict(test[predictors])
    combined = pd.DataFrame(dict(actual=test["target"], prediction=preds), index=test.index)
    precision = precision_score(test["target"], preds)
    return combined, precision

## uses the make_predictions function to get the predictions and accuracy of predictions
combined, precision = make_predictions(matches_rolling, predictors + new_cols)

## combines the home and away predictions
combined = combined.merge(matches_rolling[["date", "team", "opponent", "result"]], left_index=True, right_index=True)

## cleans the data by unifying team names as one
class MissingDict (dict):
    __missing__ = lambda self, key: key

map_values = {
    "Brighton and Hove Albion": "Brighton",
    "Manchester United": "Manchester Utd",
    "Newcastle United": "Newcastle Utd",
    "Tottenham Hotspur": "Tottenham",
    "West Ham United": "West Ham",
    "Wolverhampton Wanderers": "Wolves"
}

mapping = MissingDict(**map_values)
combined["new_team"] = combined["team"].map(mapping)

## combines the prediction from both teams on the same game and see if they match: if they match merge them
merged = combined.merge(combined, left_on=["date", "new_team"], right_on=["date", "opponent"])

merged[(merged["prediction_x"]==1) & (merged["prediction_y"]==0)]["actual_x"].value_counts()

print(merged)


